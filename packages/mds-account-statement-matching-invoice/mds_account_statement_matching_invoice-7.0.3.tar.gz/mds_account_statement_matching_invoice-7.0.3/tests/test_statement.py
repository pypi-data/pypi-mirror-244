# -*- coding: utf-8 -*-
# This file is part of the account-statement-matching-invoice-module
# from m-ds.de for Tryton. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction, activate_module
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart, get_fiscalyear
from trytond.modules.account_statement_mt940.tests.test_statement import \
    StatementTestCase as Mt940TestCase
from trytond.modules.account_statement_mt940.tests.mt940data import \
    mt940_testdata, mt940_bytes

from datetime import date
from decimal import Decimal


def set_invoice_sequences(fiscalyear):
    pool = Pool()
    Sequence = pool.get('ir.sequence.strict')
    SequenceType = pool.get('ir.sequence.type')
    InvoiceSequence = pool.get('account.fiscalyear.invoice_sequence')
    ModelData = pool.get('ir.model.data')

    sequence, = Sequence.create([{
        'name': fiscalyear.name,
        'sequence_type': SequenceType(ModelData.get_id(
            'account_invoice', 'sequence_type_account_invoice')),
        'company': fiscalyear.company.id,
        }])
    fiscalyear.invoice_sequences = []
    invoice_sequence = InvoiceSequence()
    invoice_sequence.fiscalyear = fiscalyear
    invoice_sequence.in_invoice_sequence = sequence
    invoice_sequence.in_credit_note_sequence = sequence
    invoice_sequence.out_invoice_sequence = sequence
    invoice_sequence.out_credit_note_sequence = sequence
    invoice_sequence.save()
    return fiscalyear


