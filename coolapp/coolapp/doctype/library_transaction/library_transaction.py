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
                frappe.throw("books is not available")
                
 

        elif self.type == "Return":
            self.validate_return()
            article.status = "Available"
            if  int(article.issued_count) >= 1:
                
                article.issued_count = (int(article.issued_count)-1)
                article.save()
            else:
                frappe.throw("No books Issued")


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

                    frappe.throw("Total Books is = " + str(total))
            else:
                frappe.throw("Your Value  is Less Than Books value")

         
         
         

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already Issued by Another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count("Library Transaction",{"library_member": self.library_member,
                                                       "type": "Issued", 
                                                       "docstatus": DocStatus.submitted()
                                                       
                                                       
                                                       },)
     
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")


     
    def validate_membership(self):
        # check if a valid membership exist for this library member
     
   
        data=frappe.db.get_list('Library Membership', filters={"library_member":self.library_member,"membership_type":['in',['Individual','group','company']],},fields=['membership_type'])
        for y in data:
            print(y)

        for data1 in y.values():
            print(data1)

        if data1 == 'Individual':

            valid_membership = frappe.db.exists(
                "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": DocStatus.submitted(),
                    "from_date": ("<=", self.date),
                    "to_date": (">=", self.date),
                    "paid": ("=", 1)
                },
            )
            
            if not valid_membership:
                frappe.throw("The member does not have a valid membership Individual ")
        elif data1 == 'group':
            
             valid_membership = frappe.db.exists(
                "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": DocStatus.submitted(),
                   
                    
        
                },
            )
             if not valid_membership:
                frappe.throw("The member does not have a valid membership group")

        elif data1 == 'company':
             
             valid_membership = frappe.db.exists(
                 "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": DocStatus.submitted(),
                    "from_date": ("<=", self.date),
                    "to_date": (">=", self.date),
                    "paid": ("=", 1),
                    "is_group": ("=", 1)

                },
            )
             if not valid_membership:
                frappe.throw("The member does not have a valid membership company")
        else:
            frappe.throw("The member does not have a valid membership")


