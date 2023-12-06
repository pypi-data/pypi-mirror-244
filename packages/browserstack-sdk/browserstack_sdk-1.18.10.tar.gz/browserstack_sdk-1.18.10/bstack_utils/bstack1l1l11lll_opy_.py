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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll11llll_opy_, bstack11lll111l_opy_, get_host_info, bstack11ll111l1l_opy_, bstack11ll11ll1l_opy_, bstack11l11l1l1l_opy_, \
    bstack11l1111ll1_opy_, bstack11l1111lll_opy_, bstack1l1111l1_opy_, bstack11l1l11l1l_opy_, bstack1lll11ll1_opy_, bstack1l11l11l11_opy_
from bstack_utils.bstack111l1l1111_opy_ import bstack111l1l11l1_opy_
from bstack_utils.bstack1l1l1l1ll1_opy_ import bstack1l11lllll1_opy_
bstack1111ll1111_opy_ = [
    bstack1lll11l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᏡ"), bstack1lll11l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᏢ"), bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᏣ"), bstack1lll11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᏤ"),
    bstack1lll11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ꮵ"), bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ꮶ"), bstack1lll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᏧ")
]
bstack1111l11l1l_opy_ = bstack1lll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᏨ")
logger = logging.getLogger(__name__)
class bstack1l1llll1ll_opy_:
    bstack111l1l1111_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1111ll11l1_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1111l1ll11_opy_():
            return
        cls.bstack1111l1llll_opy_()
        bstack11ll1111ll_opy_ = bstack11ll111l1l_opy_(bs_config)
        bstack11ll111l11_opy_ = bstack11ll11ll1l_opy_(bs_config)
        data = {
            bstack1lll11l_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨᏩ"): bstack1lll11l_opy_ (u"ࠩ࡭ࡷࡴࡴࠧᏪ"),
            bstack1lll11l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩᏫ"): bs_config.get(bstack1lll11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᏬ"), bstack1lll11l_opy_ (u"ࠬ࠭Ꮽ")),
            bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᏮ"): bs_config.get(bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᏯ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᏰ"): bs_config.get(bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᏱ")),
            bstack1lll11l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᏲ"): bs_config.get(bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᏳ"), bstack1lll11l_opy_ (u"ࠬ࠭Ᏼ")),
            bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡤࡺࡩ࡮ࡧࠪᏵ"): datetime.datetime.now().isoformat(),
            bstack1lll11l_opy_ (u"ࠧࡵࡣࡪࡷࠬ᏶"): bstack11l11l1l1l_opy_(bs_config),
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ᏷"): get_host_info(),
            bstack1lll11l_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪᏸ"): bstack11lll111l_opy_(),
            bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᏹ"): os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᏺ")),
            bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪᏻ"): os.environ.get(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᏼ"), False),
            bstack1lll11l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩᏽ"): bstack11ll11llll_opy_(),
            bstack1lll11l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᏾"): {
                bstack1lll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ᏿"): bstack1111ll11l1_opy_.get(bstack1lll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ᐀"), bstack1lll11l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᐁ")),
                bstack1lll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᐂ"): bstack1111ll11l1_opy_.get(bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᐃ")),
                bstack1lll11l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᐄ"): bstack1111ll11l1_opy_.get(bstack1lll11l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᐅ"))
            }
        }
        config = {
            bstack1lll11l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᐆ"): (bstack11ll1111ll_opy_, bstack11ll111l11_opy_),
            bstack1lll11l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᐇ"): cls.default_headers()
        }
        response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠫࡕࡕࡓࡕࠩᐈ"), cls.request_url(bstack1lll11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷࠬᐉ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᐊ")] = bstack1lll11l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᐋ")
            os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᐌ")] = bstack1lll11l_opy_ (u"ࠩࡱࡹࡱࡲࠧᐍ")
            os.environ[bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᐎ")] = bstack1lll11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᐏ")
            os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᐐ")] = bstack1lll11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᐑ")
            bstack1111l1l111_opy_ = response.json()
            if bstack1111l1l111_opy_ and bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᐒ")]:
                error_message = bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᐓ")]
                if bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᐔ")] == bstack1lll11l_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡌࡒ࡛ࡇࡌࡊࡆࡢࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࠨᐕ"):
                    logger.error(error_message)
                elif bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᐖ")] == bstack1lll11l_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠫᐗ"):
                    logger.info(error_message)
                elif bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᐘ")] == bstack1lll11l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡓࡅࡍࡢࡈࡊࡖࡒࡆࡅࡄࡘࡊࡊࠧᐙ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lll11l_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᐚ"))
            return [None, None, None]
        logger.debug(bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᐛ"))
        os.environ[bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᐜ")] = bstack1lll11l_opy_ (u"ࠫࡹࡸࡵࡦࠩᐝ")
        bstack1111l1l111_opy_ = response.json()
        if bstack1111l1l111_opy_.get(bstack1lll11l_opy_ (u"ࠬࡰࡷࡵࠩᐞ")):
            os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᐟ")] = bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠧ࡫ࡹࡷࠫᐠ")]
            os.environ[bstack1lll11l_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᐡ")] = json.dumps({
                bstack1lll11l_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᐢ"): bstack11ll1111ll_opy_,
                bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᐣ"): bstack11ll111l11_opy_
            })
        if bstack1111l1l111_opy_.get(bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᐤ")):
            os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᐥ")] = bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᐦ")]
        if bstack1111l1l111_opy_.get(bstack1lll11l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᐧ")):
            os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᐨ")] = str(bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᐩ")])
        return [bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠪ࡮ࡼࡺࠧᐪ")], bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᐫ")], bstack1111l1l111_opy_[bstack1lll11l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᐬ")]]
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᐭ")] == bstack1lll11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᐮ") or os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᐯ")] == bstack1lll11l_opy_ (u"ࠤࡱࡹࡱࡲࠢᐰ"):
            print(bstack1lll11l_opy_ (u"ࠪࡉ࡝ࡉࡅࡑࡖࡌࡓࡓࠦࡉࡏࠢࡶࡸࡴࡶࡂࡶ࡫࡯ࡨ࡚ࡶࡳࡵࡴࡨࡥࡲࠦࡒࡆࡓࡘࡉࡘ࡚ࠠࡕࡑࠣࡘࡊ࡙ࡔࠡࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠡ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᐱ"))
            return {
                bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᐲ"): bstack1lll11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᐳ"),
                bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᐴ"): bstack1lll11l_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬᐵ")
            }
        else:
            cls.bstack111l1l1111_opy_.shutdown()
            data = {
                bstack1lll11l_opy_ (u"ࠨࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࠫᐶ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1lll11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᐷ"): cls.default_headers()
            }
            bstack11llll111l_opy_ = bstack1lll11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫᐸ").format(os.environ[bstack1lll11l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᐹ")])
            bstack1111l1lll1_opy_ = cls.request_url(bstack11llll111l_opy_)
            response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠬࡖࡕࡕࠩᐺ"), bstack1111l1lll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lll11l_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧᐻ"))
    @classmethod
    def bstack1l1l11ll1l_opy_(cls):
        if cls.bstack111l1l1111_opy_ is None:
            return
        cls.bstack111l1l1111_opy_.shutdown()
    @classmethod
    def bstack1l111l11_opy_(cls):
        if cls.on():
            print(
                bstack1lll11l_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪᐼ").format(os.environ[bstack1lll11l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᐽ")]))
    @classmethod
    def bstack1111l1llll_opy_(cls):
        if cls.bstack111l1l1111_opy_ is not None:
            return
        cls.bstack111l1l1111_opy_ = bstack111l1l11l1_opy_(cls.bstack1111l111ll_opy_)
        cls.bstack111l1l1111_opy_.start()
    @classmethod
    def bstack1l11lll1l1_opy_(cls, bstack1l1l111l11_opy_, bstack1111ll111l_opy_=bstack1lll11l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᐾ")):
        if not cls.on():
            return
        bstack11lllllll_opy_ = bstack1l1l111l11_opy_[bstack1lll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᐿ")]
        bstack1111l11111_opy_ = {
            bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᑀ"): bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᑁ"),
            bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑂ"): bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᑃ"),
            bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᑄ"): bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔ࡭࡬ࡴࡵ࡫ࡤࡠࡗࡳࡰࡴࡧࡤࠨᑅ"),
            bstack1lll11l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᑆ"): bstack1lll11l_opy_ (u"ࠫࡑࡵࡧࡠࡗࡳࡰࡴࡧࡤࠨᑇ"),
            bstack1lll11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᑈ"): bstack1lll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡘࡺࡡࡳࡶࡢ࡙ࡵࡲ࡯ࡢࡦࠪᑉ"),
            bstack1lll11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᑊ"): bstack1lll11l_opy_ (u"ࠨࡊࡲࡳࡰࡥࡅ࡯ࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᑋ"),
            bstack1lll11l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᑌ"): bstack1lll11l_opy_ (u"ࠪࡇࡇ࡚࡟ࡖࡲ࡯ࡳࡦࡪࠧᑍ")
        }.get(bstack11lllllll_opy_)
        if bstack1111ll111l_opy_ == bstack1lll11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᑎ"):
            cls.bstack1111l1llll_opy_()
            cls.bstack111l1l1111_opy_.add(bstack1l1l111l11_opy_)
        elif bstack1111ll111l_opy_ == bstack1lll11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᑏ"):
            cls.bstack1111l111ll_opy_([bstack1l1l111l11_opy_], bstack1111ll111l_opy_)
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1111l111ll_opy_(cls, bstack1l1l111l11_opy_, bstack1111ll111l_opy_=bstack1lll11l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᑐ")):
        config = {
            bstack1lll11l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᑑ"): cls.default_headers()
        }
        response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᑒ"), cls.request_url(bstack1111ll111l_opy_), bstack1l1l111l11_opy_, config)
        bstack11ll11111l_opy_ = response.json()
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1l11l1l1l1_opy_(cls, bstack1l1l1l1lll_opy_):
        bstack1111l11lll_opy_ = []
        for log in bstack1l1l1l1lll_opy_:
            bstack1111l11ll1_opy_ = {
                bstack1lll11l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᑓ"): bstack1lll11l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬᑔ"),
                bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᑕ"): log[bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᑖ")],
                bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᑗ"): log[bstack1lll11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᑘ")],
                bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨᑙ"): {},
                bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᑚ"): log[bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᑛ")],
            }
            if bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑜ") in log:
                bstack1111l11ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑝ")] = log[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑞ")]
            elif bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑟ") in log:
                bstack1111l11ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑠ")] = log[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑡ")]
            bstack1111l11lll_opy_.append(bstack1111l11ll1_opy_)
        cls.bstack1l11lll1l1_opy_({
            bstack1lll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᑢ"): bstack1lll11l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᑣ"),
            bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᑤ"): bstack1111l11lll_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1111l1ll1l_opy_(cls, steps):
        bstack1111l1111l_opy_ = []
        for step in steps:
            bstack1111ll11ll_opy_ = {
                bstack1lll11l_opy_ (u"࠭࡫ࡪࡰࡧࠫᑥ"): bstack1lll11l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪᑦ"),
                bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑧ"): step[bstack1lll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᑨ")],
                bstack1lll11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᑩ"): step[bstack1lll11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᑪ")],
                bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑫ"): step[bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑬ")],
                bstack1lll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᑭ"): step[bstack1lll11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᑮ")]
            }
            if bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑯ") in step:
                bstack1111ll11ll_opy_[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑰ")] = step[bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑱ")]
            elif bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑲ") in step:
                bstack1111ll11ll_opy_[bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑳ")] = step[bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑴ")]
            bstack1111l1111l_opy_.append(bstack1111ll11ll_opy_)
        cls.bstack1l11lll1l1_opy_({
            bstack1lll11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᑵ"): bstack1lll11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᑶ"),
            bstack1lll11l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᑷ"): bstack1111l1111l_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1l1lllll11_opy_(cls, screenshot):
        cls.bstack1l11lll1l1_opy_({
            bstack1lll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᑸ"): bstack1lll11l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᑹ"),
            bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࡶࠫᑺ"): [{
                bstack1lll11l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᑻ"): bstack1lll11l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪᑼ"),
                bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᑽ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬᑾ"),
                bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑿ"): screenshot[bstack1lll11l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᒀ")],
                bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᒁ"): screenshot[bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᒂ")]
            }]
        }, bstack1111ll111l_opy_=bstack1lll11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒃ"))
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack11l111l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11lll1l1_opy_({
            bstack1lll11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᒄ"): bstack1lll11l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᒅ"),
            bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᒆ"): {
                bstack1lll11l_opy_ (u"ࠧࡻࡵࡪࡦࠥᒇ"): cls.current_test_uuid(),
                bstack1lll11l_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧᒈ"): cls.bstack1l11ll111l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᒉ"), None) is None or os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᒊ")] == bstack1lll11l_opy_ (u"ࠤࡱࡹࡱࡲࠢᒋ"):
            return False
        return True
    @classmethod
    def bstack1111l1ll11_opy_(cls):
        return bstack1lll11ll1_opy_(cls.bs_config.get(bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᒌ"), False))
    @staticmethod
    def request_url(url):
        return bstack1lll11l_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᒍ").format(bstack1111l11l1l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1lll11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᒎ"): bstack1lll11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᒏ"),
            bstack1lll11l_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᒐ"): bstack1lll11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᒑ")
        }
        if os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᒒ"), None):
            headers[bstack1lll11l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᒓ")] = bstack1lll11l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᒔ").format(os.environ[bstack1lll11l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙ࠨᒕ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᒖ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᒗ"), None)
    @staticmethod
    def bstack1l11ll1l11_opy_():
        if getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᒘ"), None):
            return {
                bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᒙ"): bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࠨᒚ"),
                bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᒛ"): getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᒜ"), None)
            }
        if getattr(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᒝ"), None):
            return {
                bstack1lll11l_opy_ (u"ࠧࡵࡻࡳࡩࠬᒞ"): bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᒟ"),
                bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒠ"): getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᒡ"), None)
            }
        return None
    @staticmethod
    def bstack1l11ll111l_opy_(driver):
        return {
            bstack11l1111lll_opy_(): bstack11l1111ll1_opy_(driver)
        }
    @staticmethod
    def bstack1111l1l11l_opy_(exception_info, report):
        return [{bstack1lll11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᒢ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l111l1l11_opy_(typename):
        if bstack1lll11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᒣ") in typename:
            return bstack1lll11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᒤ")
        return bstack1lll11l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᒥ")
    @staticmethod
    def bstack1111l11l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1llll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1l1l1l11_opy_(test, hook_name=None):
        bstack1111l1l1ll_opy_ = test.parent
        if hook_name in [bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᒦ"), bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᒧ"), bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᒨ"), bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᒩ")]:
            bstack1111l1l1ll_opy_ = test
        scope = []
        while bstack1111l1l1ll_opy_ is not None:
            scope.append(bstack1111l1l1ll_opy_.name)
            bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l111l1_opy_(hook_type):
        if hook_type == bstack1lll11l_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥᒪ"):
            return bstack1lll11l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥᒫ")
        elif hook_type == bstack1lll11l_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦᒬ"):
            return bstack1lll11l_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣᒭ")
    @staticmethod
    def bstack1111l1l1l1_opy_(bstack1lll1ll1l_opy_):
        try:
            if not bstack1l1llll1ll_opy_.on():
                return bstack1lll1ll1l_opy_
            if os.environ.get(bstack1lll11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢᒮ"), None) == bstack1lll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᒯ"):
                tests = os.environ.get(bstack1lll11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣᒰ"), None)
                if tests is None or tests == bstack1lll11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᒱ"):
                    return bstack1lll1ll1l_opy_
                bstack1lll1ll1l_opy_ = tests.split(bstack1lll11l_opy_ (u"࠭ࠬࠨᒲ"))
                return bstack1lll1ll1l_opy_
        except Exception as exc:
            print(bstack1lll11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣᒳ"), str(exc))
        return bstack1lll1ll1l_opy_
    @classmethod
    def bstack1l1l11l1l1_opy_(cls, event: str, bstack1l1l111l11_opy_: bstack1l11lllll1_opy_):
        bstack1l1l111111_opy_ = {
            bstack1lll11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᒴ"): event,
            bstack1l1l111l11_opy_.bstack1l1l11l111_opy_(): bstack1l1l111l11_opy_.bstack1l11ll1ll1_opy_(event)
        }
        bstack1l1llll1ll_opy_.bstack1l11lll1l1_opy_(bstack1l1l111111_opy_)