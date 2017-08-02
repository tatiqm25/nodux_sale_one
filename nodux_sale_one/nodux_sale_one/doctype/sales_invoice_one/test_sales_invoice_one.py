# -*- coding: utf-8 -*-
# Copyright (c) 2015, NODUX and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

# test_records = frappe.get_test_records('Sale Invoice One')
class TestSaleInvoiceOne(unittest.TestCase):
	create_sales_invoice(customer="_Test Customer USD", currency="USD")

def create_sales_invoice(**args):
	si = frappe.new_doc("Sales Invoice One")
	args = frappe._dict(args)
	if args.posting_date:
		si.set_posting_time = 1
	si.posting_date = args.posting_date or nowdate()

	si.company = args.company or "_Test Company"
	si.customer = args.customer or "_Test Customer"
	si.currency=args.currency or "INR"

	si.append("items", {
		"item_code": args.item or args.item_code or "_Test Item",
		"qty": args.qty or 1,
		"income_account": "Sales - _TC",
		"expense_account": "Cost of Goods Sold - _TC",
		"serial_no": args.serial_no
	})

	if not args.do_not_save:
		si.insert()
		if not args.do_not_submit:
			si.submit()
	return si
