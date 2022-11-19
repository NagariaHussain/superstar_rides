// Copyright (c) 2022, Hussain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ride Order", {
  refresh(frm) {
    frm.add_custom_button(
      "Create Ride",
      () => {
        let dialog = new frappe.ui.Dialog({
          title: "Select Driver",
          fields: [
            {
              fieldtype: "Link",
              fieldname: "driver",
              label: "Driver",
              options: "Driver",
            },
          ],
          primary_action_label: "Create Ride",
          primary_action: (data) => {
            console.log(data);
            let { driver } = data;

            frappe.new_doc("Ride", {
              ride_order: frm.doc.name,
              driver: driver,
            });
          },
        });

        dialog.show();
      },
      "Actions"
    );
  },
});
