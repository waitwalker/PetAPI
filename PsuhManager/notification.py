# -*- coding: utf-8 -*-

import time
from .pushclient import PushClientMixin

__all__ = ["Notification", "AndroidNotification", "IosNotification"]


class AndPayload(object):
    __slots__ = ('display_type', 'body', 'extra')

    def __int__(self):
        pass


class AndBody(object):
    __slots__ = ("ticker", "title", "text", "icon", "largeIcon", "img", "sound",
                 "builder_id", "play_vibrate", "play_lights", "play_sound", "after_open",
                 "url", "activity", "custom")

    def __init__(self):
        pass


class IosPayload(object):
    __slots__ = ('aps', 'jumpkey', 'extra')

    def __init__(self):
        pass


class IosAps(object):
    __slots__ = ('alert', 'badge', 'sound', 'content_available', 'category')

    def __init__(self):
        pass


class Policy(object):
    __slots__ = ('start_time', 'expire_time', 'max_send_num', 'out_biz_no', 'apns_collapse_id')

    def __int__(self):
        pass


class Notification(object):
    __slots__ = ('appkey', 'master_screte', 'type', 'device_tokens', 'alias_type', 'alias',''
                 'file_id', 'filter', 'production_mode', 'description', 'thirdparty_id',
                 'body', 'payload', 'policy')

    def __init__(self, app_key, master_secret, ptype):
        self.appkey = app_key
        self.master_screte = master_secret
        self.type = ptype
        self.filter = {}
        self.production_mode = "true"
        self.policy = Policy()
        self.description = ""

    def to_json(self):
        raise NotImplementedError()

    def set_alias(self, alias):
        if isinstance(alias, (tuple, list)):
            self.alias = ','.join(str(e) for e in alias)
        else:
            self.alias = str(alias)

    @property
    def start_time(self):
        return self.policy.start_time

    @start_time.setter
    def start_time(self, v):
        self.policy.start_time = v

    @property
    def expire_time(self):
        return self.policy.expire_time

    @expire_time.setter
    def expire_time(self, v):
        self.policy.expire_time = v

    @property
    def max_send_num(self):
        return self.policy.max_send_num

    @max_send_num.setter
    def max_send_num(self, v):
        self.policy.max_send_num = v


class AndroidNotification(Notification, PushClientMixin):

    def __init__(self, app_key, master_secret, ptype):
        """

        """
        super(AndroidNotification, self).__init__(app_key, master_secret, ptype)
        self.payload = AndPayload()
        self.payload.body = self.body = AndBody()

    def to_json(self):
        body = {k: getattr(self.body, k) for k in self.body.__slots__
                if getattr(self.body, k, None) is not None}
        policy = {k: getattr(self.policy, k) for k in self.policy.__slots__
                  if getattr(self.policy, k, None) is not None}
        payload = {k: getattr(self.payload, k) for k in self.payload.__slots__
                   if getattr(self.payload, k, None) is not None}
        data = {k: getattr(self, k) for k in self.__slots__
                if getattr(self, k, None) is not None}

        del data['master_screte']
        del data['body']
        del data['policy']

        data['payload'] = payload
        data['payload']['body'] = body
        data['timestamp'] = int(time.time() * 1000)

        if policy:
            data['policy'] = policy

        return data

    @property
    def out_biz_no(self):
        return self.policy.out_biz_no

    @out_biz_no.setter
    def out_biz_no(self, v):
        self.policy.out_biz_no = v

    @property
    def display_type(self):
        return self.payload.display_type

    @display_type.setter
    def display_type(self, v):
        self.payload.display_type = v

    @property
    def ticker(self):
        return self.body.ticker

    @ticker.setter
    def ticker(self, v):
        self.body.ticker = v

    @property
    def title(self):
        return self.body.title

    @title.setter
    def title(self, v):
        self.body.title = v

    @property
    def text(self):
        return self.body.text

    @text.setter
    def text(self, v):
        self.body.text = v

    @property
    def icon(self):
        return self.body.icon

    @icon.setter
    def icon(self, v):
        self.body.icon = v

    @property
    def largeIcon(self):
        return self.body.largeIcon

    @largeIcon.setter
    def largeIcon(self, v):
        self.body.largeIcon = v

    @property
    def img(self):
        return self.body.img

    @img.setter
    def img(self, v):
        self.body.img = v

    @property
    def sound(self):
        return self.body.sound

    @sound.setter
    def sound(self, v):
        self.body.sound = v

    @property
    def builder_id(self):
        return self.body.builder_id

    @builder_id.setter
    def builder_id(self, v):
        self.body.builder_id = v

    @property
    def play_vibrate(self):
        return self.body.play_vibrate

    @play_vibrate.setter
    def play_vibrate(self, v):
        self.body.play_vibrate = v

    @property
    def play_sound(self):
        return self.body.play_sound

    @play_sound.setter
    def play_sound(self, v):
        self.body.play_sound = v

    @property
    def play_lights(self):
        return self.body.play_lights

    @play_lights.setter
    def play_lights(self, v):
        self.body.play_lights = v

    @property
    def after_open(self):
        return self.body.after_open

    @after_open.setter
    def after_open(self, v):
        self.body.after_open = v

    @property
    def url(self):
        return self.body.url

    @url.setter
    def url(self, v):
        self.body.url = v

    @property
    def activity(self):
        return self.body.activity

    @activity.setter
    def activity(self, v):
        self.body.activity = v

    @property
    def custom(self):
        return self.body.custom

    @custom.setter
    def custom(self, v):
        self.body.custom = v

    @property
    def extra(self):
        return self.payload.extra

    @extra.setter
    def extra(self, v):
        self.payload.extra = v


