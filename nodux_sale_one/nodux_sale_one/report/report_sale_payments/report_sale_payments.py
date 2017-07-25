# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _

def execute(filters=None):
	#moificar columns y verificar filtros
	if not filters: filters = {}

	invoice_list = get_invoices(filters)
	columns = get_columns(invoice_list)

	if not invoice_list:
		msgprint(_("No record found"))
		return columns, invoice_list

	data = []
	for inv in invoice_list:
		row = [inv.name, inv.posting_date, inv.customer, inv.total, inv.paid_amount]
		data.append(row)
	return columns, data


def get_columns(invoice_list):
	"""return columns based on filters"""
	columns = [
		_("Invoice") + ":Link/Sales Invoice One:150", _("Posting Date") + ":Date:80",
		_("Customer Name") + "::360"]
	columns = columns + [_("Grand Total") + ":Currency/currency:120",
		_("Payment Amount") + ":Currency/currency:120"]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"): conditions += " and company=%(company)s"
	if filters.get("customer"): conditions += " and customer = %(customer)s"
	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"

	return conditions

def get_invoices(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select name, posting_date, customer, customer_name,
		total, paid_amount
		from `tabSales Invoice One`
		where docstatus = 1 %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)
