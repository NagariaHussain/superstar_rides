import frappe
from frappe.utils import add_days

def on_submit_events(doc, method=None):
	create_purchase_order(doc)

def create_purchase_order(doc):
	'''
		po_mapper = {
			"Supplier 1": [
				so_item_object1,
				so_item_object2,
			],
			"Supplier 2": [
				so_item_object3,
				so_item_object4,
			]
		}
	'''

	po_mapper = {}

	for row in doc.items:
		default_supplier = frappe.db.get_value("Item Default",
			{"parent": row.item_code, "company": doc.company}, "default_supplier")

		actual_qty = frappe.db.get_value("Bin",
			{"item_code": row.item_code, "warehouse": row.warehouse},
			["actual_qty"]
		)

		if row.qty > actual_qty:
			po_mapper.setdefault(default_supplier, []).append(row)

	for supplier, so_list in po_mapper.items():
		po_doc = frappe.get_doc({
			"doctype": "Purchase Order",
			"supplier": supplier,
			"company": doc.company,
			"schedule_date": add_days(doc.delivery_date, -1),
			"price_list": "Standard Buying",
		})

		for row in so_list:
			rate = frappe.db.get_value("Item Price",
				{"price_list": "Standard Buying", "item_code": row.item_code},
				"price_list_rate"
			)

			po_doc.append("items", {
				"item_code": row.item_code,
				"item_name": row.item_name,
				"description": row.description,
				"qty": row.qty,
				"uom": row.uom,
				"conversion_factor": 1,
				"rate": rate,
				"amount": rate * row.qty,
			})
		po_doc.set_missing_values()
		po_doc.calculate_taxes_and_totals()

		po_doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_availability(item_code):
	return frappe.get_all("Bin",
		fields = ["warehouse", "actual_qty"],
		filters = {
			"item_code": item_code,
			"actual_qty": [">", 0]
		},
	)