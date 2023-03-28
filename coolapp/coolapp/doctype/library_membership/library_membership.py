# Copyright (c) 2023, jagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe import utils

class LibraryMembership(Document):
    def before_submit(self):
        if self.membership_type == 'Individual':
            exists = frappe.db.exists("Library Membership",
             {
                  "library_member": self.library_member,
                  "docstatus": DocStatus.submitted(),
                  "to_date": (">", self.from_date),
                  "paid": ("=", 1),
                  },
                  )
            if exists:
                frappe.throw("This member already exists")
                
        elif self.membership_type == 'group':
            exists = frappe.db.exists ("Library Membership",
             {
                     "library_member": self.library_member,
                     "docstatus": DocStatus.submitted(),
                     "parent_library_membership":self.parent_library_membership,
                     "membership_type":"group"
                     },
                     )
            if exists:
                frappe.throw("This group member already exists")
                           
        elif self.membership_type == 'company':
        
            exists = frappe.db.exists("Library Membership",
                    {
                        "library_member": self.library_member,
                        "docstatus": DocStatus.submitted(),
                        "to_date": (">", self.from_date),
                        "paid": ("=", 1),
                        "is_group": ("=", 1)
                    },
                )
            if exists:
                frappe.throw("This company already exists")
        else:
            frappe.throw("There is an active membership for this member")
                
        
            