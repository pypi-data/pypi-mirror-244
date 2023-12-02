import sys
from pathlib import Path
import os
import docker
import typer
import json
import re
import validators

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # visionai/visionai directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


from visionai.util.license_server_services import LicenseServerCommunication

license_server_com =  LicenseServerCommunication()


import uuid
from datetime import datetime,timedelta
from config import SECRET_FILE_PATH,cipher_suite,VISIONAI_FOLDER,ENV_FILE_PATH




def check_config_folder():
    '''
    create config folder if not exists
    '''

    return os.path.exists(VISIONAI_FOLDER)


def check_env_file_exists():
    '''
    check if env file exists
    '''
    if not os.path.exists(ENV_FILE_PATH):
        return False
    return True



def get_mac_address() -> str:
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                    for elements in range(0,2*6,2)][::-1])
    return mac


def save_registration_data(company:str,
                           license_type:str="trial",
                           license_end_date:str=None,
                           sites:int=1,
                           is_trial:bool=True,
                           action_type:str="create",
                           site_name:str="trial"):
    '''
    save registration data to secret.txt file
    and push to visionify license server
    '''
    current_mac = get_mac_address()
    if not license_end_date:
        today = datetime.now()
        trail_data = today + timedelta(days=30)
        license_end_date = trail_data.strftime('%Y-%m-%d')
    license_key = f'{company}_{current_mac}_{str(license_end_date)}_{license_type}_{sites}'
    registration_data = (license_key).encode()
    encrypted_data = cipher_suite.encrypt(registration_data)
    
    with open(SECRET_FILE_PATH, 'w') as f:
        f.write(encrypted_data.decode())

    # push to visionify license server
    license_data = {
        "license":f'{company}_{license_type}',
        "trial":is_trial,
        "customer":company,
        # "site":site_name, TODO add site name
        "scenarios":"PPE detection",
        "cameras":5,
        "mac_address":current_mac,
        "license_key":encrypted_data.decode(),
        "valid_till":license_end_date,
        "created_from":'Cli',
    }
    if action_type == "create":
        license_server_com.create_license(license_data)



def is_registered() -> bool:
    status = {
        "status":"registered",
        "days_left":0
    }
    if not os.path.exists(SECRET_FILE_PATH):
        status["status"] = "not_registered"
        return status
    
    with open(SECRET_FILE_PATH, 'r') as f:
        encrypted_data = f.read().encode()

    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    created_date = datetime.strptime(decrypted_data.split("_")[2],"%Y-%m-%d")    
    current_date = datetime.now()

    days_difference = (created_date - current_date).days
    if days_difference < 0:
        status["status"] = "expired"
        return status
        
    status["days_left"] = days_difference
    return status





def print_container_status(container_name, tail):
    try:
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(f'{container_name} status....')
        client = docker.from_env()
        ctainer = client.containers.get(container_name)
        ctainer_status = typer.style(ctainer.status, fg=typer.colors.WHITE, bg=typer.colors.GREEN)
        typer.echo(f"{container_name}: {ctainer_status}")
        logs = ctainer.logs(tail=tail)
        log_message= logs.decode("utf-8")
        print(log_message)
        web_service_port_message = typer.style(json.dumps(ctainer.ports), fg=typer.colors.WHITE, bg=typer.colors.GREEN)
        typer.echo(web_service_port_message)
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')

    except docker.errors.NotFound:
        message = typer.style(f"{container_name} not running", fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(message)


def valid_email(email: str) -> str:
    if not validators.email(email):
        raise typer.BadParameter("Invalid email format")
    return email

def valid_phone(phone: str) -> str:
    # Assuming a general international phone format.
    # You can adjust the regex based on your specific requirements.
    if not re.match(r"^\+?[\d\- ]+$", phone):
        raise typer.BadParameter("Invalid phone number format")
    return phone

def valid_name(name: str) -> str:
    if not name or len(name) < 3:
        raise typer.BadParameter("Invalid name")
    return name