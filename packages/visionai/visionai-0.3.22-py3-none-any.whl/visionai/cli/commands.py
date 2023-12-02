import typer
from rich import print
import docker
from rich.console import Console
from cryptography.fernet import Fernet



import sys
from pathlib import Path
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # visionai/visionai directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH



from config import *
from util.docker_utils import *
from models.triton_client import TritonClient

from visionai.util.license_server_services import LicenseServerCommunication
license_server_com =  LicenseServerCommunication()

from visionai.util.cmd_utils import save_registration_data, is_registered
from visionai.util.cmd_utils import  print_container_status,check_env_file_exists,check_config_folder

err_console = Console(stderr=True)
tc = TritonClient()

def stop_cmd():
    try:
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(f'Stop web-app....')
        client = docker.from_env()
        web_service_container = client.containers.get(VISIONAI_API_CONTAINER_NAME)
        web_service_container.stop()
    except docker.errors.NotFound :
        message = typer.style(f"Web-app not running", fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(message)



def status_cmd(
    tail: int = typer.Option(20, help='tail number of lines')
    ):
    print_container_status(WEB_APP_CONTAINER_NAME, tail)
    print_container_status(VISIONAI_API_CONTAINER_NAME, tail)
    print_container_status(REDIS_CONTAINER_NAME, tail)
    print_container_status(TRITON_SERVER_CONTAINER_NAME, tail)


def restart_cmd():
    '''
    Restart all services
    with env file
    '''
    pass


def register_company_cmd(
        fname,
        lname,
        email,
        phone,
        company,
        company_address = 'not updated',
        company_website = 'not updated',
        distrubuter=False):
    '''
    Register for VisionAI Toolkit
    :Todo push this details to visionify license server
    '''
    status = is_registered()
    if status["status"] == "registered":
        print(f"Device already registered and You have {status['days_left']} days left to renew your license")
        return
    
    if license_server_com.login():
        if license_server_com.create_customer(fname,lname,email,phone,company,company_address,company_website,distrubuter):
            save_registration_data(company)
            print("Registeration successful you can use visionai toolkit for 30 days as part of trial")
        else:
            print("Registeration failed Please contact support at support@visionify.ai")

    else:
        print("Registeration failed Please contact support at support@visionify.ai")




def update_visionai_images_cmd(service):
    from util.docker_utils import pull_latest_image
    if service == "visionai-web":
        pull_latest_image("visionify/visionai-dashboard")
    elif service == "visionai-inference":
        pull_latest_image("visionify/visionai-api")
    elif service == "visionai-email":
        pull_latest_image("visionify/visionai-email")
    else:
        print("Invalid service name")
        return False
    
    return True


def init_cmd():
    '''
    Start all services using init command
    get env file path from root path "~/.visionai" folder 
    '''

    try:
        # check visionai folder if not exists
        if not check_config_folder():
            print("[bold red] Visionai config folder not found please create [bold yellow].visionai[/bold yellow] folder in home directory and paste [bold yellow].env[/bold yellow] file before do visionai init[/bold red]")
            return False
    
        if not check_env_file_exists():
            print("[bold red] .env file not found in ~/.visionai folder please create .env file before do visionai init[/bold red]")
            return False
            
        status = is_registered()

        if status["status"] == "not_registered":
            print("[bold yellow]Please register your device before use with using [bold green]`visionai register`[/bold green] command[/bold yellow]")
            return False
        elif status["status"] == "expired":
            print("[bold red]Your license has expired please contact support@visionify.ai to renew your license[/bold red]")
            return False
        elif status["status"] == "registered":
            print(f'[bold green]Your license is valid You have [bold yellow]{status["days_left"]}[/bold yellow] days left renew your license[/bold green]')

        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')

        # Package dependencies:
        # opencv-python = "^4.6.0"
        # torch = "^1.11.0"
        # torchvision = ">=0.12,<0.15"
        # pandas = "^1.3.5"
        # seaborn = ">=0.11.2,<0.13.0"
        # tritonclient = {extras = ["all"], version = "^2.29.0"}
        check_requirements(['opencv-python', 'torch', 'torchvision', 'pandas', 'seaborn', 'tritonclient[all]'], install=True)

        # Check if already running
        web_app_running = False
        web_api_running = False
        redis_running = False
        triton_running = False

        client = docker.from_env()
        containers = client.containers.list()
        for container in containers:
            if container.name == VISIONAI_API_CONTAINER_NAME:
                web_api_running = True
            if container.name == WEB_APP_CONTAINER_NAME:
                web_app_running = True
            if container.name == REDIS_CONTAINER_NAME:
                redis_running = True
            if container.name == TRITON_SERVER_CONTAINER_NAME:
                triton_running = True
        # If all services are running, return
        if web_app_running and web_api_running and redis_running and triton_running:
            return

        if web_api_running is False:
            print(f'Starting web service API at port {VISIONAI_API_PORT}')
            if sys.platform == 'win32':
                DOCKER_SOCK = '//var/run/docker.sock'
            elif sys.platform == 'darwin':
                DOCKER_SOCK = '/var/run/docker.sock'
            else:
                DOCKER_SOCK = '/var/run/docker.sock'
                print(VISIONAI_FOLDER)
                visionai_env = {
                    'HOST_PATH': VISIONAI_FOLDER
                    }
            
            docker_container_start(
                container_name=VISIONAI_API_CONTAINER_NAME,
                image=VISIONAI_API_DOCKER_IMAGE,
                portmap={3002:VISIONAI_API_PORT},
                network_name=DOCKER_NETWORK,
                volmap=[
                    f'{DOCKER_SOCK}:/var/run/docker.sock',
                    f'{ENV_FILE_PATH}:/App/.env',
                    f'{VISIONAI_FOLDER}:/App/.visionai'
                ],
                envmap=visionai_env
                # command=f"-e HOST_PATH={VISIONAI_FOLDER}"
            )
            print(f'Web service API available at: http://localhost:{VISIONAI_API_PORT}') 



    except Exception as e:
        err_console.print_exception()
        print(f'Error: {e}')



if __name__ == '__main__':
    # init_cmd()
    # stop_cmd()
    status_cmd()
