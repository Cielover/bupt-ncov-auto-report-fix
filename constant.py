from abc import ABCMeta, abstractmethod
from typing import Optional
import os

"""
USERS=[("学号","密码","姓名/昵称",0)]
WECOM=("企业ID③", "应用ID①", "应用secret②")
"""

if os.getenv('USERS') is None:
    USERS = []
else:
    USERS = eval(os.environ['USERS'])
if os.getenv('USERS') is None:
    WECOM = [None, None, None]
else:
    WECOM = eval(os.environ['WECOM'])

LOGIN_API = 'https://auth.bupt.edu.cn/authserver/login'
# LOGIN_API = 'https://app.bupt.edu.cn/uc/wap/login/check'
GET_API = 'https://app.bupt.edu.cn/ncov/wap/default/index'
REPORT_API = 'https://app.bupt.edu.cn/ncov/wap/default/save'
GETEven_API = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/index'
POSTEven_API = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/save'

# 当今日没有填报时，在https://app.bupt.edu.cn/ncov/wap/default/index下进行填报，
# 全部填完，不要提交，f12打开控制台，在Console页面下输入代码 console.log(vm.info) 就会得到以下信息，之后每天就默认填以下信息
if os.getenv('DATA_DAILY') is None:
    INFO = r"""{
        "address":"北京市海淀区北太平庄街道北京邮电大学北京邮电大学海淀校区",
        "area":"北京市  海淀区",
        "bztcyy":"",
        "city":"北京市",
        "csmjry":"0",
        "fjqszgjdq":"",
        "geo_api_info":"{\"type\":\"complete\",\"position\":{\"Q\":39.963315158421,\"R\":116.35622233073002,\"lng\":116.356222,\"lat\":39.963315},\"location_type\":\"html5\",\"message\":\"Get geolocation success.Convert Success.Get address success.\",\"accuracy\":40,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"010\",\"adcode\":\"110108\",\"businessAreas\":[{\"name\":\"北下关\",\"id\":\"110108\",\"location\":{\"Q\":39.955976,\"R\":116.33873,\"lng\":116.33873,\"lat\":39.955976}},{\"name\":\"小西天\",\"id\":\"110108\",\"location\":{\"Q\":39.957147,\"R\":116.364058,\"lng\":116.364058,\"lat\":39.957147}},{\"name\":\"西直门\",\"id\":\"110102\",\"location\":{\"Q\":39.942856,\"R\":116.34666099999998,\"lng\":116.346661,\"lat\":39.942856}}],\"neighborhoodType\":\"科教文化服务;学校;高等院校\",\"neighborhood\":\"北京邮电大学\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"西土城路\",\"streetNumber\":\"10号\",\"country\":\"中国\",\"province\":\"北京市\",\"city\":\"\",\"district\":\"海淀区\",\"towncode\":\"110108008000\",\"township\":\"北太平庄街道\"},\"formattedAddress\":\"北京市海淀区北太平庄街道北京邮电大学北京邮电大学海淀校区\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
        "glksrq":"",
        "gllx":"",
        "gtjzzchdfh":"",
        "gtjzzfjsj":"",
        "ismoved":"0",
        "jcbhlx":"",
        "jcbhrq":"",
        "jchbryfs":"",
        "jcjgqr":"0",
        "jcwhryfs":"",
        "jhfjhbcc":"",
        "jhfjjtgj":"",
        "jhfjrq":"",
        "mjry":"0",
        "province":"北京市",
        "qksm":"",
        "remark":"",
        "sfcxtz":"0",
        "sfcxzysx":"0",
        "sfcyglq":"0",
        "sfjcbh":"0",
        "sfjchbry":"0",
        "sfjcwhry":"0",
        "sfjzdezxgym":"1",
        "sfjzxgym":"1",
        "sfsfbh":"0",
        "sftjhb":"0",
        "sftjwh":"0",
        "sfxk":"0",
        "sfygtjzzfj":"",
        "sfyyjc":"0",
        "sfzx":1,
        "szcs":"",
        "szgj":"",
        "szsqsfybl":"0",
        "tw":"2",
        "xjzd":"",
        "xkqq":"",
        "xwxgymjzqk":"3",
        "ymjzxgqk":"已接种",
        "zgfxdq":"0"
        }"""
