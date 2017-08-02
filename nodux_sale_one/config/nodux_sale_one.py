from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Reporte Venta"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "report",
					"name": "Cierre de Caja",
					"doctype": "Sales Invoice One",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Report Receivable",
					"doctype": "Sales Invoice One",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Report Sale Payments",
					"doctype": "Sales Invoice One",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Sale One",
					"doctype": "Sales Invoice One",
					"is_query_report": True
				}

			]
		}
	]
