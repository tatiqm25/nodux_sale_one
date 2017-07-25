// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Sales Invoice One'] = {
	add_fields: ["posting_date", "status"],
	get_indicator: function(doc) {
		if((doc.status)=="Draft") {
			return [__("Draft"), "orange", "status,=,Draft"];
		} else if((doc.status)=="Done") {
			return [__("Done"), "green", "status,=,Done"]
		} else if((doc.status)=="Confirmed"){
			return[__("Confirmed"), "yellow", "status,=,Confirmed"]
		} else if ((doc.status)=="Anulled") {
			return[__("Anulled"), "red", "status,=,Anulled"]
		}
	},
	right_column: "posting_date"
};
