import pymysql
import requests

import base

connection = pymysql.connect(host=base.host,
                             user=base.user,
                             password=base.password,
                             database=base.database)
cursor = connection.cursor()

if __name__ == '__main__':
    # 邀请用户加入的公司id
    company_id = None
    # 测试个数
    test_number = 1
    if company_id is None:
        sql = "select * from company LIMIT 0, 1"
        cursor.execute(sql)
    else:
        sql = f"select * from company where id = {company_id}"
        cursor.execute(sql)

    columns = cursor.description
    column_names = [column[0] for column in columns]
    row = cursor.fetchone()

    if row is None:
        print("没有查询到该公司数据")
    else:
        # 根据字段名来获取字段值
        company_id_index = column_names.index("id")
        user_id_index = column_names.index("user_id")

        company_id = row[company_id_index]
        user_id = row[user_id_index]

        usernames = base.GenerateUtil.generate_names(test_number)
        phone_numbers = base.GenerateUtil.generate_phone_numbers(test_number)
        for i in range(test_number):
            base.login_with_phone_number_and_password(phone_numbers[i], usernames[i], "123456")
            base.inviteUsers(user_id, company_id, phone_numbers[i])

cursor.close()








