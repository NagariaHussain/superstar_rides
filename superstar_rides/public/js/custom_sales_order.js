frappe.ui.form.on("Sales Order", {
    show_availability_in_dialog(frm, row, data) {
        let dialog = new frappe.ui.Dialog({
            title: __("Availability"),
            fields: [
                {
                    fieldtype: "Link",
                    options: "Item",
                    label: __("Item Code"),
                    fieldname: "item_code",
                    read_only: 1,
                    default: row.item_code
                },
                {
                    fieldtype: 'Table',
                    data: [],
                    fieldname: 'availability',
                    label: __('Availability'),
                    fields: [
                        {
                            fieldtype: "Link",
                            options: "Warehouse",
                            in_list_view: 1,
                            label: __("Warehouse"),
                            fieldname: "warehouse",
                        },
                        {
                            fieldtype: "Float",
                            in_list_view: 1,
                            label: __("Available Qty"),
                            fieldname: "actual_qty",
                        }
                    ]
                }
            ]
        });

        data.forEach(row => {
            dialog.fields_dict.availability.df.data.push({
                warehouse: row.warehouse,
                actual_qty: row.actual_qty
            })
        });

        dialog.fields_dict.availability.grid.refresh();

        dialog.show();
    }
})


frappe.ui.form.on("Sales Order Item", {
    show_availability(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        frappe.call({
            method: "superstar_rides.custom_folder.custom_sales_order.get_availability",
            args: {
                item_code: row.item_code
            },
            callback: function(r) {
                if (r.message) {
                    debugger
                    frm.events.show_availability_in_dialog(frm, row, r.message);
                }
            }
        });
    }
})