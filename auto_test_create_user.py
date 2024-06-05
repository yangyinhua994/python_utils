import random
from datetime import datetime

from faker import Faker
from hanziconv import HanziConv

import base

company_handle_status_agree = 1
company_handle_status_refuse = 2
interface_url = "http://localhost:8080"


def get_user_by_id(id):
    url = f"http://localhost:8080/user/selectById?id={id}"
    response_success, response_json = base.send_get_request(url)
    if response_success:
        if response_json.get("code") == base.success_code:
            return True, response_json
        else:
            message = json.get("message")
            print(f"获取用户数据失败，失败原因为：{message}")
    return False, response_json


class GenerateUtil:

    @staticmethod
    def generate_phone_numbers(number_of_phone_numbers):
        numbers = []
        for _ in range(number_of_phone_numbers):
            number = "1"  # 以1开头
            for _ in range(10):
                number += str(random.randint(0, 9))
            numbers.append(number)
        return numbers

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
    base.cursor.execute("DELETE FROM user WHERE id NOT IN ({})".format(','.join(map(str, ignore_user_ids))))

    # 删除user_role表中user_id不在user_ids列表中的数据
    base.cursor.execute("DELETE FROM user_role WHERE user_id NOT IN ({})".format(','.join(map(str, ignore_user_ids))))

    base.cursor.execute("DELETE FROM company WHERE id NOT IN ({})".format(','.join(map(str, ignore_company_ids))))

    base.cursor.execute("DELETE FROM role_message")

    base.cursor.execute("DELETE FROM company_role WHERE id NOT IN ({})".format(','.join(map(str, ignore_company_ids))))

    # 提交事务
    base.connection.commit()
    print("数据已成功清理")


# 处理消息
def updateMessageById(id, handleStatus):
    url = f"{interface_url}/roleMessage/updateMessageById"
    params = {
        "id": id,
        "handleStatus": handleStatus,
    }
    response_success, response_json = base.send_post_request(url, params)
    if response_success:
        if response_json.get("code") != base.success_code:
            print(f"处理消息失败，原因为:{response_json.get('message')}")
        else:
            return True, response_json

    return False


def get_role_message(send_role_id, receive_phone_number, joined_company_id):
    url = f"{interface_url}/roleMessage/getRoleMessage"

    # 定义请求参数
    params = {
        "sendRoleId": send_role_id,
        "receivePhoneNumber": receive_phone_number,
        "joinedCompanyId": joined_company_id
    }
    response_success, response_json = base.send_post_request(url, params)
    if response_success:
        if response_json.get("code") == base.success_code:
            print(f"查询消息数据成功")
            return True, response_json
        else:
            print(f"查询消息数据失败，原因为:{response_json.get('message')}")
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
    response_success, response_json = base.send_post_request(url, params)
    if response_success:
        if response_json.get("code") == base.success_code:
            print(f"邀请加入企业成功")
            return True, response_json
        else:
            print(f"邀请加入企业失败，原因为:{response_json.get('message')}")
            return False

    return False


# 企业邀请用户
def inviteUser(companyId, receive_phone_number):
    url = f"{interface_url}/roleMessage/inviteUser"

    # 定义请求参数
    params = {
        "companyId": companyId,
        "receivePhoneNumber": receive_phone_number
    }
    response_success, response_json = base.send_post_request(url, params)
    if response_success:
        if response_json.get("code") == base.success_code:
            print(f"邀请加入企业成功")
            return True, response_json
        else:
            print(f"邀请加入企业失败，原因为:{response_json.get('message')}")
            return False

    return False


def add_company(id):
    fake = Faker(locale='zh_CN')
    manager_id = id
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
    sql = (
        f'INSERT INTO company (user_id, manager_id, company_name, company_legal_person, company_address, company_type, '
        'company_number, company_register_date, company_phone_number, company_register_number, '
        'company_register_capital, company_credit_code, company_business, company_registration_org, '
        'status, create_time, update_time, company_valid_period) '
        'VALUES '
        '(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    # 执行SQL语句插入数据
    base.cursor.execute(sql, (
        id, manager_id, company_name, company_legal_person, company_address, company_type, company_number,
        company_register_date, company_phone_number, company_register_number, company_register_capital,
        company_credit_code, company_business, company_registration_org, status, create_time, update_time,
        company_valid_period))
    base.connection.commit()

    return get_company_by_id(base.cursor.lastrowid)


def get_company_by_id(id):
    sql = f"SELECT * FROM company WHERE id = {id}"
    base.cursor.execute(sql)

    column_names = [column[0] for column in base.cursor.description]
    company = base.cursor.fetchone()
    return company is not None, company, column_names


if __name__ == '__main__':

    # 测试个数
    test_number = 1
    # 邀请用户加入的公司id
    company_id = None

    # 操作人id
    admin_id = 1
    # 公司邀请处理状态[1：统一，2：拒绝]
    company_handle_status = company_handle_status_agree
    company_refuse_reason = None

    success, json = get_user_by_id(admin_id)
    if success:
        usernames = GenerateUtil.generate_names(test_number)
        phone_numbers = GenerateUtil.generate_phone_numbers(test_number)
        for i in range(test_number):
            all_success = False
            phone_number = phone_numbers[i]
            success, json = base.login_with_sms_code(interface_url, phone_number, usernames[i],
                                                     "123456")
            user_id = None
            if success:
                switching_role_id = 0
                data = json.get("data")
                user_id = data.get("id")
                for userRole in data.get("userRoles"):
                    if userRole.get("isUsed") == 1:
                        switching_role_id = userRole.get("id")
                if switching_role_id == 0:
                    switching_role_id = data.get("userRoles")[0].get("id")
                # 切换角色
                success, json = base.changeRole(interface_url, user_id, switching_role_id)
                if success:
                    if company_id is None:
                        success, row, columns = add_company(admin_id)
                    else:
                        success, row, columns = get_company_by_id(company_id)
                    if success:
                        company_id = row[columns.index("id")]
                        success, json = inviteUser(company_id, phone_number)
                        if success and company_handle_status is not None:
                            success, json = updateMessageById(json.get("data").get("id"), company_handle_status)
                            all_success = True

            if all_success:
                print(f"用户:{usernames[i]} ，电话号码:{phone_number} ,新增成功")
            else:
                print(f"用户:{usernames[i]} ，电话号码:{phone_number} ,新增失败")

    print("自动化测试全部成功")
