# coding: UTF-8
import sys
bstack111l11_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack1lll11l_opy_ (bstack1l11l11_opy_):
    global bstack1l11111_opy_
    bstack1ll111_opy_ = ord (bstack1l11l11_opy_ [-1])
    bstack11l_opy_ = bstack1l11l11_opy_ [:-1]
    bstack1l11ll1_opy_ = bstack1ll111_opy_ % len (bstack11l_opy_)
    bstack11lll_opy_ = bstack11l_opy_ [:bstack1l11ll1_opy_] + bstack11l_opy_ [bstack1l11ll1_opy_:]
    if bstack111l11_opy_:
        bstack111ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack11lllll_opy_ + bstack1ll111_opy_) % bstack1ll1l1_opy_) for bstack11lllll_opy_, char in enumerate (bstack11lll_opy_)])
    else:
        bstack111ll1_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack11lllll_opy_ + bstack1ll111_opy_) % bstack1ll1l1_opy_) for bstack11lllll_opy_, char in enumerate (bstack11lll_opy_)])
    return eval (bstack111ll1_opy_)
class bstack1ll1l1ll1l_opy_:
    def __init__(self, handler):
        self._111l11l1ll_opy_ = None
        self.handler = handler
        self._111l11ll11_opy_ = self.bstack111l11lll1_opy_()
        self.patch()
    def patch(self):
        self._111l11l1ll_opy_ = self._111l11ll11_opy_.execute
        self._111l11ll11_opy_.execute = self.bstack111l11ll1l_opy_()
    def bstack111l11ll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._111l11l1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11ll11_opy_.execute = self._111l11l1ll_opy_
    @staticmethod
    def bstack111l11lll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver