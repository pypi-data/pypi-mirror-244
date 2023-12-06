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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111lll1l1l_opy_
def bstack111ll1llll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111ll1l11l_opy_(bstack111ll1l1l1_opy_, bstack111ll1lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111ll1l1l1_opy_):
        with open(bstack111ll1l1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111ll1llll_opy_(bstack111ll1l1l1_opy_):
        pac = get_pac(url=bstack111ll1l1l1_opy_)
    else:
        raise Exception(bstack1lll11l_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ጗").format(bstack111ll1l1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lll11l_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥጘ"), 80))
        bstack111ll1ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111ll1ll11_opy_ = bstack1lll11l_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫጙ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111ll1lll1_opy_, bstack111ll1ll11_opy_)
    return proxy_url
def bstack1l1lll1ll_opy_(config):
    return bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧጚ") in config or bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩጛ") in config
def bstack11llllll_opy_(config):
    if not bstack1l1lll1ll_opy_(config):
        return
    if config.get(bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩጜ")):
        return config.get(bstack1lll11l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪጝ"))
    if config.get(bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬጞ")):
        return config.get(bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ጟ"))
def bstack1llll11l1l_opy_(config, bstack111ll1lll1_opy_):
    proxy = bstack11llllll_opy_(config)
    proxies = {}
    if config.get(bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ጠ")) or config.get(bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨጡ")):
        if proxy.endswith(bstack1lll11l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪጢ")):
            proxies = bstack1ll11l111_opy_(proxy, bstack111ll1lll1_opy_)
        else:
            proxies = {
                bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬጣ"): proxy
            }
    return proxies
def bstack1ll11l111_opy_(bstack111ll1l1l1_opy_, bstack111ll1lll1_opy_):
    proxies = {}
    global bstack111ll1ll1l_opy_
    if bstack1lll11l_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪጤ") in globals():
        return bstack111ll1ll1l_opy_
    try:
        proxy = bstack111ll1l11l_opy_(bstack111ll1l1l1_opy_, bstack111ll1lll1_opy_)
        if bstack1lll11l_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣጥ") in proxy:
            proxies = {}
        elif bstack1lll11l_opy_ (u"ࠤࡋࡘ࡙ࡖࠢጦ") in proxy or bstack1lll11l_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤጧ") in proxy or bstack1lll11l_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥጨ") in proxy:
            bstack111ll1l1ll_opy_ = proxy.split(bstack1lll11l_opy_ (u"ࠧࠦࠢጩ"))
            if bstack1lll11l_opy_ (u"ࠨ࠺࠰࠱ࠥጪ") in bstack1lll11l_opy_ (u"ࠢࠣጫ").join(bstack111ll1l1ll_opy_[1:]):
                proxies = {
                    bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧጬ"): bstack1lll11l_opy_ (u"ࠤࠥጭ").join(bstack111ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩጮ"): str(bstack111ll1l1ll_opy_[0]).lower() + bstack1lll11l_opy_ (u"ࠦ࠿࠵࠯ࠣጯ") + bstack1lll11l_opy_ (u"ࠧࠨጰ").join(bstack111ll1l1ll_opy_[1:])
                }
        elif bstack1lll11l_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧጱ") in proxy:
            bstack111ll1l1ll_opy_ = proxy.split(bstack1lll11l_opy_ (u"ࠢࠡࠤጲ"))
            if bstack1lll11l_opy_ (u"ࠣ࠼࠲࠳ࠧጳ") in bstack1lll11l_opy_ (u"ࠤࠥጴ").join(bstack111ll1l1ll_opy_[1:]):
                proxies = {
                    bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩጵ"): bstack1lll11l_opy_ (u"ࠦࠧጶ").join(bstack111ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫጷ"): bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢጸ") + bstack1lll11l_opy_ (u"ࠢࠣጹ").join(bstack111ll1l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧጺ"): proxy
            }
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨጻ"), bstack111lll1l1l_opy_.format(bstack111ll1l1l1_opy_, str(e)))
    bstack111ll1ll1l_opy_ = proxies
    return proxies