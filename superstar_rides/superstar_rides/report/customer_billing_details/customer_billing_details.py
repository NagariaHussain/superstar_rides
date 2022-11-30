# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	return columns, data

def get_columns():
	return [
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Invoice Date"),
			"fieldname": "invoice_date",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": _("Invoice Number"),
			"fieldname": "invoice_number",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Invoice Amount"),
			"fieldname": "invoice_amount",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Invoice Status"),
			"fieldname": "invoice_status",
			"fieldtype": "Data",
			"width": 150
		}
	]