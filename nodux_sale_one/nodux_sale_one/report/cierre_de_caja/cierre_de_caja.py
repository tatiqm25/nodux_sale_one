# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _

def execute(filters=None):
	if not filters: filters = {}

	invoice_list = get_invoices(filters)
	columns = get_columns()

	if not invoice_list:
		msgprint(_("No record found"))
		return columns, invoice_list

	total_ventas = get_total_ventas(filters)
	credito = get_credito(filters)
	cobros_abonos = get_cobros_abonos(filters)
	total_gastos = get_total_gastos(filters)

	data = []

	row1 = ["VENTAS AL CONTADO"]
	row2 = ["TOTAL VENTAS EFECTIVO", total_ventas]
	row3 = ["VENTAS A CREDITO", ]
	row4 = ["VENTAS A CREDITO", credito]
	row5 = ["DETALLE DE RECAUDACIONES DE CXC"]
	row6 = ["COBROS Y ABONOS POR VENTAS A CREDITO", cobros_abonos]
	row7 = ["GASTOS"]
	row8 = ["TOTAL GASTOS", total_gastos]
	row9 = ["FLUJO DE EFECTIVO"]
	row10 = ["TOTAL DE VENTAS", total_ventas]
	row11 = ["COBROS Y ABONOS POR VENTAS A CREDITO", cobros_abonos]
	row12 = ["(-)GASTOS", total_gastos]
	row13 = ["TOTAL CAJA", ((total_ventas+cobros_abonos)-total_gastos)]

	data.append(row1)
	data.append(row2)
	data.append(row3)
	data.append(row4)
	data.append(row5)
	data.append(row6)
	data.append(row7)
	data.append(row8)
	data.append(row9)
	data.append(row10)
	data.append(row11)
	data.append(row12)
	data.append(row13)

	return columns, data

def get_columns():
	columns = [
		_("Description") + "::360", _("Amount") + ":Currency/currency:120"]

	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company=%(company)s"
	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"

	return conditions

def get_conditions_payments(filters):
	conditions = ""

	if filters.get("from_date"): conditions += " and date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and date <= %(to_date)s"

	return conditions

def get_total_ventas(filters):
	conditions = get_conditions(filters)
	invoices = frappe.db.sql("""select posting_date, due_date, total from `tabSales Invoice One`
		where docstatus = 1 %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)
	total = 0

	for i in invoices:
		if i.posting_date == i.due_date:
			total += i.total

	return total

def get_credito(filters):
	conditions = get_conditions(filters)
	invoices = frappe.db.sql("""select name, posting_date, due_date, total from `tabSales Invoice One`
		where docstatus = 1 %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)
	total = 0

	for i in invoices:
		if i.due_date > i.posting_date:
			total += i.total

	return total

def get_cobros_abonos(filters):
	conditions = get_conditions_payments(filters)

	invoices = frappe.db.sql("""select amount, date from `tabSales Invoice Payment One`
		where amount > 0 %s order by date desc, amount desc""" %
		conditions, filters, as_dict=1)
	total = 0

	for i in invoices:
		total += i.amount

	return total

def get_total_gastos(filters):
	conditions = get_conditions(filters)
	invoices = frappe.db.sql("""select posting_date, due_date, total from `tabPurchases Invoice One`
		where docstatus = 1 %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)
	total = 0

	for i in invoices:
		total += i.total

	return total

def get_invoices(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select name, posting_date, customer, customer_name,
		total, paid_amount, residual_amount
		from `tabSales Invoice One`
		where docstatus = 1 and status ='Confirmed' %s order by posting_date desc, name desc""" %
		conditions, filters, as_dict=1)
