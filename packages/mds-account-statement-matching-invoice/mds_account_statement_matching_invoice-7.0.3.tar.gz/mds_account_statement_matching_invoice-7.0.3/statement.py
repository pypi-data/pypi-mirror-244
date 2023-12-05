# -*- coding: utf-8 -*-
# This file is part of the account-statement-matching-invoice-module
# from m-ds.de for Tryton. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from decimal import Decimal


class StatementImport(metaclass=PoolMeta):
    __name__ = 'account.statement.import'

    def do_import_(self, action):
        """ try to find invoices for account statement lines
        """
        pool = Pool()
        Statement = pool.get('account.statement')
        StatementLine = pool.get('account.statement.line')
        Invoice = pool.get('account.invoice')

        (action, data) = super(StatementImport, self).do_import_(action)

        if 'res_id' in data:
            for i in data['res_id']:
                stm = Statement(i)
                for k in stm.origins:
                    if (k.party is None) or (k.amount is None) or \
                            (k.description is None):
                        continue
                    if k.amount == Decimal('0.0'):
                        continue

                    # find candidates of unpaied invoices
                    invoices = Invoice.search([
                            ('party', '=', k.party),
                            ('state', '=', 'posted'),
                            ('total_amount', '=', k.amount),
                        ])
                    # check if invoice number appears
                    # in purpose of statement lines
                    for invoice in invoices:
                        if invoice.number is None:
                            continue

                        if (invoice.number.lower() in k.description.lower()):
                            # match!
                            stm_lines = list(stm.lines)
                            stm_lines.append(StatementLine(
                                related_to=invoice, account=invoice.account, origin=k))
                            k.account = invoice.account
                            k.save()
                            stm.lines = stm_lines
                            # fill fields of statement line from origin
                            stm.lines[len(stm.lines) - 1].on_change_related_to()
                            stm.lines[len(stm.lines) - 1].on_change_origin()
                            stm.on_change_lines()
                            stm.save()
                            break
        return (action, data)

# end StatementImport