class IosNotification(Notification, PushClientMixin):

    def __init__(self, app_key, master_secret, ptype):
        super(IosNotification, self).__init__(app_key, master_secret, ptype)
        self.payload = IosPayload()
        self.payload.aps = self.aps = IosAps()

    def to_json(self):
        aps = {k: getattr(self.aps, k) for k in self.aps.__slots__
               if getattr(self.aps, k, None) is not None}
        policy = {k: getattr(self.policy, k) for k in self.policy.__slots__
                  if getattr(self.policy, k, None) is not None}
        payload = {k: getattr(self.payload, k) for k in self.payload.__slots__
                   if getattr(self.payload, k, None) is not None}
        data = {k: getattr(self, k) for k in self.__slots__
                if getattr(self, k, None) is not None}

        del data['master_screte']
        del data['payload']
        del data['policy']

        if 'content_available' in aps:
            aps['content-available'] = aps.pop('content_available')

        data['payload'] = payload
        data['payload']['aps'] = aps
        data['timestamp'] = int(time.time() * 1000)

        if policy:
            if 'apns_collapse_id' in policy:
                policy['apns-collapse-id'] = policy.pop('apns_collapse_id')
            data['policy'] = policy

        return data

    @property
    def apns_collapse_id(self):
        return self.policy.apns_collapse_id

    @apns_collapse_id.setter
    def apns_collapse_id(self, v):
        self.policy.apns_collapse_id = v

    @property
    def jumpkey(self):
        return self.payload.jumpkey

    @jumpkey.setter
    def jumpkey(self, v):
        self.payload.jumpkey = v

    @property
    def extra(self):
        return self.payload.extra

    @extra.setter
    def extra(self, v):
        self.payload.extra = v

    @property
    def alert(self):
        return self.aps.alert

    @alert.setter
    def alert(self, v):
        self.aps.alert = v

    @property
    def badge(self):
        return self.aps.badge

    @badge.setter
    def badge(self, v):
        self.aps.badge = v

    @property
    def sound(self):
        return self.aps.sound

    @sound.setter
    def sound(self, v):
        self.aps.sound = v

    @property
    def content_available(self):
        return self.aps.content_available

    @content_available.setter
    def content_available(self, v):
        self.aps.content_available = v

    @property
    def category(self):
        return self.aps.category

    @category.setter
    def category(self, v):
        self.aps.category = v

