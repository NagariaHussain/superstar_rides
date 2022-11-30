// Copyright (c) 2022, Hussain and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ride Billing Report"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "MultiSelectList",
			options: "Vehicle",
			get_data: function(txt) {
				return frappe.db.get_link_options('Vehicle', txt);
			}
		},
		{
			fieldname: "sales_invoice_id",
			label: __("Sales Invoice"),
			fieldtype: "Link",
			options: "Sales Invoice",
			get_query: function() {
				return {
					filters: {
						"docstatus": ["<", 2]
					}
				}
			}
		},
		{
			fieldname: "posting_date",
			label: __("Sales Invoice Date"),
			fieldtype: "Date",

		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "sales_invoice_id") {
			let color = "red";
			if (!data["outstanding_amount"]) {
				color = "green";
			}

			value = "<a style='color:" + color + "' href='app/sales-invoice/" + data.sales_invoice_id + "'>" + data.sales_invoice_id + "</a>";
		}

		return value;
	}
};
