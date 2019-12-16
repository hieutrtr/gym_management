import os, time
from services.Fingerprint import Fingerprint
from services.DB import DB


next_client_id = 0


def register():
    client = DB()
    client_id = client.add()
    if client_id is False:
        print("Thêm thông tin khách hàng không hoàn thành!!")
        return None
    print("Đặt ngón tay bất kỳ để lấy dấu vân tay:")
    fg = Fingerprint()
    ok = fg.add_with_id(client_id)
    if ok:
        print("Chúc mừng quý khách đã đăng ký thành công !!!")
        client.print()


def checkin_out():
    print("Đặt ngón tay đã đăng ký để quét dấu vân tay:")
    fg = Fingerprint()
    client_id = fg.check_in_out()
    if client_id is False:
        print("Vui lòng thử lại!!!")
        return None
    client = DB()
    info = client.check_in_out(client_id)
    print("Thông tin của quý khách: \n{}".format(info))


def extend_new_package():
    print("Đặt ngón tay đã đăng ký để quét dấu vân tay:")


def buy_goods():
    print("Đặt ngón tay đã đăng ký để quét dấu vân tay:")


if __name__ == '__main__':
    message = """
    1. Đăng Ký
    2. Checkin/Checkout
    3. Gia hạn gói mới
    4. Mua hàng
    Vui lòng chọn theo số như trên : 
    """
    print(message)
    operation = int(input())
    {
        1: register,
        2: checkin_out,
        3: extend_new_package,
        4: buy_goods
    }[operation]()
