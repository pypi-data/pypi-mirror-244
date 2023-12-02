import docker
import requests
import typer

from config import WEB_APP_CONTAINER_NAME


def get_web_app_docker_status():
    '''
    Get web app docker status for communication tasks like listing cameras, creation, etc.
    '''
 
    client = docker.from_env()
    try:
        web_service_container = client.containers.get(WEB_APP_CONTAINER_NAME)
        if web_service_container.status != 'running':
            typer.echo("Visionai Web is not running properly. Please check.")
            raise typer.Exit(code=1)
        

    except docker.errors.NotFound:
        typer.echo("Visionai Web is not running. Please check.")
        raise typer.Exit(code=1)
    
    finally:
        client.close()  # Cleanup Docker client
        return True


def common_option(f):
    return typer.Option(
        "--common-opt",  # this can be any shared option name
        callback=get_web_app_docker_status,
        is_eager=True,  # ensures the callback is executed early
        expose_value=False,  # ensures the value won't be passed to the command function
        help="Common option for validation purposes",
    )(f)
    

    

# def require_registration(func):
#     def wrapper(*args, **kwargs):
#         if not is_registered():  # Assuming is_registered is your checking function
#             typer.echo("You need to register first!")
#             raise typer.Exit(code=1)
#         return func(*args, **kwargs)
#     return wrapper