import requests

import base


def invite_users():
    url = f"{base.interface_url}/roleMessage/test"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInN1YiI6IjE4NzE3MDg4N"
                         "DE0IiwiaWF0IjoxNzExNjA1MDA1LCJleHAiOjg4MTExNjA1MDA1fQ.wrFojucpq4y"
                         "tvF65ZbDrt-0zc0-MUCTirVm7c_06UIs",
        "Content-Type": "application/json"
    }

    # 构建请求体
    data = {
        "sendRoleId": 1,
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, params=data)
    print(response)


invite_users()
