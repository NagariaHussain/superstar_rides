# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	chart_data = get_chart_data(data)

	return columns, data, None, chart_data

def get_chart_data(data):
	return {
		"data": {
			"labels": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
			"datasets": [
				{ "name": "Dataset 1", "values": [18, 40, 30, 35, 8, 52, 17, -4] },
			]
		},
		"type": "bar",
	}

def get_columns():
	return [
		{
			"label": _("Ride ID"),
			"fieldname": "ride_id",
			"fieldtype": "Link",
			"options": "Ride",
		},
		{
			"label": _("Ride Order"),
			"fieldname": "ride_order",
			"fieldtype": "Link",
			"options": "Ride Order",
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"label": _("Vehicle"),
			"fieldname": "vehicle",
			"fieldtype": "Link",
			"options": "Vehicle"
		},
		{
			"label": _("Sales Invoice Id"),
			"fieldname": "sales_invoice_id",
			"fieldtype": "Link",
			"options": "Sales Invoice"
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency"
		},
		{
			"label": _("Sales Invoice Amount"),
			"fieldname": "rounded_total",
			"fieldtype": "Float",
		},
		{
			"label": _("Outstanding Amount"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"options": "currency"
		}
	]

def get_data(filters):
	ride_details = frappe.get_all("Ride",
		fields = ["ride_order", "name", "customer", "vehicle"]
	)

	invoice_cond = ""
	if filters.get("sales_invoice_id"):
		invoice_cond = f" AND `tabSales Invoice`.name = '{filters.sales_invoice_id}'"

	sales_invoice_details = frappe.db.sql(f"""
		SELECT
			`tabSales Invoice`.name as sales_invoice_id,
			`tabSales Invoice`.rounded_total,
			`tabSales Invoice`.outstanding_amount,
			`tabSales Invoice Item`.item_code,
			`tabSales Invoice Item`.ride
		FROM
			`tabSales Invoice`, `tabSales Invoice Item`
		WHERE
			`tabSales Invoice`.name = `tabSales Invoice Item`.parent
			AND `tabSales Invoice Item`.docstatus < 2
			AND `tabSales Invoice Item`.ride IS NOT NULL
			{invoice_cond}
	""", as_dict=1)

	ride_billing_details = {}
	for row in sales_invoice_details:
		ride_billing_details.setdefault(row.ride, []).append(row)

	data = []

	for ride in ride_details:
		ride_dict = {
			"ride_id": ride.name,
			"ride_order": ride.ride_order,
			"customer": ride.customer,
			"vehicle": ride.vehicle,
			"currency": "USD"
		}

		if ride_billing_details.get(ride.name):
			for invoice_details in ride_billing_details.get(ride.name):
				ride_dict.update({
					"sales_invoice_id": invoice_details.sales_invoice_id,
					"item_code": invoice_details.item_code,
					"rounded_total": invoice_details.rounded_total,
					"outstanding_amount": invoice_details.outstanding_amount
				})
				data.append(ride_dict)

	return data