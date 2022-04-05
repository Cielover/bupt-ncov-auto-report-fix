from constant import *
from wecom import *

import requests, re, json, copy, traceback, time
from requests.adapters import HTTPAdapter
import socket

socket.setdefaulttimeout(120)

wecom_cid, wecom_aid, wecom_secret = WECOM
RETRY_TIMES = 5
RETRY_SLOT = 10  # 重试间隔时间（秒）


def ncov_report(username, password, is_useold):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    print('登录统一身份认证...')
    login_get = session.get(
        LOGIN_API,
        headers={**COMMON_HEADERS}
    )
    if login_get.status_code != 200:
        raise RuntimeError('login_get 状态码不是 200')

    pattern = re.compile('<input name="execution" value="(.+?)"/><input name="_eventId" value="submit"/>')
    execution = pattern.findall(login_get.text)[0]

    login_res = session.post(
        LOGIN_API,
        data={'username': username,
              'password': password,
              'submit': "LOGIN",
              'type': "username_password",
              '_eventId': "submit",
              'execution': execution},
        headers={**COMMON_HEADERS}
    )
    if login_res.status_code != 200:
        raise RuntimeError('login_res 状态码不是 200')

    print('获取历史提交数据...')
    get_res = session.get(
        GET_API,
        headers={**COMMON_HEADERS, 'Accept': HEADERS.ACCEPT_HTML},
    )
    if get_res.status_code != 200:
        raise RuntimeError('get_res 状态码不是 200')
    try:
        old_data = json.loads('{' + re.search(r'(?<=oldInfo: {).+(?=})', get_res.text)[0] + '}')
    except:
        raise RuntimeError('未获取到昨日打卡数据，请今日手动打卡明日再执行脚本或使用固定打卡数据')
    post_data = json.loads(copy.deepcopy(INFO).replace("\n", "").replace(" ", ""))
    if is_useold:
        try:
            for k, v in old_data.items():
                if k in post_data:
                    post_data[k] = v
            geo = json.loads(old_data['geo_api_info'])

            province = geo['addressComponent']['province']
            city = geo['addressComponent']['city']
            if geo['addressComponent']['city'].strip() == "" and len(re.findall(r'北京市|上海市|重庆市|天津市', province)) != 0:
                city = geo['addressComponent']['province']
            area = province + " " + city + " " + geo['addressComponent']['district']
            address = geo['formattedAddress']
            post_data['province'] = province
            post_data['city'] = city
            post_data['area'] = area
            post_data['address'] = address

            # 强行覆盖一些字段
            post_data['ismoved'] = 0  # 是否移动了位置？否
            post_data['bztcyy'] = ''  # 不在同城原因？空
            post_data['sfsfbh'] = 0  # 是否省份不合？否
        except:
            print("加载昨日数据错误，采用固定数据")
            post_data = json.loads(copy.deepcopy(INFO).replace("\n", "").replace(" ", ""))
    print('提交填报数据...')
    report_res = session.post(
        REPORT_API,
        data=post_data,
        headers={**COMMON_HEADERS, **COMMON_POST_HEADERS, 'Referer': HEADERS.REFERER_POST_API, },
    )
    if report_res.status_code != 200:
        raise RuntimeError('report_res 状态码不是 200')
    session.close()
    return post_data, report_res.text


