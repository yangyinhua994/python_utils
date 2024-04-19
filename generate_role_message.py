import pymysql
import requests

import base

connection = pymysql.connect(host=base.host,
                             user=base.user,
                             password=base.password,
                             database=base.database)
cursor = connection.cursor()


# 处理消息
def updateMessageById(ids: list, handleStatus):
    url = f"{base.interface_url}/roleMessage/updateMessageById"
    for id in ids:
        params = {
            "id": id,
            "handleStatus": handleStatus,
        }
        json = base.send_post_request(url, params)
        if json is not None:
            if json.get("code") == 200:
                print("操作成功")


# 企业邀请用户
def inviteUsers(sendRoleId, companyId, receive_phone_numbers):
    url = f"{base.interface_url}/roleMessage/inviteUsers"

    # 定义请求参数
    params = {
        "sendRoleId": sendRoleId,
        "companyId": companyId,
        "receivePhoneNumbers": receive_phone_numbers
    }
    base.send_post_request(url, params)
    cursor.close()


# 从数据库中获取
# cursor.execute("select phone_number from user_role where company_id is null ")
# phone_numbers = cursor.fetchall()
# receive_phone_numbers = [phone_number[0] for phone_number in phone_numbers]

# 随机生成
# phone_numbers = base.GenerateUtil.generate_phone_numbers(100)
# receive_phone_numbers = [phone_number for phone_number in phone_numbers]
#
# inviteUsers(1, 6, receive_phone_numbers)
cursor.execute("select id from role_message where handle_status = 0")
data = cursor.fetchall()
ids = [id[0] for id in data]
updateMessageById(ids, 1)

connection.close()
