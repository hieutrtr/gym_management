import os, datetime
import mysql.connector
from dotenv import load_dotenv
load_dotenv()


db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': os.getenv('MYSQL_PORT'),
    'database': os.getenv('MYSQL_DB'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASS'),
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
    'auth_plugin': 'mysql_native_password'
}


class DB:
    name = None
    dob = None
    address = None
    email = None
    gender = None
    phone = None
    ordinal_num = None
    package = None
    start_date = None
    end_date = None

    def __init__(self):
        pass

    @staticmethod
    def _connect():
        db = mysql.connector.connect(**db_config)
        conn = db.cursor()
        return db, conn

    def _execute(self, query):
        db, conn = self._connect()
        conn.execute(query)
        db.commit()
        return conn.lastrowid, conn.rowcount

    def _select(self, query):
        db, conn = self._connect()
        conn.execute(query)
        result = conn.fetchone()
        return result

    def print(self):
        print("""
        - Tên: {}
        - Ngày sinh: {}
        - Giới tính: {}
        - Địa chỉ: {}
        - Email: {}
        - Phone: {}
        - Số điện thoại người thân: {}
        - Gói đăng ký: {}
        - Thời hạn: {} to {}
        """.format(self.name, self.dob, self.gender, self.address, self.email, self.phone, self.ordinal_phone,
                   self.package, self.start_date, self.end_date))

    def _collect_client_info(self):
        ok = False
        while ok is False:
            print("Nhập tên:")
            self.name = input()
            print("Nhập ngày sinh (tháng/ngày/năm):")
            self.dob = input()
            print("Nhập địa chỉ:")
            self.address = input()
            print("Nhập email:")
            self.email = input()
            print("Nhập giới tính (M hoặc F):")
            self.gender = input()
            print("Nhập số điện thoại:")
            self.phone = input()
            print("Nhập số điện thoại người thân:")
            self.ordinal_phone = input()
            print("Nhập gói đăng ký:")
            print("""
            mem_30_full,
            mem_30_morning, 
            mem_15_entries, 
            mem_90_full, 
            mem_180_full, 
            mem_annual
            """)
            self.package = input()
            print("Nhập ngày bắt đầu (tháng/ngày/năm):")
            self.start_date = input().split('/')
            service = self._get_package_period()
            self.start_date = datetime.datetime(int(self.start_date[2]), int(self.start_date[0]), int(self.start_date[1]))
            self.end_date = self.start_date + datetime.timedelta(days=int(service[1]))
            print("Vui lòng kiểm tra kĩ thông tin đăng ký: (yes/no)")
            self.print()
            ok = True if input() == 'yes' else False

    def _insert_client(self):
        dob = self.dob.split('/')
        self.dob = datetime.datetime(int(dob[2]), int(dob[0]), int(dob[1]))
        query = 'INSERT INTO clients(name, DOB, address, email, gender, phone, ordinal_phone) \
        VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(self.name, self.dob,
                                                                                self.address, self.email,
                                                                                self.gender, self.phone,
                                                                                self.ordinal_phone)
        return self._execute(query)

    def _get_package_period(self):
        query = "SELECT id, period FROM services WHERE service_code = '{}';".format(self.package)
        service = self._select(query)
        return service

    def _insert_client_packages(self, client_id):
        service = self._get_package_period()
        query = 'INSERT INTO client_services(client_id, service_id, status, start_date, expiry_date) \
            VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');' \
            .format(client_id, service[0], \
                    'ACTIVATED', self.start_date, self.end_date)
        return self._execute(query)

    def add(self):
        self._collect_client_info()
        client_id, count = self._insert_client()
        client_package_id, count = self._insert_client_packages(client_id)
        if count == 0:
            return False
        return client_id

    def _get_check_in_status(self, client_id):
        query = "SELECT ci.type FROM client_services cs JOIN checkins ci ON cs.id = ci.client_services_id WHERE cs.client_id = {} ORDER BY time DESC LIMIT 1;".format(client_id)
        result = self._select(query)
        return result[0] if result is not None else None

    def _get_current_package(self, client_id):
        query = "SELECT s.service_code, s.price, s.description, cs.id AS client_services_id, cs.start_date, cs.expiry_date, c.name, c.phone, c.ordinal_phone " \
                "FROM services s JOIN client_services cs ON s.id = cs.service_id JOIN clients c ON c.id = cs.client_id " \
                "WHERE c.id = {} AND cs.status = 'ACTIVATED' AND cs.expiry_date > NOW() ORDER BY cs.start_date ASC LIMIT 1".format(client_id)
        result = self._select(query)
        if result is not None:
            return {
                'service_code' : result[0],
                'price': result[1],
                'description': result[2],
                'client_services_id': result[3],
                'start_date': result[4],
                'expiry_date': result[5],
                'name': result[6],
                'phone': result[7],
                'ordinal_phone': result[8]
            }
        else:
            return None

    def _get_latest_package(self, client_id):
        query = "SELECT s.service_code, s.price, s.description, cs.id AS client_services_id, cs.start_date, cs.expiry_date, c.name, c.phone, c.ordinal_phone " \
                "FROM services s JOIN client_services cs ON s.id = cs.service_id JOIN clients c ON c.id = cs.client_id " \
                "WHERE c.id = {} ORDER BY cs.expiry_date DESC LIMIT 1".format(client_id)
        result = self._select(query)
        if result is not None:
            return {
                'service_code' : result[0],
                'price': result[1],
                'description': result[2],
                'client_services_id': result[3],
                'start_date': result[4],
                'expiry_date': result[5],
                'name': result[6],
                'phone': result[7],
                'ordinal_phone': result[8]
            }
        else:
            return None

    def _record_checkout(self, client_service_id):
        query = 'INSERT INTO checkins(client_services_id, type) \
            VALUES({}, \'{}\');' \
            .format(client_service_id, 'CHECKOUT')
        return self._execute(query)


    def _record_checkin(self, client_service_id):
        query = 'INSERT INTO checkins(client_services_id, type) \
            VALUES({}, \'{}\');' \
            .format(client_service_id, 'CHECKIN')
        return self._execute(query)

    def _gather_checkin_info(self, package, status):
        status = "CÒN HẠN" if status == 'AVAILABLE' else "HẾT HẠN"
        return """
        - Tên: {}
        - Phone: {}
        - Số điện thoại người thân: {}
        - Gói đăng ký: {} ({})
        - Giá gói đăng ký: {}
        - Thời hạn: {} to {}
        - Tình trạng: {}
        """.format(package.get('name'), package.get('phone'), package.get('ordinal_phone'), package.get('description'),
                   package.get('service_code'), package.get('price'), package.get('start_date'),
                   package.get('expiry_date'), status)


    def check_in_out(self, client_id):
        check_in_status = self._get_check_in_status(client_id)
        package = self._get_current_package(client_id)
        status = 'AVAILABLE'
        if package is None:
            package = self._get_latest_package(client_id)
            status = 'EXPIRED'
        else:
            if check_in_status == 'CHECKIN':
                self._record_checkout(package.get('client_services_id'))
            else:
                self._record_checkin(package.get('client_services_id'))
        return self._gather_checkin_info(package, status)
