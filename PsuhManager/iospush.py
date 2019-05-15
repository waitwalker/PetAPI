# -*- coding: utf-8 -*-
from .notification import IosNotification


class IosPush(IosNotification):

    def __init__(self, app_key, master_secret):
        super(IosPush, self).__init__(app_key, master_secret, "customizedcast")
        self.alias_type = "user_id"

    @property
    def user_id(self):
        return self.alias

    @user_id.setter
    def user_id(self, user_id):
        self.set_alias(user_id)
