// Copyright (c) 2022, Hussain and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Billing Details"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		}
	]
};
