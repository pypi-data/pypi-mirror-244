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
import multiprocessing
import os
import json
from browserstack_sdk.bstack111l1l11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111111_opy_
class bstack1ll11ll111_opy_:
    def __init__(self, args, logger, bstack1l111l1l1l_opy_, bstack1l111llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111l1l1l_opy_ = bstack1l111l1l1l_opy_
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll1ll1l_opy_ = []
        self.bstack1l111ll1l1_opy_ = None
        self.bstack1l1l1l11l_opy_ = []
        self.bstack1l111l1lll_opy_ = self.bstack1ll11111ll_opy_()
        self.bstack11ll11l1_opy_ = -1
    def bstack1l11l1l11_opy_(self, bstack1l111l1ll1_opy_):
        self.parse_args()
        self.bstack1l11l1111l_opy_()
        self.bstack1l111ll111_opy_(bstack1l111l1ll1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l111ll11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11ll11l1_opy_ = -1
        if bstack1lll11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඦ") in self.bstack1l111l1l1l_opy_:
            self.bstack11ll11l1_opy_ = int(self.bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩට")])
        try:
            bstack1l11l111l1_opy_ = [bstack1lll11l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬඨ"), bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧඩ"), bstack1lll11l_opy_ (u"ࠬ࠳ࡰࠨඪ")]
            if self.bstack11ll11l1_opy_ >= 0:
                bstack1l11l111l1_opy_.extend([bstack1lll11l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧණ"), bstack1lll11l_opy_ (u"ࠧ࠮ࡰࠪඬ")])
            for arg in bstack1l11l111l1_opy_:
                self.bstack1l111ll11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l11l1111l_opy_(self):
        bstack1l111ll1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l111ll1l1_opy_ = bstack1l111ll1l1_opy_
        return bstack1l111ll1l1_opy_
    def bstack1llll1l1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l11l11111_opy_ = importlib.find_loader(bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪත"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l111111_opy_)
    def bstack1l111ll111_opy_(self, bstack1l111l1ll1_opy_):
        bstack11ll1l11l_opy_ = Config.get_instance()
        if bstack1l111l1ll1_opy_:
            self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ථ"))
            self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠪࡘࡷࡻࡥࠨද"))
        if bstack11ll1l11l_opy_.bstack1l111lll1l_opy_():
            self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪධ"))
            self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"࡚ࠬࡲࡶࡧࠪන"))
        self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"࠭࠭ࡱࠩ඲"))
        self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬඳ"))
        self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪප"))
        self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩඵ"))
        if self.bstack11ll11l1_opy_ > 1:
            self.bstack1l111ll1l1_opy_.append(bstack1lll11l_opy_ (u"ࠪ࠱ࡳ࠭බ"))
            self.bstack1l111ll1l1_opy_.append(str(self.bstack11ll11l1_opy_))
    def bstack1l111lll11_opy_(self):
        bstack1l1l1l11l_opy_ = []
        for spec in self.bstack1lll1ll1l_opy_:
            bstack11ll1l11_opy_ = [spec]
            bstack11ll1l11_opy_ += self.bstack1l111ll1l1_opy_
            bstack1l1l1l11l_opy_.append(bstack11ll1l11_opy_)
        self.bstack1l1l1l11l_opy_ = bstack1l1l1l11l_opy_
        return bstack1l1l1l11l_opy_
    def bstack1ll11111ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l111l1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack1l111l1lll_opy_ = False
        return self.bstack1l111l1lll_opy_
    def bstack11ll11ll1_opy_(self, bstack1l111ll1ll_opy_, bstack1l11l1l11_opy_):
        bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫභ")] = self.bstack1l111l1l1l_opy_
        multiprocessing.set_start_method(bstack1lll11l_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫම"))
        if bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඹ") in self.bstack1l111l1l1l_opy_:
            bstack1lll1lll_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll1lllll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪය")]):
                bstack1lll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l111ll1ll_opy_,
                                                           args=(self.bstack1l111ll1l1_opy_, bstack1l11l1l11_opy_, bstack1lll1lllll_opy_)))
            i = 0
            bstack1l111lllll_opy_ = len(self.bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫර")])
            for t in bstack1lll1lll_opy_:
                os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ඼")] = str(i)
                os.environ[bstack1lll11l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫල")] = json.dumps(self.bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ඾")][i % bstack1l111lllll_opy_])
                i += 1
                t.start()
            for t in bstack1lll1lll_opy_:
                t.join()
            return list(bstack1lll1lllll_opy_)