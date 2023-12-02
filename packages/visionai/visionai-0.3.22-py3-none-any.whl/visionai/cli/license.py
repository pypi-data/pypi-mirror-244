import typer
import os
from config import SECRET_FILE_PATH,cipher_suite
from visionai.util.cmd_utils import save_registration_data, is_registered
from datetime import datetime
from rich import print

from visionai.util.license_server_services import LicenseServerCommunication
license_server_com =  LicenseServerCommunication()



# Auth app
license_app = typer.Typer()


@license_app.command('create')
def create_license():
    '''
    Create license key
    '''
    pass

@license_app.command('update')
def update_license(
    license_txt: str = typer.Option(...,prompt='Enter license key', help='License key to update')
    ):
    '''
    update license with new license key
    
    '''
    decrypted_data = cipher_suite.decrypt(license_txt).decode()
    company = decrypted_data.split("_")[0]
    date_string = decrypted_data.split("_")[2]
    license_end_date = datetime.strptime(date_string,"%Y-%m-%d").date()
    license_type = decrypted_data.split("_")[3]
    sites = decrypted_data.split("_")[4]
    if license_type == "trial":
        is_trial = True
    else:
        is_trial = False
    save_registration_data(company=company,
                           license_type=license_type,
                           license_end_date = license_end_date,
                           sites=sites,
                           is_trial=is_trial,
                           action_type="update")
    


@license_app.command('status')
def check_license_cmd():
    '''
    Check license status
    '''
    license_data = is_registered()
    if license_data["status"] == "registered":
        print(f'You have [bold]{license_data["days_left"]}[/bold] days left to renew your license')
    elif license_data["status"] == "expired":
        print(f'Your license has [bold red]expired[/bold red]. Please contact support@visionify.ai to renew your license')
    else:
        print(f'Please register your device before use using [bold yellow]`visionai register`[/bold yellow] command')    
