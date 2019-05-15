# coding: utf-8

from .notification import AndroidNotification, IosNotification
# from notification import AndroidNotification, IosNotification


key = "5b737e3ea40fa31a7b000721"
secret = "rj3j31g6gxl4xlsu8j4h1k8fstslvss2"


def android_noti():
    noti = AndroidNotification(key, secret, "customizedcast")
    noti.alias_type = "user_id"

    noti.ticker = "ticker"
    noti.title = "title"
    noti.custom = "custom"
    noti.largeIcon = "notify_icon"
    noti.icon = "notify_bg"
    noti.img = "img"

    noti.text = "message"

    noti.extra = {
        'key1': "aa",
        'key2': "key2",
    }

    noti.production_mode = False

    noti.set_alias([1, 2, 3])

    noti.send()


def ios_noti():
    noti = AndroidNotification(key, secret, "customizedcast")
    noti.alias_type = "user_id"

    noti.alert = "message"
    noti.jumpkey = "jumpkey"

    noti.extra = {
        'key1': "key1",
        'key2': "key2",
    }

    noti.production_mode = False
    noti.set_alias([1, 2, 3])

    noti.send()

def ios_notification():
    noti = IosNotification(app_key=key, master_secret=secret, ptype="broadcast")
    noti.production_mode = False
    noti.filter = {
        "where":
            {
                "and": [{"app_version": "1.2"}]
            }
    }

    #noti.body = "新的推送来了"
    noti.sound = "default"
    noti.description = "测试2"
    noti.alert = {"title": "test",
                  "subtitle": "testsub",
                  "body": "新的推送来了"
                  }
    noti.send()





def main():
    #android_noti()
    #ios_noti()
    ios_notification()


if __name__ == "__main__":
    main()