def ncov_even_report(username, password, is_useold):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    print('登录统一身份认证...')
    login_get = session.get(
        LOGIN_API,
        headers={**COMMON_HEADERS}
    )
    if login_get.status_code != 200:
        raise RuntimeError('login_get 状态码不是 200')

    pattern = re.compile('<input name="execution" value="(.+?)"/><input name="_eventId" value="submit"/>')
    execution = pattern.findall(login_get.text)[0]

    login_res = session.post(
        LOGIN_API,
        data={'username': username,
              'password': password,
              'submit': "LOGIN",
              'type': "username_password",
              '_eventId': "submit",
              'execution': execution},
        headers={**COMMON_HEADERS}
    )
    if login_res.status_code != 200:
        raise RuntimeError('login_res 状态码不是 200')

    print('获取历史提交数据...')
    get_res = session.get(
        GET_API,
        headers={**COMMON_HEADERS, 'Accept': HEADERS.ACCEPT_HTML},
    )
    if get_res.status_code != 200:
        raise RuntimeError('get_res 状态码不是 200')
    try:
        old_data = json.loads('{' + re.search(r'(?<=oldInfo: {).+(?=})', get_res.text)[0] + '}')
    except:
        raise RuntimeError('未获取到昨日打卡数据，请今日手动打卡明日再执行脚本或使用固定打卡数据')

    get_res = session.get(
        GETEven_API,
        headers={**COMMON_HEADERS, 'Accept': HEADERS.ACCEPT_HTML},
    )
    if get_res.status_code != 200:
        raise RuntimeError('get_res 状态码不是 200')

    post_data = json.loads(copy.deepcopy(INFO_E))
    if is_useold:
        try:
            for k, v in old_data.items():
                if k in post_data:
                    post_data[k] = v
            geo = old_data
            info = geo['geo_api_info']
            geo = json.loads(info)

            province = geo['addressComponent']['province']
            city = geo['addressComponent']['city']
            district = geo['addressComponent']['district']
            if geo['addressComponent']['city'].strip() == "" and len(re.findall(r'北京市|上海市|重庆市|天津市', province)) != 0:
                city = geo['addressComponent']['province']

            # area = province + " " + city + " " + geo['addressComponent']['district']
            area = province + city + district
            address = geo['formattedAddress']
            post_data['geo_api_info'] = info
            post_data['province'] = province
            post_data['city'] = city
            post_data['area'] = area
            post_data['address'] = address

            # 强行覆盖一些字段

        except:
            print("加载上次晨午晚检数据错误，采用固定数据")
            post_data = json.loads(copy.deepcopy(INFO_E).replace("\n", "").replace(" ", ""))
    print('提交填报数据...')
    report_res = session.post(
        POSTEven_API,
        data=post_data,
        headers={**COMMON_HEADERS, **COMMON_POST_HEADERS, 'Referer': HEADERS.REFERER_POST_API, },
    )
    if report_res.status_code != 200:
        raise RuntimeError('report_res 状态码不是 200')
    session.close()
    return post_data, report_res.text


if __name__ == '__main__':
    now_hour = datetime.datetime.utcnow().hour

    for user in USERS:
        username, password, name, useold = user

        if (22 <= now_hour <= 24 or 0 <= now_hour <= 3):
            success_final = False
            success = False
            msg_push = ''
            for i in range(RETRY_TIMES):
                try:
                    data, res = ncov_report(username=username, password=password, is_useold=(useold == 0))
                    success = True
                except requests.exceptions.RequestException:
                    success = False
                    data, res = '', "网络连接错误"
                except:
                    success = False
                    data, res = '', traceback.format_exc()
                time.sleep(RETRY_SLOT)
                success_final = success_final or success
                msg1 = f' {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {name}《每日填报》填报成功!服务器返回数据:\n{res}\n\n每日填报填报数据:\n{data}\n' if success else f'{name}《每日填报》填报失败!发生如下异常:\n{res}'
                print(msg1)
                if success:
                    msg_push = msg1
            if success_final:
                msg_push = "【成功】 " + msg_push
            else:
                msg_push = "【失败】 " + msg1
            send_to_wecom(msg_push, wecom_cid, wecom_aid, wecom_secret)
            # print(f'填报数据:\n{data}\n')

        success_final = False
        success = False
        msg_push = ''
        for i in range(RETRY_TIMES):
            try:
                data, res = ncov_even_report(username=username, password=password, is_useold=(useold == 0))
                success = True
            except requests.exceptions.RequestException:
                success = False
                data, res = '', "网络连接错误"
            except:
                success = False
                data, res = '', traceback.format_exc()
            time.sleep(RETRY_SLOT)
            success_final = success_final or success
            msg2 = f' {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {name}的《晨午晚检》填报成功!服务器返回数据:\n{res}\n\n晨午晚检填报数据:\n{data}\n' if success else f'{name}《晨午晚检》填报失败!发生如下异常:\n{res}'
            print(msg2)
            if success:
                msg_push = msg2
        if success_final:
            msg_push = "【成功】 " + msg_push
        else:
            msg_push = "【失败】 " + msg2
        send_to_wecom(msg_push, wecom_cid, wecom_aid, wecom_secret)
