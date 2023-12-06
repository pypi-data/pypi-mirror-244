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
import re
from bstack_utils.bstack11l1l11ll_opy_ import bstack111ll11lll_opy_
def bstack111ll1l111_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጼ")):
        return bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬጽ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጾ")):
        return bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬጿ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬፀ")):
        return bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬፁ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፂ")):
        return bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬፃ")
def bstack111l1ll1ll_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩፄ"), fixture_name))
def bstack111ll1111l_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ፅ"), fixture_name))
def bstack111ll11l1l_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ፆ"), fixture_name))
def bstack111ll11l11_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩፇ")):
        return bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩፈ"), bstack1lll11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧፉ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪፊ")):
        return bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪፋ"), bstack1lll11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩፌ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፍ")):
        return bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫፎ"), bstack1lll11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬፏ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬፐ")):
        return bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬፑ"), bstack1lll11l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧፒ")
    return None, None
def bstack111l1llll1_opy_(hook_name):
    if hook_name in [bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫፓ"), bstack1lll11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨፔ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1lllll_opy_(hook_name):
    if hook_name in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨፕ"), bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧፖ")]:
        return bstack1lll11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧፗ")
    elif hook_name in [bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩፘ"), bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩፙ")]:
        return bstack1lll11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩፚ")
    elif hook_name in [bstack1lll11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ፛"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ፜")]:
        return bstack1lll11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ፝")
    elif hook_name in [bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ፞"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ፟")]:
        return bstack1lll11l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ፠")
    return hook_name
def bstack111ll111l1_opy_(node, scenario):
    if hasattr(node, bstack1lll11l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ፡")):
        parts = node.nodeid.rsplit(bstack1lll11l_opy_ (u"ࠨ࡛ࠣ።"))
        params = parts[-1]
        return bstack1lll11l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ፣").format(scenario.name, params)
    return scenario.name
def bstack111ll11111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lll11l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ፤")):
            examples = list(node.callspec.params[bstack1lll11l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ፥")].values())
        return examples
    except:
        return []
def bstack111ll111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111ll11ll1_opy_(report):
    try:
        status = bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ፦")
        if report.passed or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ፧"))):
            status = bstack1lll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ፨")
        elif report.skipped:
            status = bstack1lll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ፩")
        bstack111ll11lll_opy_(status)
    except:
        pass
def bstack1l1lll1lll_opy_(status):
    try:
        bstack111l1lll1l_opy_ = bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ፪")
        if status == bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ፫"):
            bstack111l1lll1l_opy_ = bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ፬")
        elif status == bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ፭"):
            bstack111l1lll1l_opy_ = bstack1lll11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ፮")
        bstack111ll11lll_opy_(bstack111l1lll1l_opy_)
    except:
        pass
def bstack111l1lll11_opy_(item=None, report=None, summary=None, extra=None):
    return