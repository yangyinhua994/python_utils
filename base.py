# 数据库连接信息
import random

import pymysql
from typing import List, Tuple

import requests

host = '192.168.0.232'
user = 'yyh'
password = '1234qwerQWER'
database = 'project'
table_name = 'company_role'

interface_url = "http://localhost:8080"

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
                random_char = chr(random.randint(0x4e00, 0x9fff))  # 随机生成一个汉字
                name += random_char
            names.append(name)
        return names


def get_sms_code(phone_number):
    url = f"{interface_url}/api/getSmsCode?phoneNumber={phone_number}"
    data = send_get_request(url)
    if data is not None and len(data) > 0:
        if data.get("code") == 200:
            sms_code = data.get("data").get("smsCode")
            return sms_code
    return None


def login_with_phone_number_and_password(phone_number, user_name, pass_word):
    url = f"{interface_url}/api/loginSmsCode"
    sms_code = get_sms_code(phone_number)
    if sms_code is None:
        print("获取验证码失败")
    else:
        params = {
            "phoneNumber": phone_number,
            "smsCode": sms_code,
            "userName": user_name,
            "password": pass_word
        }
        json = send_post_request(url, params=params)
        if json.get("code") == 200:
            print(f"{phone_number} 登陆成功")
        else:
            message = json.get("message")
            print(f"{phone_number} 登陆失败，原因为:{message}")


# 企业邀请用户
def inviteUsers(sendRoleId, companyId, receive_phone_numbers):
    url = f"{interface_url}/roleMessage/inviteUsers"

    # 定义请求参数
    params = {
        "sendRoleId": sendRoleId,
        "companyId": companyId,
        "receivePhoneNumbers": receive_phone_numbers
    }
    json = send_post_request(url, params)
    if json.get("code") == 200:
        print(f"邀请{receive_phone_numbers}加入企业成功")
    else:
        message = json.get("message")
        print(f'邀请{receive_phone_numbers}加入企业失败，原因为:{message}')


def send_post_request(url, params=None, data=None):
    response = requests.post(url, params=params, data=data, headers=headers)
    if response.status_code == 200:
        json = response.json()
        return json
    else:
        print("请求失败")
        return None


def send_get_request(url):
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("code") == 200:
        return response.json()
    else:
        print(response.json().get("message"))


def get_file_name():
    s = ""
    for e in table_name.split("_"):
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


connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database)


# 获取表字段和类型以及注释
def get_table_fields_with_comments() -> List[Tuple[str, str, str]]:
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW FULL COLUMNS FROM {table_name};")
            fields = cursor.fetchall()
            return [(field[0], field[1], field[8]) for field in fields]
    except pymysql.Error as e:
        print("Error getting table fields:", e)
        return []


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
