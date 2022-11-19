# Copyright (c) 2022, Hussain and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class Vehicle(WebsiteGenerator):
    def before_save(self):
        if not self.route:
            self.route = f"/vehicles/{self.name}"
