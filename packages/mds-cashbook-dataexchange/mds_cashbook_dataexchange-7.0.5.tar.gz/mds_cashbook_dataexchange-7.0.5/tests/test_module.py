# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.modules.cashbook.tests.test_module import CashbookTestCase
from .category import CategoryTestCase
from .party import PartyTestCase
from .transaction import TransactionTestCase


class CashbookExchangeTestCase(
        CashbookTestCase,
        CategoryTestCase,
        PartyTestCase,
        TransactionTestCase):
    'Test cashbook exchange module'
    module = 'cashbook_dataexchange'

# end CashbookExchangeTestCase


del CashbookTestCase
