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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1ll1l1l_opy_, bstack1l11llll_opy_, bstack1l1111111_opy_, bstack1l1llll1l_opy_, \
    bstack11l11ll11l_opy_
def bstack1llllll1ll_opy_(bstack111l11l1l1_opy_):
    for driver in bstack111l11l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11llll1l1_opy_(driver, status, reason=bstack1lll11l_opy_ (u"ࠬ࠭፯")):
    bstack11ll1l11l_opy_ = Config.get_instance()
    if bstack11ll1l11l_opy_.bstack1l111lll1l_opy_():
        return
    bstack1l1lll111_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ፰"), bstack1lll11l_opy_ (u"ࠧࠨ፱"), status, reason, bstack1lll11l_opy_ (u"ࠨࠩ፲"), bstack1lll11l_opy_ (u"ࠩࠪ፳"))
    driver.execute_script(bstack1l1lll111_opy_)
def bstack11ll11lll_opy_(page, status, reason=bstack1lll11l_opy_ (u"ࠪࠫ፴")):
    try:
        if page is None:
            return
        bstack11ll1l11l_opy_ = Config.get_instance()
        if bstack11ll1l11l_opy_.bstack1l111lll1l_opy_():
            return
        bstack1l1lll111_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ፵"), bstack1lll11l_opy_ (u"ࠬ࠭፶"), status, reason, bstack1lll11l_opy_ (u"࠭ࠧ፷"), bstack1lll11l_opy_ (u"ࠧࠨ፸"))
        page.evaluate(bstack1lll11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ፹"), bstack1l1lll111_opy_)
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ፺"), e)
def bstack1l11lll11_opy_(type, name, status, reason, bstack1l1l11111_opy_, bstack1lll1l111l_opy_):
    bstack1l111111_opy_ = {
        bstack1lll11l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ፻"): type,
        bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ፼"): {}
    }
    if type == bstack1lll11l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ፽"):
        bstack1l111111_opy_[bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ፾")][bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭፿")] = bstack1l1l11111_opy_
        bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᎀ")][bstack1lll11l_opy_ (u"ࠩࡧࡥࡹࡧࠧᎁ")] = json.dumps(str(bstack1lll1l111l_opy_))
    if type == bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᎂ"):
        bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᎃ")][bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᎄ")] = name
    if type == bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᎅ"):
        bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᎆ")][bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᎇ")] = status
        if status == bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᎈ") and str(reason) != bstack1lll11l_opy_ (u"ࠥࠦᎉ"):
            bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᎊ")][bstack1lll11l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᎋ")] = json.dumps(str(reason))
    bstack1lllllll1_opy_ = bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᎌ").format(json.dumps(bstack1l111111_opy_))
    return bstack1lllllll1_opy_
def bstack111l1ll1_opy_(url, config, logger, bstack1lll1llll_opy_=False):
    hostname = bstack1l11llll_opy_(url)
    is_private = bstack1l1llll1l_opy_(hostname)
    try:
        if is_private or bstack1lll1llll_opy_:
            file_path = bstack11l1ll1l1l_opy_(bstack1lll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᎍ"), bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᎎ"), logger)
            if os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᎏ")) and eval(
                    os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ᎐"))):
                return
            if (bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᎑") in config and not config[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ᎒")]):
                os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ᎓")] = str(True)
                bstack111l111lll_opy_ = {bstack1lll11l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ᎔"): hostname}
                bstack11l11ll11l_opy_(bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ᎕"), bstack1lll11l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ᎖"), bstack111l111lll_opy_, logger)
    except Exception as e:
        pass
def bstack111l111ll_opy_(caps, bstack111l11l11l_opy_):
    if bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᎗") in caps:
        caps[bstack1lll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᎘")][bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ᎙")] = True
        if bstack111l11l11l_opy_:
            caps[bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᎚")][bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᎛")] = bstack111l11l11l_opy_
    else:
        caps[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭᎜")] = True
        if bstack111l11l11l_opy_:
            caps[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᎝")] = bstack111l11l11l_opy_
def bstack111ll11lll_opy_(bstack1l11ll11ll_opy_):
    bstack111l11l111_opy_ = bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ᎞"), bstack1lll11l_opy_ (u"ࠫࠬ᎟"))
    if bstack111l11l111_opy_ == bstack1lll11l_opy_ (u"ࠬ࠭Ꭰ") or bstack111l11l111_opy_ == bstack1lll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᎡ"):
        threading.current_thread().testStatus = bstack1l11ll11ll_opy_
    else:
        if bstack1l11ll11ll_opy_ == bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᎢ"):
            threading.current_thread().testStatus = bstack1l11ll11ll_opy_