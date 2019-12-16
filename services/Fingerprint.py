import os, datetime
# from r305 import R305


device = os.getenv('FG_DEVICE', 'COM4')
baudrate = os.getenv('FG_BAUDRATE', '57600')  # the default baudrate for this module is 57600

class Fingerprint:

    def _callback(data):
        x = input(data)

    def add_with_id(self, client_id):
        return True
        # fg_device = R305(device, baudrate)
        # fg_result = fg_device.StoreFingerPrint(IgnoreChecksum=True, callback=self._callback, templateNum=client_id)
        #
        # if type(fg_result) != str:
        #     return True
        # return False

    def check_in_out(self):
        # fg_device = R305(device, baudrate)
        # result = fg_device.SearchFingerPrint(IgnoreChecksum=True)
        # print('scan_fingerprint: {}'.format(result))
        # if (type(result) != str):
        #     pageid = result.get('pageid')
        #     matchstore = result.get('matchstore')
        #     return int(pageid*100 + matchstore)
        # return False
        return 2

