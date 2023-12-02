# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.cashbook.tests.test_module import CashbookTestCase
from .category import CategoryTestCase
from .line import LineTestCase


class CashbookAccountTestCase(
        CategoryTestCase,
        LineTestCase,
        CashbookTestCase):
    """ run all test from 'cashbook', add test for accounting
    """
    module = 'cashbook_account'

# end CashbookAccountTestCase


del CashbookTestCase
