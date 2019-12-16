from r305 import R305
import sys, time
from Client import Client

device = sys.argv[1]
baudrate = sys.argv[2]  # the default baudrate for this module is 57600

dev = R305(device, baudrate)

def callback(data):
    x = input(data)


def register(client):
    is_correct = False
    while(is_correct is False):
        client.add_name()
        client.add_dob()
        client.add_address()
        client.add_email()
        client.add_gender()
        client.add_phone()
        client.add_ordinal_num()
        print("Vui Long Kiem Tra Ky Thong Tin:")
        print(client.get_info())
        print("Da chinh xac chua ? (yes/no)")
        is_correct = input()
        is_correct = True if is_correct == 'yes' else False

    return client.store_client()


if __name__ == '__main__':
    try:
        # dev.DeleteAll()
        client = Client()
        client_count = client.count()
        next_client_id = client_count + 1 if (client_count != None) else 0
        print('client id is: {}'.format(next_client_id))
        fg_result = dev.StoreFingerPrint(IgnoreChecksum=True, callback=callback, templateNum=next_client_id)
        print(fg_result)
        if(type(fg_result) != str):
            result = register(client)
            print(result)
            result = client.add_package(next_client_id)
            print(result)
    except Exception as ex:
        print(ex)
