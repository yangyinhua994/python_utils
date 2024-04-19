# 数据库连接信息
import random
from datetime import datetime
from hanziconv import HanziConv
import pymysql
from typing import List, Tuple
from faker import Faker
import requests

host = '192.168.0.232'
database_username = 'yyh'
database_password = '1234qwerQWER'
database_name = 'project'
database_table_name = 'company_role'

interface_url = "http://localhost:8080"
success_code = 200

connection = pymysql.connect(host=host,
                             user=database_username,
                             password=database_password,
                             database=database_name)
cursor = connection.cursor()
# 定义请求头信息
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInN1YiI6IjE4NzE3MDg4NDE0IiwiaWF0IjoxNzExNjA1MDA1LCJl"
                     "eHAiOjg4MTExNjA1MDA1fQ.wrFojucpq4ytvF65ZbDrt-0zc0-MUCTirVm7c_06UIs",
    "Content-Type": "application/json"
}

write_path = "/root/IdeaProjects/spring-cloud-project/project/src/main/java/com/example"
entity_write_path = write_path + "/entity"
dto_write_path = write_path + "/dto"
vo_write_path = write_path + "/vo"

# vo对象去除的字段
entity_remove_fields = []

# entity对象增加的字段,格式为字段名，数据类型，注释，默认值
entity_add_fields = []

# vo对象去除的字段
vo_remove_fields = ["password", "status", "is_set_password", "file_save_relative_path", "file_type_id",
                    "upload_user_id", "create_time", "update_time", "id_card"]

# vo对象增加的字段,格式为字段名，数据类型，注释，默认值
# user表字段,难得改了,先注释掉
# vo_add_fields = [["refreshJwt", "String", "刷新token", ""],
#                  ["token", "String", "token", ""],
#                  ["smsCode", "String", "短信验证码", ""]]

vo_add_fields = []

# dto对象去除的字段
dto_remove_fields = []
# dto对象增加的字段,格式为字段名，数据类型，注释，默认值
dto_add_fields = [["pageNum", "int", "当前页码", "1"],
                  ["pageSize", "int", "每页记录数", "10"]
                  ]


# user表字段,难得改了,先注释掉
# dto_add_fields = [["refreshJwt", "String", "刷新token", ""],
#                   ["newPassword", "String", "新密码", ""],
#                   ["smsCode", "String", "短信验证码", ""],
#                   ["pageNum", "int", "当前页码", "1"],
#                   ["pageSize", "int", "每页记录数", "10"]]


class GenerateUtil:

    @staticmethod
    def generate_phone_numbers(number_of_phone_numbers):
        phone_numbers = []
        for _ in range(number_of_phone_numbers):
            phone_number = "1"  # 以1开头
            for _ in range(10):
                phone_number += str(random.randint(0, 9))
            phone_numbers.append(phone_number)
        return phone_numbers

    @staticmethod
    def generate_names(number_of_names):
        surnames = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩",
                    "杨", "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶",
                    "姜",
                    "戚", "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘", "葛", "奚", "范", "彭", "郎"]
        names = []
        for _ in range(number_of_names):
            name = random.choice(surnames)  # 随机选择一个姓氏
            name_length = random.randint(1, 2)  # 随机名字的长度，可以是1位或2位
            for _ in range(name_length):
                random_char = chr(random.randint(0x4e00, 0x9fff))
                name += random_char
            names.append(HanziConv.toSimplified(name))
        return names


def clear_data(ignore_user_ids=None, ignore_company_ids=None):
    if ignore_user_ids is None:
        ignore_user_ids = []
    if ignore_company_ids is None:
        ignore_company_ids = []

    ignore_user_ids.append(1)
    ignore_user_ids.append(3)
    ignore_company_ids.append(6)
    # 删除user表中id不在user_ids列表中的数据
    cursor.execute("DELETE FROM user WHERE id NOT IN ({})".format(','.join(map(str, ignore_user_ids))))

    # 删除user_role表中user_id不在user_ids列表中的数据
    cursor.execute("DELETE FROM user_role WHERE user_id NOT IN ({})".format(','.join(map(str, ignore_user_ids))))

    cursor.execute("DELETE FROM company WHERE id NOT IN ({})".format(','.join(map(str, ignore_company_ids))))

    cursor.execute("DELETE FROM role_message")

    # 提交事务
    connection.commit()
    print("数据已成功清理")


