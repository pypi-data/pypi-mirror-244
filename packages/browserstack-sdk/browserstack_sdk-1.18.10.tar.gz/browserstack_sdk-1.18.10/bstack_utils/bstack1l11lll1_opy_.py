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
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll1ll11l_opy_ as bstack11ll11l11l_opy_
from bstack_utils.helper import bstack11l111ll1_opy_, bstack1ll1111l1l_opy_, bstack11ll111l1l_opy_, bstack11ll11ll1l_opy_, bstack11lll111l_opy_, get_host_info, bstack11ll11llll_opy_, bstack1l1111l1_opy_, bstack1l11l11l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11l11l11_opy_(class_method=False)
def _11ll1l1l1l_opy_(driver, bstack11llllll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1lll11l_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨร"): caps.get(bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧฤ"), None),
        bstack1lll11l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ล"): bstack11llllll1_opy_.get(bstack1lll11l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฦ"), None),
        bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪว"): caps.get(bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪศ"), None),
        bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨษ"): caps.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨส"), None)
    }
  except Exception as error:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬห") + str(error))
  return response
def bstack1lll11l11l_opy_(config):
  return config.get(bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩฬ"), False) or any([p.get(bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪอ"), False) == True for p in config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧฮ")]])
def bstack111l1111l_opy_(config, bstack1ll1ll11_opy_):
  try:
    if not bstack1ll1111l1l_opy_(config):
      return False
    bstack11ll1l111l_opy_ = config.get(bstack1lll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬฯ"), False)
    bstack11ll1l11l1_opy_ = config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩะ")][bstack1ll1ll11_opy_].get(bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧั"), None)
    if bstack11ll1l11l1_opy_ != None:
      bstack11ll1l111l_opy_ = bstack11ll1l11l1_opy_
    bstack11ll1l11ll_opy_ = os.getenv(bstack1lll11l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭า")) is not None and len(os.getenv(bstack1lll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧำ"))) > 0 and os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨิ")) != bstack1lll11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩี")
    return bstack11ll1l111l_opy_ and bstack11ll1l11ll_opy_
  except Exception as error:
    logger.debug(bstack1lll11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬึ") + str(error))
  return False
def bstack1l11lllll_opy_(bstack11ll1l1lll_opy_, test_tags):
  bstack11ll1l1lll_opy_ = os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧื"))
  if bstack11ll1l1lll_opy_ is None:
    return True
  bstack11ll1l1lll_opy_ = json.loads(bstack11ll1l1lll_opy_)
  try:
    include_tags = bstack11ll1l1lll_opy_[bstack1lll11l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩุࠬ")] if bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪู࠭") in bstack11ll1l1lll_opy_ and isinstance(bstack11ll1l1lll_opy_[bstack1lll11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ฺࠧ")], list) else []
    exclude_tags = bstack11ll1l1lll_opy_[bstack1lll11l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ฻")] if bstack1lll11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ฼") in bstack11ll1l1lll_opy_ and isinstance(bstack11ll1l1lll_opy_[bstack1lll11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ฽")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ฾") + str(error))
  return False
def bstack1ll111ll1_opy_(config, bstack11ll111lll_opy_, bstack11ll11l1ll_opy_):
  bstack11ll1111ll_opy_ = bstack11ll111l1l_opy_(config)
  bstack11ll111l11_opy_ = bstack11ll11ll1l_opy_(config)
  if bstack11ll1111ll_opy_ is None or bstack11ll111l11_opy_ is None:
    logger.error(bstack1lll11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ฿"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩเ"), bstack1lll11l_opy_ (u"ࠩࡾࢁࠬแ")))
    data = {
        bstack1lll11l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨโ"): config[bstack1lll11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩใ")],
        bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨไ"): config.get(bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩๅ"), os.path.basename(os.getcwd())),
        bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪๆ"): bstack11l111ll1_opy_(),
        bstack1lll11l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭็"): config.get(bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲ่ࠬ"), bstack1lll11l_opy_ (u"้ࠪࠫ")),
        bstack1lll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨ๊ࠫ"): {
            bstack1lll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩ๋ࠬ"): bstack11ll111lll_opy_,
            bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ์"): bstack11ll11l1ll_opy_,
            bstack1lll11l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫํ"): __version__
        },
        bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ๎"): settings,
        bstack1lll11l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ๏"): bstack11ll11llll_opy_(),
        bstack1lll11l_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ๐"): bstack11lll111l_opy_(),
        bstack1lll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭๑"): get_host_info(),
        bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ๒"): bstack1ll1111l1l_opy_(config)
    }
    headers = {
        bstack1lll11l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ๓"): bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ๔"),
    }
    config = {
        bstack1lll11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭๕"): (bstack11ll1111ll_opy_, bstack11ll111l11_opy_),
        bstack1lll11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ๖"): headers
    }
    response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ๗"), bstack11ll11l11l_opy_ + bstack1lll11l_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨ๘"), data, config)
    bstack11ll11111l_opy_ = response.json()
    if bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭๙")]:
      parsed = json.loads(os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ๚"), bstack1lll11l_opy_ (u"ࠧࡼࡿࠪ๛")))
      parsed[bstack1lll11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๜")] = bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ๝")][bstack1lll11l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๞")]
      os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๟")] = json.dumps(parsed)
      return bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠬࡪࡡࡵࡣࠪ๠")][bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ๡")], bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠧࡥࡣࡷࡥࠬ๢")][bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫ๣")]
    else:
      logger.error(bstack1lll11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪ๤") + bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๥")])
      if bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๦")] == bstack1lll11l_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧ๧"):
        for bstack11ll11ll11_opy_ in bstack11ll11111l_opy_[bstack1lll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭๨")]:
          logger.error(bstack11ll11ll11_opy_[bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๩")])
      return None, None
  except Exception as error:
    logger.error(bstack1lll11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤ๪") +  str(error))
    return None, None
def bstack1ll111l1l_opy_():
  if os.getenv(bstack1lll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ๫")) is None:
    return {
        bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ๬"): bstack1lll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ๭"),
        bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๮"): bstack1lll11l_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬ๯")
    }
  data = {bstack1lll11l_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨ๰"): bstack11l111ll1_opy_()}
  headers = {
      bstack1lll11l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ๱"): bstack1lll11l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪ๲") + os.getenv(bstack1lll11l_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣ๳")),
      bstack1lll11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ๴"): bstack1lll11l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ๵")
  }
  response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"࠭ࡐࡖࡖࠪ๶"), bstack11ll11l11l_opy_ + bstack1lll11l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩ๷"), data, { bstack1lll11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ๸"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1lll11l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥ๹") + datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬ๺"))
      return {bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ๻"): bstack1lll11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭๼"), bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๽"): bstack1lll11l_opy_ (u"ࠧࠨ๾")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1lll11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦ๿") + str(error))
    return {
        bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ຀"): bstack1lll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩກ"),
        bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຂ"): str(error)
    }