"""
安卓参数说明
{
    "appkey":"xx",        // 必填，应用唯一标识
    "timestamp":"xx",    // 必填，时间戳，10位或者13位均可，时间戳有效期为10分钟
    "type":"xx",        // 必填，消息发送类型,其值可以为: 
                        //   unicast-单播
                        //   listcast-列播，要求不超过500个device_token
                        //   filecast-文件播，多个device_token可通过文件形式批量发送
                        //   broadcast-广播
                        //   groupcast-组播，按照filter筛选用户群, 请参照filter参数
                        //   customizedcast，通过alias进行推送，包括以下两种case:
                        //     - alias: 对单个或者多个alias进行推送
                        //     - file_id: 将alias存放到文件后，根据file_id来推送
    "device_tokens":"xx",    // 当type=unicast时, 必填, 表示指定的单个设备
                            // 当type=listcast时, 必填, 要求不超过500个, 以英文逗号分隔
    "alias_type": "xx",    // 当type=customizedcast时, 必填
                        // alias的类型, alias_type可由开发者自定义, 开发者在SDK中
                        // 调用setAlias(alias, alias_type)时所设置的alias_type
    "alias":"xx",        // 当type=customizedcast时, 选填(此参数和file_id二选一)
                        // 开发者填写自己的alias, 要求不超过500个alias, 多个alias以英文逗号间隔
                        // 在SDK中调用setAlias(alias, alias_type)时所设置的alias
    "file_id":"xx",    // 当type=filecast时，必填，file内容为多条device_token，以回车符分割
                    // 当type=customizedcast时，选填(此参数和alias二选一)
                    //   file内容为多条alias，以回车符分隔。注意同一个文件内的alias所对应
                    //   的alias_type必须和接口参数alias_type一致。
                    // 使用文件播需要先调用文件上传接口获取file_id，参照"文件上传"
    "filter":{},    // 当type=groupcast时，必填，用户筛选条件，如用户标签、渠道等，参考附录G。
    "payload": {    // 必填，JSON格式，具体消息内容(Android最大为1840B)
        "display_type":"xx",    // 必填，消息类型: notification(通知)、message(消息)
        "body": {    // 必填，消息体。
                // 当display_type=message时，body的内容只需填写custom字段。
                // 当display_type=notification时，body包含如下参数:
            // 通知展现内容:
            "ticker":"xx",    // 必填，通知栏提示文字
            "title":"xx",    // 必填，通知标题
            "text":"xx",    // 必填，通知文字描述 

            // 自定义通知图标:
            "icon":"xx",    // 可选，状态栏图标ID，R.drawable.[smallIcon]，
            // 如果没有，默认使用应用图标。
            // 图片要求为24*24dp的图标，或24*24px放在drawable-mdpi下。
            // 注意四周各留1个dp的空白像素
            "largeIcon":"xx",    // 可选，通知栏拉开后左侧图标ID，R.drawable.[largeIcon]，
            // 图片要求为64*64dp的图标，
            // 可设计一张64*64px放在drawable-mdpi下，
            // 注意图片四周留空，不至于显示太拥挤
            "img": "xx",    // 可选，通知栏大图标的URL链接。该字段的优先级大于largeIcon。
                            // 该字段要求以http或者https开头。

            // 自定义通知声音:
            "sound": "xx",    // 可选，通知声音，R.raw.[sound]。
                            // 如果该字段为空，采用SDK默认的声音，即res/raw/下的
                            // umeng_push_notification_default_sound声音文件。如果
                            // SDK默认声音文件不存在，则使用系统默认Notification提示音。

            // 自定义通知样式:
            "builder_id": xx,    // 可选，默认为0，用于标识该通知采用的样式。使用该参数时，
                                // 开发者必须在SDK里面实现自定义通知栏样式。

            // 通知到达设备后的提醒方式，注意，"true/false"为字符串
            "play_vibrate":"true/false",    // 可选，收到通知是否震动，默认为"true"
            "play_lights":"true/false",        // 可选，收到通知是否闪灯，默认为"true"
            "play_sound":"true/false",        // 可选，收到通知是否发出声音，默认为"true"

            // 点击"通知"的后续行为，默认为打开app。
            "after_open": "xx",    // 可选，默认为"go_app"，值可以为:
                                //   "go_app": 打开应用
                                //   "go_url": 跳转到URL
                                //   "go_activity": 打开特定的activity
                                //   "go_custom": 用户自定义内容。
            "url": "xx",    // 当after_open=go_url时，必填。
                            // 通知栏点击后跳转的URL，要求以http或者https开头
            "activity":"xx",    // 当after_open=go_activity时，必填。
                                // 通知栏点击后打开的Activity
            "custom":"xx"/{}    // 当display_type=message时, 必填
                                // 当display_type=notification且
                                // after_open=go_custom时，必填
                                // 用户自定义内容，可以为字符串或者JSON格式。
        },
        extra:{    // 可选，JSON格式，用户自定义key-value。只对"通知"
                // (display_type=notification)生效。
                // 可以配合通知到达后，打开App/URL/Activity使用。
            "key1": "value1",
            "key2": "value2",
            ...
        }
    },
    "policy":{    // 可选，发送策略
        "start_time":"xx",    // 可选，定时发送时，若不填写表示立即发送。
                            // 定时发送时间不能小于当前时间
                            // 格式: "yyyy-MM-dd HH:mm:ss"。 
                            // 注意，start_time只对任务类消息生效。
        "expire_time":"xx",    // 可选，消息过期时间，其值不可小于发送时间或者
                            // start_time(如果填写了的话)，
                            // 如果不填写此参数，默认为3天后过期。格式同start_time
        "max_send_num": xx,    // 可选，发送限速，每秒发送的最大条数。最小值1000
                            // 开发者发送的消息如果有请求自己服务器的资源，可以考虑此参数。
        "out_biz_no": "xx"    // 可选，开发者对消息的唯一标识，服务器会根据这个标识避免重复发送。
                            // 有些情况下（例如网络异常）开发者可能会重复调用API导致
                            // 消息多次下发到客户端。如果需要处理这种情况，可以考虑此参数。
                            // 注意, out_biz_no只对任务类消息生效。
    },
    "production_mode":"true/false",    // 可选，正式/测试模式。默认为true
                                    // 测试模式只会将消息发给测试设备。测试设备需要到web上添加。
                                    // Android: 测试设备属于正式设备的一个子集。
    "description": "xx",    // 可选，发送消息描述，建议填写。  
    "mipush": "true/false",    // 可选，默认为false。当为true时，表示MIUI、EMUI、Flyme系统设备离线转为系统下发
    "mi_activity": "xx",    // 可选，mipush值为true时生效，表示走系统通道时打开指定页面acitivity的完整包路径。
}
"""

