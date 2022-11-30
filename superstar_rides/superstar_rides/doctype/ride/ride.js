// Copyright (c) 2022, Hussain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ride", {
	setup(frm) {
        frm.set_query("item_code", "cost_breakup", () => {
            return {
                filters: {
                    item_group: "Services",
                    is_stock_item: 0
                }
            }
        });

        frm.set_query("price_list", () => {
            return {
                filters: {
                    selling: 1
                }
            }
        });
	},

    refresh(frm) {
        frm.trigger("make_sales_invoice")
    },

    make_sales_invoice(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Sales Invoice"), () => {
                frappe.model.open_mapped_doc({
                    method: "superstar_rides.superstar_rides.doctype.ride.ride.make_sales_invoice",
                    frm: frm
                });
            }, __("Make"))
        }
    }
});





























// refresh(frm) {
//     if (frm.doc.docstatus === 1) {
//         frm.add_custom_button("Make Invoice", () => {
//             frappe.model.open_mapped_doc({
//                 method: "superstar_rides.custom_folder.server_scripts.make_invoice",
//                 frm: frm
//             });
//         });
//     }
// }