def bstack1l1ll111l_opy_(caps, options):
  try:
    bstack11ll1111l1_opy_ = caps.get(bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭຃"), {}).get(bstack1lll11l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪຄ"), caps.get(bstack1lll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ຅"), bstack1lll11l_opy_ (u"ࠨࠩຆ")))
    if bstack11ll1111l1_opy_:
      logger.warn(bstack1lll11l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨງ"))
      return False
    browser = caps.get(bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨຈ"), bstack1lll11l_opy_ (u"ࠫࠬຉ")).lower()
    if browser != bstack1lll11l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬຊ"):
      logger.warn(bstack1lll11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ຋"))
      return False
    browser_version = caps.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຌ"), caps.get(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪຍ")))
    if browser_version and browser_version != bstack1lll11l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩຎ") and int(browser_version.split(bstack1lll11l_opy_ (u"ࠪ࠲ࠬຏ"))[0]) <= 94:
      logger.warn(bstack1lll11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠴࠯ࠤຐ"))
      return False
    if not options is None:
      bstack11ll11l1l1_opy_ = options.to_capabilities().get(bstack1lll11l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪຑ"), {})
      if bstack1lll11l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪຒ") in bstack11ll11l1l1_opy_.get(bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬຓ"), []):
        logger.warn(bstack1lll11l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥດ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1lll11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦຕ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11ll111ll1_opy_ = config.get(bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪຖ"), {})
    bstack11ll111ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧທ")] = os.getenv(bstack1lll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪຘ"))
    bstack11ll1l1ll1_opy_ = json.loads(os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧນ"), bstack1lll11l_opy_ (u"ࠧࡼࡿࠪບ"))).get(bstack1lll11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩປ"))
    caps[bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩຜ")] = True
    if bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫຝ") in caps:
      caps[bstack1lll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬພ")][bstack1lll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬຟ")] = bstack11ll111ll1_opy_
      caps[bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧຠ")][bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧມ")][bstack1lll11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩຢ")] = bstack11ll1l1ll1_opy_
    else:
      caps[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨຣ")] = bstack11ll111ll1_opy_
      caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ຤")][bstack1lll11l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬລ")] = bstack11ll1l1ll1_opy_
  except Exception as error:
    logger.debug(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ຦") +  str(error))
def bstack1l1ll1l11_opy_(driver, bstack11ll1ll111_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11ll11lll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll11lll1_opy_ = False
      bstack11ll11lll1_opy_ = url.scheme in [bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳࠦວ"), bstack1lll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨຨ")]
      if bstack11ll11lll1_opy_:
        if bstack11ll1ll111_opy_:
          logger.info(bstack1lll11l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣຩ"))
          driver.execute_async_script(bstack1lll11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦ࠽ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࡟ࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠨ࠮ࠣࡪࡳ࠸ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡆࡘࡔࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰ࠵ࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡴࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤສ"))
          logger.info(bstack1lll11l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠥຫ"))
        else:
          driver.execute_script(bstack1lll11l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣࡋࡕࡒࡄࡇࡢࡗ࡙ࡕࡐࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢຬ"))
      return bstack11ll1ll111_opy_
  except Exception as e:
    logger.error(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣອ") + str(e))
    return False
def bstack1l1111lll_opy_(driver, class_name, name, module_name, path, bstack11llllll1_opy_):
  try:
    bstack11ll1l1111_opy_ = [class_name] if not class_name is None else []
    bstack11ll1l1l11_opy_ = {
        bstack1lll11l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦຮ"): True,
        bstack1lll11l_opy_ (u"ࠢࡵࡧࡶࡸࡉ࡫ࡴࡢ࡫࡯ࡷࠧຯ"): {
            bstack1lll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨະ"): name,
            bstack1lll11l_opy_ (u"ࠤࡷࡩࡸࡺࡒࡶࡰࡌࡨࠧັ"): os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩາ")),
            bstack1lll11l_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨຳ"): str(path),
            bstack1lll11l_opy_ (u"ࠧࡹࡣࡰࡲࡨࡐ࡮ࡹࡴࠣິ"): [module_name, *bstack11ll1l1111_opy_, name],
        },
        bstack1lll11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣີ"): _11ll1l1l1l_opy_(driver, bstack11llllll1_opy_)
    }
    driver.execute_script(bstack1lll11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡲࡺࡲ࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࠨࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣ࡙ࡘࡁࡏࡕࡓࡓࡗ࡚ࡅࡓࠩ࠯ࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡺࡡࡱࡖࡵࡥࡳࡹࡰࡰࡴࡷࡩࡷࡊࡡࡵࡣࠣࡁࠥ࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠢࡀࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡋࡎࡅࠩ࠯ࠤࢀࠦࡤࡦࡶࡤ࡭ࡱࡀࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨຶ"), bstack11ll1l1l11_opy_)
    logger.info(bstack1lll11l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦື"))
  except Exception as bstack11ll11l111_opy_:
    logger.error(bstack1lll11l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ຸࠣࠦ") + str(path) + bstack1lll11l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ູࠧ") + str(bstack11ll11l111_opy_))