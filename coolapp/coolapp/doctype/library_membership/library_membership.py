# Copyright (c) 2023, jagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe import utils





class LibraryMembership(Document):


	
	def before_submit(self):

		
		if self.membership_type == 'Individual':
			self.active_member()
			if self.library_member and self.from_date and self.to_date and self.paid:
				print("ok")
			else:
				frappe.throw("Your Text Field Not Fill")
				
				
			
		elif self.membership_type == 'group':
			if self.library_member  and self.parent_library_membership:
				print('ok')
			else:
				frappe.throw("Your Text Field Not Fill")
				
		elif self.membership_type == 'company':
			self.active_member()
			if self.library_member and self.from_date and self.to_date and self.paid and self.is_group:
				print("ok")
			else:
				frappe.throw("Your Text Field Not Fill")
		elif self.membership_type == None:

			frappe.throw("Pls Select Membership Type")
			
		else:
			frappe.throw("Pls Select Membership Type")
	def active_member(self):
	
		exists = frappe.db.exists("Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "to_date": (">", self.from_date),
            },
        )
		if exists:
			("There is an active membership for this member")
