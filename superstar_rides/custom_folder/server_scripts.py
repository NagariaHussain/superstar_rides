import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def create_ride(ride_order):
	doc = frappe.new_doc("Ride")
	return doc





















'''
@frappe.whitelist()
def create_sales_invoice(source_name, target_doc=None):
	def update_item_quantity(source, target, source_parent) -> None:
		pass

	doc = get_mapped_doc(
		"Ride",
		source_name,
		{
			"Ride": {"doctype": "Sales Invoice"},
			"Ride Details": {
				"doctype": "Sales Invoice Item",
				"field_map": {"parent": "ride", "name": "ride_details"},
				"postprocess": update_item_quantity
			},
		},
		target_doc,
	)

	return doc


@frappe.whitelist()
def create_purchase_invoice(source_name, target_doc=None):
	def update_item_quantity(source, target, source_parent) -> None:
		pass

	doc = get_mapped_doc(
		"Ride",
		source_name,
		{
			"Ride": {"doctype": "Purchase Invoice"},
			"Ride Details": {
				"doctype": "Purchase Invoice Item",
				"field_map": {"parent": "ride", "name": "ride_details"},
				"postprocess": update_item_quantity
			},
		},
		target_doc,
	)

	return doc
'''