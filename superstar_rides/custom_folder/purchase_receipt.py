import frappe
from frappe.utils import flt
from frappe import _
from erpnext.accounts.general_ledger import (
	process_gl_map,
)
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt

class CustomPurchaseReceipt(PurchaseReceipt):
	def get_gl_entries(
		self, warehouse_account=None, default_expense_account=None, default_cost_center=None
	):

		items = [d.item_code for d in self.items]
		warehouse_account = get_item_account_map(items)

		sle_map = self.get_stock_ledger_details()
		voucher_details = self.get_voucher_details(default_expense_account, default_cost_center, sle_map)

		gl_list = []
		warehouse_with_no_account = []
		precision = self.get_debit_field_precision()
		for item_row in voucher_details:
			sle_list = sle_map.get(item_row.name)
			sle_rounding_diff = 0.0
			if sle_list:
				for sle in sle_list:
					if warehouse_account.get(item_row.item_code):
						# from warehouse account

						sle_rounding_diff += flt(sle.stock_value_difference)

						self.check_expense_account(item_row)

						# expense account/ target_warehouse / source_warehouse
						if item_row.get("target_warehouse"):
							warehouse = item_row.get("target_warehouse")
							expense_account = warehouse_account[item_row.item_code]["account"]
						else:
							expense_account = item_row.expense_account

						gl_list.append(
							self.get_gl_dict(
								{
									"account": warehouse_account[item_row.item_code]["account"],
									"against": expense_account,
									"cost_center": item_row.cost_center,
									"project": item_row.project or self.get("project"),
									"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
									"debit": flt(sle.stock_value_difference, precision),
									"is_opening": item_row.get("is_opening") or self.get("is_opening") or "No",
								},
								warehouse_account[item_row.item_code]["account_currency"],
								item=item_row,
							)
						)

						gl_list.append(
							self.get_gl_dict(
								{
									"account": expense_account,
									"against": warehouse_account[item_row.item_code]["account"],
									"cost_center": item_row.cost_center,
									"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
									"debit": -1 * flt(sle.stock_value_difference, precision),
									"project": item_row.get("project") or self.get("project"),
									"is_opening": item_row.get("is_opening") or self.get("is_opening") or "No",
								},
								item=item_row,
							)
						)
					elif item_row.item_code not in warehouse_with_no_account:
						warehouse_with_no_account.append(item_row.item_code)

			if abs(sle_rounding_diff) > (1.0 / (10**precision)) and self.is_internal_transfer():
				warehouse_asset_account = ""
				if self.get("is_internal_customer"):
					warehouse_asset_account = warehouse_account[item_row.item_code]["account"]
				elif self.get("is_internal_supplier"):
					warehouse_asset_account = warehouse_account[item_row.item_code]["account"]

				expense_account = frappe.get_cached_value("Company", self.company, "default_expense_account")

				gl_list.append(
					self.get_gl_dict(
						{
							"account": expense_account,
							"against": warehouse_asset_account,
							"cost_center": item_row.cost_center,
							"project": item_row.project or self.get("project"),
							"remarks": _("Rounding gain/loss Entry for Stock Transfer"),
							"debit": sle_rounding_diff,
							"is_opening": item_row.get("is_opening") or self.get("is_opening") or "No",
						},
						warehouse_account[item_row.item_code]["account_currency"],
						item=item_row,
					)
				)

				gl_list.append(
					self.get_gl_dict(
						{
							"account": warehouse_asset_account,
							"against": expense_account,
							"cost_center": item_row.cost_center,
							"remarks": _("Rounding gain/loss Entry for Stock Transfer"),
							"credit": sle_rounding_diff,
							"project": item_row.get("project") or self.get("project"),
							"is_opening": item_row.get("is_opening") or self.get("is_opening") or "No",
						},
						item=item_row,
					)
				)

		if warehouse_with_no_account:
			for item_code in warehouse_with_no_account:
				frappe.throw(_(f"Inventory account not set for the item {item_code}"))

		return process_gl_map(gl_list, precision=precision)

def get_item_account_map(items):
	item_inventory_account = frappe._dict()
	for row in frappe.get_all("Item",
		fields= ["name", "inventory_account"],
		filters= {"name": ["in", items]}
	):
		item_inventory_account[row.name] = {
			"account": row.inventory_account,
			"account_currency": frappe.get_cached_value("Account", row.inventory_account, "account_currency")
		}

	return item_inventory_account