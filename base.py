from typing import List, Tuple

import pymysql
import requests

host = '192.168.0.232'
database_username = 'yyh'
database_password = '1234qwerQWER'
database_name = 'project'
database_table_name = 'project'
write_path = "/root/IdeaProjects/spring-cloud-project/project_server/src/main/java/com/example"
entity_write_path = write_path + "/entity"
dto_write_path = write_path + "/dto"
vo_write_path = write_path + "/vo"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInN1YiI6IjE4NzE3MDg4NDE0IiwiaWF0IjoxNzExNjA1MDA1LCJl"
                     "eHAiOjg4MTExNjA1MDA1fQ.wrFojucpq4ytvF65ZbDrt-0zc0-MUCTirVm7c_06UIs",
    "Content-Type": "application/json"
}

success_code = 200

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

dto_check_null_fields = ["roleId", "projectGroupId", "projectFileId", "projectName", "projectCoverFileId", "isPublic",
                         "isFree", "isRelease", "projectGroupName", "roleId"]

# user表字段,难得改了,先注释掉
# dto_add_fields = [["refreshJwt", "String", "刷新token", ""],
#                   ["newPassword", "String", "新密码", ""],
#                   ["smsCode", "String", "短信验证码", ""],
#                   ["pageNum", "int", "当前页码", "1"],
#                   ["pageSize", "int", "每页记录数", "10"]]


connection = pymysql.connect(host=host,
                             user=database_username,
                             password=database_password,
                             database=database_name)
cursor = connection.cursor()


# 定义请求头信息


def get_sms_code(interface_url, phone_number):
    url = f"{interface_url}/api/getSmsCode?phoneNumber={phone_number}"
    success, json = send_get_request(url)
    if success:
        if json.get("code") == success_code:
            return True, json
    return False, json


def changeRole(interface_url, userId, targetRoleId):
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


def login_with_sms_code(interface_url, phone_number, user_name, pass_word):
    url = f"{interface_url}/api/loginSmsCode"
    success, json = get_sms_code(interface_url, phone_number)
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


def setToken(token):
    global headers
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }


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
    if field == "upload_user_id":
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


def type_database_to_java_packaging_type(field_type: str):
    # 根据数据库字段类型映射为Java类型
    if field_type.startswith('varchar'):
        java_type = 'String'
    elif field_type == 'String':
        java_type = 'String'
    elif field_type == 'bigint':
        java_type = 'Long'
    elif field_type == 'int':
        java_type = 'Integer'
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
