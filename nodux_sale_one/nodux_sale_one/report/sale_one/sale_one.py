# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt
#	columns, data = [], []
#	return columns, data

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

	income_accounts = []
	invoice_income_map = get_invoice_income_map(invoice_list)
	invoice_income_map, invoice_tax_map = get_invoice_tax_map(invoice_list,
		invoice_income_map, income_accounts)

	invoice_so_dn_map = get_invoice_so_dn_map(invoice_list)
	customer_map = get_customer_details(invoice_list)
	company_currency = frappe.db.get_value("Company", filters.company, "default_currency")
	mode_of_payments = get_mode_of_payments([inv.name for inv in invoice_list])

	data = []
	for inv in invoice_list:
		# invoice details
		sales_order = list(set(invoice_so_dn_map.get(inv.name, {}).get("sales_order", [])))
		delivery_note = list(set(invoice_so_dn_map.get(inv.name, {}).get("delivery_note", [])))

		row = [inv.name, inv.posting_date, inv.customer, inv.customer_name, inv.base_imponible,
		inv.total_taxes, inv.total, inv.residual_amount]
		data.append(row)

	return columns, data


def get_columns(invoice_list):
	"""return columns based on filters"""
	columns = [
		_("Invoice") + ":Link/Sales Invoice One:120", _("Posting Date") + ":Date:80",
		_("Customer Id") + "::120", _("Customer Name") + "::120"]


	columns = columns + [_("Net Total") + ":Currency/currency:120"] + \
		[_("Total Tax") + ":Currency/currency:120", _("Grand Total") + ":Currency/currency:120",
		_("Outstanding Amount") + ":Currency/currency:120"]

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
		base_imponible, total_taxes, total, residual_amount
		from `tabSales Invoice One`
		where docstatus = 1 %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)

def get_invoice_income_map(invoice_list):
	invoice_income_map = {}
	return invoice_income_map

def get_invoice_tax_map(invoice_list, invoice_income_map, income_accounts):
	invoice_tax_map = {}
	return invoice_income_map, invoice_tax_map

def get_invoice_so_dn_map(invoice_list):
	invoice_so_dn_map = {}

	return invoice_so_dn_map

def get_customer_details(invoice_list):
	customer_map = {}
	customers = list(set([inv.customer for inv in invoice_list]))
	for cust in frappe.db.sql("""select name, territory, customer_group from `tabCustomer`
		where name in (%s)""" % ", ".join(["%s"]*len(customers)), tuple(customers), as_dict=1):
			customer_map.setdefault(cust.name, cust)

	return customer_map


def get_mode_of_payments(invoice_list):
	mode_of_payments = {}

	return mode_of_payments
