import re
import json
from urllib.request import urlopen
class GeoLocalisation:
    def __init__(self, ip_address: str):
        super().__init__()
        self.ip_address = ip_address
    def locate(self):
        try :
            url = 'http://ip-api.com/json/'+ self.ip_address
            response = urlopen(url)
            data = json.load(response)
            try :  
                pays=data['country']
                return pays
            except :
                return "local"
        except :
            return "No internet acces"