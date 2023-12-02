# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool


class Book(metaclass=PoolMeta):
    __name__ = 'cashbook.book'

    analytic = fields.Many2One(
        string='Analytic Account', ondelete='RESTRICT',
        model_name='analytic_account.account',
        domain=[
            ('company.id', '=', Eval('company', -1)),
            ('type', 'in', ['normal', 'distribution']),
            ],
        depends=['company'])
    analytic_mode = fields.Selection(
        string='Method', depends=['analytic'],
        selection=[
            ('both', 'Item and Cash Book Line'),
            ('item', 'Item Line'),
            ('book', 'Cash Book Line'),
        ],
        help='Stores analytic amounts on one or both sides of the move.',
        states={
            'required': Bool(Eval('analytic')),
        })

    @classmethod
    def default_analytic_mode(cls):
        """ default: both
        """
        return 'both'

# end Book
