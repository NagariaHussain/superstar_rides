# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ride(Document):
    def before_save(self):
        self.total_amount = 0
        for item in self.cost_breakup:
            self.total_amount += item.cost
