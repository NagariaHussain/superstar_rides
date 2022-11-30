frappe.pages['training-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Vehicle List',
		single_column: true
	});

	new erpnext.VehicleListView(wrapper);
}

erpnext.VehicleListView = class VehicleListView {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.page = wrapper.page;
		this.body = $('<div></div>').appendTo(this.wrapper);
		this.layout = $(wrapper).find(".layout-main")
		this.setup_filters();
		this.get_data();
		this.render_data();
	}

	setup_filters() {
		this.page.add_field({
			fieldname: 'vehicle',
			label: __('Vehicle'),
			fieldtype: 'Link',
			options: 'Vehicle',
			reqd: 1,
			change: () => {
				this.training_session = this.page.fields_dict.training_session.get_value();
				this.get_data();
			}
		});
	}
}