# Copyright (c) 2023, jagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


#import pdb; pdb.set_trace()
class LibraryTransaction(Document):

    def before_submit(self):
        
        article = frappe.get_doc("Article",self.article)

        if self.type == 'Issued':
            self.validate_issue()
            self.validate_maximum_limit()
         
            if  int(article.owned_book) >= 1:
               
                article.issued_count = (int(article.issued_count)+1)
                article.save()
            else:
                frappe.throw("no books available")
                
 

        elif self.type == "Return":
            self.validate_return()
            article.status = "Available"
            if  int(article.issued_count) >= 1:
                
                article.issued_count = (int(article.issued_count)-1)
                article.save()
            else:
                frappe.throw("no books Issued")


        elif self.type == 'Buy':
            
            article.owned_book= (int(article.owned_book)+self.qty)
            article.save()

        elif self.type == 'Sell':
            
            total=int(article.owned_book)-int(article.issued_count)

            if  self.qty >= 1:
               
                if int(total) >= self.qty:
                    
                    article.owned_book = (int(article.owned_book) - self.qty)
                    article.save()
                
                else:

                    frappe.throw("total book is" + str(total))
            else:
                frappe.throw("value is less than")

         
         
         

    def validate_issue(self):
        #self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member},
        )
     
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles js")


     
    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
