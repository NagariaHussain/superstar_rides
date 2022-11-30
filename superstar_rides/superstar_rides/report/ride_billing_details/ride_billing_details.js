// Copyright (c) 2022, Hussain and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ride Billing Details"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle",
		}
	],
};








































// "formatter": function(value, row, column, data, default_formatter) {
// 	value = default_formatter(value, row, column, data);

// 	if (column.fieldname == "production_item_name" && data && data.qty_to_manufacture > data.available_qty ) {
// 		value = `<div style="color:red">${value}</div>`;
// 	}

// 	if (column.fieldname == "production_item" && !data.name ) {
// 		value = "";
// 	}

// 	if (column.fieldname == "raw_material_name" && data && data.required_qty > data.allotted_qty ) {
// 		value = `<div style="color:red">${value}</div>`;
// 	}

// 	return value;
// },