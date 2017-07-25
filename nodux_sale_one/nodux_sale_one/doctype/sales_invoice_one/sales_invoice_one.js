// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice One', {
	onload: function(frm) {
		var me = this;
		// if (!frm.doc.status)
		// 	frm.doc.status = 'Draft';
		frm.refresh_fields();

		frm.call({
			method: "nodux_sale_one.nodux_sale_one.doctype.sales_invoice_one.sales_invoice_one.get_series",
			callback: function(r) {
				if(!r.exc) {
					set_field_options("naming_series", r.message);
				}
			}
		});

	},

	refresh: function(frm) {
		// if (frm.doc.status == 'Draft') {
		// 	frm.add_custom_button(__("Quotation"), function() {
		// 		frm.events.update_to_quotation_sale(frm);
		// 	}).addClass("btn-primary");
		// }
		// if (frm.doc.status == 'Quotation' && frm.doc.docstatus=='1') {
		// 	frm.add_custom_button(__("Payment"), function() {
		// 		frm.events.update_to_pay_sale(frm);
		// 	}).addClass("btn-primary");
		// }

		if (frm.doc.status == 'Draft' && frm.doc.docstatus=='1') {
			frm.add_custom_button(__("Payment"), function() {
				frm.events.update_to_pay_sale(frm);
			}).addClass("btn-primary");
		}

		if (frm.doc.status == 'Confirmed' && frm.doc.docstatus=='1') {
			frm.add_custom_button(__("Payment"), function() {
				frm.events.update_to_pay_sale(frm);
			}).addClass("btn-primary");
		}

		if (frm.doc.status == 'Done' && frm.doc.docstatus=='1') {
			frm.add_custom_button(__("Anulled"), function() {
				frm.events.update_to_anulled_sale(frm);
			}).addClass("btn-primary");
		}
		frm.refresh_fields();
	},

	customer: function(frm) {
		if (frm.doc.customer){
			frm.set_value("customer_name", frm.doc.customer);
			frm.set_value("due_date", frappe.datetime.nowdate());
		}
		frm.refresh_fields();
	},

	update_to_quotation_sale: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_to_quotation_sale",
			freeze: true,
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		})
	},

	update_to_anulled_sale: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_to_anulled_sale",
			freeze: true,
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		})
	},

	update_to_pay_sale: function(frm) {
		var d = new frappe.ui.Dialog({
			title: __("Payment"),
			fields: [
				{"fieldname":"customer", "fieldtype":"Link", "label":__("Customer"),
					options:"Customer", reqd: 1, label:"Customer", "default":frm.doc.customer_name},
				{"fieldname":"total", "fieldtype":"Currency", "label":__("Total Amount"),
					label:"Total Amount", "default":frm.doc.residual_amount},
				{fieldname:"pay", "label":__("Pay"), "fieldtype":"Button"}]
		});

		d.get_input("pay").on("click", function() {
			var values = d.get_values();
			if(!values) return;
			if(values["total"] < 0) frappe.throw("Ingrese monto a pagar");
			if(values["total"] > frm.doc.total) frappe.throw("Monto a pagar no puede ser mayor al monto total de venta");
			return frappe.call({
				doc: frm.doc,
				method: "update_to_pay_sale",
				args: values,
				freeze: true,
				callback: function(r) {
					var row = frm.add_child("payments");
					row.amount = values["total"];
					row.date = frappe.datetime.nowdate();
					d.hide();
					frm.refresh_fields();
					frm.refresh();
					//location.reload();
				}
			})
		});

		d.show();
		refresh_field("payments");
		frm.refresh_fields();
		frm.refresh();
	}
});

frappe.ui.form.on('Sales Invoice Item One', {
	item_name: function(frm, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);
		if(!item.item_name) {
			item.item_name = "";
		} else {
			item.item_name = item.item_name;
		}
	},

	barcode: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.barcode) {
			args = {
				'barcode'			: d.barcode
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "get_item_code_sale",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("items");
						cur_frm.refresh_fields();
						calculate_base_imponible(frm);
					}
				}
			});
		}
		cur_frm.refresh_fields();
	},

	item_code: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var base_imponible = 0;
		var total_taxes = 0;
		var total = 0;
		var doc = frm.doc;

		if(d.item_code) {
			args = {
				'item_code'			: d.item_code,
				'qty'				: d.qty
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "get_item_details_sale",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("items");
						cur_frm.refresh_fields();
						calculate_base_imponible(frm)
					}
				}
			});

			frm.refresh_fields();
		}
	},

	qty: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.qty) {
			args = {
				'item_code'			: d.item_code,
				'qty'				: d.qty,
				'unit_price': d.unit_price
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "update_prices_sale",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("items");
						cur_frm.refresh_fields();
						calculate_base_imponible(frm);
					}
				}
			});
		}
	},

	unit_price: function(frm, cdt, cdn){
		// if user changes the rate then set margin Rate or amount to 0
		var d = locals[cdt][cdn];
		if(d.item_code){
			args = {
				'item_code'			: d.item_code,
				'qty'				: d.qty,
				'unit_price': d.unit_price
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "update_prices_sale",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("items");
						cur_frm.refresh_fields();
						calculate_base_imponible(frm);
					}
				}
			});
		}
	}
})

var calculate_base_imponible = function(frm) {
	var doc = frm.doc;
	doc.base_imponible = 0;
	doc.total_taxes = 0;
	doc.total = 0;

	if(doc.items) {
		$.each(doc.items, function(index, data){
			doc.base_imponible += (data.unit_price * data.qty);
			doc.total_taxes += (data.unit_price_with_tax - data.unit_price) * data.qty;
		})
		doc.total += doc.base_imponible + doc.total_taxes;
	}
	refresh_field('base_imponible')
	refresh_field('total_taxes')
	refresh_field('total')
}
