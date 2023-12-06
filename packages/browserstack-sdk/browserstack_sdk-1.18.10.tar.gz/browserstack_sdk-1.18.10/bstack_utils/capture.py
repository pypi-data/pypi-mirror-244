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
import sys
class bstack1l1l111lll_opy_:
    def __init__(self, handler):
        self._11l1llll1l_opy_ = sys.stdout.write
        self._11ll111111_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1llllll_opy_
        sys.stdout.error = self.bstack11l1lllll1_opy_
    def bstack11l1llllll_opy_(self, _str):
        self._11l1llll1l_opy_(_str)
        if self.handler:
            self.handler({bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮຺ࠪ"): bstack1lll11l_opy_ (u"ࠬࡏࡎࡇࡑࠪົ"), bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"): _str})
    def bstack11l1lllll1_opy_(self, _str):
        self._11ll111111_opy_(_str)
        if self.handler:
            self.handler({bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຽ"): bstack1lll11l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ຾"), bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ຿"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1llll1l_opy_
        sys.stderr.write = self._11ll111111_opy_