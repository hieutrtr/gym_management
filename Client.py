import mysql.connector
import datetime

db_config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'therockgym',
        'user': 'root',
        'password': '1547896sS',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
        'auth_plugin': 'mysql_native_password'
    }

class Client():
    name = None
    dob = None
    address = None
    email = None
    gender = None
    phone = None 
    ordinal_num = None

    def __init__(self):
        pass

    def count(self):
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MAX(id) FROM clients;")
        myresult = mycursor.fetchone()
        print(myresult[0])
        return myresult[0]

    def add_name(self):
        print("Nhap ten:")
        self.name = raw_input()
    def add_dob(self):
        print("Nhap ngay sinh (Thang/Ngay/Nam):")
        self.dob = raw_input()
    def add_address(self):
        print("Nhap dia chi:")
        self.address = raw_input()
    def add_email(self):
        print("Nhap email:")
        self.email = raw_input()
    def add_gender(self):
        print("Nhap gioi tinh (M hoac F):")
        self.gender = raw_input()
    def add_phone(self):
        print("Nhap so dien thoai:")
        self.phone = raw_input()
    def add_ordinal_num(self):
        print("Nhap so dien thoai nguoi than:")
        self.ordinal_num = raw_input()
    def add_package(self, client_id):
        package_codes = """
        mem_30_full,
        mem_30_morning, 
        mem_15_entries, 
        mem_90_full, 
        mem_180_full, 
        mem_annual
        """

        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        is_correct = False
        while(is_correct is False):
            print("Nhap package_code: {}".format(package_codes))
            service_code = raw_input()
            mycursor.execute("SELECT id, period FROM services WHERE service_code = '{}';".format(service_code))
            service = mycursor.fetchone()
            
            print("Nhap ngay bat dau (Thang/Ngay/Nam):")
            start_date = raw_input().split('/')
            start_date = datetime.datetime(int(start_date[2]), int(start_date[0]), int(start_date[1]))
            expiry_date = start_date + datetime.timedelta(days=int(service[1]))
            
            print("Vui Long Kiem Tra Ky Thong Tin:")
            print("""
            - Goi tap: {}
            - Co thoi han trong vong: {}
            - Ngay bat dau: {}
            - Ngay ket thuc: {}
            """.format(service_code, service[1], start_date, expiry_date))
            print("Da chinh xac chua ? (yes/no)")
            is_correct = raw_input()
            is_correct = True if is_correct == 'yes' else False
            
        mycursor.execute('INSERT INTO client_services(client_id, service_id, status, start_date, expiry_date) \
            VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'\
            .format(client_id, service[0], \
                'ACTIVATED', start_date, expiry_date))

        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return mycursor.rowcount
        

    def store_client(self):
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        dob = self.dob.split('/')
        self.dob = datetime.datetime(int(dob[2]), int(dob[0]), int(dob[1]))
        mycursor.execute('INSERT INTO clients(name, DOB, address, email, gender, phone, ordinal_num) \
            VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'\
            .format(self.name, self.dob, \
                self.address, self.email, self.gender, self.phone, self.ordinal_num))
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return mycursor.rowcount

    def get_info(self):
        return """
        - Ten: {}
        - Ngay sinh: {}
        - Gioi tinh: {}
        - Dia chi: {}
        - Email: {}
        - Phone: {}
        - So dien thoai nguoi than: {}
        """.format(self.name, self.dob, self.gender, self.address, self.email, self.phone, self.ordinal_num)

    def checkin_membership(self, client_id):
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        print(client_id)
        mycursor.execute("SELECT cs.id as cs_id, cs.service_id, cs.start_date, cs.expiry_date, s.service_code, s.description, s.price, s.version, ci.time, ci.type \
            FROM clients c JOIN client_services cs ON c.id = cs.client_id JOIN services s ON s.id = cs.service_id \
            LEFT JOIN checkins ci ON cs.id = ci.client_services_id WHERE c.id = {} AND cs.status = 'ACTIVATED' AND cs.expiry_date > NOW() ORDER BY cs.start_date ASC;".format(client_id))
        checkin_record = mycursor.fetchone()
        print(checkin_record)
        if(checkin_record is None):
            return None
        cs_id, service_id, start_date, expiry_date, service_code, description, price, version, time, type = checkin_record
        next_type = 'CHECKOUT' if type == 'CHECKIN' else 'CHECKIN'
        mycursor.execute('INSERT INTO checkins(client_services_id, type) \
            VALUES({}, \'{}\');'\
            .format(cs_id, next_type))
        mydb.commit()

        return {
            'service': service_code,
            'description': description,
            'start_date': start_date,
            'expiry_date': expiry_date,
            'version': version
        }