# 处理消息
def updateMessageById(id, handleStatus):
    url = f"{interface_url}/roleMessage/updateMessageById"
    params = {
        "id": id,
        "handleStatus": handleStatus,
    }
    success, json = send_post_request(url, params)
    if success:
        if json.get("code") != success_code:
            print(f"处理消息失败，原因为:{json.get('message')}")
        else:
            return True, json

    return False


def get_role_message(send_role_id, receive_phone_number, joined_company_id):
    url = f"{interface_url}/roleMessage/getRoleMessage"

    # 定义请求参数
    params = {
        "sendRoleId": send_role_id,
        "receivePhoneNumber": receive_phone_number,
        "joinedCompanyId": joined_company_id
    }
    success, json = send_post_request(url, params)
    if success:
        if json.get("code") == success_code:
            print(f"查询消息数据成功")
            return True, json
        else:
            print(f"查询消息数据失败，原因为:{json.get('message')}")
            return False

    return False


# 企业邀请用户
def inviteUsers(sendRoleId, companyId, receive_phone_numbers):
    url = f"{interface_url}/roleMessage/inviteUsers"

    # 定义请求参数
    params = {
        "sendRoleId": sendRoleId,
        "companyId": companyId,
        "receivePhoneNumbers": receive_phone_numbers
    }
    success, json = send_post_request(url, params)
    if success:
        if json.get("code") == success_code:
            print(f"邀请加入企业成功")
            return True, json
        else:
            print(f"邀请加入企业失败，原因为:{json.get('message')}")
            return False

    return False


# 企业邀请用户
def inviteUser(sendRoleId, companyId, receive_phone_number):
    url = f"{interface_url}/roleMessage/inviteUser"

    # 定义请求参数
    params = {
        "sendRoleId": sendRoleId,
        "companyId": companyId,
        "receivePhoneNumber": receive_phone_number
    }
    success, json = send_post_request(url, params)
    if success:
        if json.get("code") == success_code:
            print(f"邀请加入企业成功")
            return True, json
        else:
            print(f"邀请加入企业失败，原因为:{json.get('message')}")
            return False

    return False