"""
iOS参数说明
{
  "appkey":"xx",    // 必填，应用唯一标识
  "timestamp":"xx", // 必填，时间戳，10位或者13位均可，时间戳有效期为10分钟
  "type":"xx",      // 必填，消息发送类型,其值可以为: 
                    //   unicast-单播
                    //   listcast-列播，要求不超过500个device_token
                    //   filecast-文件播，多个device_token可通过文件形式批量发送
                    //   broadcast-广播
                    //   groupcast-组播，按照filter筛选用户群, 请参照filter参数
                    //   customizedcast，通过alias进行推送，包括以下两种case:
                    //     - alias: 对单个或者多个alias进行推送
                    //     - file_id: 将alias存放到文件后，根据file_id来推送
  "device_tokens":"xx", // 当type=unicast时, 必填, 表示指定的单个设备
                        // 当type=listcast时, 必填, 要求不超过500个, 以英文逗号分隔
  "alias_type": "xx", // 当type=customizedcast时, 必填
                      // alias的类型, alias_type可由开发者自定义, 开发者在SDK中
                      // 调用setAlias(alias, alias_type)时所设置的alias_type
  "alias":"xx", // 当type=customizedcast时, 选填(此参数和file_id二选一)
                // 开发者填写自己的alias, 要求不超过500个alias, 多个alias以英文逗号间隔
                // 在SDK中调用setAlias(alias, alias_type)时所设置的alias
  "file_id":"xx", // 当type=filecast时，必填，file内容为多条device_token，以回车符分割
                  // 当type=customizedcast时，选填(此参数和alias二选一)
                  //   file内容为多条alias，以回车符分隔。注意同一个文件内的alias所对应
                  //   的alias_type必须和接口参数alias_type一致。
                  // 使用文件播需要先调用文件上传接口获取file_id，参照"2.4文件上传接口"
  "filter":{}, // 当type=groupcast时，必填，用户筛选条件，如用户标签、渠道等，参考附录G。
  "payload":   // 必填，JSON格式，具体消息内容(iOS最大为2012B)
  {
    "aps":      // 必填，严格按照APNs定义来填写
    {
        "alert":""/{ // 当content-available=1时(静默推送)，可选; 否则必填。
                     // 可为JSON类型和字符串类型
            "title":"title",
            "subtitle":"subtitle",
            "body":"body"
        }                   
        "badge": xx,           // 可选        
        "sound": "xx",         // 可选         
        "content-available":1  // 可选，代表静默推送     
        "category": "xx",      // 可选，注意: ios8才支持该字段。
    },
    "key1":"value1",       // 可选，用户自定义内容, "d","p"为友盟保留字段，
                           // key不可以是"d","p"
    "key2":"value2",       
    ...
  },
  "policy":               // 可选，发送策略
  {
      "start_time":"xx",   // 可选，定时发送时间，若不填写表示立即发送。
                           // 定时发送时间不能小于当前时间
                           // 格式: "yyyy-MM-dd HH:mm:ss"。 
                           // 注意，start_time只对任务生效。
      "expire_time":"xx",  // 可选，消息过期时间，其值不可小于发送时间或者
                           // start_time(如果填写了的话), 
                           // 如果不填写此参数，默认为3天后过期。格式同start_time
      "out_biz_no": "xx"   // 可选，开发者对消息的唯一标识，服务器会根据这个标识避免重复发送。
                           // 有些情况下（例如网络异常）开发者可能会重复调用API导致
                           // 消息多次下发到客户端。如果需要处理这种情况，可以考虑此参数。
                           // 注意，out_biz_no只对任务生效。
      "apns_collapse_id": "xx" // 可选，多条带有相同apns_collapse_id的消息，iOS设备仅展示
                               // 最新的一条，字段长度不得超过64bytes
  },
  "production_mode":"true/false" // 可选，正式/测试模式。默认为true
                                 // 测试模式只会将消息发给测试设备。测试设备需要到web上添加。
  "description": "xx"      // 可选，发送消息描述，建议填写。     
}"""