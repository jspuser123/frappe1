// Copyright (c) 2023, jagan and contributors
// For license information, please see license.txt
frappe.ui.form.on('Library Membership', {
	refresh: function(frm) {
			cur_frm.fields_dict['parent_library_membership'].get_query = function(doc) 
			{
				return {filters: {	"membership_type":'company'}}
			}
			frm.doc.paid=true	
			frm.doc.is_group=true			
		},
	library_member: function(frm){
			if (frm.doc.library_member)
			{
				let lis =frappe.db.get_list('Library Membership', 
				{
					filters: 
					{
					"membership_type":['in',['group','company']],
					"library_member":frm.doc.library_member,
					}
				}).then(lis =>

				{
				
				if(lis.length == 0)
					{
					console.log("value is emty")
					}
				else
					{
					let c = frappe.db.get_doc("Library Membership",lis[0].name).then(rowdata =>
						{
						if (rowdata.membership_type == "group")
							{
								var x =lis[0].parent_library_membership
								frappe.msgprint("A member of this group ",x)
							}
						else if (rowdata.membership_type == "company")
							{
								var y = lis[0].library_member
								frappe.msgprint("A member of this company",y)
							}
						else
							{
								console.log("else if ",rowdata)
							}
					
						});

					}
				});
		    }	
		},

	from_date: function(frm ){frm.set_value("from_date", frappe.datetime.add_days(frappe.datetime.nowdate()))},

});
