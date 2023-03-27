// Copyright (c) 2023, jagan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Membership', {

	refresh: function(frm) 
	{
		

		cur_frm.fields_dict['parent_library_membership'].get_query = function(doc) 
		{
			return {
			filters: 	{
			


				"membership_type":'company'
				
						}
					}
		}
	 						
	},

	library_member: function(frm)
	{
		
		// let list1 = frappe.db.get_list("Library Membership").then();
		//let in1 = frappe.db.get_doc("Library Membership","LMS00014" ).then(in1 => {console.log("input=======>",in1.full_name)})

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
							
							
							frappe.msgprint("A member of this group ",lis[0].parent_library_membership)
						}
					else if (rowdata.membership_type == "company")
						{
						
							frappe.msgprint("A member of this company",lis[0].library_member)

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

	from_date: function(frm )
	{

		//frappe.utils.get_datetime(frm.doc.from_date).strftime('%Y-%m-%d')
		//datetime.strfdate('%d/%m/%Y')

		//doc.get_formatted('frm.doc.from_date', 'en-us')

		//frappe.format('2019-09-08', { fieldtype: 'from_date' })


		//frm.doc.from_date=datetime.now().strftime('%Y-%m-%d')

		//frm.doc.from_date=frappe.datetime.get_day_diff(begin, end);

		frm.set_value("from_date", frappe.datetime.add_days(frappe.datetime.nowdate()));

	}

	
});
