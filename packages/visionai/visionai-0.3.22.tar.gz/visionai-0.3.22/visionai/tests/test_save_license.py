from cryptography.fernet import Fernet
import uuid
import os
from datetime import datetime,timedelta


SECRET_FILE_PATH = os.path.expanduser("~/.visionai/.secret.lic")
KEY = b"MHHD3HQDKlkN8Z69mQeNbzzsvEAtRdLKImH1Z1NmjE0="  # Should be 32 url-safe base64-encoded bytes
cipher_suite = Fernet(KEY)

def save_registration_data(company:str,
                           license_type:str="trial",
                           license_end_date:str=None,
                           sites:int=1,
                           is_trial:bool=True,
                           action_type:str="create"):
    '''
    save registration data to secret.txt file
    and push to visionify license server
    '''
    current_mac = get_mac_address()
    if not license_end_date:
        today = datetime.now()
        trail_data = today + timedelta(days=300)
        license_end_date = trail_data.strftime('%Y-%m-%d')
    license_key = f'{company}_{current_mac}_{str(license_end_date)}_{license_type}_{sites}'
    registration_data = (license_key).encode()
    encrypted_data = cipher_suite.encrypt(registration_data)
    print(encrypted_data.decode())
    # print(SECRET_FILE_PATH)
    # with open(SECRET_FILE_PATH, 'w') as f:
    #     f.write(encrypted_data.decode())




def get_mac_address() -> str:
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                    for elements in range(0,2*6,2)][::-1])
    return mac

save_registration_data("test")
