// Copyright (c) 2023, jagan and contributors
// For license information, please see license.txt
frappe.ui.form.on('Library Membership', {
	refresh: function(frm) {
		cur_frm.fields_dict['parent_library_membership'].get_query = function(doc) 
		{
			return {filters: {	"membership_type":'company',
								"to_date":['>=',frappe.datetime.nowdate()]}
							}
						}
		},
	library_member: function(frm){
		if (frm.doc.library_member)
			{				
				frappe.db.get_list('Library Membership', 
				{
					filters: 
					{
					"membership_type":['in',['company','Individual']],
					"library_member":frm.doc.library_member,
					"to_date":['>=',frappe.datetime.nowdate()]
					}
			}).then(membership_list => {
		if(membership_list.length > 0)
				{
					frappe.db.get_doc("Library Membership",membership_list[0].name).then(row_data =>
					{						
					if (row_data.membership_type == "company")
						frappe.msgprint("Already active membership this member in company")
					
					else if (row_data.membership_type == "Individual")
						frappe.msgprint("already active membership this member in Individual")										
					});
				}
			});
				frappe.db.get_list('Library Membership', {
					filters: {
					"membership_type":'group',
					"library_member":frm.doc.library_member,
						
					},fields:["parent_library_membership"]}).then(membership_list1 => {
				
		if(membership_list1.length > 0)
				{	
				frappe.db.get_doc("Library Membership",membership_list1[0].parent_library_membership).then(row_data1 =>
						{
						if (row_data1.to_date >= frappe.datetime.nowdate())
							frappe.msgprint("already active membership this member in group")
						});
				}
			})
		}	
	},
	from_date:function(frm ){
		frm.set_value("from_date", frappe.datetime.add_days(frappe.datetime.nowdate(),)) 
		frm.fields_dict.to_date.datepicker.update({
            minDate: frm.doc.from_date ? new Date(frm.doc.from_date) : null
        });
	}	
});

