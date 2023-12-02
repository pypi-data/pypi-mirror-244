# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool


class Line(metaclass=PoolMeta):
    __name__ = 'cashbook.line'

    analytic_lines = fields.Function(fields.One2Many(
        string='Analytic Lines', readonly=True, field=None,
        model_name='analytic_account.line',
        states={
            'invisible': ~Bool(Eval('analytic_lines')),
        }),
        'on_change_with_analytic_lines')

    @fields.depends('moves')
    def on_change_with_analytic_lines(self, name=None):
        """ get analytic-lines of move-line
        """
        if len(self.moves) > 0:
            return [
                z.id for x in self.moves
                for y in x.lines for z in y.analytic_lines]

    @classmethod
    def get_create_analytic_lines(cls, account, move_date, credit, debit):
        """ generate code to create analytic-lines
        """
        debit_lst = account.distribute(debit)
        credit_lst = account.distribute(credit)

        # put credit/debits-lists in one dict
        analytic_dict = {x[0].id: {'credit': x[1]} for x in credit_lst}
        for x in debit_lst:
            analytic_dict[x[0].id]['debit'] = x[1]

        lines = [{
                'account': x,
                'date': move_date,
                'credit': analytic_dict[x]['credit'],
                'debit': analytic_dict[x]['debit'],
            } for x in analytic_dict.keys()]

        return [('create', lines)]

    @classmethod
    def get_book_line(cls, line_date, cashbook, amounts):
        """ create line for book-boooking
        """
        move_line = super(Line, cls).get_book_line(
            line_date, cashbook, amounts)

        analytic_account = cashbook.analytic
        analytic_mode = cashbook.analytic_mode

        if analytic_account and (analytic_mode in ['both', 'book']):
            move_line['analytic_lines'] = \
                cls.get_create_analytic_lines(
                    account=analytic_account,
                    move_date=line_date,
                    credit=move_line['credit'],
                    debit=move_line['debit'])
        return move_line

    @classmethod
    def get_article_lines(cls, line, description=None):
        """ add analytic account
        """
        move_lines = super(Line, cls).get_article_lines(line, description)

        analytic_account = None
        analytic_mode = None
        cb_line = None
        if line.__name__ == 'cashbook.line':
            cb_line = line
        elif line.__name__ == 'cashbook.split':
            cb_line = line.line
        else:
            raise ValueError('invalid model: %s' % line._name__)

        analytic_account = cb_line.cashbook.analytic
        analytic_mode = cb_line.cashbook.analytic_mode

        if analytic_account and (analytic_mode in ['both', 'item']):
            for num in range(len(move_lines)):
                move_lines[num]['analytic_lines'] = \
                    cls.get_create_analytic_lines(
                        account=analytic_account,
                        move_date=cb_line.date,
                        credit=move_lines[num]['credit'],
                        debit=move_lines[num]['debit'])
        return move_lines

# end Line
