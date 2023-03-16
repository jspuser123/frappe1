# Copyright (c) 2023, jagan and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document

class LibraryMember(Document):
	def before_save(self):
         self.full_name = f'{self.first_name}{" "+self.last_name if self.last_name else ""}'
         
        
    
     