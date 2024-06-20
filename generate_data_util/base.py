import pymysql
import requests

host = '10.1.10.49'
database_username = 'root'
database_password = 'root'
database_name = 'project'
database_table_name = 'textures'
write_path = "/root/IdeaProjects/spring-cloud-project/project-server/src/main/java/com/example"
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
