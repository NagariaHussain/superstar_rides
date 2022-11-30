import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def create_ride(ride_order):
	doc = frappe.new_doc("Ride")
	return doc


def on_update_events(doc, method=None):
	create_customer(doc)

def create_customer(doc):
	frappe.get_doc({
		"doctype": "Customer",
		"customer_name": doc.full_name,
		"customer_group": "Commercial",
		"territory": "All Territories",
		"customer_type": "Individual"
	}).insert(ignore_permissions=True)


















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
			"Ride Cost Breakup": {
				"doctype": "Sales Invoice Item",
				# "field_map": {"parent": "ride", "name": "ride_details"},
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