# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Nodux Sale One",
			"color": "red",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Nodux Sale One")
		},

		{
			"module_name": "Nodux Sale One",
			"_doctype": "Sales Invoice One",
			"color": "#f39c12",
			"icon": "octicon octicon-package",
			"type": "link",
			"link": "List/Sales Invoice One"
		}
	]
