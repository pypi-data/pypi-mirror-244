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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1lll11l_opy_, bstack11l1ll11_opy_, bstack1lll1l11_opy_, bstack11l11l11_opy_
from bstack_utils.messages import bstack111l11l11_opy_, bstack1l1ll1lll_opy_
from bstack_utils.proxy import bstack1llll11l1l_opy_, bstack11llllll_opy_
from browserstack_sdk.bstack1l1ll1ll11_opy_ import *
from browserstack_sdk.bstack1l1l1l1l1l_opy_ import *
bstack11ll1l11l_opy_ = Config.get_instance()
def bstack11ll111l1l_opy_(config):
    return config[bstack1lll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᄓ")]
def bstack11ll11ll1l_opy_(config):
    return config[bstack1lll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᄔ")]
def bstack1ll11ll1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1ll1111_opy_(obj):
    values = []
    bstack11l111l1l1_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᄕ"), re.I)
    for key in obj.keys():
        if bstack11l111l1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1l1l_opy_(config):
    tags = []
    tags.extend(bstack11l1ll1111_opy_(os.environ))
    tags.extend(bstack11l1ll1111_opy_(config))
    return tags
def bstack11l11ll1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l11ll1_opy_(bstack11l11lllll_opy_):
    if not bstack11l11lllll_opy_:
        return bstack1lll11l_opy_ (u"࠭ࠧᄖ")
    return bstack1lll11l_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᄗ").format(bstack11l11lllll_opy_.name, bstack11l11lllll_opy_.email)
def bstack11ll11llll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1ll11ll_opy_ = repo.common_dir
        info = {
            bstack1lll11l_opy_ (u"ࠣࡵ࡫ࡥࠧᄘ"): repo.head.commit.hexsha,
            bstack1lll11l_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᄙ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lll11l_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᄚ"): repo.active_branch.name,
            bstack1lll11l_opy_ (u"ࠦࡹࡧࡧࠣᄛ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lll11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᄜ"): bstack11l1l11ll1_opy_(repo.head.commit.committer),
            bstack1lll11l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᄝ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lll11l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᄞ"): bstack11l1l11ll1_opy_(repo.head.commit.author),
            bstack1lll11l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᄟ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lll11l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᄠ"): repo.head.commit.message,
            bstack1lll11l_opy_ (u"ࠥࡶࡴࡵࡴࠣᄡ"): repo.git.rev_parse(bstack1lll11l_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᄢ")),
            bstack1lll11l_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᄣ"): bstack11l1ll11ll_opy_,
            bstack1lll11l_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᄤ"): subprocess.check_output([bstack1lll11l_opy_ (u"ࠢࡨ࡫ࡷࠦᄥ"), bstack1lll11l_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᄦ"), bstack1lll11l_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᄧ")]).strip().decode(
                bstack1lll11l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᄨ")),
            bstack1lll11l_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᄩ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lll11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᄪ"): repo.git.rev_list(
                bstack1lll11l_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᄫ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11ll111_opy_ = []
        for remote in remotes:
            bstack11l1l1l1ll_opy_ = {
                bstack1lll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᄬ"): remote.name,
                bstack1lll11l_opy_ (u"ࠣࡷࡵࡰࠧᄭ"): remote.url,
            }
            bstack11l11ll111_opy_.append(bstack11l1l1l1ll_opy_)
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄮ"): bstack1lll11l_opy_ (u"ࠥ࡫࡮ࡺࠢᄯ"),
            **info,
            bstack1lll11l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᄰ"): bstack11l11ll111_opy_
        }
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᄱ").format(err))
        return {}
def bstack11lll111l_opy_():
    env = os.environ
    if (bstack1lll11l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᄲ") in env and len(env[bstack1lll11l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᄳ")]) > 0) or (
            bstack1lll11l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᄴ") in env and len(env[bstack1lll11l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᄵ")]) > 0):
        return {
            bstack1lll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᄶ"): bstack1lll11l_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧᄷ"),
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᄸ"): env.get(bstack1lll11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᄹ")),
            bstack1lll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᄺ"): env.get(bstack1lll11l_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥᄻ")),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᄼ"): env.get(bstack1lll11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᄽ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠦࡈࡏࠢᄾ")) == bstack1lll11l_opy_ (u"ࠧࡺࡲࡶࡧࠥᄿ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣᅀ"))):
        return {
            bstack1lll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅁ"): bstack1lll11l_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥᅂ"),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅃ"): env.get(bstack1lll11l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᅄ")),
            bstack1lll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅅ"): env.get(bstack1lll11l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤᅆ")),
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅇ"): env.get(bstack1lll11l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥᅈ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠣࡅࡌࠦᅉ")) == bstack1lll11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅊ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥᅋ"))):
        return {
            bstack1lll11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅌ"): bstack1lll11l_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣᅍ"),
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅎ"): env.get(bstack1lll11l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢᅏ")),
            bstack1lll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅐ"): env.get(bstack1lll11l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᅑ")),
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅒ"): env.get(bstack1lll11l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᅓ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠧࡉࡉࠣᅔ")) == bstack1lll11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᅕ") and env.get(bstack1lll11l_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣᅖ")) == bstack1lll11l_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥᅗ"):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅘ"): bstack1lll11l_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧᅙ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅚ"): None,
            bstack1lll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅛ"): None,
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅜ"): None
        }
    if env.get(bstack1lll11l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᅝ")) and env.get(bstack1lll11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᅞ")):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅟ"): bstack1lll11l_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᅠ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅡ"): env.get(bstack1lll11l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᅢ")),
            bstack1lll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅣ"): None,
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅤ"): env.get(bstack1lll11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᅥ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠤࡆࡍࠧᅦ")) == bstack1lll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᅧ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᅨ"))):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅩ"): bstack1lll11l_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᅪ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅫ"): env.get(bstack1lll11l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᅬ")),
            bstack1lll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅭ"): None,
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅮ"): env.get(bstack1lll11l_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅯ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠧࡉࡉࠣᅰ")) == bstack1lll11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᅱ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᅲ"))):
        return {
            bstack1lll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅳ"): bstack1lll11l_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᅴ"),
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅵ"): env.get(bstack1lll11l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᅶ")),
            bstack1lll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅷ"): env.get(bstack1lll11l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᅸ")),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅹ"): env.get(bstack1lll11l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᅺ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠤࡆࡍࠧᅻ")) == bstack1lll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᅼ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᅽ"))):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅾ"): bstack1lll11l_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᅿ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆀ"): env.get(bstack1lll11l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᆁ")),
            bstack1lll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆂ"): env.get(bstack1lll11l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᆃ")),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆄ"): env.get(bstack1lll11l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᆅ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠨࡃࡊࠤᆆ")) == bstack1lll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧᆇ") and bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᆈ"))):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆉ"): bstack1lll11l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᆊ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆋ"): env.get(bstack1lll11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᆌ")),
            bstack1lll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆍ"): env.get(bstack1lll11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᆎ")) or env.get(bstack1lll11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᆏ")),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆐ"): env.get(bstack1lll11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆑ"))
        }
    if bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᆒ"))):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆓ"): bstack1lll11l_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᆔ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆕ"): bstack1lll11l_opy_ (u"ࠣࡽࢀࡿࢂࠨᆖ").format(env.get(bstack1lll11l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᆗ")), env.get(bstack1lll11l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᆘ"))),
            bstack1lll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆙ"): env.get(bstack1lll11l_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᆚ")),
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆛ"): env.get(bstack1lll11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᆜ"))
        }
    if bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᆝ"))):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆞ"): bstack1lll11l_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᆟ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆠ"): bstack1lll11l_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᆡ").format(env.get(bstack1lll11l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᆢ")), env.get(bstack1lll11l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᆣ")), env.get(bstack1lll11l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᆤ")), env.get(bstack1lll11l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᆥ"))),
            bstack1lll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆦ"): env.get(bstack1lll11l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᆧ")),
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆨ"): env.get(bstack1lll11l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆩ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᆪ")) and env.get(bstack1lll11l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᆫ")):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆬ"): bstack1lll11l_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᆭ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆮ"): bstack1lll11l_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᆯ").format(env.get(bstack1lll11l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᆰ")), env.get(bstack1lll11l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᆱ")), env.get(bstack1lll11l_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᆲ"))),
            bstack1lll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆳ"): env.get(bstack1lll11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᆴ")),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆵ"): env.get(bstack1lll11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᆶ"))
        }
    if any([env.get(bstack1lll11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᆷ")), env.get(bstack1lll11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᆸ")), env.get(bstack1lll11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᆹ"))]):
        return {
            bstack1lll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆺ"): bstack1lll11l_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᆻ"),
            bstack1lll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆼ"): env.get(bstack1lll11l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᆽ")),
            bstack1lll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆾ"): env.get(bstack1lll11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᆿ")),
            bstack1lll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇀ"): env.get(bstack1lll11l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᇁ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᇂ")):
        return {
            bstack1lll11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇃ"): bstack1lll11l_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᇄ"),
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇅ"): env.get(bstack1lll11l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᇆ")),
            bstack1lll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇇ"): env.get(bstack1lll11l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᇈ")),
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇉ"): env.get(bstack1lll11l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᇊ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᇋ")) or env.get(bstack1lll11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᇌ")):
        return {
            bstack1lll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇍ"): bstack1lll11l_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᇎ"),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇏ"): env.get(bstack1lll11l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᇐ")),
            bstack1lll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇑ"): bstack1lll11l_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᇒ") if env.get(bstack1lll11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᇓ")) else None,
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇔ"): env.get(bstack1lll11l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᇕ"))
        }
    if any([env.get(bstack1lll11l_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᇖ")), env.get(bstack1lll11l_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᇗ")), env.get(bstack1lll11l_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᇘ"))]):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇙ"): bstack1lll11l_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᇚ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇛ"): None,
            bstack1lll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇜ"): env.get(bstack1lll11l_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᇝ")),
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇞ"): env.get(bstack1lll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᇟ"))
        }
    if env.get(bstack1lll11l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᇠ")):
        return {
            bstack1lll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇡ"): bstack1lll11l_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᇢ"),
            bstack1lll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇣ"): env.get(bstack1lll11l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᇤ")),
            bstack1lll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇥ"): bstack1lll11l_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᇦ").format(env.get(bstack1lll11l_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᇧ"))) if env.get(bstack1lll11l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᇨ")) else None,
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇩ"): env.get(bstack1lll11l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇪ"))
        }
    if bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᇫ"))):
        return {
            bstack1lll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇬ"): bstack1lll11l_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᇭ"),
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇮ"): env.get(bstack1lll11l_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᇯ")),
            bstack1lll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇰ"): env.get(bstack1lll11l_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᇱ")),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇲ"): env.get(bstack1lll11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇳ"))
        }
    if bstack1lll11ll1_opy_(env.get(bstack1lll11l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᇴ"))):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇵ"): bstack1lll11l_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᇶ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇷ"): bstack1lll11l_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᇸ").format(env.get(bstack1lll11l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᇹ")), env.get(bstack1lll11l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᇺ")), env.get(bstack1lll11l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᇻ"))),
            bstack1lll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇼ"): env.get(bstack1lll11l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᇽ")),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇾ"): env.get(bstack1lll11l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᇿ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠤࡆࡍࠧሀ")) == bstack1lll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣሁ") and env.get(bstack1lll11l_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦሂ")) == bstack1lll11l_opy_ (u"ࠧ࠷ࠢሃ"):
        return {
            bstack1lll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሄ"): bstack1lll11l_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢህ"),
            bstack1lll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሆ"): bstack1lll11l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧሇ").format(env.get(bstack1lll11l_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧለ"))),
            bstack1lll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሉ"): None,
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሊ"): None,
        }
    if env.get(bstack1lll11l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤላ")):
        return {
            bstack1lll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሌ"): bstack1lll11l_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥል"),
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሎ"): None,
            bstack1lll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሏ"): env.get(bstack1lll11l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧሐ")),
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሑ"): env.get(bstack1lll11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧሒ"))
        }
    if any([env.get(bstack1lll11l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥሓ")), env.get(bstack1lll11l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣሔ")), env.get(bstack1lll11l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢሕ")), env.get(bstack1lll11l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦሖ"))]):
        return {
            bstack1lll11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሗ"): bstack1lll11l_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣመ"),
            bstack1lll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሙ"): None,
            bstack1lll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack1lll11l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤማ")) or None,
            bstack1lll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack1lll11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧም"), 0)
        }
    if env.get(bstack1lll11l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤሞ")):
        return {
            bstack1lll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሟ"): bstack1lll11l_opy_ (u"ࠨࡇࡰࡅࡇࠦሠ"),
            bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሡ"): None,
            bstack1lll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሢ"): env.get(bstack1lll11l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሣ")),
            bstack1lll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሤ"): env.get(bstack1lll11l_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥሥ"))
        }
    if env.get(bstack1lll11l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሦ")):
        return {
            bstack1lll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሧ"): bstack1lll11l_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥረ"),
            bstack1lll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሩ"): env.get(bstack1lll11l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሪ")),
            bstack1lll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧራ"): env.get(bstack1lll11l_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢሬ")),
            bstack1lll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦር"): env.get(bstack1lll11l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦሮ"))
        }
    return {bstack1lll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሯ"): None}
def get_host_info():
    return {
        bstack1lll11l_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥሰ"): platform.node(),
        bstack1lll11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦሱ"): platform.system(),
        bstack1lll11l_opy_ (u"ࠥࡸࡾࡶࡥࠣሲ"): platform.machine(),
        bstack1lll11l_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧሳ"): platform.version(),
        bstack1lll11l_opy_ (u"ࠧࡧࡲࡤࡪࠥሴ"): platform.architecture()[0]
    }
def bstack1llll11l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1111lll_opy_():
    if bstack11ll1l11l_opy_.get_property(bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧስ")):
        return bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ሶ")
    return bstack1lll11l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧሷ")
def bstack11l1111ll1_opy_(driver):
    info = {
        bstack1lll11l_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨሸ"): driver.capabilities,
        bstack1lll11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧሹ"): driver.session_id,
        bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬሺ"): driver.capabilities.get(bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪሻ"), None),
        bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨሼ"): driver.capabilities.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨሽ"), None),
        bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪሾ"): driver.capabilities.get(bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨሿ"), None),
    }
    if bstack11l1111lll_opy_() == bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩቀ"):
        info[bstack1lll11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬቁ")] = bstack1lll11l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫቂ") if bstack111ll1lll_opy_() else bstack1lll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨቃ")
    return info
