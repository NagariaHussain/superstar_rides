# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Driver(Document):
	def on_update(self):
		self.create_supplier()

	def create_supplier(self):
		if not frappe.db.exists("Supplier", {"driver": self.name}):
			frappe.get_doc({
				"doctype": "Supplier",
				"supplier_name": self.full_name,
				"supplier_type": "Individual",
				"supplier_group": "Driver",
				"driver": self.name
			}).insert(ignore_permissions=True)
