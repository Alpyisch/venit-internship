from urllib import request
import json
import sys

def ipfind(ip_address):
    url = f"https://api.country.is/{ip_address}/"
    try:
        response = request.urlopen(url)
        if response.getcode() == 200:                   #200 değeri sunucu isteği alınımış demek#
            data = response.read()
            json_data = json.loads(data)
            if 'country' in json_data:
               print("IP adresi ülke kodu:",json_data['country']) 
        else:
            print('Hatali bir IP adresi girdiniz!: ', response.getcode())
    except Exception as e:
        print(f"Hatali bir IP adresi girdiniz! ",e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanim: python script.py <ip_address>")
        sys.exit(1)

    ip_address = sys.argv[1]
    ipfind(ip_address)