def add_company(user_id):
    fake = Faker(locale='zh_CN')
    company_name = fake.company()
    company_legal_person = fake.name()
    company_address = fake.address()
    company_type = fake.company_suffix()
    company_number = fake.random_number(digits=6)
    company_register_date = datetime.strptime(fake.date(), "%Y-%m-%d").strftime("%Y年%m月%d日")
    company_phone_number = fake.phone_number()
    company_register_number = fake.random_number(digits=8)
    company_register_capital = fake.random_number(digits=7)
    company_credit_code = fake.random_number(digits=18)
    company_business = fake.sentence(nb_words=6)
    company_registration_org = fake.company_suffix()
    status = 2
    create_time = fake.date_time()
    update_time = fake.date_time()
    company_valid_period = fake.date()

    # 插入数据的SQL语句
    sql = (f'INSERT INTO company (user_id, company_name, company_legal_person, company_address, company_type, '
           'company_number, company_register_date, company_phone_number, company_register_number, '
           'company_register_capital, company_credit_code, company_business, company_registration_org, '
           'status, create_time, update_time, company_valid_period) '
           'VALUES '
           '(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    # 执行SQL语句插入数据
    cursor.execute(sql, (
        user_id, company_name, company_legal_person, company_address, company_type, company_number,
        company_register_date, company_phone_number, company_register_number, company_register_capital,
        company_credit_code, company_business, company_registration_org, status, create_time, update_time,
        company_valid_period))
    connection.commit()

    return get_company_by_id(cursor.lastrowid)


def get_company_by_id(company_id):
    sql = f"SELECT * FROM company WHERE id = {company_id}"
    cursor.execute(sql)

    columns = cursor.description
    column_names = [column[0] for column in columns]
    company = cursor.fetchone()
    return company is not None, company, column_names


def get_user_by_id(user_id):
    url = f"http://localhost:8080/user/selectById?id={user_id}"
    success, json = send_get_request(url)
    if success:
        if json.get("code") == success_code:
            return True, json
        else:
            message = json.get("message")
            print(f"获取用户数据失败，失败原因为：{message}")
    return False, json


def get_sms_code(phone_number):
    url = f"{interface_url}/api/getSmsCode?phoneNumber={phone_number}"
    success, json = send_get_request(url)
    if success:
        if json.get("code") == success_code:
            return True, json
    return False, json


def changeRole(userId, targetRoleId):
    url = f"{interface_url}/userRole/changeRole"
    params = {
            "userId": userId,
            "targetRoleId": targetRoleId
        }
    success, json = send_post_request(url, params=params)
    if success:
        if json.get("code") == success_code:
            print("切换角色成功")
            return True, json
        else:
            message = json.get("message")
            print(f"切换角色成功, 原因为{message}")
    return False, json

def login_with_sms_code(phone_number, user_name, pass_word):
    url = f"{interface_url}/api/loginSmsCode"
    success, json = get_sms_code(phone_number)
    if success:
        params = {
            "phoneNumber": phone_number,
            "smsCode": json.get("data").get("smsCode"),
            "userName": user_name,
            "password": pass_word
        }
        success, json = send_post_request(url, params=params)
        if success:
            if json.get("code") == success_code:
                print(f"{phone_number} 登陆成功")
                return True, json
            else:
                message = json.get("message")
                print(f"{phone_number} 登陆失败，原因为:{message}")
    else:
        print("获取验证码失败")
    return False, json


def send_post_request(url, params=None, data=None):
    response = requests.post(url, params=params, data=data, headers=headers)
    if response.status_code == success_code:
        return True, response.json()
    else:
        print("请求失败")
        return False, response.json()


def send_get_request(url):
    response = requests.get(url, headers=headers)
    if response.status_code == success_code:
        return True, response.json()
    else:
        print("请求失败")
        return False


def get_file_name():
    s = ""
    for e in database_table_name.split("_"):
        s += e.capitalize()
    return s


def get_default_value(field: str):
    default_value = ""
    if field == "id":
        default_value = "0L"
    elif field == "upload_user_id":
        default_value = "0L"
    elif field == "file_type_id":
        default_value = "0L"
    elif field == "status":
        default_value = "2"
    elif field == "user_type":
        default_value = "0"
    elif field == "is_set_password":
        default_value = "2"
    elif field == "is_set_real_name":
        default_value = "2"
    elif field == "upload_user_id":
        default_value = "0"
    elif field == "file_type_id":
        default_value = "0"
    return default_value


def get_example_value(field_type: str):
    example_value = ""
    if field_type == "bigint" or field_type == "int" or field_type == "Long":
        example_value = "0"
    return example_value


# 获取表字段和类型以及注释
def get_table_fields_with_comments() -> List[Tuple[str, str, str]]:
    cursor.execute(f"SHOW FULL COLUMNS FROM {database_table_name};")
    fields = cursor.fetchall()
    return [(field[0], field[1], field[8]) for field in fields]


def type_database_to_java(field_type: str):
    # 根据数据库字段类型映射为Java类型
    if field_type.startswith('varchar'):
        java_type = 'String'
    elif field_type == 'String':
        java_type = 'String'
    elif field_type == 'bigint':
        java_type = 'Long'
    elif field_type == 'int':
        java_type = 'int'
    elif field_type == 'timestamp':
        java_type = 'Timestamp'
    elif field_type == 'Long':
        java_type = 'Long'
    else:
        java_type = 'field_type'  # 未知类型
    return java_type


def write_file(data: str, path: str):
    try:
        with open(path, 'w') as f:
            f.write(data)
        print("写入成功")
    except Exception as e:
        print(f"写入文件时发生错误：{e}")
