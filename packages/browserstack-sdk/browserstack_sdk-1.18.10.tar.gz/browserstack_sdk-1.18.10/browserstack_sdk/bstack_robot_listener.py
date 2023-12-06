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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l1l1l1l1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1l111lll_opy_
from bstack_utils.bstack1l1l1l1ll1_opy_ import bstack1l11lllll1_opy_, bstack1l1l11llll_opy_, bstack1l11l1l111_opy_
from bstack_utils.bstack1l1l11lll_opy_ import bstack1l1llll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1111111_opy_, bstack11l111ll1_opy_, Result, \
    bstack1l11l11l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ೮"): [],
        bstack1lll11l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭೯"): [],
        bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ೰"): []
    }
    bstack1l11l1l11l_opy_ = []
    @staticmethod
    def bstack1l11ll1111_opy_(log):
        if not (log[bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪೱ")] and log[bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫೲ")].strip()):
            return
        active = bstack1l1llll1ll_opy_.bstack1l11ll1l11_opy_()
        log = {
            bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪೳ"): log[bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ೴")],
            bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ೵"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"࡛ࠧࠩ೶"),
            bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ೷"): log[bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ೸")],
        }
        if active:
            if active[bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨ೹")] == bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ೺"):
                log[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ೻")] = active[bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭೼")]
            elif active[bstack1lll11l_opy_ (u"ࠧࡵࡻࡳࡩࠬ೽")] == bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭೾"):
                log[bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ೿")] = active[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪഀ")]
        bstack1l1llll1ll_opy_.bstack1l11l1l1l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l11lll11l_opy_ = None
        self._1l11ll11l1_opy_ = None
        self._1l1l1ll11l_opy_ = OrderedDict()
        self.bstack1l1l11111l_opy_ = bstack1l1l111lll_opy_(self.bstack1l11ll1111_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11llllll_opy_()
        if not self._1l1l1ll11l_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧഁ")), None):
            self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠬ࡯ࡤࠨം"))] = {}
        bstack1l11l11lll_opy_ = bstack1l11l1l111_opy_(
                bstack1l1l111l1l_opy_=attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩഃ")),
                name=name,
                bstack1l1l1ll1ll_opy_=bstack11l111ll1_opy_(),
                file_path=os.path.relpath(attrs[bstack1lll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧഄ")], start=os.getcwd()) if attrs.get(bstack1lll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨഅ")) != bstack1lll11l_opy_ (u"ࠩࠪആ") else bstack1lll11l_opy_ (u"ࠪࠫഇ"),
                framework=bstack1lll11l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪഈ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1lll11l_opy_ (u"ࠬ࡯ࡤࠨഉ"), None)
        self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩഊ"))][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪഋ")] = bstack1l11l11lll_opy_
    @bstack1l11l11l11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l1l111ll1_opy_()
        self._1l11ll1l1l_opy_(messages)
        for bstack1l1l11l11l_opy_ in self.bstack1l11l1l11l_opy_:
            bstack1l1l11l11l_opy_[bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪഌ")][bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ഍")].extend(self.store[bstack1lll11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩഎ")])
            bstack1l1llll1ll_opy_.bstack1l11lll1l1_opy_(bstack1l1l11l11l_opy_)
        self.bstack1l11l1l11l_opy_ = []
        self.store[bstack1lll11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪഏ")] = []
    @bstack1l11l11l11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l1l11111l_opy_.start()
        if not self._1l1l1ll11l_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠬ࡯ࡤࠨഐ")), None):
            self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩ഑"))] = {}
        driver = bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ഒ"), None)
        bstack1l1l1l1ll1_opy_ = bstack1l11l1l111_opy_(
            bstack1l1l111l1l_opy_=attrs.get(bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫഓ")),
            name=name,
            bstack1l1l1ll1ll_opy_=bstack11l111ll1_opy_(),
            file_path=os.path.relpath(attrs[bstack1lll11l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഔ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1l1l1l11_opy_(attrs.get(bstack1lll11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪക"), None)),
            framework=bstack1lll11l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪഖ"),
            tags=attrs[bstack1lll11l_opy_ (u"ࠬࡺࡡࡨࡵࠪഗ")],
            hooks=self.store[bstack1lll11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬഘ")],
            bstack1l11l11l1l_opy_=bstack1l1llll1ll_opy_.bstack1l11ll111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1lll11l_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤങ").format(bstack1lll11l_opy_ (u"ࠣࠢࠥച").join(attrs[bstack1lll11l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧഛ")]), name) if attrs[bstack1lll11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨജ")] else name
        )
        self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧഝ"))][bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨഞ")] = bstack1l1l1l1ll1_opy_
        threading.current_thread().current_test_uuid = bstack1l1l1l1ll1_opy_.bstack1l1l1ll111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩട"), None)
        self.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨഠ"), bstack1l1l1l1ll1_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l1l11111l_opy_.reset()
        bstack1l11ll11ll_opy_ = bstack1l1l1111l1_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨഡ")), bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪഢ"))
        self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠪ࡭ࡩ࠭ണ"))][bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧത")].stop(time=bstack11l111ll1_opy_(), duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪഥ"), bstack1lll11l_opy_ (u"࠭࠰ࠨദ"))), result=Result(result=bstack1l11ll11ll_opy_, exception=attrs.get(bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨധ")), bstack1l11lll1ll_opy_=[attrs.get(bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩന"))]))
        self.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫഩ"), self._1l1l1ll11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠪ࡭ࡩ࠭പ"))][bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧഫ")], True)
        self.store[bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩബ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11l11l11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11llllll_opy_()
        current_test_id = bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨഭ"), None)
        bstack1l11lll111_opy_ = current_test_id if bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩമ"), None) else bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫയ"), None)
        if attrs.get(bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧര"), bstack1lll11l_opy_ (u"ࠪࠫറ")).lower() in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪല"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧള")]:
            hook_type = bstack1l11llll1l_opy_(attrs.get(bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫഴ")), bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫവ"), None))
            bstack1l11l1lll1_opy_ = bstack1l1l11llll_opy_(
                bstack1l1l111l1l_opy_=bstack1l11lll111_opy_ + bstack1lll11l_opy_ (u"ࠨ࠯ࠪശ") + attrs.get(bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧഷ"), bstack1lll11l_opy_ (u"ࠪࠫസ")).lower(),
                name=bstack1lll11l_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬഹ").format(hook_type, attrs.get(bstack1lll11l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬഺ"), bstack1lll11l_opy_ (u"഻࠭ࠧ"))) if hook_type in [bstack1lll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏ഼ࠫ"), bstack1lll11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫഽ")] else bstack1lll11l_opy_ (u"ࠩࡾࢁࠬാ").format(attrs.get(bstack1lll11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪി"), bstack1lll11l_opy_ (u"ࠫࠬീ"))),
                bstack1l1l1ll1ll_opy_=bstack11l111ll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1lll11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬു")), start=os.getcwd()),
                framework=bstack1lll11l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬൂ"),
                tags=attrs[bstack1lll11l_opy_ (u"ࠧࡵࡣࡪࡷࠬൃ")],
                scope=RobotHandler.bstack1l1l1l1l11_opy_(attrs.get(bstack1lll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨൄ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11l1lll1_opy_.bstack1l1l1ll111_opy_()
            threading.current_thread().current_hook_id = bstack1l11lll111_opy_ + bstack1lll11l_opy_ (u"ࠩ࠰ࠫ൅") + attrs.get(bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨെ"), bstack1lll11l_opy_ (u"ࠫࠬേ")).lower()
            self.store[bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩൈ")] = [bstack1l11l1lll1_opy_.bstack1l1l1ll111_opy_()]
            if bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ൉"), None):
                self.store[bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫൊ")].append(bstack1l11l1lll1_opy_.bstack1l1l1ll111_opy_())
            else:
                self.store[bstack1lll11l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧോ")].append(bstack1l11l1lll1_opy_.bstack1l1l1ll111_opy_())
            if bstack1l11lll111_opy_:
                self._1l1l1ll11l_opy_[bstack1l11lll111_opy_ + bstack1lll11l_opy_ (u"ࠩ࠰ࠫൌ") + attrs.get(bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨ്"), bstack1lll11l_opy_ (u"ࠫࠬൎ")).lower()] = { bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ൏"): bstack1l11l1lll1_opy_ }
            bstack1l1llll1ll_opy_.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ൐"), bstack1l11l1lll1_opy_)
        else:
            bstack1l11l1ll1l_opy_ = {
                bstack1lll11l_opy_ (u"ࠧࡪࡦࠪ൑"): uuid4().__str__(),
                bstack1lll11l_opy_ (u"ࠨࡶࡨࡼࡹ࠭൒"): bstack1lll11l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ൓").format(attrs.get(bstack1lll11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪൔ")), attrs.get(bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩൕ"), bstack1lll11l_opy_ (u"ࠬ࠭ൖ"))) if attrs.get(bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫൗ"), []) else attrs.get(bstack1lll11l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ൘")),
                bstack1lll11l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ൙"): attrs.get(bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ൚"), []),
                bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ൛"): bstack11l111ll1_opy_(),
                bstack1lll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ൜"): bstack1lll11l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭൝"),
                bstack1lll11l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ൞"): attrs.get(bstack1lll11l_opy_ (u"ࠧࡥࡱࡦࠫൟ"), bstack1lll11l_opy_ (u"ࠨࠩൠ"))
            }
            if attrs.get(bstack1lll11l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪൡ"), bstack1lll11l_opy_ (u"ࠪࠫൢ")) != bstack1lll11l_opy_ (u"ࠫࠬൣ"):
                bstack1l11l1ll1l_opy_[bstack1lll11l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭൤")] = attrs.get(bstack1lll11l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ൥"))
            threading.current_thread().current_step_uuid = bstack1l11l1ll1l_opy_[bstack1lll11l_opy_ (u"ࠧࡪࡦࠪ൦")]
            self._1l1l1ll11l_opy_[self._1l1l1l11l1_opy_()][bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൧")].add_step(bstack1l11l1ll1l_opy_)
    @bstack1l11l11l11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l1l111ll1_opy_()
        self._1l11ll1l1l_opy_(messages)
        current_test_id = bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ൨"), None)
        bstack1l11lll111_opy_ = current_test_id if current_test_id else bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭൩"), None)
        bstack1l1l11lll1_opy_ = bstack1l1l1111l1_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ൪")), bstack1lll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭൫"))
        bstack1l1l1lll11_opy_ = attrs.get(bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ൬"))
        if bstack1l1l11lll1_opy_ != bstack1lll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ൭") and not attrs.get(bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ൮")) and self._1l11lll11l_opy_:
            bstack1l1l1lll11_opy_ = self._1l11lll11l_opy_
        bstack1l1l11ll11_opy_ = Result(result=bstack1l1l11lll1_opy_, exception=bstack1l1l1lll11_opy_, bstack1l11lll1ll_opy_=[bstack1l1l1lll11_opy_])
        if attrs.get(bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൯"), bstack1lll11l_opy_ (u"ࠪࠫ൰")).lower() in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ൱"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ൲")]:
            bstack1l11lll111_opy_ = current_test_id if current_test_id else bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ൳"), None)
            if bstack1l11lll111_opy_:
                bstack1l1l1l11ll_opy_ = bstack1l11lll111_opy_ + bstack1lll11l_opy_ (u"ࠢ࠮ࠤ൴") + attrs.get(bstack1lll11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭൵"), bstack1lll11l_opy_ (u"ࠩࠪ൶")).lower()
                self._1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭൷")].stop(time=bstack11l111ll1_opy_(), duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ൸"), bstack1lll11l_opy_ (u"ࠬ࠶ࠧ൹"))), result=bstack1l1l11ll11_opy_)
                bstack1l1llll1ll_opy_.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨൺ"), self._1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൻ")])
        else:
            bstack1l11lll111_opy_ = current_test_id if current_test_id else bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪർ"), None)
            if bstack1l11lll111_opy_:
                current_step_uuid = bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ൽ"), None)
                self._1l1l1ll11l_opy_[bstack1l11lll111_opy_][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ൾ")].bstack1l1l1111ll_opy_(current_step_uuid, duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩൿ"), bstack1lll11l_opy_ (u"ࠬ࠶ࠧ඀"))), result=bstack1l1l11ll11_opy_)
    def log_message(self, message):
        try:
            if message.get(bstack1lll11l_opy_ (u"࠭ࡨࡵ࡯࡯ࠫඁ"), bstack1lll11l_opy_ (u"ࠧ࡯ࡱࠪං")) == bstack1lll11l_opy_ (u"ࠨࡻࡨࡷࠬඃ"):
                return
            self.messages.push(message)
            bstack1l1l1l1lll_opy_ = []
            if bstack1l1llll1ll_opy_.bstack1l11ll1l11_opy_():
                bstack1l1l1l1lll_opy_.append({
                    bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ඄"): bstack11l111ll1_opy_(),
                    bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඅ"): message.get(bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬආ")),
                    bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫඇ"): message.get(bstack1lll11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬඈ")),
                    **bstack1l1llll1ll_opy_.bstack1l11ll1l11_opy_()
                })
                if len(bstack1l1l1l1lll_opy_) > 0:
                    bstack1l1llll1ll_opy_.bstack1l11l1l1l1_opy_(bstack1l1l1l1lll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l1llll1ll_opy_.bstack1l1l11ll1l_opy_()
    def _1l1l1l11l1_opy_(self):
        for bstack1l1l111l1l_opy_ in reversed(self._1l1l1ll11l_opy_):
            bstack1l1l1ll1l1_opy_ = bstack1l1l111l1l_opy_
            data = self._1l1l1ll11l_opy_[bstack1l1l111l1l_opy_][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඉ")]
            if isinstance(data, bstack1l1l11llll_opy_):
                if not bstack1lll11l_opy_ (u"ࠨࡇࡄࡇࡍ࠭ඊ") in data.bstack1l11l1ll11_opy_():
                    return bstack1l1l1ll1l1_opy_
            else:
                return bstack1l1l1ll1l1_opy_
    def _1l11ll1l1l_opy_(self, messages):
        try:
            bstack1l1l1l1111_opy_ = BuiltIn().get_variable_value(bstack1lll11l_opy_ (u"ࠤࠧࡿࡑࡕࡇࠡࡎࡈ࡚ࡊࡒࡽࠣඋ")) in (bstack1l11l1l1ll_opy_.DEBUG, bstack1l11l1l1ll_opy_.TRACE)
            for message, bstack1l1l11l1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඌ"))
                level = message.get(bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪඍ"))
                if level == bstack1l11l1l1ll_opy_.FAIL:
                    self._1l11lll11l_opy_ = name or self._1l11lll11l_opy_
                    self._1l11ll11l1_opy_ = bstack1l1l11l1ll_opy_.get(bstack1lll11l_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨඎ")) if bstack1l1l1l1111_opy_ and bstack1l1l11l1ll_opy_ else self._1l11ll11l1_opy_
        except:
            pass
    @classmethod
    def bstack1l1l11l1l1_opy_(self, event: str, bstack1l1l111l11_opy_: bstack1l11lllll1_opy_, bstack1l11llll11_opy_=False):
        if event == bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨඏ"):
            bstack1l1l111l11_opy_.set(hooks=self.store[bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫඐ")])
        if event == bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩඑ"):
            event = bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫඒ")
        if bstack1l11llll11_opy_:
            bstack1l1l111111_opy_ = {
                bstack1lll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧඓ"): event,
                bstack1l1l111l11_opy_.bstack1l1l11l111_opy_(): bstack1l1l111l11_opy_.bstack1l11ll1ll1_opy_(event)
            }
            self.bstack1l11l1l11l_opy_.append(bstack1l1l111111_opy_)
        else:
            bstack1l1llll1ll_opy_.bstack1l1l11l1l1_opy_(event, bstack1l1l111l11_opy_)
class Messages:
    def __init__(self):
        self._1l11ll1lll_opy_ = []
    def bstack1l11llllll_opy_(self):
        self._1l11ll1lll_opy_.append([])
    def bstack1l1l111ll1_opy_(self):
        return self._1l11ll1lll_opy_.pop() if self._1l11ll1lll_opy_ else list()
    def push(self, message):
        self._1l11ll1lll_opy_[-1].append(message) if self._1l11ll1lll_opy_ else self._1l11ll1lll_opy_.append([message])
class bstack1l11l1l1ll_opy_:
    FAIL = bstack1lll11l_opy_ (u"ࠫࡋࡇࡉࡍࠩඔ")
    ERROR = bstack1lll11l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫඕ")
    WARNING = bstack1lll11l_opy_ (u"࠭ࡗࡂࡔࡑࠫඖ")
    bstack1l11l111ll_opy_ = bstack1lll11l_opy_ (u"ࠧࡊࡐࡉࡓࠬ඗")
    DEBUG = bstack1lll11l_opy_ (u"ࠨࡆࡈࡆ࡚ࡍࠧ඘")
    TRACE = bstack1lll11l_opy_ (u"ࠩࡗࡖࡆࡉࡅࠨ඙")
    bstack1l1l1l111l_opy_ = [FAIL, ERROR]
def bstack1l11l1llll_opy_(bstack1l11l11ll1_opy_):
    if not bstack1l11l11ll1_opy_:
        return None
    if bstack1l11l11ll1_opy_.get(bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ක"), None):
        return getattr(bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧඛ")], bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪග"), None)
    return bstack1l11l11ll1_opy_.get(bstack1lll11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫඝ"), None)
def bstack1l11llll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ඞ"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪඟ")]:
        return
    if hook_type.lower() == bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨච"):
        if current_test_uuid is None:
            return bstack1lll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧඡ")
        else:
            return bstack1lll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩජ")
    elif hook_type.lower() == bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧඣ"):
        if current_test_uuid is None:
            return bstack1lll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩඤ")
        else:
            return bstack1lll11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫඥ")