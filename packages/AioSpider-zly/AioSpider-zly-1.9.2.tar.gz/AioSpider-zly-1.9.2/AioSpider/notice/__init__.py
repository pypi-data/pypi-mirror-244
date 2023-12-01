from .robot import WechatRobot, Robot


class Message():

    def __init__(self):
        self._wechat = WechatRobot()
    
    def add_platform_robot(self, name, spider, config):
        pass
    
    def add_wechat_robot(self, *args, **kwargs):
        self._wechat.add_robot(*args, **kwargs)
    
    def add_dingding_robot(self, name, spider, config):
        pass
    
    def add_email_robot(self, name, spider, config):
        pass

    def debug(self, msg, platform=False, wechat=False, dingding=False, email=False, to='system', *args, **kwargs):
        if wechat:
            self._wechat.debug(msg, to)

    def info(self, msg, platform=False, wechat=False, dingding=False, email=False, to='system', *args, **kwargs):
        if wechat:
            self._wechat.info(msg, to)

    def warning(self, msg, platform=False, wechat=False, dingding=False, email=False, to='system', *args, **kwargs):
        if wechat:
            self._wechat.warning(msg, to)

    def error(self, msg, platform=False, wechat=False, dingding=False, email=False, to='system', *args, **kwargs):
        if wechat:
            self._wechat.error(msg, to)

    def critical(self, msg, platform=False, wechat=False, dingding=False, email=False, to='system', *args, **kwargs):
        if wechat:
            self._wechat.critical(msg, to)