else:
    INFO = eval(os.environ['DATA_DAILY'])

if os.getenv('DATA_REPORT') is None:
    INFO_E = r"""{
        "sfzx": "1",
        "tw":"1",
        "area":"北京市  海淀区",
        "city":"北京市",
        "province":"北京市",
        "address":"北京市海淀区北太平庄街道北京邮电大学北京邮电大学海淀校区",
        "geo_api_info":"{\"type\":\"complete\",\"position\":{\"Q\":39.963315158421,\"R\":116.35622233073002,\"lng\":116.356222,\"lat\":39.963315},\"location_type\":\"html5\",\"message\":\"Get geolocation success.Convert Success.Get address success.\",\"accuracy\":40,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"010\",\"adcode\":\"110108\",\"businessAreas\":[{\"name\":\"北下关\",\"id\":\"110108\",\"location\":{\"Q\":39.955976,\"R\":116.33873,\"lng\":116.33873,\"lat\":39.955976}},{\"name\":\"小西天\",\"id\":\"110108\",\"location\":{\"Q\":39.957147,\"R\":116.364058,\"lng\":116.364058,\"lat\":39.957147}},{\"name\":\"西直门\",\"id\":\"110102\",\"location\":{\"Q\":39.942856,\"R\":116.34666099999998,\"lng\":116.346661,\"lat\":39.942856}}],\"neighborhoodType\":\"科教文化服务;学校;高等院校\",\"neighborhood\":\"北京邮电大学\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"西土城路\",\"streetNumber\":\"10号\",\"country\":\"中国\",\"province\":\"北京市\",\"city\":\"\",\"district\":\"海淀区\",\"towncode\":\"110108008000\",\"township\":\"北太平庄街道\"},\"formattedAddress\":\"北京市海淀区北太平庄街道北京邮电大学北京邮电大学海淀校区\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
        "sfcyglq": "0",
        "sfyzz": "0",
        "qtqk": "",
        "askforleave": "0"
        }"""
else:
    INFO = eval(os.environ['DATA_REPORT'])

REASONABLE_LENGTH = 24
TIMEOUT_SECOND = 25


class HEADERS:
    REFERER_LOGIN_API = 'https://app.bupt.edu.cn/uc/wap/login'
    REFERER_POST_API = 'https://app.bupt.edu.cn/ncov/wap/default/index'
    ORIGIN_BUPTAPP = 'https://app.bupt.edu.cn'

    NEW_ORIGIN_LOGIN = 'https://auth.bupt.edu.cn'
    NEW_REFERER_LOGIN = 'https://auth.bupt.edu.cn/authserver/login'

    UA = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55')
    ACCEPT_JSON = 'application/json'
    ACCEPT_HTML = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    REQUEST_WITH_XHR = 'XMLHttpRequest'
    ACCEPT_LANG = 'zh-cn'
    CONTENT_TYPE_UTF8 = 'application/x-www-form-urlencoded; charset=UTF-8'

    def __init__(self) -> None:
        raise NotImplementedError


COMMON_HEADERS = {
    'User-Agent': HEADERS.UA,
    'Accept-Language': HEADERS.ACCEPT_LANG,
    'sec-gpc': '1',
    'sec-fetch-user': '?1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'sec-ch-ua-platform': 'Windows',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"'
}
COMMON_POST_HEADERS = {
    'Accept': HEADERS.ACCEPT_JSON,
    'Origin': HEADERS.ORIGIN_BUPTAPP,
    'X-Requested-With': HEADERS.REQUEST_WITH_XHR,
    'Content-Type': HEADERS.CONTENT_TYPE_UTF8,
}


class INotifier(metaclass=ABCMeta):
    @property
    @abstractmethod
    def PLATFORM_NAME(self) -> str:
        """
        将 PLATFORM_NAME 设为类的 Class Variable，内容是通知平台的名字（用于打日志）。
        如：PLATFORM_NAME = 'Telegram 机器人'
        :return: 通知平台名
        """

    @abstractmethod
    def notify(self, *, success, msg, data, username, name) -> None:
        """
        通过该平台通知用户操作成功的消息。失败时将抛出各种异常。
        :param success: 表示是否成功
        :param msg: 成功时表示服务器的返回值，失败时表示失败原因；None 表示没有上述内容
        :return: None
        """
