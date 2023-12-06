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
class RobotHandler():
    def __init__(self, args, logger, bstack1l111l1l1l_opy_, bstack1l111llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111l1l1l_opy_ = bstack1l111l1l1l_opy_
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1l1l1l11_opy_(bstack1l111l11ll_opy_):
        bstack1l111l11l1_opy_ = []
        if bstack1l111l11ll_opy_:
            tokens = str(os.path.basename(bstack1l111l11ll_opy_)).split(bstack1lll11l_opy_ (u"ࠧࡥࠢ඿"))
            camelcase_name = bstack1lll11l_opy_ (u"ࠨࠠࠣව").join(t.title() for t in tokens)
            suite_name, bstack1l111l111l_opy_ = os.path.splitext(camelcase_name)
            bstack1l111l11l1_opy_.append(suite_name)
        return bstack1l111l11l1_opy_
    @staticmethod
    def bstack1l111l1l11_opy_(typename):
        if bstack1lll11l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥශ") in typename:
            return bstack1lll11l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤෂ")
        return bstack1lll11l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥස")