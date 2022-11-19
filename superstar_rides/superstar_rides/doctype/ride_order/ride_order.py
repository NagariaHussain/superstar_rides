# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RideOrder(Document):
    def before_insert(self):
        session_user = frappe.session.user
        self.customer = session_user
