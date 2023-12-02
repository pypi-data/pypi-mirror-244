import os
import sys
from pathlib import Path
import json
import requests
from rich import print

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # visionai/visionai directory
VISIONAI_WEB = FILE.parents[2]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

# License file and key
from cryptography.fernet import Fernet
SECRET_FILE_PATH = os.path.expanduser("~/.visionai/.visionai.lic")
KEY = b"MHHD3HQDKlkN8Z69mQeNbzzsvEAtRdLKImH1Z1NmjE0="  # Should be 32 url-safe base64-encoded bytes
cipher_suite = Fernet(KEY)

VISIONAI_FOLDER = os.path.expanduser("~/.visionai")
ENV_FILE_PATH = os.path.expanduser("~/.visionai/.env")


# Config file
CONFIG_FOLDER = ROOT / 'config'
CONFIG_FILE = ROOT / 'config' / 'config.json'
# CONFIG_FILE = os.getenv('CONFIG_FILE') if os.getenv('CONFIG_FILE') is not None else Path(VISIONAI_WEB / 'visioniai-dashboard/test/camera.ui/database/database.json')


VISIONAI_API_URL = 'http://localhost:3002'



SCENARIOS_URL = "https://docsvisionify.blob.core.windows.net/docs-images/scenarios.json"
# SCENARIOS_URL = "https://raw.githubusercontent.com/visionify/visionai/main/visionai/scenarios/scenarios.json"
SCENARIOS_OVERRIDE = ROOT / 'config' / 'scenarios-override.jsn'

# Triton server endpoints
TRITON_HTTP_URL = 'http://localhost:8000'
TRITON_GRPC_URL = 'grpc://localhost:8001'
TRITON_METRICS_URL = 'http://localhost:8002/metrics'

TRITON_SERVER_CONTAINER_NAME = 'visionai-triton'
TRITON_SERVER_DOCKER_IMAGE = 'nvcr.io/nvidia/tritonserver:22.12-py3'
TRITON_SERVER_EXEC = 'tritonserver'
TRITON_SERVER_COMMAND = 'tritonserver --model-repository=/models'
TRITON_MODELS_REPO = ROOT / 'models-repo'

# visionai-api
VISIONAI_API_CONTAINER_NAME = 'visionai-api'
VISIONAI_API_DOCKER_IMAGE = 'visionify/visionai-api'
VISIONAI_API_PORT = 3002
VISIONAI_API_URL = f'http://localhost:{VISIONAI_API_PORT}'
VISIONAI_API_MODELS_REPO = ROOT / 'models-repo'
VISIONAI_API_CONFIG_FOLDER = ROOT / 'config'


# Redis server configuration
REDIS_ENABLED = True
REDIS_SERVER_DOCKER_IMAGE = 'redis'
REDIS_SERVER_PORT = 6379
REDIS_CONTAINER_NAME = 'visionai-redis'



# Web application (front-end)
WEB_APP_DOCKER_IMAGE = 'visionify/visionai-dashboard'
WEB_APP_PORT = 3001
WEB_APP_CONTAINER_NAME = 'visionai-web'



# Docker network
DOCKER_NETWORK = 'visionai-network'

# Test stuff
if os.environ.get('VISIONAI_EXEC') == 'visionai':
    VISIONAI_EXEC = 'visionai'
else:
    VISIONAI_EXEC = 'python -m visionai'

def check_visionai_api():
    try:
        resp = requests.get(VISIONAI_API_URL)
        resp.raise_for_status()
        print(resp.json())
        print(f'init(): VisionAI API is running at {VISIONAI_API_URL}')
        return True
    except requests.exceptions.ConnectionError:
        print("VisionAI API Failed to establish a connection to the server. Please check if the server is running and reachable.")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"VisionAI API An HTTP error occurred: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"VisionAI API An error occurred while making the request: {e}")
        return False
    except Exception as e:
        print(f"VisionAI API An unexpected error occurred: {e}")
        return False


def service_communication(url:str):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print("VisionAI API Failed to establish a connection to the server. Please check if the server is running and reachable.")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"VisionAI API An HTTP error occurred: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"VisionAI API An error occurred while making the request: {e}")
        return False
    except Exception as e:
        print(f"VisionAI API An unexpected error occurred: {e}")
        return False
    


def init_config():
    '''
    Set up initial configuration (one-time only)
    '''

    if not os.path.isdir(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER, exist_ok=True)
        print(f'init(): Created config folder: {CONFIG_FOLDER}')

    if not os.path.exists(CONFIG_FILE):
        config_data = {
            'version': '0.1',
            'cameras': []
            }
    
