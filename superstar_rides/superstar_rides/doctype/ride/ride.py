# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document


class Ride(Document):
	def before_save(self):
		self.total_amount = 0
		for item in self.cost_breakup:
			self.total_amount += item.cost

	def before_submit(self):
		self.validate_customer()

	def validate_customer(self):
		if not frappe.db.exists("Customer", self.customer):
			frappe.throw(_(f"Customer {self.customer} does not exist"))

	def on_submit(self):
		self.create_sales_invoice()
		self.create_purchase_invoice()

	def create_sales_invoice(self):
		doc = make_sales_invoice(self.name)
		doc.save()

	def create_purchase_invoice(self):
		make_purchase_invoice(self)

	def on_cancel(self):
		self.delete_sales_invoice()

	def delete_sales_invoice(self):
		sales_invoices = frappe.get_all("Sales Invoice Item",
			fields = ["distinct parent as name"],
			filters = {
				"ride": self.name,
			}
		)

		for row in sales_invoices:
			if frappe.db.get_value("Sales Invoice", row.name, "docstatus") == 1:
				frappe.throw(_(f"Sales Invoice {row.name} is submitted, kindly cancel it first."))

			frappe.delete_doc("Sales Invoice", row.name)


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item_quantity(source, target, source_parent):
		target.qty = 1
		target.rate = source.cost
		target.amount = source.cost

	doclist = get_mapped_doc(
		"Ride",
		source_name,
		{
			"Ride": {
				"doctype": "Sales Invoice",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Ride Cost Breakup": {
				"doctype": "Sales Invoice Item",
				"field_map": {
					"parent": "ride",
					"name": "ride_details",
				},
				"postprocess": update_item_quantity,
				"condition": lambda doc: doc.docstatus == 1,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist


def make_purchase_invoice(ride):
	doc = frappe.new_doc("Purchase Invoice")
	doc.supplier = frappe.db.get_value("Supplier", {"driver": ride.driver}, "name")
	doc.due_date = today()

	for row in ride.cost_breakup:
		uom = frappe.db.get_value("Item", row.item_code, "stock_uom")

		item = doc.append("items", {
			"item_code": row.item_code,
			"qty": 1,
			"ride": ride.name,
			"ride_details": row.name,
			"rate": row.cost,
			"amount": row.cost,
			"uom": uom,
			"stock_uom": uom,
			"conversion_factor": 1,
		})

	doc.set_missing_values()
	doc.calculate_taxes_and_totals()

	doc.save()

	return doc

@frappe.whitelist()
def test_method():
	return "Test method"