import frappe
from frappe import _


def get_data():
	return {
		"fieldname": "ride",
		"transactions": [
			{
				"label": _("Sales"),
				"items": ["Sales Invoice"],
			},
			{
				"label": _("Purchase"),
				"items": ["Purchase Invoice"],
			}
		]
	}