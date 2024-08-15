import os
from typing import List, Tuple

import pymysql

server_name = "project-server"
database_name = 'project'
database_table_name = 'project_label'
this_example_path = f"/root/IdeaProjects/bjq_parent/{server_name}/src/main/java/com/example"
common_example_path = "/root/IdeaProjects/bjq_parent/common/src/main/java/com/example"
host = 'localhost'
database_username = 'yyh'
database_password = '1234qwerQWER'
entity_write_path = os.path.join(common_example_path, 'entity')
dto_write_path = os.path.join(common_example_path, 'dto')
vo_write_path = os.path.join(common_example_path, 'vo')
controller_path = os.path.join(this_example_path, 'controller')
service_path = os.path.join(common_example_path, 'service')
service_impl_path = os.path.join(common_example_path, 'service/impl')
mapper_path = os.path.join(common_example_path, 'mapper')

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInN1YiI6IjE4NzE3MDg4NDE0IiwiaWF0IjoxNzExNjA1MDA1LCJl"
                     "eHAiOjg4MTExNjA1MDA1fQ.wrFojucpq4ytvF65ZbDrt-0zc0-MUCTirVm7c_06UIs",
    "Content-Type": "application/json"
}

success_code = 200

# vo对象去除的字段
entity_remove_fields = ["id", "create_time", "update_time", "status"]

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

resource_vo_add_fields = [["modelFile", "File", "模型文件", ""], ["modelCoverFile", "File", "模型封面文件", ""]]
project_vo_add_fields = []
project_group_role_vo_add_fields = []

vo_add_fields = project_vo_add_fields

# dto对象去除的字段
dto_remove_fields = ["create_time", "update_time"]
# dto对象增加的字段,格式为字段名，数据类型，注释，默认值
user_dto_add_fields = [["refreshJwt", "String", "刷新token", ""],
                       ["newPassword", "String", "新密码", ""],
                       ["smsCode", "String", "短信验证码", ""],
                       ["pageNum", "Integer", "当前页码", "1"],
                       ["pageSize", "Integer", "每页记录数", "10"]]
base_dto = [["pageNum", "Integer", "当前页码", "1"], ["pageSize", "Integer", "每页记录数", "10"]]
project_dto_add_fields = [["orderType", "Integer", "排序方式", "0"]]
label_dto_add_fields = []
model_label_dto_add_fields = []

dto_add_fields = base_dto + model_label_dto_add_fields

dto_not_check_null_fields = ["id", "createTime", "updateTime", "status", "pageNum", "pageSize", "jsonFilePath",
                             "project_cover_file_id", "project_file_id", "is_free", "is_public", "label_id",
                             "is_release", "json_file_id"]

connection = pymysql.connect(host=host,
                             user=database_username,
                             password=database_password,
                             database=database_name)
cursor = connection.cursor()


def get_default_value(field: str):
    default_value = ""
    if field == "upload_user_id":
        default_value = "0L"
    elif field == "file_type_id":
        default_value = "0L"
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
    if field_type == "bigint" or field_type == "Integer" or field_type == "Long":
        example_value = "0"
    return example_value


# 获取表字段和类型以及注释
def get_table_fields_with_comments() -> List[Tuple[str, str, str]]:
    cursor.execute(f"SHOW FULL COLUMNS FROM {database_table_name};")
    fields = cursor.fetchall()
    return [(field[0], field[1], field[8]) for field in fields]


def type_database_to_java(field_type: str):
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
        java_type = field_type
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
        java_type = field_type
    return java_type


def write_file(data: str, path: str):
    p = os.path.dirname(path)
    if not os.path.exists(p):
        os.makedirs(p)
    try:
        with open(path, 'w') as f:
            f.write(data)
        print(f"文件创建成功: {path}")
    except Exception as e:
        print(f"写入文件时发生错误：{e}")


def get_file_name_last_upper():
    s = ""
    for e in database_table_name.split("_"):
        s += e.capitalize()
    return s[0].upper() + s[1:]


def get_file_name_last_lower():
    s = ""
    for e in database_table_name.split("_"):
        s += e.capitalize()
    return s[0].lower() + s[1:]
