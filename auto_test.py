import base

company_handle_status_agree = 1
company_handle_status_refuse = 2

if __name__ == '__main__':

    # 测试个数
    test_number = 4000
    # 邀请用户加入的公司id
    company_id = None

    # 操作人id
    admin_id = 1
    # 公司邀请处理状态[1：统一，2：拒绝]
    company_handle_status = company_handle_status_agree
    company_refuse_reason = None

    success, json = base.get_user_by_id(admin_id)
    if success:
        usernames = base.GenerateUtil.generate_names(test_number)
        phone_numbers = base.GenerateUtil.generate_phone_numbers(test_number)
        for i in range(test_number):
            all_success = False
            phone_number = phone_numbers[i]
            success, json = base.login_with_sms_code(phone_number, usernames[i], "123456")
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
                success, json = base.changeRole(user_id, switching_role_id)
                if success:
                    if company_id is None:
                        success, row, columns = base.add_company(admin_id)
                    else:
                        success, row, columns = base.get_company_by_id(company_id)
                    if success:
                        company_id = row[columns.index("id")]
                        success, json = base.inviteUser(admin_id, company_id, phone_number)
                        if success and company_handle_status is not None:
                            success, json = base.updateMessageById(json.get("data").get("id"), company_handle_status)
                            all_success = True

            if all_success:
                print(f"用户:{usernames[i]} ，电话号码:{phone_number} ,新增成功")
            else:
                print(f"用户:{usernames[i]} ，电话号码:{phone_number} ,新增失败")

    print("自动化测试全部成功")