import typer
import time
from rich import print


# Auth app
auth_app = typer.Typer()



@auth_app.command('register')
def register(
    name: str = typer.Option('Enter your name', help='', prompt=True),
    email: str = typer.Option('Enter email address', help='', prompt=True),
    phone: str = typer.Option('Enter phone number', help='', prompt=True),
    company: str = typer.Option('Enter company name', help='', prompt=True),
    distrubuter: bool = typer.Option(False, help='Are you a distrubuter?')
):
    '''
    Register for VisionAI Toolkit

    Register for VisionAI Toolkit. This will create a new account
    for you on the Visionify platform. You can use this account
    to login to the VisionAI Toolkit and manage your devices,
    scenarios, pipelines, and models.

    '''
    print('Registering user')

@auth_app.command('status')
def auth_status():
    '''
    Check login status

    Check the current login system.
    '''
    print('Print whether logged in or not')

@auth_app.command('login')
def login(
    token: str = typer.Option(..., help='Authenticate the app through token')
):
    '''
    Login with an application token.

    Get the auth token from our website
    '''
    print('Logging using the authorization token: {token}')

@auth_app.command('logout')
def logout():
    '''
    Logout from your session

    Get the auth token from our website
    '''
    print(f'Logging out of current session')

@auth_app.callback()
def callback():
    '''
    Authorization (logging in/out)

    Login and get authorization token etc.

    You can login/logout check authorization token with this.
    '''




if __name__ == '__main__':
    auth_app()
