
import os
import requests



class LicenseServerCommunication:
    def __init__(self):
        # make this env variable :TODO
        self.secret = '002b94a70f6f735'
        self.apikey = "e8ca1299b419a4d"
        self.license_base_uri = 'https://license.visionify.ai'
        self.login_url = f'{self.license_base_uri}/api/method/frappe.auth.get_logged_user'
        self.customers_url = f'{self.license_base_uri}/api/resource/Customers'
        self.license_url = f'{self.license_base_uri}/api/resource/Licenses'
        self.site_url = f'{self.license_base_uri}/api/resource/Sites'

        # auth headers for license server restapi
        self.headers = {
            'Authorization': f'token {self.apikey}:{self.secret}'
        }


    def login(self):
        '''
        login to license server to create registration, create license and validate license

        '''

        user = requests.post(self.login_url,headers=self.headers).json()
        if 'exc_type' not in user:
            return True
        else:
            return False



    def check_customer_exists(self,company):
        '''
        check if customer exists on license server
        '''
        customer = requests.get(f'{self.customers_url}/{company}',
                                headers=self.headers).json()
        
        if 'data' in customer :
            return False
        elif 'exc_type' in customer:
            return False
    


    def create_customer(self,fname,lname,email,phone,company,company_address,company_website,distrubuter):
        '''
        create customer on license server
        '''
        customer = {
            "first_name":fname,
            "last_name":lname,
            "email":email,
            "phone_number":phone,
            "company":company,
            "company_website":company_website,
            "address":company_address,
            'no_of_sites':1,
            "total_licenses":1,
            "distrubuter":distrubuter,
            }

        customer = requests.post(f'{self.customers_url}',
                                headers=self.headers,json=customer).json()
        if 'exc_type' not in customer.keys():
            if 'exception' in customer.keys():
                if 'frappe.exceptions.DuplicateEntryError' in customer['exception'] :
                    print("Customer already exists")
                    return False
            else:
                site_data = {
                    "customer_name":company,
                    "site_name":f'{company}_trial',
                    "trial":True,
                }
                self.create_sites(site_data)
                return True
        else:
            return False
    

    def create_sites(self,site_data):
        '''
        create sites on license server 
        NOTE: one customer have multiple sites
        '''
        site = requests.post(f'{self.site_url}',
                        headers=self.headers,json=site_data).json()
        
        if 'exc_type' not in site.keys():
            if 'exception' in site.keys():
                if 'frappe.exceptions.DuplicateEntryError' in site['exception'] :
                    print("Site already exists")
                    return False
            else:
                return True
        else:
            return False
        


    def create_license(self,license_data):
        '''
        create license on license server 
        NOTE: This function will use only installation time to create trail license
        '''

        # if self.check_license_exists(license_data['license']):
        #     return False
        license = requests.post(f'{self.license_url}',
                        headers=self.headers,json=license_data).json()

        
        if 'exc_type' not in license.keys():
            if 'exception' in license.keys():
                if 'frappe.exceptions.DuplicateEntryError' in license['exception'] :
                    print("License already exists")
                    return False
            else:
                return True
        else:
            return False
        
    def check_license_exists(self,license):
        '''
        check if license exists on license server
        '''
        license = requests.get(f'{self.license_url}/{license}',
                                headers=self.headers).json()
        
        print(license,"check_license_exists")
        
        if 'data' in license :
            return False
        elif 'exc_type' in license:
            return False
            

if __name__ == '__main__':
    # login()
    # create_customer("sumanth","s@visionify",837414113,"visionify",False)
    license_server = LicenseServerCommunication()
    print(license_server.check_customer_exists("visionify"))



