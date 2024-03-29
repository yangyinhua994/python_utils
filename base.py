# 数据库连接信息
import pymysql
from typing import List, Tuple

host = 'localhost'
user = 'root'
password = '1234qwerQWER'
database = 'project'
table_name = 'user_role'

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
                    "upload_user_id"]

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
                  ["pageSize", "int", "每页记录数", "10"]]


# user表字段,难得改了,先注释掉
# dto_add_fields = [["refreshJwt", "String", "刷新token", ""],
#                   ["newPassword", "String", "新密码", ""],
#                   ["smsCode", "String", "短信验证码", ""],
#                   ["pageNum", "int", "当前页码", "1"],
#                   ["pageSize", "int", "每页记录数", "10"]]


def get_file_name():
    s = ""
    for e in table_name.split("_"):
        s += e.capitalize()
    return s


def get_default_value(field: str):
    default_value = ""
    if field == "id":
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
