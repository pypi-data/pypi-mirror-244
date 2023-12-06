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