class StatementTestCase(Mt940TestCase):
    'Test statement module'
    module = 'account_statement_matching_invoice'

    @classmethod
    def setUpClass(cls):
        """ add modules
        """
        super(StatementTestCase, cls).setUpClass()
        activate_module(['account_statement_mt940'])

    def prep_match_fiscalyear(self, company1):
        """ prepare fiscal year, sequences...
        """
        pool = Pool()
        FiscalYear = pool.get('account.fiscalyear')

        # fiscal year
        fisc_year = get_fiscalyear(company1, today=date(2020, 8, 2))
        set_invoice_sequences(fisc_year)
        self.assertEqual(len(fisc_year.invoice_sequences), 1)
        self.assertEqual(
            fisc_year.invoice_sequences[0].in_invoice_sequence.name,
            '2020')
        self.assertEqual(
            fisc_year.invoice_sequences[0].in_credit_note_sequence.name,
            '2020')
        self.assertEqual(
            fisc_year.invoice_sequences[0].out_invoice_sequence.name,
            '2020')
        self.assertEqual(
            fisc_year.invoice_sequences[0].out_credit_note_sequence.name,
            '2020')

        # sequence-invoice
        fisc_year.invoice_sequences[0].out_invoice_sequence.prefix = 'INV.'
        fisc_year.invoice_sequences[0].out_invoice_sequence.padding = 4
        fisc_year.invoice_sequences[0].out_invoice_sequence.save()
        self.assertEqual(
            fisc_year.invoice_sequences[0].out_invoice_sequence.prefix,
            'INV.')
        self.assertEqual(
            fisc_year.invoice_sequences[0].out_invoice_sequence.padding, 4)
        FiscalYear.create_period([fisc_year])

    def prep_match_paymentterm(self):
        """ create a paymentterm-item
        """
        pool = Pool()
        PaymentTerm = pool.get('account.invoice.payment_term')

        # payment term
        pay1, = PaymentTerm.create([{
            'name': '14 days',
            'lines': [('create', [{
                'type': 'remainder',
                'relativedeltas': [('create', [{
                    'days': 14,
                    }])],
                }])],
            }])

        pay_term, = PaymentTerm.search([])
        self.assertEqual(pay_term.name, '14 days')
        self.assertEqual(len(pay_term.lines), 1)
        self.assertEqual(pay_term.lines[0].type, 'remainder')
        self.assertEqual(len(pay_term.lines[0].relativedeltas), 1)
        self.assertEqual(pay_term.lines[0].relativedeltas[0].days, 14)
        return pay_term

    @with_transaction()
    def test_match_wizard_no_invoice(self):
        """ run import wizard, check result
        """
        pool = Pool()
        StatementImport = pool.get('account.statement.import', type='wizard')
        Statement = pool.get('account.statement')
        Party = pool.get('party.party')
        transaction = Transaction()

        company1 = create_company('m-ds')
        self.prep_currency_euro()
        self.prep_bank('WELADED1PMB')

        # add party for statement applicant
        pty1, = Party.create([{
            'name': 'Schliffenbacher Josef',
            'addresses': [('create', [{
                'street': 'Applicant Street 1',
                'postal_code': '12345',
                'city': 'Usertown',
                }])],
            }])

        b_acc1 = self.prep_bank_account(
            'WELADED1PMB', '74061813/0100033626', company1.party)
        b_acc2 = self.prep_bank_account(
            'WELADED1PMB', '74061813/0000033626', company1.party)
        # applicant account
        self.prep_bank_account(
            'WELADED1PMB', 'DE14740618130000033626', pty1)

        with set_company(company1):
            with transaction.set_context({'company': company1.id}):
                create_chart(company=company1, tax=True)
                self.prep_statement_journal(b_acc1, 'C123', company1)
                self.prep_statement_journal(b_acc2, 'C124', company1)

                # create wizard
                (sess_id, start_state, end_state) = StatementImport.create()
                StatementImport(sess_id)
                self.assertEqual(start_state, 'start')
                self.assertEqual(end_state, 'end')

                # run start
                result = StatementImport.execute(sess_id, {}, start_state)
                self.assertEqual(list(result.keys()), ['view'])

                # prepare wizard for import
                r1 = {}
                result['view']['defaults']['file_format'] = 'mt940'
                result['view']['defaults']['file_'] = mt940_bytes
                result['view']['defaults']['file_encoding'] = 'utf8'
                result['view']['defaults']['company'] = company1.id
                for i in result['view']['defaults'].keys():
                    if i not in ['company.rec_name', 'company.']:
                        r1[i] = result['view']['defaults'][i]

                # run import
                result = StatementImport.execute(
                    sess_id, {start_state: r1}, 'import_')
                StatementImport.delete(sess_id)

                s_lst = Statement.search([])
                self.assertEqual(len(s_lst), 1)

                self.assertEqual(s_lst[0].state, 'draft')
                self.assertTrue(
                    s_lst[0].name.endswith('74061813/0000033626 | 15002'))
                self.assertEqual(s_lst[0].journal.name, 'AccStatJournal')
                self.assertEqual(s_lst[0].journal.journal.code, 'C124')
                self.assertEqual(len(s_lst[0].journal.bank_account.numbers), 1)
                self.assertEqual(
                    s_lst[0].journal.bank_account.numbers[0].number,
                    '74061813/0000033626')
                self.assertEqual(str(s_lst[0].date), '2015-04-08')
                self.assertEqual(str(s_lst[0].start_balance), '25.43')
                self.assertEqual(str(s_lst[0].end_balance), '25.69')
                self.assertEqual(str(s_lst[0].total_amount), '0.26')
                self.assertEqual(s_lst[0].number_of_lines, 10)
                self.assertEqual(len(s_lst[0].lines), 0)
                self.assertEqual(len(s_lst[0].origins), 10)

                # origin 1
                self.assertEqual(s_lst[0].origins[0].number, '1')
                self.assertEqual(str(s_lst[0].origins[0].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[0].amount, Decimal('0.12'))
                self.assertEqual(
                    s_lst[0].origins[0].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[0].description,
                    'Zweite SEPA-Ueberweisung EREF: STZV-EtE06042015-111' +
                    '3-2 IBAN: DE14740618130000033626 BIC: GENODEF1PFK' +
                    ' ABWE: Test')
                self.assertEqual(len(s_lst[0].origins[0].information), 16)
                # origin 2
                self.assertEqual(s_lst[0].origins[1].number, '2')
                self.assertEqual(str(s_lst[0].origins[1].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[1].amount, Decimal('0.50'))
                self.assertEqual(
                    s_lst[0].origins[1].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[1].description,
                    'Verwendungszweck EREF: STZV-EtE06042015-1113-1 ' +
                    'IBAN: DE14740618130000033626 BIC: GENODEF1PFK ' +
                    'ABWE: Testkonto 2')
                self.assertEqual(len(s_lst[0].origins[1].information), 16)
                # origin 3
                self.assertEqual(s_lst[0].origins[2].number, '3')
                self.assertEqual(str(s_lst[0].origins[2].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[2].amount, Decimal('-0.33'))
                self.assertEqual(
                    s_lst[0].origins[2].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[2].description,
                    'Ueberweisung mit VR-Networld EREF: JS12345 IBAN: ' +
                    'DE14740618130000033626 BIC:GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[2].information), 16)
                # origin 4
                self.assertEqual(s_lst[0].origins[3].number, '4')
                self.assertEqual(str(s_lst[0].origins[3].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[3].amount, Decimal('-0.62'))
                self.assertEqual(s_lst[0].origins[3].party, None)
                self.assertEqual(
                    s_lst[0].origins[3].description,
                    'SEPA Sammel-Ueberweisung mit 2 Ueberweisungen ' +
                    'MSG-ID: STZV-Msg06042015-1113')
                self.assertEqual(len(s_lst[0].origins[3].information), 12)
                # origin 5
                self.assertEqual(s_lst[0].origins[4].number, '5')
                self.assertEqual(str(s_lst[0].origins[4].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[4].amount, Decimal('0.33'))
                self.assertEqual(s_lst[0].origins[4].party, None)
                self.assertEqual(
                    s_lst[0].origins[4].description,
                    'Ueberweisung mit VR-Networld EREF: JS12345 ' +
                    'IBAN: DE58740618130100033626 BIC:GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[4].information), 15)
                # origin 6
                self.assertEqual(s_lst[0].origins[5].number, '6')
                self.assertEqual(str(s_lst[0].origins[5].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[5].amount, Decimal('-0.45'))
                self.assertEqual(
                    s_lst[0].origins[5].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[5].description,
                    'BEITRAG 2015 Huber Gerhard Tennis JAHR 0,15 ' +
                    'Fussball JAHR 0,10 Tennis JAHR 0,20 EREF: ' +
                    'PC-VAB-EtE06042015-1103-1 MREF: Mandat2 CRED: ' +
                    'DE79ZZZ00000000584 IBAN:')
                self.assertEqual(len(s_lst[0].origins[5].information), 19)
                # origin 7
                self.assertEqual(s_lst[0].origins[6].number, '7')
                self.assertEqual(str(s_lst[0].origins[6].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[6].amount, Decimal('-0.35'))
                self.assertEqual(
                    s_lst[0].origins[6].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[6].description,
                    'BEITRAG 2015 Maier Max Fussball JAHR 0,10 Tennis' +
                    'JAHR 0,15 Fussball JAHR 0,10 EREF: PC-VAB-EtE060' +
                    '42015-1103-2 MREF: Mandat1 CRED: DE79ZZZ0000000' +
                    '0584 IBAN: DE')
                self.assertEqual(len(s_lst[0].origins[6].information), 19)
                # origin 8
                self.assertEqual(s_lst[0].origins[7].number, '8')
                self.assertEqual(str(s_lst[0].origins[7].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[7].amount, Decimal('0.54'))
                self.assertEqual(
                    s_lst[0].origins[7].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[7].description,
                    'Testbuchung EREF: JS7654343 IBAN: DE1474061813000' +
                    '0033626 BIC: GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[7].information), 15)
                # origin 9
                self.assertEqual(s_lst[0].origins[8].number, '9')
                self.assertEqual(str(s_lst[0].origins[8].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[8].amount, Decimal('0.80'))
                self.assertEqual(s_lst[0].origins[8].party, None)
                self.assertEqual(
                    s_lst[0].origins[8].description,
                    'SEPA Sammel-Basislastschrift mit 2 Lastschriften' +
                    'MSG-ID: PC-VAB-Msg06042015-1103')
                self.assertEqual(len(s_lst[0].origins[8].information), 12)
                # origin 10
                self.assertEqual(s_lst[0].origins[9].number, '10')
                self.assertEqual(str(s_lst[0].origins[9].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[9].amount, Decimal('-0.54'))
                self.assertEqual(s_lst[0].origins[9].party, None)
                self.assertEqual(
                    s_lst[0].origins[9].description,
                    'Testbuchung EREF: JS7654343 IBAN: DE5874061813010' +
                    '0033626 BIC: GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[9].information), 16)

    @with_transaction()
    def test_match_wizard_with_invoice(self):
        """ run import wizard, check result
        """
        pool = Pool()
        StatementImport = pool.get('account.statement.import', type='wizard')
        Statement = pool.get('account.statement')
        Party = pool.get('party.party')
        Invoice = pool.get('account.invoice')
        InvoiceLine = pool.get('account.invoice.line')
        Account = pool.get('account.account')
        Currency = pool.get('currency.currency')
        transaction = Transaction()

        company1 = create_company('m-ds')
        self.prep_currency_euro()
        self.prep_bank('WELADED1PMB')

        currency1, = Currency.search([('code', '=', 'EUR')])
        company1.currency = currency1
        company1.save()

        b_acc1 = self.prep_bank_account(
            'WELADED1PMB', '74061813/0100033626', company1.party)
        b_acc2 = self.prep_bank_account(
            'WELADED1PMB', '74061813/0000033626', company1.party)

        with set_company(company1):
            with transaction.set_context({
                    'company': company1.id,
                    '_skip_warnings': True}):
                create_chart(company=company1, tax=True)
                self.prep_match_paymentterm()
                self.prep_statement_journal(b_acc1, 'C123', company1)
                self.prep_statement_journal(b_acc2, 'C124', company1)
                self.prep_match_fiscalyear(company1)

                accounts = Account.search([
                        ('name', 'in', ['Main Revenue', 'Main Receivable']),
                        ('company', '=', company1.id),
                        ], order=[('name', 'ASC')])
                self.assertEqual(len(accounts), 2)
                self.assertEqual(accounts[0].name, 'Main Receivable')
                self.assertEqual(accounts[1].name, 'Main Revenue')

                # add party for statement applicant
                pty1, = Party.create([{
                    'name': 'Schliffenbacher Josef',
                    'addresses': [('create', [{
                        'street': 'Applicant Street 1',
                        'postal_code': '12345',
                        'city': 'Usertown',
                        }])],
                    }])

                # applicant account
                self.prep_bank_account(
                    'WELADED1PMB', 'DE14740618130000033626', pty1)

                inv1 = Invoice(
                        company=Invoice.default_company(),
                        party=pty1,
                        type='out',
                        payment_term=pty1.customer_payment_term,
                        invoice_date=date(2020, 5, 1),
                        account=accounts[0],
                    )
                inv1.on_change_type()
                inv1.on_change_party()
                inv1.save()

                inv_lst = Invoice.search([])
                self.assertEqual(len(inv_lst), 1)
                self.assertEqual(inv_lst[0].number, None)
                # add product to invoice
                invline1 = InvoiceLine(invoice=inv_lst[0])
                invline1.type = 'line'
                invline1.quantity = Decimal('1.0')
                invline1.unit_price = Decimal('0.50')
                invline1.account = accounts[1]
                invline1.save()
                Invoice.validate_invoice([inv_lst[0]])
                Invoice.post([inv_lst[0]])
                inv_lst2 = Invoice.search([])
                self.assertEqual(len(inv_lst2), 1)
                self.assertEqual(inv_lst2[0].total_amount, Decimal('0.5'))
                self.assertTrue(inv_lst2[0].number.startswith('INV.00'))
                self.assertEqual(inv_lst2[0].state, 'posted')
                self.assertEqual(inv_lst2[0].party.payable, Decimal('0.0'))
                self.assertEqual(inv_lst2[0].party.receivable, Decimal('0.50'))

                # create wizard
                (sess_id, start_state, end_state) = StatementImport.create()
                StatementImport(sess_id)
                self.assertEqual(start_state, 'start')
                self.assertEqual(end_state, 'end')

                # run start
                result = StatementImport.execute(sess_id, {}, start_state)
                self.assertEqual(list(result.keys()), ['view'])

                # prepare wizard for import
                r1 = {}
                result['view']['defaults']['file_format'] = 'mt940'
                # insert current invoice number
                result['view']['defaults']['file_'] = mt940_testdata.replace(
                    'EtE06042015', inv_lst2[0].number).encode()
                result['view']['defaults']['file_encoding'] = 'utf8'
                result['view']['defaults']['company'] = company1.id
                for i in result['view']['defaults'].keys():
                    if i not in ['company.rec_name', 'company.']:
                        r1[i] = result['view']['defaults'][i]

                self.assertEqual(Statement.search_count([]), 0)

                # run import
                result = StatementImport.execute(
                    sess_id, {start_state: r1}, 'import_')
                StatementImport.delete(sess_id)

                s_lst = Statement.search([])
                self.assertEqual(len(s_lst), 1)

                self.assertEqual(s_lst[0].state, 'draft')
                self.assertTrue(
                    s_lst[0].name.endswith('74061813/0000033626 | 15002'))
                self.assertEqual(s_lst[0].journal.name, 'AccStatJournal')
                self.assertEqual(len(s_lst[0].journal.bank_account.numbers), 1)
                self.assertEqual(
                    s_lst[0].journal.bank_account.numbers[0].number,
                    '74061813/0000033626')
                self.assertEqual(s_lst[0].date, date(2015, 4, 8))
                self.assertEqual(s_lst[0].start_balance, Decimal('25.43'))
                self.assertEqual(s_lst[0].end_balance, Decimal('25.69'))
                self.assertEqual(s_lst[0].total_amount, Decimal('0.26'))
                self.assertEqual(s_lst[0].number_of_lines, 10)
                self.assertEqual(len(s_lst[0].lines), 1)
                self.assertEqual(len(s_lst[0].origins), 10)

                # lines 1
                self.assertEqual(
                    s_lst[0].lines[0].invoice.number, inv_lst2[0].number)
                self.assertEqual(s_lst[0].lines[0].origin.rec_name, '2')
                self.assertTrue(
                    s_lst[0].lines[0].statement.rec_name.endswith(
                        '74061813/0000033626 | 15002'))
                self.assertEqual(s_lst[0].lines[0].number, '2')
                self.assertEqual(str(s_lst[0].lines[0].date), '2015-04-07')
                self.assertEqual(s_lst[0].lines[0].amount, Decimal('0.50'))
                self.assertEqual(
                    s_lst[0].lines[0].party.rec_name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].lines[0].account.rec_name,
                    'Main Receivable')
                self.assertEqual(
                    s_lst[0].lines[0].description,
                    'Verwendungszweck EREF: STZV-INV.0001-1113-1 IBAN:' +
                    ' DE14740618130000033626 BIC: GENODEF1PFK ' +
                    'ABWE: Testkonto 2')

                # origin 1
                self.assertEqual(s_lst[0].origins[0].number, '1')
                self.assertEqual(str(s_lst[0].origins[0].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[0].amount, Decimal('0.12'))
                self.assertEqual(
                    s_lst[0].origins[0].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[0].description,
                    'Zweite SEPA-Ueberweisung EREF: STZV-INV.0001-1113-' +
                    '2 IBAN: DE14740618130000033626 BIC: GENODEF1PFK ' +
                    'ABWE: Test')
                self.assertEqual(len(s_lst[0].origins[0].information), 16)
                # origin 2
                self.assertEqual(s_lst[0].origins[1].number, '2')
                self.assertEqual(str(s_lst[0].origins[1].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[1].amount, Decimal('0.50'))
                self.assertEqual(
                    s_lst[0].origins[1].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[1].description,
                    'Verwendungszweck EREF: STZV-INV.0001-1113-1 ' +
                    'IBAN: DE14740618130000033626 BIC: GENODEF1PFK ' +
                    'ABWE: Testkonto 2')
                self.assertEqual(len(s_lst[0].origins[1].information), 16)
                # origin 3
                self.assertEqual(s_lst[0].origins[2].number, '3')
                self.assertEqual(str(s_lst[0].origins[2].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[2].amount, Decimal('-0.33'))
                self.assertEqual(
                    s_lst[0].origins[2].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[2].description,
                    'Überweisung mit VR-Networld EREF: JS12345 IBAN: ' +
                    'DE14740618130000033626 BIC:GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[2].information), 16)
                # origin 4
                self.assertEqual(s_lst[0].origins[3].number, '4')
                self.assertEqual(str(s_lst[0].origins[3].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[3].amount, Decimal('-0.62'))
                self.assertEqual(s_lst[0].origins[3].party, None)
                self.assertEqual(
                    s_lst[0].origins[3].description,
                    'SEPA Sammel-Ueberweisung mit 2 Ueberweisungen ' +
                    'MSG-ID: STZV-Msg06042015-1113')
                self.assertEqual(len(s_lst[0].origins[3].information), 12)
                # origin 5
                self.assertEqual(s_lst[0].origins[4].number, '5')
                self.assertEqual(str(s_lst[0].origins[4].date), '2015-04-07')
                self.assertEqual(s_lst[0].origins[4].amount, Decimal('0.33'))
                self.assertEqual(s_lst[0].origins[4].party, None)
                self.assertEqual(
                    s_lst[0].origins[4].description,
                    'Überweisung mit VR-Networld EREF: JS12345 IBAN: ' +
                    'DE58740618130100033626 BIC:GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[4].information), 15)
                # origin 6
                self.assertEqual(s_lst[0].origins[5].number, '6')
                self.assertEqual(str(s_lst[0].origins[5].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[5].amount, Decimal('-0.45'))
                self.assertEqual(
                    s_lst[0].origins[5].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[5].description,
                    'BEITRAG 2015 Huber Gerhard Tennis JAHR 0,15 Fussball' +
                    ' JAHR 0,10 Tennis JAHR 0,20 EREF: PC-VAB-EtE060420' +
                    '15-1103-1 MREF: Mandat2 CRED: DE79ZZZ00000000584 IBAN:')
                self.assertEqual(len(s_lst[0].origins[5].information), 19)
                # origin 7
                self.assertEqual(s_lst[0].origins[6].number, '7')
                self.assertEqual(str(s_lst[0].origins[6].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[6].amount, Decimal('-0.35'))
                self.assertEqual(
                    s_lst[0].origins[6].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[6].description,
                    'BEITRAG 2015 Maier Max Fussball JAHR 0,10 Tennis' +
                    'JAHR 0,15 Fussball JAHR 0,10 EREF: PC-VAB-INV.0001-' +
                    '1103-2 MREF: Mandat1 CRED: DE79ZZZ00000000584 IBAN: DE')
                self.assertEqual(len(s_lst[0].origins[6].information), 19)
                # origin 8
                self.assertEqual(s_lst[0].origins[7].number, '8')
                self.assertEqual(str(s_lst[0].origins[7].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[7].amount, Decimal('0.54'))
                self.assertEqual(
                    s_lst[0].origins[7].party.name,
                    'Schliffenbacher Josef')
                self.assertEqual(
                    s_lst[0].origins[7].description,
                    'Testbuchung EREF: JS7654343 IBAN: DE1474061813000' +
                    '0033626 BIC: GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[7].information), 15)
                # origin 9
                self.assertEqual(s_lst[0].origins[8].number, '9')
                self.assertEqual(str(s_lst[0].origins[8].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[8].amount, Decimal('0.80'))
                self.assertEqual(s_lst[0].origins[8].party, None)
                self.assertEqual(
                    s_lst[0].origins[8].description,
                    'SEPA Sammel-Basislastschrift mit 2 Lastschriften' +
                    'MSG-ID: PC-VAB-Msg06042015-1103')
                self.assertEqual(len(s_lst[0].origins[8].information), 12)
                # origin 10
                self.assertEqual(s_lst[0].origins[9].number, '10')
                self.assertEqual(str(s_lst[0].origins[9].date), '2015-04-08')
                self.assertEqual(s_lst[0].origins[9].amount, Decimal('-0.54'))
                self.assertEqual(s_lst[0].origins[9].party, None)
                self.assertEqual(
                    s_lst[0].origins[9].description,
                    'Testbuchung EREF: JS7654343 IBAN: DE587406181301000' +
                    '33626 BIC: GENODEF1PFK')
                self.assertEqual(len(s_lst[0].origins[9].information), 16)

# end StatementTestCase


del Mt940TestCase
