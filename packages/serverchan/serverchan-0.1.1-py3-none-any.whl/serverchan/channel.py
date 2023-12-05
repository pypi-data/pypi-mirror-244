from enum import Enum

class Channels(Enum):
    # 方糖服务号=9
    WECHAT_SERVICE_ACCOUNT = 9
    # 企业微信应用消息=66
    WEWORK_SERVICE_ACCOUNT = 66
    # Bark iOS=8
    BARK_IOS = 8
    # 企业微信群机器人=1
    WEWORK_ROBOT = 1
    # 钉钉群机器人=2
    DINGTALK_WEBHOOK = 2
    # 飞书群机器人=3
    LARK_WEBHOOK = 3
    # 测试号=0
    TEST_ACCOUNT = 0
    # 自定义=88
    CUSTOM = 88
    # PushDeer=18
    PUSHDEER = 18
    # 官方Android版·β=98
    ANDROID_APP = 98