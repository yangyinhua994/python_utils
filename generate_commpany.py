import datetime
import pymysql
from faker import Faker

import base

connection = pymysql.connect(host=base.host,
                             user=base.user,
                             password=base.password,
                             database=base.database)
cursor = connection.cursor()

cursor.execute("SELECT user.id FROM user LEFT JOIN company ON user.id = company.user_id WHERE company.user_id IS NULL;")
user_ids = cursor.fetchall()

fake = Faker(locale='zh_CN')

# 插入数据的SQL语句
sql = ("INSERT INTO company (user_id, company_name, company_legal_person, company_address, company_type, "
       "company_number, company_register_date, company_phone_number, company_register_number, "
       "company_register_capital, company_credit_code, company_business, company_registration_org, "
       "status, create_time, update_time, company_valid_period) "
       "VALUES "
       "(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

num_companies_per_user = len(user_ids)

for user_id in user_ids:
    # 生成虚假数据
    company_name = fake.company()
    company_legal_person = fake.name()
    company_address = fake.address()
    company_type = fake.company_suffix()
    company_number = fake.random_number(digits=6)
    company_register_date = datetime.datetime.strptime(fake.date(), "%Y-%m-%d").strftime("%Y年%m月%d日")
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

    # 执行SQL语句插入数据
    cursor.execute(sql, (
        user_id[0], company_name, company_legal_person, company_address, company_type, company_number,
        company_register_date, company_phone_number, company_register_number, company_register_capital,
        company_credit_code, company_business, company_registration_org, status, create_time, update_time,
        company_valid_period))

# 提交事务
connection.commit()

# 关闭游标和数据库连接
cursor.close()
connection.close()

print("数据插入成功")