def bstack111ll1lll_opy_():
    if bstack11ll1l11l_opy_.get_property(bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ቄ")):
        return True
    if bstack1lll11ll1_opy_(os.environ.get(bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩቅ"), None)):
        return True
    return False
def bstack1l1111l1_opy_(bstack11l11l11l1_opy_, url, data, config):
    headers = config.get(bstack1lll11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪቆ"), None)
    proxies = bstack1llll11l1l_opy_(config, url)
    auth = config.get(bstack1lll11l_opy_ (u"ࠪࡥࡺࡺࡨࠨቇ"), None)
    response = requests.request(
            bstack11l11l11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11ll1lll1_opy_(bstack1lll1111l1_opy_, size):
    bstack1l1ll11l11_opy_ = []
    while len(bstack1lll1111l1_opy_) > size:
        bstack1ll11ll11l_opy_ = bstack1lll1111l1_opy_[:size]
        bstack1l1ll11l11_opy_.append(bstack1ll11ll11l_opy_)
        bstack1lll1111l1_opy_ = bstack1lll1111l1_opy_[size:]
    bstack1l1ll11l11_opy_.append(bstack1lll1111l1_opy_)
    return bstack1l1ll11l11_opy_
def bstack11l1l11l1l_opy_(message, bstack11l111l11l_opy_=False):
    os.write(1, bytes(message, bstack1lll11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪቈ")))
    os.write(1, bytes(bstack1lll11l_opy_ (u"ࠬࡢ࡮ࠨ቉"), bstack1lll11l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬቊ")))
    if bstack11l111l11l_opy_:
        with open(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ቋ") + os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧቌ")] + bstack1lll11l_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧቍ"), bstack1lll11l_opy_ (u"ࠪࡥࠬ቎")) as f:
            f.write(message + bstack1lll11l_opy_ (u"ࠫࡡࡴࠧ቏"))
def bstack11l11ll1l1_opy_():
    return os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨቐ")].lower() == bstack1lll11l_opy_ (u"࠭ࡴࡳࡷࡨࠫቑ")
def bstack1l1l1llll_opy_(bstack11llll111l_opy_):
    return bstack1lll11l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ቒ").format(bstack11l1lll11l_opy_, bstack11llll111l_opy_)
def bstack11l111ll1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠨ࡜ࠪቓ")
def bstack11l11lll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1lll11l_opy_ (u"ࠩ࡝ࠫቔ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1lll11l_opy_ (u"ࠪ࡞ࠬቕ")))).total_seconds() * 1000
def bstack11l111l111_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1lll11l_opy_ (u"ࠫ࡟࠭ቖ")
def bstack11l1ll1l11_opy_(bstack11l11llll1_opy_):
    date_format = bstack1lll11l_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ቗")
    bstack11l111llll_opy_ = datetime.datetime.strptime(bstack11l11llll1_opy_, date_format)
    return bstack11l111llll_opy_.isoformat() + bstack1lll11l_opy_ (u"࡚࠭ࠨቘ")
def bstack11l1111l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ቙")
    else:
        return bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨቚ")
def bstack1lll11ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1lll11l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧቛ")
def bstack11l1l11lll_opy_(val):
    return val.__str__().lower() == bstack1lll11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩቜ")
def bstack1l11l11l11_opy_(bstack11l1l111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l111l1_opy_ as e:
                print(bstack1lll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦቝ").format(func.__name__, bstack11l1l111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l1l1l1_opy_(bstack11l1l1lll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1lll1_opy_(cls, *args, **kwargs)
            except bstack11l1l111l1_opy_ as e:
                print(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧ቞").format(bstack11l1l1lll1_opy_.__name__, bstack11l1l111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l1l1l1_opy_
    else:
        return decorator
def bstack1ll1111l1l_opy_(bstack1l111l1l1l_opy_):
    if bstack1lll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ቟") in bstack1l111l1l1l_opy_ and bstack11l1l11lll_opy_(bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫበ")]):
        return False
    if bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪቡ") in bstack1l111l1l1l_opy_ and bstack11l1l11lll_opy_(bstack1l111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫቢ")]):
        return False
    return True
def bstack1ll11llll1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack11l1111l_opy_(hub_url):
    if bstack1llll1l1_opy_() <= version.parse(bstack1lll11l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪባ")):
        if hub_url != bstack1lll11l_opy_ (u"ࠫࠬቤ"):
            return bstack1lll11l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨብ") + hub_url + bstack1lll11l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥቦ")
        return bstack1lll1l11_opy_
    if hub_url != bstack1lll11l_opy_ (u"ࠧࠨቧ"):
        return bstack1lll11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥቨ") + hub_url + bstack1lll11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥቩ")
    return bstack11l11l11_opy_
def bstack11l1l1111l_opy_():
    return isinstance(os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩቪ")), str)
def bstack1l11llll_opy_(url):
    return urlparse(url).hostname
def bstack1l1llll1l_opy_(hostname):
    for bstack1llll1llll_opy_ in bstack11l1ll11_opy_:
        regex = re.compile(bstack1llll1llll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1ll1l1l_opy_(bstack11l11l1111_opy_, file_name, logger):
    bstack1l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠫࢃ࠭ቫ")), bstack11l11l1111_opy_)
    try:
        if not os.path.exists(bstack1l11l1ll_opy_):
            os.makedirs(bstack1l11l1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧቬ")), bstack11l11l1111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lll11l_opy_ (u"࠭ࡷࠨቭ")):
                pass
            with open(file_path, bstack1lll11l_opy_ (u"ࠢࡸ࠭ࠥቮ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111l11l11_opy_.format(str(e)))
def bstack11l11ll11l_opy_(file_name, key, value, logger):
    file_path = bstack11l1ll1l1l_opy_(bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨቯ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lllll1_opy_ = json.load(open(file_path, bstack1lll11l_opy_ (u"ࠩࡵࡦࠬተ")))
        else:
            bstack1l1lllll1_opy_ = {}
        bstack1l1lllll1_opy_[key] = value
        with open(file_path, bstack1lll11l_opy_ (u"ࠥࡻ࠰ࠨቱ")) as outfile:
            json.dump(bstack1l1lllll1_opy_, outfile)
def bstack11l1l11l1_opy_(file_name, logger):
    file_path = bstack11l1ll1l1l_opy_(bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫቲ"), file_name, logger)
    bstack1l1lllll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lll11l_opy_ (u"ࠬࡸࠧታ")) as bstack1111ll11l_opy_:
            bstack1l1lllll1_opy_ = json.load(bstack1111ll11l_opy_)
    return bstack1l1lllll1_opy_
def bstack1l1ll111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪቴ") + file_path + bstack1lll11l_opy_ (u"ࠧࠡࠩት") + str(e))
def bstack1llll1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lll11l_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥቶ")
def bstack1lllll1l11_opy_(config):
    if bstack1lll11l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨቷ") in config:
        del (config[bstack1lll11l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩቸ")])
        return False
    if bstack1llll1l1_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪቹ")):
        return False
    if bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫቺ")):
        return True
    if bstack1lll11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ቻ") in config and config[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧቼ")] is False:
        return False
    else:
        return True
def bstack11l1111l1_opy_(args_list, bstack11l111ll1l_opy_):
    index = -1
    for value in bstack11l111ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11lll1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11lll1ll_opy_ = bstack1l11lll1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨች"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቾ"), exception=exception)
    def bstack1l111l1l11_opy_(self):
        if self.result != bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪቿ"):
            return None
        if bstack1lll11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢኀ") in self.exception_type:
            return bstack1lll11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨኁ")
        return bstack1lll11l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢኂ")
    def bstack11l1ll11l1_opy_(self):
        if self.result != bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኃ"):
            return None
        if self.bstack1l11lll1ll_opy_:
            return self.bstack1l11lll1ll_opy_
        return bstack11l1l1llll_opy_(self.exception)
def bstack11l1l1llll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l111l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1111111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1lll1l_opy_(config, logger):
    try:
        import playwright
        bstack11l1ll111l_opy_ = playwright.__file__
        bstack11l1l1ll1l_opy_ = os.path.split(bstack11l1ll111l_opy_)
        bstack11l111lll1_opy_ = bstack11l1l1ll1l_opy_[0] + bstack1lll11l_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫኄ")
        os.environ[bstack1lll11l_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬኅ")] = bstack11llllll_opy_(config)
        with open(bstack11l111lll1_opy_, bstack1lll11l_opy_ (u"ࠪࡶࠬኆ")) as f:
            bstack1l1ll1111_opy_ = f.read()
            bstack11l1l1l11l_opy_ = bstack1lll11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪኇ")
            bstack11l111l1ll_opy_ = bstack1l1ll1111_opy_.find(bstack11l1l1l11l_opy_)
            if bstack11l111l1ll_opy_ == -1:
              process = subprocess.Popen(bstack1lll11l_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤኈ"), shell=True, cwd=bstack11l1l1ll1l_opy_[0])
              process.wait()
              bstack11l1l11111_opy_ = bstack1lll11l_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭኉")
              bstack11l11l11ll_opy_ = bstack1lll11l_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦኊ")
              bstack11l1l111ll_opy_ = bstack1l1ll1111_opy_.replace(bstack11l1l11111_opy_, bstack11l11l11ll_opy_)
              with open(bstack11l111lll1_opy_, bstack1lll11l_opy_ (u"ࠨࡹࠪኋ")) as f:
                f.write(bstack11l1l111ll_opy_)
    except Exception as e:
        logger.error(bstack1l1ll1lll_opy_.format(str(e)))
def bstack1ll1ll1lll_opy_():
  try:
    bstack11l1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩኌ"))
    bstack11l11l1l11_opy_ = []
    if os.path.exists(bstack11l1l1l111_opy_):
      with open(bstack11l1l1l111_opy_) as f:
        bstack11l11l1l11_opy_ = json.load(f)
      os.remove(bstack11l1l1l111_opy_)
    return bstack11l11l1l11_opy_
  except:
    pass
  return []
def bstack1ll11ll1_opy_(bstack1ll11111l_opy_):
  try:
    bstack11l11l1l11_opy_ = []
    bstack11l1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪኍ"))
    if os.path.exists(bstack11l1l1l111_opy_):
      with open(bstack11l1l1l111_opy_) as f:
        bstack11l11l1l11_opy_ = json.load(f)
    bstack11l11l1l11_opy_.append(bstack1ll11111l_opy_)
    with open(bstack11l1l1l111_opy_, bstack1lll11l_opy_ (u"ࠫࡼ࠭኎")) as f:
        json.dump(bstack11l11l1l11_opy_, f)
  except:
    pass
def bstack1lll11ll_opy_(logger, bstack11l11l1lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1lll11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ኏"), bstack1lll11l_opy_ (u"࠭ࠧነ"))
    if test_name == bstack1lll11l_opy_ (u"ࠧࠨኑ"):
        test_name = threading.current_thread().__dict__.get(bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧኒ"), bstack1lll11l_opy_ (u"ࠩࠪና"))
    bstack11l11lll11_opy_ = bstack1lll11l_opy_ (u"ࠪ࠰ࠥ࠭ኔ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l1lll_opy_:
        bstack1ll1ll11_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫን"), bstack1lll11l_opy_ (u"ࠬ࠶ࠧኖ"))
        bstack1ll1lllll_opy_ = {bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫኗ"): test_name, bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ኘ"): bstack11l11lll11_opy_, bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧኙ"): bstack1ll1ll11_opy_}
        bstack11l111ll11_opy_ = []
        bstack11l11l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨኚ"))
        if os.path.exists(bstack11l11l1ll1_opy_):
            with open(bstack11l11l1ll1_opy_) as f:
                bstack11l111ll11_opy_ = json.load(f)
        bstack11l111ll11_opy_.append(bstack1ll1lllll_opy_)
        with open(bstack11l11l1ll1_opy_, bstack1lll11l_opy_ (u"ࠪࡻࠬኛ")) as f:
            json.dump(bstack11l111ll11_opy_, f)
    else:
        bstack1ll1lllll_opy_ = {bstack1lll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩኜ"): test_name, bstack1lll11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫኝ"): bstack11l11lll11_opy_, bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬኞ"): str(multiprocessing.current_process().name)}
        if bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫኟ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1lllll_opy_)
  except Exception as e:
      logger.warn(bstack1lll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧአ").format(e))
def bstack11ll1lll_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l11l11_opy_ = []
    bstack1ll1lllll_opy_ = {bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧኡ"): test_name, bstack1lll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩኢ"): error_message, bstack1lll11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪኣ"): index}
    bstack11l1l1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ኤ"))
    if os.path.exists(bstack11l1l1ll11_opy_):
        with open(bstack11l1l1ll11_opy_) as f:
            bstack11l1l11l11_opy_ = json.load(f)
    bstack11l1l11l11_opy_.append(bstack1ll1lllll_opy_)
    with open(bstack11l1l1ll11_opy_, bstack1lll11l_opy_ (u"࠭ࡷࠨእ")) as f:
        json.dump(bstack11l1l11l11_opy_, f)
  except Exception as e:
    logger.warn(bstack1lll11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥኦ").format(e))
def bstack1llll1ll1l_opy_(bstack11111l111_opy_, name, logger):
  try:
    bstack1ll1lllll_opy_ = {bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኧ"): name, bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨከ"): bstack11111l111_opy_, bstack1lll11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩኩ"): str(threading.current_thread()._name)}
    return bstack1ll1lllll_opy_
  except Exception as e:
    logger.warn(bstack1lll11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣኪ").format(e))
  return
def bstack1lll11111_opy_(framework):
    if framework.lower() == bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬካ"):
        return bstack1ll11ll111_opy_.version()
    elif framework.lower() == bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬኬ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1lll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧክ"):
        import behave
        return behave.__version__
    else:
        return bstack1lll11l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩኮ")