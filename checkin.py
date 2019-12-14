from r305 import R305
import sys, time
from Client import Client

device   = sys.argv[1]
baudrate = sys.argv[2] # the default baudrate for this module is 57600

dev = R305(device, baudrate)

def callback(data):
    x = raw_input(data)

def scan_fingerprint():
    time.sleep(0.5)
    result = dev.SearchFingerPrint(IgnoreChecksum=True)
    print('scan_fingerprint: {}'.format(result))
    if (type(result) != str):
        pageid = result.get('pageid')
        matchstore = result.get('matchstore')
        return int(pageid*100 + matchstore)
    return None
    
def check_in(client_id):
    client = Client()
    info = client.checkin_membership(client_id)
    return info

def notice(check_in_info):
    if check_in_info is None:
        print("Goi tap cua ban da het han. Vui long dang ky goi moi")
    else:
        print("""
        - Dich vu: {}
        - Noi dung: {}
        - Ngay bat dau: {}
        - Ngay ket thuc: {}
        - version: {}
        """.format(check_in_info.get('service'), check_in_info.get('description'), check_in_info.get('start_date'),
        check_in_info.get('expiry_date'), check_in_info.get('version')))

while(True):
    operate = raw_input()
    if operate == 'yes':
        client_id = scan_fingerprint()
        if (client_id is None or type(client_id) is str):
            print('Quet van tay khong thanh cong !!')
            continue
        else:
            check_in_info = check_in(client_id)
            notice(check_in_info)