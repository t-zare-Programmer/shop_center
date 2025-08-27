def create_random_code(count):
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)

#_________________________________________________________
from kavenegar import *

def send_sms(mobile_number, message):
    pass
    # try:
    #     api = KavenegarAPI('62654E637679314B566137653850334E386E2B4170554235494B4D654256325977634274594567456535343D')
    #     params = {'sender': '2000660110','receptor': mobile_number,'message': message,}
    #     response = api.sms_send(params)
    #     return response
    # except APIException as error:
    #     print(f'error1: {error}')
    # except HTTPException as error:
    #     print(f'error2: {error}')

#_________________________________________________________
import os
from uuid import uuid4

class FileUpload:
    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix

    def upload_to(self,instance, filename):
        filename,ext = os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'