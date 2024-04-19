import random

import pymysql
import requests

import base

connection = pymysql.connect(host=base.host,
                             user=base.user,
                             password=base.password,
                             database=base.database)
cursor = connection.cursor()


def login_with_receive_phone_number():
    url = "http://localhost:8080/api/loginSmsCode"

    cursor.execute("select receive_phone_number from role_message where receive_phone_number is not null "
                   "and handle_status = 0")
    receive_phone_numbers = [phone_number[0] for phone_number in cursor.fetchall()]
    for receive_phone_number in receive_phone_numbers:
        sms_code = get_sms_code(receive_phone_number)
        if sms_code is None:
            print("获取验证码失败")
        params = {
            "phoneNumber": receive_phone_number,
            "smsCode": sms_code,
        }
        json = base.send_post_request(url, params=params)
        if json is not None:
            if json.get("code") == 200:
                print("操作成功")
            else:
                print("操作失败")


if __name__ == "__main__":
    number = 1
    phone_numbers = base.GenerateUtil.generate_phone_numbers(number)
    names = base.GenerateUtil.generate_names(number)
    for i in range(number):
        base.login_with_phone_number_and_password(phone_numbers[i], names[i], "123456")
        base.inviteUsers()
    # login_with_receive_phone_number()

    cursor.close()
