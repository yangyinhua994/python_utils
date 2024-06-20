import base

model_names = ["蓝色跑车", "山坡小屋", "铁塔之光", "钛合金齿轮", "太空探索者", "森林木屋", "铜色塔楼", "钢铁之心",
               "极速飞车", "海边别墅", "黑曜石柱", "黄金齿轮", "大陆巡航", "草原小屋", "钻石塔峰", "永动机", "城市猎手",
               "山谷小屋", "银河之柱", "风暴机关", "赛车之王", "小木屋", "银色圆锥", "绿色越野车", "花园小屋",
               "黑色电力塔", "红色跑车", "钢铁齿轮", "蓝色速度", "黄铜齿轮", "太空漫步者", "梦幻小屋", "太阳之塔",
               "精密齿轮", "银河飞车", "湖边小屋", "高塔之巅", "极速齿轮", "豪华跑车", "沙漠别墅"
               ]

# 新建项目组
project_group_name = ["园区", "机场", "体育馆", "仓库", "水利", "地铁", "写字楼"]
insert_project_groupGroup = "http://localhost:8888/projectGroupGroup/insert"
insert_project = "http://localhost:8888/project/insert"
phoneNumber = "18717088414"
password = "123456"

response_success, response_json = base.login_with_phoneNumber_password(phoneNumber, password)
if response_success:
    base.setToken(response_json.get("data").get("token"))
else:
    print(f'登陆失败: {response_json.get("message")}')
    exit(1)

for e in project_group_name:
    project_group_data = {
        "projectGroupName": f"{e}",
        "roleId": 5757,
        "parentId": 0
    }
    response_success, response_json = base.send_post_request(insert_project_groupGroup, data=project_group_data)
    if response_success:
        project_groupGroup_id = response_json.get("data").get("id")
        project_data = {

        }
