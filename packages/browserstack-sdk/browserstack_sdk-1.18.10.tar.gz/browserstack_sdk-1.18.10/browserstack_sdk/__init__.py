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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack111l1llll_opy_():
  global CONFIG
  headers = {
        bstack1lll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1lll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1llll11l1l_opy_(CONFIG, bstack1ll11lll_opy_)
  try:
    response = requests.get(bstack1ll11lll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11l1111_opy_ = response.json()[bstack1lll11l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111llll11_opy_.format(response.json()))
      return bstack1l11l1111_opy_
    else:
      logger.debug(bstack1111lll1_opy_.format(bstack1lll11l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1111lll1_opy_.format(e))
def bstack1lll1111l_opy_(hub_url):
  global CONFIG
  url = bstack1lll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1lll11l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1lll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1lll11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1llll11l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack111llllll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11ll11111_opy_.format(hub_url, e))
def bstack111ll1l1_opy_():
  try:
    global bstack1lll111l1l_opy_
    bstack1l11l1111_opy_ = bstack111l1llll_opy_()
    bstack11l111l1l_opy_ = []
    results = []
    for bstack1llll1l1ll_opy_ in bstack1l11l1111_opy_:
      bstack11l111l1l_opy_.append(bstack111l11ll1_opy_(target=bstack1lll1111l_opy_,args=(bstack1llll1l1ll_opy_,)))
    for t in bstack11l111l1l_opy_:
      t.start()
    for t in bstack11l111l1l_opy_:
      results.append(t.join())
    bstack1llll1111_opy_ = {}
    for item in results:
      hub_url = item[bstack1lll11l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1lll11l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1llll1111_opy_[hub_url] = latency
    bstack1l11l1lll_opy_ = min(bstack1llll1111_opy_, key= lambda x: bstack1llll1111_opy_[x])
    bstack1lll111l1l_opy_ = bstack1l11l1lll_opy_
    logger.debug(bstack1l1l1l1l_opy_.format(bstack1l11l1lll_opy_))
  except Exception as e:
    logger.debug(bstack11l11111_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1111l1_opy_, bstack1l1l1llll_opy_, bstack1l1111111_opy_, bstack1ll1111l1l_opy_, Notset, bstack1lllll1l11_opy_, \
  bstack11l1l11l1_opy_, bstack1l1ll111l1_opy_, bstack11l1111l1_opy_, bstack11lll111l_opy_, bstack1ll11llll1_opy_, bstack1llll11l11_opy_, bstack1ll11ll1ll_opy_, \
  bstack11l1lll1l_opy_, bstack1ll1ll1lll_opy_, bstack1ll11ll1_opy_, bstack1llll1ll1l_opy_, bstack1lll11ll_opy_, bstack11ll1lll_opy_, \
  bstack1lll11111_opy_, bstack1lll11ll1_opy_
from bstack_utils.bstack11lll11l1_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.bstack11l1l11ll_opy_ import bstack11llll1l1_opy_, bstack11ll11lll_opy_
from bstack_utils.bstack1l1l11lll_opy_ import bstack1l1llll1ll_opy_
from bstack_utils.proxy import bstack1ll11l111_opy_, bstack1llll11l1l_opy_, bstack11llllll_opy_, bstack1l1lll1ll_opy_
import bstack_utils.bstack1l11lll1_opy_ as bstack11l11llll_opy_
from browserstack_sdk.bstack1l1ll1ll11_opy_ import *
from browserstack_sdk.bstack111l1l11l_opy_ import *
from bstack_utils.bstack1l111l1l1_opy_ import bstack1l1lll1lll_opy_
bstack1ll111lll_opy_ = bstack1lll11l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11111l1l1_opy_ = bstack1lll11l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l1lllllll_opy_ = None
CONFIG = {}
bstack1111l1l1l_opy_ = {}
bstack1lll11l1ll_opy_ = {}
bstack1ll1ll1ll_opy_ = None
bstack11ll111ll_opy_ = None
bstack1lllll11ll_opy_ = None
bstack11111llll_opy_ = -1
bstack111ll1111_opy_ = 0
bstack11l11ll1l_opy_ = bstack111l11l1l_opy_
bstack1ll11l1ll1_opy_ = 1
bstack1ll1111ll1_opy_ = False
bstack11lll111_opy_ = False
bstack1l1l11l1l_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࢂ")
bstack1ll11ll1l_opy_ = bstack1lll11l_opy_ (u"ࠩࠪࢃ")
bstack1l1l1lll_opy_ = False
bstack1lll11llll_opy_ = True
bstack1ll11llll_opy_ = bstack1lll11l_opy_ (u"ࠪࠫࢄ")
bstack111l1ll1l_opy_ = []
bstack1lll111l1l_opy_ = bstack1lll11l_opy_ (u"ࠫࠬࢅ")
bstack1lllll1ll1_opy_ = False
bstack111111ll1_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1ll1l1ll_opy_ = -1
bstack1ll1l1111_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧࢆ")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1lll11l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1111l1lll_opy_ = 0
bstack1111ll1ll_opy_ = []
bstack1lll111l_opy_ = []
bstack1l11l11l_opy_ = []
bstack111l1lll_opy_ = []
bstack1ll111l1l1_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࢉ")
bstack11l1ll1l1_opy_ = bstack1lll11l_opy_ (u"ࠩࠪࢊ")
bstack1llll111ll_opy_ = False
bstack1ll11l11ll_opy_ = False
bstack111ll11l1_opy_ = {}
bstack1l1l11ll1_opy_ = None
bstack111lll1l_opy_ = None
bstack1lll111l1_opy_ = None
bstack11l11ll1_opy_ = None
bstack111111l1l_opy_ = None
bstack1111ll111_opy_ = None
bstack1llll111l_opy_ = None
bstack111ll11ll_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack11l1lll1_opy_ = None
bstack1llll11ll_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack1lllllll11_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l1llllll1_opy_ = None
bstack111ll1l11_opy_ = None
bstack11l11l111_opy_ = None
bstack1lll11l1_opy_ = None
bstack1lllll11l1_opy_ = bstack1lll11l_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l11ll1l_opy_,
                    format=bstack1lll11l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack1lll11l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack11ll1l11l_opy_ = Config.get_instance()
percy = bstack1lll111ll_opy_()
def bstack1ll1l1llll_opy_():
  global CONFIG
  global bstack11l11ll1l_opy_
  if bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack11l11ll1l_opy_ = bstack111l1l1ll_opy_[CONFIG[bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack11l11ll1l_opy_)
def bstack1l1ll11l_opy_():
  global CONFIG
  global bstack1llll111ll_opy_
  global bstack11ll1l11l_opy_
  bstack1111l1ll_opy_ = bstack1l1llll11l_opy_(CONFIG)
  if (bstack1lll11l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1111l1ll_opy_ and str(bstack1111l1ll_opy_[bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack1lll11l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1llll111ll_opy_ = True
  bstack11ll1l11l_opy_.bstack1l1l11l1_opy_(bstack1111l1ll_opy_.get(bstack1lll11l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1l111l111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11ll11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lll11l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack1lll11l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll11llll_opy_
      bstack1ll11llll_opy_ += bstack1lll11l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1l1ll11l1_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1lll1ll11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll11l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1lll11l_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack1lll11l_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack11l11ll11_opy_():
  bstack1ll1lll1l1_opy_ = bstack1l11ll11l_opy_()
  if bstack1ll1lll1l1_opy_ and os.path.exists(os.path.abspath(bstack1ll1lll1l1_opy_)):
    fileName = bstack1ll1lll1l1_opy_
  if bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack1l1lll_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1lll_opy_ = bstack1lll11l_opy_ (u"ࠩࠪ࢟")
  bstack1l11llll1_opy_ = os.getcwd()
  bstack1llll1ll11_opy_ = bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1llll1l11l_opy_ = bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack1l1lll_opy_)) and bstack1l11llll1_opy_ != bstack1lll11l_opy_ (u"ࠧࠨࢢ"):
    bstack1l1lll_opy_ = os.path.join(bstack1l11llll1_opy_, bstack1llll1ll11_opy_)
    if not os.path.exists(bstack1l1lll_opy_):
      bstack1l1lll_opy_ = os.path.join(bstack1l11llll1_opy_, bstack1llll1l11l_opy_)
    if bstack1l11llll1_opy_ != os.path.dirname(bstack1l11llll1_opy_):
      bstack1l11llll1_opy_ = os.path.dirname(bstack1l11llll1_opy_)
    else:
      bstack1l11llll1_opy_ = bstack1lll11l_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack1l1lll_opy_):
    bstack1l111lll_opy_(
      bstack1ll1l111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1lll_opy_, bstack1lll11l_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack1lll11l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1l1ll11l1_opy_)
      yaml.add_constructor(bstack1lll11l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1lll1ll11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1lll_opy_, bstack1lll11l_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l111lll_opy_(bstack1l1ll1l111_opy_.format(str(exc)))
def bstack1lll1l1lll_opy_(config):
  bstack1ll1lll111_opy_ = bstack1111111l_opy_(config)
  for option in list(bstack1ll1lll111_opy_):
    if option.lower() in bstack1llll1l111_opy_ and option != bstack1llll1l111_opy_[option.lower()]:
      bstack1ll1lll111_opy_[bstack1llll1l111_opy_[option.lower()]] = bstack1ll1lll111_opy_[option]
      del bstack1ll1lll111_opy_[option]
  return config
def bstack1ll1lllll1_opy_():
  global bstack1lll11l1ll_opy_
  for key, bstack1ll1l1ll1_opy_ in bstack1ll1l1l1l_opy_.items():
    if isinstance(bstack1ll1l1ll1_opy_, list):
      for var in bstack1ll1l1ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll11l1ll_opy_[key] = os.environ[var]
          break
    elif bstack1ll1l1ll1_opy_ in os.environ and os.environ[bstack1ll1l1ll1_opy_] and str(os.environ[bstack1ll1l1ll1_opy_]).strip():
      bstack1lll11l1ll_opy_[key] = os.environ[bstack1ll1l1ll1_opy_]
  if bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1lll11l1ll_opy_[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1lll11l1ll_opy_[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1ll1111l1_opy_():
  global bstack1111l1l1l_opy_
  global bstack1ll11llll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1lll11l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack1111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack1111l1l1l_opy_[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lll1ll1_opy_ in bstack1l1l1lll1_opy_.items():
    if isinstance(bstack1lll1ll1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll1ll1_opy_:
          if idx < len(sys.argv) and bstack1lll11l_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack1111l1l1l_opy_:
            bstack1111l1l1l_opy_[key] = sys.argv[idx + 1]
            bstack1ll11llll_opy_ += bstack1lll11l_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack1lll11l_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1lll11l_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack1lll1ll1_opy_.lower() == val.lower() and not key in bstack1111l1l1l_opy_:
          bstack1111l1l1l_opy_[key] = sys.argv[idx + 1]
          bstack1ll11llll_opy_ += bstack1lll11l_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack1lll1ll1_opy_ + bstack1lll11l_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1111l111l_opy_(config):
  bstack1ll11111l1_opy_ = config.keys()
  for bstack1l11l111_opy_, bstack1l1llll111_opy_ in bstack111ll111l_opy_.items():
    if bstack1l1llll111_opy_ in bstack1ll11111l1_opy_:
      config[bstack1l11l111_opy_] = config[bstack1l1llll111_opy_]
      del config[bstack1l1llll111_opy_]
  for bstack1l11l111_opy_, bstack1l1llll111_opy_ in bstack1l1llll1l1_opy_.items():
    if isinstance(bstack1l1llll111_opy_, list):
      for bstack1l11111ll_opy_ in bstack1l1llll111_opy_:
        if bstack1l11111ll_opy_ in bstack1ll11111l1_opy_:
          config[bstack1l11l111_opy_] = config[bstack1l11111ll_opy_]
          del config[bstack1l11111ll_opy_]
          break
    elif bstack1l1llll111_opy_ in bstack1ll11111l1_opy_:
      config[bstack1l11l111_opy_] = config[bstack1l1llll111_opy_]
      del config[bstack1l1llll111_opy_]
  for bstack1l11111ll_opy_ in list(config):
    for bstack1l111l1l_opy_ in bstack11ll1111_opy_:
      if bstack1l11111ll_opy_.lower() == bstack1l111l1l_opy_.lower() and bstack1l11111ll_opy_ != bstack1l111l1l_opy_:
        config[bstack1l111l1l_opy_] = config[bstack1l11111ll_opy_]
        del config[bstack1l11111ll_opy_]
  bstack1111ll11_opy_ = []
  if bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1111ll11_opy_ = config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1111ll11_opy_:
    for bstack1l11111ll_opy_ in list(platform):
      for bstack1l111l1l_opy_ in bstack11ll1111_opy_:
        if bstack1l11111ll_opy_.lower() == bstack1l111l1l_opy_.lower() and bstack1l11111ll_opy_ != bstack1l111l1l_opy_:
          platform[bstack1l111l1l_opy_] = platform[bstack1l11111ll_opy_]
          del platform[bstack1l11111ll_opy_]
  for bstack1l11l111_opy_, bstack1l1llll111_opy_ in bstack1l1llll1l1_opy_.items():
    for platform in bstack1111ll11_opy_:
      if isinstance(bstack1l1llll111_opy_, list):
        for bstack1l11111ll_opy_ in bstack1l1llll111_opy_:
          if bstack1l11111ll_opy_ in platform:
            platform[bstack1l11l111_opy_] = platform[bstack1l11111ll_opy_]
            del platform[bstack1l11111ll_opy_]
            break
      elif bstack1l1llll111_opy_ in platform:
        platform[bstack1l11l111_opy_] = platform[bstack1l1llll111_opy_]
        del platform[bstack1l1llll111_opy_]
  for bstack1lll1l1111_opy_ in bstack11ll1l111_opy_:
    if bstack1lll1l1111_opy_ in config:
      if not bstack11ll1l111_opy_[bstack1lll1l1111_opy_] in config:
        config[bstack11ll1l111_opy_[bstack1lll1l1111_opy_]] = {}
      config[bstack11ll1l111_opy_[bstack1lll1l1111_opy_]].update(config[bstack1lll1l1111_opy_])
      del config[bstack1lll1l1111_opy_]
  for platform in bstack1111ll11_opy_:
    for bstack1lll1l1111_opy_ in bstack11ll1l111_opy_:
      if bstack1lll1l1111_opy_ in list(platform):
        if not bstack11ll1l111_opy_[bstack1lll1l1111_opy_] in platform:
          platform[bstack11ll1l111_opy_[bstack1lll1l1111_opy_]] = {}
        platform[bstack11ll1l111_opy_[bstack1lll1l1111_opy_]].update(platform[bstack1lll1l1111_opy_])
        del platform[bstack1lll1l1111_opy_]
  config = bstack1lll1l1lll_opy_(config)
  return config
def bstack111ll11l_opy_(config):
  global bstack1ll11ll1l_opy_
  if bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack1lll11l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      bstack11l1l1l1_opy_ = bstack11l111ll1_opy_.strftime(bstack1lll11l_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack1lllll1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lll11l_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack11l1l1l1_opy_, hostname, bstack1lllll1ll_opy_)
      config[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack1lll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1ll11ll1l_opy_ = config[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack11111ll1l_opy_():
  bstack1l1l11ll_opy_ =  bstack11lll111l_opy_()[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack1l1l11ll_opy_ if bstack1l1l11ll_opy_ else -1
def bstack1lll111111_opy_(bstack1l1l11ll_opy_):
  global CONFIG
  if not bstack1lll11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack1lll11l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack1l1l11ll_opy_)
  )
def bstack1l111l11l_opy_():
  global CONFIG
  if not bstack1lll11l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack11l111ll1_opy_ = datetime.datetime.now()
  bstack11l1l1l1_opy_ = bstack11l111ll1_opy_.strftime(bstack1lll11l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack1lll11l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack11l1l1l1_opy_
  )
def bstack1l11111l1_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack1lll11l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack1lll11l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack1l111l11l_opy_()
    os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack1lll11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack1l1l11ll_opy_ = bstack1lll11l_opy_ (u"ࠪࠫࣟ")
  bstack111lll11l_opy_ = bstack11111ll1l_opy_()
  if bstack111lll11l_opy_ != -1:
    bstack1l1l11ll_opy_ = bstack1lll11l_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack111lll11l_opy_)
  if bstack1l1l11ll_opy_ == bstack1lll11l_opy_ (u"ࠬ࠭࣡"):
    bstack1l1ll11ll1_opy_ = bstack1l1lll111l_opy_(CONFIG[bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack1l1ll11ll1_opy_ != -1:
      bstack1l1l11ll_opy_ = str(bstack1l1ll11ll1_opy_)
  if bstack1l1l11ll_opy_:
    bstack1lll111111_opy_(bstack1l1l11ll_opy_)
    os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack11111lll_opy_(bstack1ll1l11lll_opy_, bstack11lll1ll1_opy_, path):
  bstack111l1l1l1_opy_ = {
    bstack1lll11l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack11lll1ll1_opy_
  }
  if os.path.exists(path):
    bstack1l1lllll1_opy_ = json.load(open(path, bstack1lll11l_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1l1lllll1_opy_ = {}
  bstack1l1lllll1_opy_[bstack1ll1l11lll_opy_] = bstack111l1l1l1_opy_
  with open(path, bstack1lll11l_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1l1lllll1_opy_, outfile)
def bstack1l1lll111l_opy_(bstack1ll1l11lll_opy_):
  bstack1ll1l11lll_opy_ = str(bstack1ll1l11lll_opy_)
  bstack1l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧࣨ")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack1l11l1ll_opy_):
      os.makedirs(bstack1l11l1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠧࡿࠩ࣪")), bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack1lll11l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lll11l_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack1lll11l_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lll11l_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1111ll11l_opy_:
      bstack11111ll1_opy_ = json.load(bstack1111ll11l_opy_)
    if bstack1ll1l11lll_opy_ in bstack11111ll1_opy_:
      bstack1l1l1ll11_opy_ = bstack11111ll1_opy_[bstack1ll1l11lll_opy_][bstack1lll11l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack1llll1ll_opy_ = int(bstack1l1l1ll11_opy_) + 1
      bstack11111lll_opy_(bstack1ll1l11lll_opy_, bstack1llll1ll_opy_, file_path)
      return bstack1llll1ll_opy_
    else:
      bstack11111lll_opy_(bstack1ll1l11lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111l11l11_opy_.format(str(e)))
    return -1
def bstack1111llll_opy_(config):
  if not config[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack1l11l1ll1_opy_(config, index=0):
  global bstack1l1l1lll_opy_
  bstack1ll1l1111l_opy_ = {}
  caps = bstack11ll111l1_opy_ + bstack1ll1ll1l_opy_
  if bstack1l1l1lll_opy_:
    caps += bstack1l1111ll_opy_
  for key in config:
    if key in caps + [bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1ll1l1111l_opy_[key] = config[key]
  if bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack11111111l_opy_ in config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack11111111l_opy_ in caps + [bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1ll1l1111l_opy_[bstack11111111l_opy_] = config[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack11111111l_opy_]
  bstack1ll1l1111l_opy_[bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack1lll11l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1ll1l1111l_opy_:
    del (bstack1ll1l1111l_opy_[bstack1lll11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1ll1l1111l_opy_
def bstack1l1l11l11_opy_(config):
  global bstack1l1l1lll_opy_
  bstack1lll1ll1l1_opy_ = {}
  caps = bstack1ll1ll1l_opy_
  if bstack1l1l1lll_opy_:
    caps += bstack1l1111ll_opy_
  for key in caps:
    if key in config:
      bstack1lll1ll1l1_opy_[key] = config[key]
  return bstack1lll1ll1l1_opy_
def bstack1l111ll1l_opy_(bstack1ll1l1111l_opy_, bstack1lll1ll1l1_opy_):
  bstack111111l1_opy_ = {}
  for key in bstack1ll1l1111l_opy_.keys():
    if key in bstack111ll111l_opy_:
      bstack111111l1_opy_[bstack111ll111l_opy_[key]] = bstack1ll1l1111l_opy_[key]
    else:
      bstack111111l1_opy_[key] = bstack1ll1l1111l_opy_[key]
  for key in bstack1lll1ll1l1_opy_:
    if key in bstack111ll111l_opy_:
      bstack111111l1_opy_[bstack111ll111l_opy_[key]] = bstack1lll1ll1l1_opy_[key]
    else:
      bstack111111l1_opy_[key] = bstack1lll1ll1l1_opy_[key]
  return bstack111111l1_opy_
def bstack111111ll_opy_(config, index=0):
  global bstack1l1l1lll_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lll1ll1l1_opy_ = bstack1l1l11l11_opy_(config)
  bstack1ll111ll11_opy_ = bstack1ll1ll1l_opy_
  bstack1ll111ll11_opy_ += bstack111llll1_opy_
  if bstack1l1l1lll_opy_:
    bstack1ll111ll11_opy_ += bstack1l1111ll_opy_
  if bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack1llllll1l_opy_ = {}
    for bstack1l111ll11_opy_ in bstack1ll111ll11_opy_:
      if bstack1l111ll11_opy_ in config[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l111ll11_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack1llllll1l_opy_[bstack1l111ll11_opy_] = str(config[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l111ll11_opy_] * 1.0)
          except:
            bstack1llllll1l_opy_[bstack1l111ll11_opy_] = str(config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l111ll11_opy_])
        else:
          bstack1llllll1l_opy_[bstack1l111ll11_opy_] = config[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l111ll11_opy_]
        del (config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l111ll11_opy_])
    bstack1lll1ll1l1_opy_ = update(bstack1lll1ll1l1_opy_, bstack1llllll1l_opy_)
  bstack1ll1l1111l_opy_ = bstack1l11l1ll1_opy_(config, index)
  for bstack1l11111ll_opy_ in bstack1ll1ll1l_opy_ + [bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1l11111ll_opy_ in bstack1ll1l1111l_opy_:
      bstack1lll1ll1l1_opy_[bstack1l11111ll_opy_] = bstack1ll1l1111l_opy_[bstack1l11111ll_opy_]
      del (bstack1ll1l1111l_opy_[bstack1l11111ll_opy_])
  if bstack1lllll1l11_opy_(config):
    bstack1ll1l1111l_opy_[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1lll1ll1l1_opy_)
    caps[bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1ll1l1111l_opy_
  else:
    bstack1ll1l1111l_opy_[bstack1lll11l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack1l111ll1l_opy_(bstack1ll1l1111l_opy_, bstack1lll1ll1l1_opy_))
    if bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack11l1111l_opy_():
  global bstack1lll111l1l_opy_
  if bstack1llll1l1_opy_() <= version.parse(bstack1lll11l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack1lll111l1l_opy_ != bstack1lll11l_opy_ (u"ࠧࠨछ"):
      return bstack1lll11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack1lll111l1l_opy_ + bstack1lll11l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack1lll1l11_opy_
  if bstack1lll111l1l_opy_ != bstack1lll11l_opy_ (u"ࠪࠫञ"):
    return bstack1lll11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack1lll111l1l_opy_ + bstack1lll11l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack11l11l11_opy_
def bstack11l11lll_opy_(options):
  return hasattr(options, bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1111l11l1_opy_(options, bstack1111ll1l_opy_):
  for bstack1111lllll_opy_ in bstack1111ll1l_opy_:
    if bstack1111lllll_opy_ in [bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack1lll11l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack1111lllll_opy_ in options._experimental_options:
      options._experimental_options[bstack1111lllll_opy_] = update(options._experimental_options[bstack1111lllll_opy_],
                                                         bstack1111ll1l_opy_[bstack1111lllll_opy_])
    else:
      options.add_experimental_option(bstack1111lllll_opy_, bstack1111ll1l_opy_[bstack1111lllll_opy_])
  if bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack1111ll1l_opy_:
    for arg in bstack1111ll1l_opy_[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack1111ll1l_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack1lll11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack1111ll1l_opy_:
    for ext in bstack1111ll1l_opy_[bstack1lll11l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack1111ll1l_opy_[bstack1lll11l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1l11ll1l_opy_(options, bstack1l1ll111ll_opy_):
  if bstack1lll11l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1l1ll111ll_opy_:
    for bstack111l1111_opy_ in bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack111l1111_opy_ in options._preferences:
        options._preferences[bstack111l1111_opy_] = update(options._preferences[bstack111l1111_opy_], bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack111l1111_opy_])
      else:
        options.set_preference(bstack111l1111_opy_, bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack111l1111_opy_])
  if bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1l1ll111ll_opy_:
    for arg in bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack1l1l111l1_opy_(options, bstack1l11ll111_opy_):
  if bstack1lll11l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1l11ll111_opy_:
    options.use_webview(bool(bstack1l11ll111_opy_[bstack1lll11l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1111l11l1_opy_(options, bstack1l11ll111_opy_)
def bstack11l11111l_opy_(options, bstack1lll11l1l_opy_):
  for bstack1l1ll11lll_opy_ in bstack1lll11l1l_opy_:
    if bstack1l1ll11lll_opy_ in [bstack1lll11l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1l1ll11lll_opy_, bstack1lll11l1l_opy_[bstack1l1ll11lll_opy_])
  if bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1lll11l1l_opy_:
    for arg in bstack1lll11l1l_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack1lll11l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1lll11l1l_opy_:
    options.bstack11l1l1l1l_opy_(bool(bstack1lll11l1l_opy_[bstack1lll11l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1lllll11l_opy_(options, bstack1ll111ll_opy_):
  for bstack1l1llll1_opy_ in bstack1ll111ll_opy_:
    if bstack1l1llll1_opy_ in [bstack1lll11l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1l1llll1_opy_] = bstack1ll111ll_opy_[bstack1l1llll1_opy_]
  if bstack1lll11l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1ll111ll_opy_:
    for bstack11lll1ll_opy_ in bstack1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack11llll11_opy_(
        bstack11lll1ll_opy_, bstack1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack11lll1ll_opy_])
  if bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1ll111ll_opy_:
    for arg in bstack1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack1ll11l1ll_opy_(options, caps):
  if not hasattr(options, bstack1lll11l_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack1lll11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1111l11l1_opy_(options, caps[bstack1lll11l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1l11ll1l_opy_(options, caps[bstack1lll11l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack1lll11l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack11l11111l_opy_(options, caps[bstack1lll11l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack1l1l111l1_opy_(options, caps[bstack1lll11l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1lllll11l_opy_(options, caps[bstack1lll11l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1lllll111_opy_(caps):
  global bstack1l1l1lll_opy_
  if isinstance(os.environ.get(bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack1l1l1lll_opy_ = eval(os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack1l1l1lll_opy_:
    if bstack1l111l111_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lll11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack1lll11l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack1lll11l_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack1lll11l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack1lll11l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack1lll11l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack1lll11l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack1lll11l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack1lll11l_opy_ (u"࠭ࡩࡦࠩख़"), bstack1lll11l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack1lll11l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack1lll11l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l11lll_opy_(options):
        return None
      for bstack1l11111ll_opy_ in caps.keys():
        options.set_capability(bstack1l11111ll_opy_, caps[bstack1l11111ll_opy_])
      bstack1ll11l1ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1ll1_opy_(options, bstack11ll1ll1l_opy_):
  if not bstack11l11lll_opy_(options):
    return
  for bstack1l11111ll_opy_ in bstack11ll1ll1l_opy_.keys():
    if bstack1l11111ll_opy_ in bstack111llll1_opy_:
      continue
    if bstack1l11111ll_opy_ in options._caps and type(options._caps[bstack1l11111ll_opy_]) in [dict, list]:
      options._caps[bstack1l11111ll_opy_] = update(options._caps[bstack1l11111ll_opy_], bstack11ll1ll1l_opy_[bstack1l11111ll_opy_])
    else:
      options.set_capability(bstack1l11111ll_opy_, bstack11ll1ll1l_opy_[bstack1l11111ll_opy_])
  bstack1ll11l1ll_opy_(options, bstack11ll1ll1l_opy_)
  if bstack1lll11l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack1lll11l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1lllll1l1l_opy_(proxy_config):
  if bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack1lll11l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack1lll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack1lll11l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack1lll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack1lll11l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack1lll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack1lll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack1lll11l_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1ll1ll1ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack1lll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1lllll1l1l_opy_(config[bstack1lll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack1lll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack111l1l1l_opy_(self):
  global CONFIG
  global bstack1llll11ll_opy_
  try:
    proxy = bstack11llllll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lll11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack1ll11l111_opy_(proxy, bstack11l1111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll11l11_opy_ = proxies.popitem()
          if bstack1lll11l_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1lll11l11_opy_:
            return bstack1lll11l11_opy_
          else:
            return bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1lll11l11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lll11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1llll11ll_opy_(self)
def bstack1llll111_opy_():
  global CONFIG
  return bstack1l1lll1ll_opy_(CONFIG) and bstack1llll11l11_opy_() and bstack1llll1l1_opy_() >= version.parse(bstack1l1111l1l_opy_)
def bstack111l11111_opy_():
  global CONFIG
  return (bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1ll11ll1ll_opy_()
def bstack1111111l_opy_(config):
  bstack1ll1lll111_opy_ = {}
  if bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1ll1lll111_opy_ = config[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1ll1lll111_opy_ = config[bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack11llllll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lll11l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1ll1lll111_opy_[bstack1lll11l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lll11l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1llll11l1l_opy_(config, bstack11l1111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll11l11_opy_ = proxies.popitem()
          if bstack1lll11l_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1lll11l11_opy_:
            parsed_url = urlparse(bstack1lll11l11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lll11l_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1lll11l11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1lll111_opy_[bstack1lll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1lll111_opy_[bstack1lll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1lll111_opy_[bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1lll111_opy_[bstack1lll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1ll1lll111_opy_
def bstack1l1llll11l_opy_(config):
  if bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack111l111ll_opy_(caps):
  global bstack1ll11ll1l_opy_
  if bstack1lll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1ll11ll1l_opy_:
      caps[bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack1lll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1ll11ll1l_opy_
  else:
    caps[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1ll11ll1l_opy_:
      caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1ll11ll1l_opy_
def bstack1ll11l1l1l_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack1lll11ll1_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1ll1lll111_opy_ = bstack1111111l_opy_(CONFIG)
    bstack1ll1l1l11_opy_(CONFIG[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll1lll111_opy_)
def bstack1ll1l1l11_opy_(key, bstack1ll1lll111_opy_):
  global bstack1l1lllllll_opy_
  logger.info(bstack1l1l1111_opy_)
  try:
    bstack1l1lllllll_opy_ = Local()
    bstack11ll111l_opy_ = {bstack1lll11l_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack11ll111l_opy_.update(bstack1ll1lll111_opy_)
    logger.debug(bstack1llll1l1l_opy_.format(str(bstack11ll111l_opy_)))
    bstack1l1lllllll_opy_.start(**bstack11ll111l_opy_)
    if bstack1l1lllllll_opy_.isRunning():
      logger.info(bstack111l11ll_opy_)
  except Exception as e:
    bstack1l111lll_opy_(bstack11lllll1_opy_.format(str(e)))
def bstack1ll1ll1111_opy_():
  global bstack1l1lllllll_opy_
  if bstack1l1lllllll_opy_.isRunning():
    logger.info(bstack1l11l11l1_opy_)
    bstack1l1lllllll_opy_.stop()
  bstack1l1lllllll_opy_ = None
def bstack1l11ll11_opy_(bstack111lll111_opy_=[]):
  global CONFIG
  bstack1lllll111l_opy_ = []
  bstack1111l1111_opy_ = [bstack1lll11l_opy_ (u"ࠨࡱࡶࠫও"), bstack1lll11l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1lll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack111lll111_opy_:
      bstack11ll11l11_opy_ = {}
      for k in bstack1111l1111_opy_:
        val = CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack11ll11l11_opy_[k] = val
      if(err[bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1lll11l_opy_ (u"ࠪࠫজ")):
        bstack11ll11l11_opy_[bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1lll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1lllll111l_opy_.append(bstack11ll11l11_opy_)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1lllll111l_opy_
def bstack1l1ll1l1ll_opy_(file_name):
  bstack1ll11lll1_opy_ = []
  try:
    bstack111ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111ll1l1l_opy_):
      with open(bstack111ll1l1l_opy_) as f:
        bstack11l1ll1l_opy_ = json.load(f)
        bstack1ll11lll1_opy_ = bstack11l1ll1l_opy_
      os.remove(bstack111ll1l1l_opy_)
    return bstack1ll11lll1_opy_
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack1llllll1ll_opy_():
  global bstack1lllll11l1_opy_
  global bstack111l1ll1l_opy_
  global bstack1111ll1ll_opy_
  global bstack1lll111l_opy_
  global bstack1l11l11l_opy_
  global bstack11l1ll1l1_opy_
  percy.shutdown()
  bstack1ll11lllll_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1ll11lllll_opy_ in [bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1l1lll11ll_opy_()
  if bstack1lllll11l1_opy_:
    logger.warning(bstack11ll1111l_opy_.format(str(bstack1lllll11l1_opy_)))
  else:
    try:
      bstack1l1lllll1_opy_ = bstack11l1l11l1_opy_(bstack1lll11l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1lllll1_opy_.get(bstack1lll11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1lllll1_opy_.get(bstack1lll11l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack11ll1111l_opy_.format(str(bstack1l1lllll1_opy_[bstack1lll11l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11llll11l_opy_)
  global bstack1l1lllllll_opy_
  if bstack1l1lllllll_opy_:
    bstack1ll1ll1111_opy_()
  try:
    for driver in bstack111l1ll1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11l111l_opy_)
  if bstack11l1ll1l1_opy_ == bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l11l11l_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack11l1ll1l1_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1lll111l_opy_) == 0:
    bstack1lll111l_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll11l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1lll111l_opy_) == 0:
      bstack1lll111l_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1l1ll1llll_opy_ = bstack1lll11l_opy_ (u"ࠩࠪর")
  if len(bstack1111ll1ll_opy_) > 0:
    bstack1l1ll1llll_opy_ = bstack1l11ll11_opy_(bstack1111ll1ll_opy_)
  elif len(bstack1lll111l_opy_) > 0:
    bstack1l1ll1llll_opy_ = bstack1l11ll11_opy_(bstack1lll111l_opy_)
  elif len(bstack1l11l11l_opy_) > 0:
    bstack1l1ll1llll_opy_ = bstack1l11ll11_opy_(bstack1l11l11l_opy_)
  elif len(bstack111l1lll_opy_) > 0:
    bstack1l1ll1llll_opy_ = bstack1l11ll11_opy_(bstack111l1lll_opy_)
  if bool(bstack1l1ll1llll_opy_):
    bstack1111111ll_opy_(bstack1l1ll1llll_opy_)
  else:
    bstack1111111ll_opy_()
  bstack1l1ll111l1_opy_(bstack1l11ll1ll_opy_, logger)
def bstack1ll1ll111_opy_(self, *args):
  logger.error(bstack1lll11ll11_opy_)
  bstack1llllll1ll_opy_()
  sys.exit(1)
def bstack1l111lll_opy_(err):
  logger.critical(bstack11l111ll_opy_.format(str(err)))
  bstack1111111ll_opy_(bstack11l111ll_opy_.format(str(err)), True)
  atexit.unregister(bstack1llllll1ll_opy_)
  bstack1l1lll11ll_opy_()
  sys.exit(1)
def bstack1l11lll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1111111ll_opy_(message, True)
  atexit.unregister(bstack1llllll1ll_opy_)
  bstack1l1lll11ll_opy_()
  sys.exit(1)
def bstack1lll1lll1l_opy_():
  global CONFIG
  global bstack1111l1l1l_opy_
  global bstack1lll11l1ll_opy_
  global bstack1lll11llll_opy_
  CONFIG = bstack11l11ll11_opy_()
  bstack1ll1lllll1_opy_()
  bstack1ll1111l1_opy_()
  CONFIG = bstack1111l111l_opy_(CONFIG)
  update(CONFIG, bstack1lll11l1ll_opy_)
  update(CONFIG, bstack1111l1l1l_opy_)
  CONFIG = bstack111ll11l_opy_(CONFIG)
  bstack1lll11llll_opy_ = bstack1ll1111l1l_opy_(CONFIG)
  bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1lll11llll_opy_)
  if (bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack1111l1l1l_opy_) or (
          bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1lll11l1ll_opy_):
    if os.getenv(bstack1lll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack1l11111l1_opy_()
  elif (bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1lll11l1ll_opy_ and bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack1111l1l1l_opy_):
    del (CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1111llll_opy_(CONFIG):
    bstack1l111lll_opy_(bstack1l111lll1_opy_)
  bstack11ll1ll11_opy_()
  bstack11111l1l_opy_()
  if bstack1l1l1lll_opy_:
    CONFIG[bstack1lll11l_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1lll11l111_opy_(CONFIG)
    logger.info(bstack11lllll11_opy_.format(CONFIG[bstack1lll11l_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack1lll1l1l_opy_(config, bstack111ll1lll_opy_):
  global CONFIG
  global bstack1l1l1lll_opy_
  CONFIG = config
  bstack1l1l1lll_opy_ = bstack111ll1lll_opy_
def bstack11111l1l_opy_():
  global CONFIG
  global bstack1l1l1lll_opy_
  if bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack1l11l1l1l_opy_)
    bstack1l1l1lll_opy_ = True
    bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1lll11l111_opy_(config):
  bstack1ll111l1ll_opy_ = bstack1lll11l_opy_ (u"࠭ࠧূ")
  app = config[bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11ll1l1l1_opy_:
      if os.path.exists(app):
        bstack1ll111l1ll_opy_ = bstack1l1l1ll1_opy_(config, app)
      elif bstack1lll111ll1_opy_(app):
        bstack1ll111l1ll_opy_ = app
      else:
        bstack1l111lll_opy_(bstack11l111l11_opy_.format(app))
    else:
      if bstack1lll111ll1_opy_(app):
        bstack1ll111l1ll_opy_ = app
      elif os.path.exists(app):
        bstack1ll111l1ll_opy_ = bstack1l1l1ll1_opy_(app)
      else:
        bstack1l111lll_opy_(bstack1llll1111l_opy_)
  else:
    if len(app) > 2:
      bstack1l111lll_opy_(bstack1llllll1l1_opy_)
    elif len(app) == 2:
      if bstack1lll11l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack1lll11l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack1lll11l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack1ll111l1ll_opy_ = bstack1l1l1ll1_opy_(config, app[bstack1lll11l_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack1lll11l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack1l111lll_opy_(bstack11l111l11_opy_.format(app))
      else:
        bstack1l111lll_opy_(bstack1llllll1l1_opy_)
    else:
      for key in app:
        if key in bstack11l11l1l_opy_:
          if key == bstack1lll11l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack1ll111l1ll_opy_ = bstack1l1l1ll1_opy_(config, app[key])
            else:
              bstack1l111lll_opy_(bstack11l111l11_opy_.format(app))
          else:
            bstack1ll111l1ll_opy_ = app[key]
        else:
          bstack1l111lll_opy_(bstack1l1llll11_opy_)
  return bstack1ll111l1ll_opy_
def bstack1lll111ll1_opy_(bstack1ll111l1ll_opy_):
  import re
  bstack111l1ll11_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack111l11lll_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack1lll11l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack1ll111l1ll_opy_ or re.fullmatch(bstack111l1ll11_opy_, bstack1ll111l1ll_opy_) or re.fullmatch(bstack111l11lll_opy_, bstack1ll111l1ll_opy_):
    return True
  else:
    return False
def bstack1l1l1ll1_opy_(config, path, bstack1lllllll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lll11l_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1ll111llll_opy_ = bstack1ll11ll11_opy_(md5_hash)
  bstack1ll111l1ll_opy_ = None
  if bstack1ll111llll_opy_:
    logger.info(bstack1l1ll1l1l1_opy_.format(bstack1ll111llll_opy_, md5_hash))
    return bstack1ll111llll_opy_
  bstack111l111l1_opy_ = MultipartEncoder(
    fields={
      bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack1lll11l_opy_ (u"ࠬࡸࡢࠨ৏")), bstack1lll11l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack1lll11l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack1lllllll1l_opy_
    }
  )
  response = requests.post(bstack1ll1l1l1ll_opy_, data=bstack111l111l1_opy_,
                           headers={bstack1lll11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack111l111l1_opy_.content_type},
                           auth=(config[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack1ll111l1ll_opy_ = res[bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1l1l1ll1l_opy_.format(bstack1ll111l1ll_opy_))
    bstack1lll1l1l1l_opy_(md5_hash, bstack1ll111l1ll_opy_)
  except ValueError as err:
    bstack1l111lll_opy_(bstack1l1ll1lll1_opy_.format(str(err)))
  return bstack1ll111l1ll_opy_
def bstack11ll1ll11_opy_():
  global CONFIG
  global bstack1ll11l1ll1_opy_
  bstack1ll11111_opy_ = 0
  bstack1111l11l_opy_ = 1
  if bstack1lll11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1111l11l_opy_ = CONFIG[bstack1lll11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1ll11111_opy_ = len(CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack1ll11l1ll1_opy_ = int(bstack1111l11l_opy_) * int(bstack1ll11111_opy_)
def bstack1ll11ll11_opy_(md5_hash):
  bstack1ll1111111_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠩࢁࠫ৚")), bstack1lll11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack1ll1111111_opy_):
    bstack1l1lll1111_opy_ = json.load(open(bstack1ll1111111_opy_, bstack1lll11l_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1l1lll1111_opy_:
      bstack1ll1llll1l_opy_ = bstack1l1lll1111_opy_[md5_hash]
      bstack1l1ll11l1l_opy_ = datetime.datetime.now()
      bstack1ll111l1_opy_ = datetime.datetime.strptime(bstack1ll1llll1l_opy_[bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack1lll11l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1l1ll11l1l_opy_ - bstack1ll111l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1llll1l_opy_[bstack1lll11l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack1ll1llll1l_opy_[bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack1lll1l1l1l_opy_(md5_hash, bstack1ll111l1ll_opy_):
  bstack1l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠪࢂࠬৢ")), bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack1l11l1ll_opy_):
    os.makedirs(bstack1l11l1ll_opy_)
  bstack1ll1111111_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧ৤")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack1lll11l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack111lll11_opy_ = {
    bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack1ll111l1ll_opy_,
    bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lll11l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack1lll11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack1ll1111111_opy_):
    bstack1l1lll1111_opy_ = json.load(open(bstack1ll1111111_opy_, bstack1lll11l_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1l1lll1111_opy_ = {}
  bstack1l1lll1111_opy_[md5_hash] = bstack111lll11_opy_
  with open(bstack1ll1111111_opy_, bstack1lll11l_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1l1lll1111_opy_, outfile)
def bstack1ll1l1l1l1_opy_(self):
  return
def bstack1111111l1_opy_(self):
  return
def bstack1l1ll111_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack11l1ll11l_opy_(self):
  global bstack1l1l11l1l_opy_
  global bstack1ll1ll1ll_opy_
  global bstack111lll1l_opy_
  try:
    if bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack1l1l11l1l_opy_ and self.session_id != None and bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack1lll11l_opy_ (u"ࠩࠪ৯")) != bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack1lll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack1lll1l1l1_opy_ == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack1lll11ll_opy_(logger)
      if self != None:
        bstack11llll1l1_opy_(self, bstack1lll1l1l1_opy_, bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1lll11l_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack111lll1l_opy_(self)
  self.session_id = None
def bstack1lll1l11ll_opy_(self, command_executor=bstack1lll11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1lll1111_opy_ = bstack1l1l11ll1_opy_(self, command_executor, *args, **kwargs)
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ৸") in command_executor._url:
      bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭৹"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor):
    bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1llll1ll_opy_.bstack11l111l1_opy_(self)
  return bstack1lll1111_opy_
def bstack1ll1lll1_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll11l1_opy_
  response = bstack1lll11l1_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack1lll11l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬৼ"):
      bstack1l1llll1ll_opy_.bstack1l1lllll11_opy_({
          bstack1lll11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ৽"): response[bstack1lll11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ৾")],
          bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ৿"): bstack1l1llll1ll_opy_.current_test_uuid() if bstack1l1llll1ll_opy_.current_test_uuid() else bstack1l1llll1ll_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1l111ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll1ll1ll_opy_
  global bstack11111llll_opy_
  global bstack1lllll11ll_opy_
  global bstack1ll1111ll1_opy_
  global bstack11lll111_opy_
  global bstack1l1l11l1l_opy_
  global bstack1l1l11ll1_opy_
  global bstack111l1ll1l_opy_
  global bstack1ll1l1ll_opy_
  global bstack111ll11l1_opy_
  CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ਀")] = str(bstack1l1l11l1l_opy_) + str(__version__)
  command_executor = bstack11l1111l_opy_()
  logger.debug(bstack1lll1l111_opy_.format(command_executor))
  proxy = bstack1ll1ll1ll1_opy_(CONFIG, proxy)
  bstack1ll1ll11_opy_ = 0 if bstack11111llll_opy_ < 0 else bstack11111llll_opy_
  try:
    if bstack1ll1111ll1_opy_ is True:
      bstack1ll1ll11_opy_ = int(multiprocessing.current_process().name)
    elif bstack11lll111_opy_ is True:
      bstack1ll1ll11_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll1ll11_opy_ = 0
  bstack11ll1ll1l_opy_ = bstack111111ll_opy_(CONFIG, bstack1ll1ll11_opy_)
  logger.debug(bstack1ll111l111_opy_.format(str(bstack11ll1ll1l_opy_)))
  if bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਁ") in CONFIG and bstack1lll11ll1_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਂ")]):
    bstack111l111ll_opy_(bstack11ll1ll1l_opy_)
  if desired_capabilities:
    bstack1l1lll11_opy_ = bstack1111l111l_opy_(desired_capabilities)
    bstack1l1lll11_opy_[bstack1lll11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨਃ")] = bstack1lllll1l11_opy_(CONFIG)
    bstack1l1ll1ll_opy_ = bstack111111ll_opy_(bstack1l1lll11_opy_)
    if bstack1l1ll1ll_opy_:
      bstack11ll1ll1l_opy_ = update(bstack1l1ll1ll_opy_, bstack11ll1ll1l_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1ll1_opy_(options, bstack11ll1ll1l_opy_)
  if not options:
    options = bstack1lllll111_opy_(bstack11ll1ll1l_opy_)
  bstack111ll11l1_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ਄"))[bstack1ll1ll11_opy_]
  if bstack11l11llll_opy_.bstack111l1111l_opy_(CONFIG, bstack1ll1ll11_opy_) and bstack11l11llll_opy_.bstack1l1ll111l_opy_(bstack11ll1ll1l_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack11l11llll_opy_.set_capabilities(bstack11ll1ll1l_opy_, CONFIG)
  if proxy and bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪਅ")):
    options.proxy(proxy)
  if options and bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪਆ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llll1l1_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਇ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll1ll1l_opy_)
  logger.info(bstack1llllll11_opy_)
  if bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ਈ")):
    bstack1l1l11ll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")):
    bstack1l1l11ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨਊ")):
    bstack1l1l11ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l11ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1ll11111l_opy_ = bstack1lll11l_opy_ (u"ࠩࠪ਋")
    if bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ਌")):
      bstack1ll11111l_opy_ = self.caps.get(bstack1lll11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ਍"))
    else:
      bstack1ll11111l_opy_ = self.capabilities.get(bstack1lll11l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ਎"))
    if bstack1ll11111l_opy_:
      bstack1ll11ll1_opy_(bstack1ll11111l_opy_)
      if bstack1llll1l1_opy_() <= version.parse(bstack1lll11l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ਏ")):
        self.command_executor._url = bstack1lll11l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣਐ") + bstack1lll111l1l_opy_ + bstack1lll11l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ਑")
      else:
        self.command_executor._url = bstack1lll11l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ਒") + bstack1ll11111l_opy_ + bstack1lll11l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦਓ")
      logger.debug(bstack1l11111l_opy_.format(bstack1ll11111l_opy_))
    else:
      logger.debug(bstack1ll1lll1l_opy_.format(bstack1lll11l_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧਔ")))
  except Exception as e:
    logger.debug(bstack1ll1lll1l_opy_.format(e))
  if bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਕ") in bstack1l1l11l1l_opy_:
    bstack1l1l1111l_opy_(bstack11111llll_opy_, bstack1ll1l1ll_opy_)
  bstack1ll1ll1ll_opy_ = self.session_id
  if bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਖ") in bstack1l1l11l1l_opy_ or bstack1lll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧਗ") in bstack1l1l11l1l_opy_ or bstack1lll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਘ") in bstack1l1l11l1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1llll1ll_opy_.bstack11l111l1_opy_(self)
  bstack111l1ll1l_opy_.append(self)
  if bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਙ") in CONFIG and bstack1lll11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਚ") in CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ")][bstack1ll1ll11_opy_]:
    bstack1lllll11ll_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ")][bstack1ll1ll11_opy_][bstack1lll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਝ")]
  logger.debug(bstack11ll11l1l_opy_.format(bstack1ll1ll1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llll1lll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lllll1ll1_opy_
      if(bstack1lll11l_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤਞ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠨࢀࠪਟ")), bstack1lll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਠ"), bstack1lll11l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਡ")), bstack1lll11l_opy_ (u"ࠫࡼ࠭ਢ")) as fp:
          fp.write(bstack1lll11l_opy_ (u"ࠧࠨਣ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣਤ")))):
          with open(args[1], bstack1lll11l_opy_ (u"ࠧࡳࠩਥ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lll11l_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧਦ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll111lll_opy_)
            lines.insert(1, bstack11111l1l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦਧ")), bstack1lll11l_opy_ (u"ࠪࡻࠬਨ")) as bstack1ll1ll1l1_opy_:
              bstack1ll1ll1l1_opy_.writelines(lines)
        CONFIG[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਩")] = str(bstack1l1l11l1l_opy_) + str(__version__)
        bstack1ll1ll11_opy_ = 0 if bstack11111llll_opy_ < 0 else bstack11111llll_opy_
        try:
          if bstack1ll1111ll1_opy_ is True:
            bstack1ll1ll11_opy_ = int(multiprocessing.current_process().name)
          elif bstack11lll111_opy_ is True:
            bstack1ll1ll11_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll1ll11_opy_ = 0
        CONFIG[bstack1lll11l_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧਪ")] = False
        CONFIG[bstack1lll11l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਫ")] = True
        bstack11ll1ll1l_opy_ = bstack111111ll_opy_(CONFIG, bstack1ll1ll11_opy_)
        logger.debug(bstack1ll111l111_opy_.format(str(bstack11ll1ll1l_opy_)))
        if CONFIG.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ")):
          bstack111l111ll_opy_(bstack11ll1ll1l_opy_)
        if bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਭ") in CONFIG and bstack1lll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਮ") in CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ")][bstack1ll1ll11_opy_]:
          bstack1lllll11ll_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")][bstack1ll1ll11_opy_][bstack1lll11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ਱")]
        args.append(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"࠭ࡾࠨਲ")), bstack1lll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧਲ਼"), bstack1lll11l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ਴")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11ll1ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦਵ"))
      bstack1lllll1ll1_opy_ = True
      return bstack1ll1l11ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll11ll1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11111llll_opy_
    global bstack1lllll11ll_opy_
    global bstack1ll1111ll1_opy_
    global bstack11lll111_opy_
    global bstack1l1l11l1l_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬਸ਼")] = str(bstack1l1l11l1l_opy_) + str(__version__)
    bstack1ll1ll11_opy_ = 0 if bstack11111llll_opy_ < 0 else bstack11111llll_opy_
    try:
      if bstack1ll1111ll1_opy_ is True:
        bstack1ll1ll11_opy_ = int(multiprocessing.current_process().name)
      elif bstack11lll111_opy_ is True:
        bstack1ll1ll11_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll1ll11_opy_ = 0
    CONFIG[bstack1lll11l_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ਷")] = True
    bstack11ll1ll1l_opy_ = bstack111111ll_opy_(CONFIG, bstack1ll1ll11_opy_)
    logger.debug(bstack1ll111l111_opy_.format(str(bstack11ll1ll1l_opy_)))
    if CONFIG.get(bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩਸ")):
      bstack111l111ll_opy_(bstack11ll1ll1l_opy_)
    if bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਹ") in CONFIG and bstack1lll11l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ਺") in CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻")][bstack1ll1ll11_opy_]:
      bstack1lllll11ll_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ਼ࠬ")][bstack1ll1ll11_opy_][bstack1lll11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ਽")]
    import urllib
    import json
    bstack111l1l11_opy_ = bstack1lll11l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ਾ") + urllib.parse.quote(json.dumps(bstack11ll1ll1l_opy_))
    browser = self.connect(bstack111l1l11_opy_)
    return browser
except Exception as e:
    pass
def bstack111lllll1_opy_():
    global bstack1lllll1ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll11ll1l_opy_
        bstack1lllll1ll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll1lll_opy_
      bstack1lllll1ll1_opy_ = True
    except Exception as e:
      pass
def bstack1111l11ll_opy_(context, bstack1111lll11_opy_):
  try:
    context.page.evaluate(bstack1lll11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨਿ"), bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪੀ")+ json.dumps(bstack1111lll11_opy_) + bstack1lll11l_opy_ (u"ࠢࡾࡿࠥੁ"))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨੂ"), e)
def bstack1ll1l111l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lll11l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ੃"), bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ੄") + json.dumps(message) + bstack1lll11l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ੅") + json.dumps(level) + bstack1lll11l_opy_ (u"ࠬࢃࡽࠨ੆"))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤੇ"), e)
def bstack1ll1lll11l_opy_(self, url):
  global bstack1lllllll11_opy_
  try:
    bstack111l1ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1llll1l11_opy_.format(str(err)))
  try:
    bstack1lllllll11_opy_(self, url)
  except Exception as e:
    try:
      bstack1llllllll_opy_ = str(e)
      if any(err_msg in bstack1llllllll_opy_ for err_msg in bstack1lll111l11_opy_):
        bstack111l1ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1llll1l11_opy_.format(str(err)))
    raise e
def bstack1lllll11_opy_(self):
  global bstack1lll1l1ll_opy_
  bstack1lll1l1ll_opy_ = self
  return
def bstack1lll11111l_opy_(self):
  global bstack111111ll1_opy_
  bstack111111ll1_opy_ = self
  return
def bstack1ll1l11l1_opy_(self, test):
  global CONFIG
  global bstack111111ll1_opy_
  global bstack1lll1l1ll_opy_
  global bstack1ll1ll1ll_opy_
  global bstack11ll111ll_opy_
  global bstack1lllll11ll_opy_
  global bstack1lll111l1_opy_
  global bstack11l11ll1_opy_
  global bstack111111l1l_opy_
  global bstack111l1ll1l_opy_
  global bstack111ll11l1_opy_
  try:
    if not bstack1ll1ll1ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠧࡿࠩੈ")), bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੉"), bstack1lll11l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੊"))) as f:
        bstack111llll1l_opy_ = json.loads(bstack1lll11l_opy_ (u"ࠥࡿࠧੋ") + f.read().strip() + bstack1lll11l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ੌ") + bstack1lll11l_opy_ (u"ࠧࢃ੍ࠢ"))
        bstack1ll1ll1ll_opy_ = bstack111llll1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack111l1ll1l_opy_:
    for driver in bstack111l1ll1l_opy_:
      if bstack1ll1ll1ll_opy_ == driver.session_id:
        if test:
          bstack1l1lll11l_opy_ = str(test.data)
          if bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ੎"), None) and bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭੏"), None):
            logger.info(bstack1lll11l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ੐"))
            bstack11l11llll_opy_.bstack1l1111lll_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack11llllll1_opy_=bstack111ll11l1_opy_)
        if not bstack1llll111ll_opy_ and bstack1l1lll11l_opy_:
          bstack1l111111_opy_ = {
            bstack1lll11l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩੑ"): bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ੒"),
            bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੓"): {
              bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ੔"): bstack1l1lll11l_opy_
            }
          }
          bstack1lllllll1_opy_ = bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੕").format(json.dumps(bstack1l111111_opy_))
          driver.execute_script(bstack1lllllll1_opy_)
        if bstack11ll111ll_opy_:
          bstack11l1l111_opy_ = {
            bstack1lll11l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੖"): bstack1lll11l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ੗"),
            bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੘"): {
              bstack1lll11l_opy_ (u"ࠪࡨࡦࡺࡡࠨਖ਼"): bstack1l1lll11l_opy_ + bstack1lll11l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ਗ਼"),
              bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫਜ਼"): bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫੜ")
            }
          }
          if bstack11ll111ll_opy_.status == bstack1lll11l_opy_ (u"ࠧࡑࡃࡖࡗࠬ੝"):
            bstack11l11l11l_opy_ = bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack11l1l111_opy_))
            driver.execute_script(bstack11l11l11l_opy_)
            bstack11llll1l1_opy_(driver, bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੟"))
          elif bstack11ll111ll_opy_.status == bstack1lll11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ੠"):
            reason = bstack1lll11l_opy_ (u"ࠦࠧ੡")
            bstack1ll1ll1l1l_opy_ = bstack1l1lll11l_opy_ + bstack1lll11l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭੢")
            if bstack11ll111ll_opy_.message:
              reason = str(bstack11ll111ll_opy_.message)
              bstack1ll1ll1l1l_opy_ = bstack1ll1ll1l1l_opy_ + bstack1lll11l_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭੣") + reason
            bstack11l1l111_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੤")] = {
              bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ੥"): bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ੦"),
              bstack1lll11l_opy_ (u"ࠪࡨࡦࡺࡡࠨ੧"): bstack1ll1ll1l1l_opy_
            }
            bstack11l11l11l_opy_ = bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੨").format(json.dumps(bstack11l1l111_opy_))
            driver.execute_script(bstack11l11l11l_opy_)
            bstack11llll1l1_opy_(driver, bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੩"), reason)
            bstack11ll1lll_opy_(reason, str(bstack11ll111ll_opy_), str(bstack11111llll_opy_), logger)
  elif bstack1ll1ll1ll_opy_:
    try:
      data = {}
      bstack1l1lll11l_opy_ = None
      if test:
        bstack1l1lll11l_opy_ = str(test.data)
      if not bstack1llll111ll_opy_ and bstack1l1lll11l_opy_:
        data[bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੪")] = bstack1l1lll11l_opy_
      if bstack11ll111ll_opy_:
        if bstack11ll111ll_opy_.status == bstack1lll11l_opy_ (u"ࠧࡑࡃࡖࡗࠬ੫"):
          data[bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੬")] = bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੭")
        elif bstack11ll111ll_opy_.status == bstack1lll11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ੮"):
          data[bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੯")] = bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬੰ")
          if bstack11ll111ll_opy_.message:
            data[bstack1lll11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ੱ")] = str(bstack11ll111ll_opy_.message)
      user = CONFIG[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩੲ")]
      key = CONFIG[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫੳ")]
      url = bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧੴ").format(user, key, bstack1ll1ll1ll_opy_)
      headers = {
        bstack1lll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩੵ"): bstack1lll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ੶"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1llll11ll1_opy_.format(str(e)))
  if bstack111111ll1_opy_:
    bstack11l11ll1_opy_(bstack111111ll1_opy_)
  if bstack1lll1l1ll_opy_:
    bstack111111l1l_opy_(bstack1lll1l1ll_opy_)
  bstack1lll111l1_opy_(self, test)
def bstack1l1l1l1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111ll111_opy_
  global CONFIG
  global bstack111l1ll1l_opy_
  global bstack1ll1ll1ll_opy_
  bstack1l1111ll1_opy_ = None
  try:
    if bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੷"), None):
      try:
        if not bstack1ll1ll1ll_opy_:
          with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"࠭ࡾࠨ੸")), bstack1lll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ੹"), bstack1lll11l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ੺"))) as f:
            bstack111llll1l_opy_ = json.loads(bstack1lll11l_opy_ (u"ࠤࡾࠦ੻") + f.read().strip() + bstack1lll11l_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ੼") + bstack1lll11l_opy_ (u"ࠦࢂࠨ੽"))
            bstack1ll1ll1ll_opy_ = bstack111llll1l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack111l1ll1l_opy_:
        for driver in bstack111l1ll1l_opy_:
          if bstack1ll1ll1ll_opy_ == driver.session_id:
            bstack1l1111ll1_opy_ = driver
    bstack1ll1l11111_opy_ = bstack11l11llll_opy_.bstack1l11lllll_opy_(CONFIG, test.tags)
    if bstack1l1111ll1_opy_:
      threading.current_thread().isA11yTest = bstack11l11llll_opy_.bstack1l1ll1l11_opy_(bstack1l1111ll1_opy_, bstack1ll1l11111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1l11111_opy_
  except:
    pass
  bstack1111ll111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll111ll_opy_
  bstack11ll111ll_opy_ = self._test
def bstack11lll1l1l_opy_():
  global bstack1ll1l1111_opy_
  try:
    if os.path.exists(bstack1ll1l1111_opy_):
      os.remove(bstack1ll1l1111_opy_)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ੾") + str(e))
def bstack11l1l111l_opy_():
  global bstack1ll1l1111_opy_
  bstack1l1lllll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll1l1111_opy_):
      with open(bstack1ll1l1111_opy_, bstack1lll11l_opy_ (u"࠭ࡷࠨ੿")):
        pass
      with open(bstack1ll1l1111_opy_, bstack1lll11l_opy_ (u"ࠢࡸ࠭ࠥ઀")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll1l1111_opy_):
      bstack1l1lllll1_opy_ = json.load(open(bstack1ll1l1111_opy_, bstack1lll11l_opy_ (u"ࠨࡴࡥࠫઁ")))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫં") + str(e))
  finally:
    return bstack1l1lllll1_opy_
def bstack1l1l1111l_opy_(platform_index, item_index):
  global bstack1ll1l1111_opy_
  try:
    bstack1l1lllll1_opy_ = bstack11l1l111l_opy_()
    bstack1l1lllll1_opy_[item_index] = platform_index
    with open(bstack1ll1l1111_opy_, bstack1lll11l_opy_ (u"ࠥࡻ࠰ࠨઃ")) as outfile:
      json.dump(bstack1l1lllll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ઄") + str(e))
def bstack111l11l1_opy_(bstack1l1l1l11_opy_):
  global CONFIG
  bstack1l1l1l111_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭અ")
  if not bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઆ") in CONFIG:
    logger.info(bstack1lll11l_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫઇ"))
  try:
    platform = CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઈ")][bstack1l1l1l11_opy_]
    if bstack1lll11l_opy_ (u"ࠩࡲࡷࠬઉ") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠪࡳࡸ࠭ઊ")]) + bstack1lll11l_opy_ (u"ࠫ࠱ࠦࠧઋ")
    if bstack1lll11l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઌ") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩઍ")]) + bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪ઎")
    if bstack1lll11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬએ") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ઐ")]) + bstack1lll11l_opy_ (u"ࠪ࠰ࠥ࠭ઑ")
    if bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭઒") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧઓ")]) + bstack1lll11l_opy_ (u"࠭ࠬࠡࠩઔ")
    if bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬક") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ખ")]) + bstack1lll11l_opy_ (u"ࠩ࠯ࠤࠬગ")
    if bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫઘ") in platform:
      bstack1l1l1l111_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬઙ")]) + bstack1lll11l_opy_ (u"ࠬ࠲ࠠࠨચ")
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭છ") + str(e))
  finally:
    if bstack1l1l1l111_opy_[len(bstack1l1l1l111_opy_) - 2:] == bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪજ"):
      bstack1l1l1l111_opy_ = bstack1l1l1l111_opy_[:-2]
    return bstack1l1l1l111_opy_
def bstack1llllll111_opy_(path, bstack1l1l1l111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll111ll1l_opy_ = ET.parse(path)
    bstack1111l1ll1_opy_ = bstack1ll111ll1l_opy_.getroot()
    bstack1ll11l11l_opy_ = None
    for suite in bstack1111l1ll1_opy_.iter(bstack1lll11l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧઝ")):
      if bstack1lll11l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩઞ") in suite.attrib:
        suite.attrib[bstack1lll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨટ")] += bstack1lll11l_opy_ (u"ࠫࠥ࠭ઠ") + bstack1l1l1l111_opy_
        bstack1ll11l11l_opy_ = suite
    bstack1111lll1l_opy_ = None
    for robot in bstack1111l1ll1_opy_.iter(bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫડ")):
      bstack1111lll1l_opy_ = robot
    bstack1l11l11ll_opy_ = len(bstack1111lll1l_opy_.findall(bstack1lll11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬઢ")))
    if bstack1l11l11ll_opy_ == 1:
      bstack1111lll1l_opy_.remove(bstack1111lll1l_opy_.findall(bstack1lll11l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ણ"))[0])
      bstack1ll1l1lll_opy_ = ET.Element(bstack1lll11l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧત"), attrib={bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧથ"): bstack1lll11l_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪદ"), bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧધ"): bstack1lll11l_opy_ (u"ࠬࡹ࠰ࠨન")})
      bstack1111lll1l_opy_.insert(1, bstack1ll1l1lll_opy_)
      bstack11l1l1l11_opy_ = None
      for suite in bstack1111lll1l_opy_.iter(bstack1lll11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ઩")):
        bstack11l1l1l11_opy_ = suite
      bstack11l1l1l11_opy_.append(bstack1ll11l11l_opy_)
      bstack11111l11l_opy_ = None
      for status in bstack1ll11l11l_opy_.iter(bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧપ")):
        bstack11111l11l_opy_ = status
      bstack11l1l1l11_opy_.append(bstack11111l11l_opy_)
    bstack1ll111ll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ફ") + str(e))
def bstack1ll1llll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111ll1l11_opy_
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨબ") in options:
    del options[bstack1lll11l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢભ")]
  bstack111l1l1l1_opy_ = bstack11l1l111l_opy_()
  for bstack111ll1ll_opy_ in bstack111l1l1l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫમ"), str(bstack111ll1ll_opy_), bstack1lll11l_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩય"))
    bstack1llllll111_opy_(path, bstack111l11l1_opy_(bstack111l1l1l1_opy_[bstack111ll1ll_opy_]))
  bstack11lll1l1l_opy_()
  return bstack111ll1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11lllll1l_opy_(self, ff_profile_dir):
  global bstack1llll111l_opy_
  if not ff_profile_dir:
    return None
  return bstack1llll111l_opy_(self, ff_profile_dir)
def bstack11l11l1ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11ll1l_opy_
  bstack1lll1ll11_opy_ = []
  if bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩર") in CONFIG:
    bstack1lll1ll11_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ઱")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lll11l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤલ")],
      pabot_args[bstack1lll11l_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥળ")],
      argfile,
      pabot_args.get(bstack1lll11l_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ઴")),
      pabot_args[bstack1lll11l_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢવ")],
      platform[0],
      bstack1ll11ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lll11l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧશ")] or [(bstack1lll11l_opy_ (u"ࠨࠢષ"), None)]
    for platform in enumerate(bstack1lll1ll11_opy_)
  ]
def bstack111l1l111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1111l111_opy_=bstack1lll11l_opy_ (u"ࠧࠨસ")):
  global bstack1l1lll1l11_opy_
  self.platform_index = platform_index
  self.bstack1ll1llll1_opy_ = bstack1111l111_opy_
  bstack1l1lll1l11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1111ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l1lll1_opy_
  global bstack1ll11llll_opy_
  if not bstack1lll11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪહ") in item.options:
    item.options[bstack1lll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ઺")] = []
  for v in item.options[bstack1lll11l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ઻")]:
    if bstack1lll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ઼࡚ࠪ") in v:
      item.options[bstack1lll11l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧઽ")].remove(v)
    if bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ા") in v:
      item.options[bstack1lll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩિ")].remove(v)
  item.options[bstack1lll11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪી")].insert(0, bstack1lll11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫુ").format(item.platform_index))
  item.options[bstack1lll11l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")].insert(0, bstack1lll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫૃ").format(item.bstack1ll1llll1_opy_))
  if bstack1ll11llll_opy_:
    item.options[bstack1lll11l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")].insert(0, bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩૅ").format(bstack1ll11llll_opy_))
  return bstack11l1lll1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11l1llll1_opy_(command, item_index):
  os.environ[bstack1lll11l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૆")] = json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫે")][item_index % bstack111ll1111_opy_])
  global bstack1ll11llll_opy_
  if bstack1ll11llll_opy_:
    command[0] = command[0].replace(bstack1lll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨૈ"), bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧૉ") + str(
      item_index) + bstack1lll11l_opy_ (u"ࠫࠥ࠭૊") + bstack1ll11llll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫો"),
                                    bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪૌ") + str(item_index), 1)
def bstack1llllll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111ll11ll_opy_
  bstack11l1llll1_opy_(command, item_index)
  return bstack111ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111ll11ll_opy_
  bstack11l1llll1_opy_(command, item_index)
  return bstack111ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll111111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111ll11ll_opy_
  bstack11l1llll1_opy_(command, item_index)
  return bstack111ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l1l1111_opy_(self, runner, quiet=False, capture=True):
  global bstack111lll1ll_opy_
  bstack111111111_opy_ = bstack111lll1ll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1lll11l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸ્ࠧ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lll11l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ૎")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111111111_opy_
def bstack1ll1l11l_opy_(self, name, context, *args):
  os.environ[bstack1lll11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૏")] = json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૐ")][int(threading.current_thread()._name) % bstack111ll1111_opy_])
  global bstack1l1lllll_opy_
  if name == bstack1lll11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૑"):
    bstack1l1lllll_opy_(self, name, context, *args)
    try:
      if not bstack1llll111ll_opy_:
        bstack1l1111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1ll_opy_(bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૒")) else context.browser
        bstack1111lll11_opy_ = str(self.feature.name)
        bstack1111l11ll_opy_(context, bstack1111lll11_opy_)
        bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૓") + json.dumps(bstack1111lll11_opy_) + bstack1lll11l_opy_ (u"ࠧࡾࡿࠪ૔"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૕").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૖"):
    bstack1l1lllll_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1lll11l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૗")):
        self.driver_before_scenario = True
      if (not bstack1llll111ll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1111lll11_opy_ = str(self.feature.name)
        bstack1111lll11_opy_ = feature_name + bstack1lll11l_opy_ (u"ࠫࠥ࠳ࠠࠨ૘") + scenario_name
        bstack1l1111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1ll_opy_(bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૙")) else context.browser
        if self.driver_before_scenario:
          bstack1111l11ll_opy_(context, bstack1111lll11_opy_)
          bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૚") + json.dumps(bstack1111lll11_opy_) + bstack1lll11l_opy_ (u"ࠧࡾࡿࠪ૛"))
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ૜").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૝"):
    try:
      bstack1l1lll1l_opy_ = args[0].status.name
      bstack1l1111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૞") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1lll1l_opy_).lower() == bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૟"):
        bstack1l1lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭ૠ")
        bstack1ll1111l_opy_ = bstack1lll11l_opy_ (u"࠭ࠧૡ")
        bstack11111lll1_opy_ = bstack1lll11l_opy_ (u"ࠧࠨૢ")
        try:
          import traceback
          bstack1l1lll1l1l_opy_ = self.exception.__class__.__name__
          bstack1l11l1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll1111l_opy_ = bstack1lll11l_opy_ (u"ࠨࠢࠪૣ").join(bstack1l11l1l1_opy_)
          bstack11111lll1_opy_ = bstack1l11l1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l111ll_opy_.format(str(e)))
        bstack1l1lll1l1l_opy_ += bstack11111lll1_opy_
        bstack1ll1l111l1_opy_(context, json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૤") + str(bstack1ll1111l_opy_)),
                            bstack1lll11l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ૥"))
        if self.driver_before_scenario:
          bstack11ll11lll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠫࡵࡧࡧࡦࠩ૦"), None), bstack1lll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ૧"), bstack1l1lll1l1l_opy_)
          bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૨") + json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૩") + str(bstack1ll1111l_opy_)) + bstack1lll11l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૪"))
        if self.driver_before_scenario:
          bstack11llll1l1_opy_(bstack1l1111ll1_opy_, bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ૫"), bstack1lll11l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ૬") + str(bstack1l1lll1l1l_opy_))
      else:
        bstack1ll1l111l1_opy_(context, bstack1lll11l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ૭"), bstack1lll11l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ૮"))
        if self.driver_before_scenario:
          bstack11ll11lll_opy_(getattr(context, bstack1lll11l_opy_ (u"࠭ࡰࡢࡩࡨࠫ૯"), None), bstack1lll11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૰"))
        bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૱") + json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ૲")) + bstack1lll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ૳"))
        if self.driver_before_scenario:
          bstack11llll1l1_opy_(bstack1l1111ll1_opy_, bstack1lll11l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ૴"))
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ૵").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭૶"):
    try:
      bstack1l1111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1ll_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૷")) else context.browser
      if context.failed is True:
        bstack1ll1l1ll11_opy_ = []
        bstack1ll1lll11_opy_ = []
        bstack1ll11l111l_opy_ = []
        bstack11111l111_opy_ = bstack1lll11l_opy_ (u"ࠨࠩ૸")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1l1ll11_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l11l1l1_opy_ = traceback.format_tb(exc_tb)
            bstack11111l11_opy_ = bstack1lll11l_opy_ (u"ࠩࠣࠫૹ").join(bstack1l11l1l1_opy_)
            bstack1ll1lll11_opy_.append(bstack11111l11_opy_)
            bstack1ll11l111l_opy_.append(bstack1l11l1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l111ll_opy_.format(str(e)))
        bstack1l1lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠪࠫૺ")
        for i in range(len(bstack1ll1l1ll11_opy_)):
          bstack1l1lll1l1l_opy_ += bstack1ll1l1ll11_opy_[i] + bstack1ll11l111l_opy_[i] + bstack1lll11l_opy_ (u"ࠫࡡࡴࠧૻ")
        bstack11111l111_opy_ = bstack1lll11l_opy_ (u"ࠬࠦࠧૼ").join(bstack1ll1lll11_opy_)
        if not self.driver_before_scenario:
          bstack1ll1l111l1_opy_(context, bstack11111l111_opy_, bstack1lll11l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ૽"))
          bstack11ll11lll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠧࡱࡣࡪࡩࠬ૾"), None), bstack1lll11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ૿"), bstack1l1lll1l1l_opy_)
          bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ଀") + json.dumps(bstack11111l111_opy_) + bstack1lll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଁ"))
          bstack11llll1l1_opy_(bstack1l1111ll1_opy_, bstack1lll11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଂ"), bstack1lll11l_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥଃ") + str(bstack1l1lll1l1l_opy_))
          bstack1ll1lllll_opy_ = bstack1llll1ll1l_opy_(bstack11111l111_opy_, self.feature.name, logger)
          if (bstack1ll1lllll_opy_ != None):
            bstack111l1lll_opy_.append(bstack1ll1lllll_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1ll1l111l1_opy_(context, bstack1lll11l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ଄") + str(self.feature.name) + bstack1lll11l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଅ"), bstack1lll11l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨଆ"))
          bstack11ll11lll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଇ"), None), bstack1lll11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥଈ"))
          bstack1l1111ll1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଉ") + json.dumps(bstack1lll11l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଊ") + str(self.feature.name) + bstack1lll11l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଋ")) + bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ଌ"))
          bstack11llll1l1_opy_(bstack1l1111ll1_opy_, bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ଍"))
          bstack1ll1lllll_opy_ = bstack1llll1ll1l_opy_(bstack11111l111_opy_, self.feature.name, logger)
          if (bstack1ll1lllll_opy_ != None):
            bstack111l1lll_opy_.append(bstack1ll1lllll_opy_)
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ଎").format(str(e)))
  else:
    bstack1l1lllll_opy_(self, name, context, *args)
  if name in [bstack1lll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪଏ"), bstack1lll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଐ")]:
    bstack1l1lllll_opy_(self, name, context, *args)
    if (name == bstack1lll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭଑") and self.driver_before_scenario) or (
            name == bstack1lll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭଒") and not self.driver_before_scenario):
      try:
        bstack1l1111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1ll_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଓ")) else context.browser
        bstack1l1111ll1_opy_.quit()
      except Exception:
        pass
def bstack1l1lll11l1_opy_(config, startdir):
  return bstack1lll11l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨଔ").format(bstack1lll11l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣକ"))
notset = Notset()
def bstack1ll1l1l11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1lll1_opy_
  if str(name).lower() == bstack1lll11l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪଖ"):
    return bstack1lll11l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଗ")
  else:
    return bstack1lll1lll1_opy_(self, name, default, skip)
def bstack1ll1111ll_opy_(item, when):
  global bstack1l1llllll1_opy_
  try:
    bstack1l1llllll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1lll11l1l1_opy_():
  return
def bstack1l11lll11_opy_(type, name, status, reason, bstack1l1l11111_opy_, bstack1lll1l111l_opy_):
  bstack1l111111_opy_ = {
    bstack1lll11l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଘ"): type,
    bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଙ"): {}
  }
  if type == bstack1lll11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩଚ"):
    bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଛ")][bstack1lll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨଜ")] = bstack1l1l11111_opy_
    bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଝ")][bstack1lll11l_opy_ (u"ࠫࡩࡧࡴࡢࠩଞ")] = json.dumps(str(bstack1lll1l111l_opy_))
  if type == bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଟ"):
    bstack1l111111_opy_[bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଠ")][bstack1lll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଡ")] = name
  if type == bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫଢ"):
    bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ")][bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪତ")] = status
    if status == bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫଥ"):
      bstack1l111111_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ")][bstack1lll11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ଧ")] = json.dumps(str(reason))
  bstack1lllllll1_opy_ = bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬନ").format(json.dumps(bstack1l111111_opy_))
  return bstack1lllllll1_opy_
def bstack1ll1ll11ll_opy_(driver_command, response):
    if driver_command == bstack1lll11l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ଩"):
        bstack1l1llll1ll_opy_.bstack1l1lllll11_opy_({
            bstack1lll11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨପ"): response[bstack1lll11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩଫ")],
            bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫବ"): bstack1l1llll1ll_opy_.current_test_uuid()
        })
def bstack1ll11lll11_opy_(item, call, rep):
  global bstack11l11l111_opy_
  global bstack111l1ll1l_opy_
  global bstack1llll111ll_opy_
  name = bstack1lll11l_opy_ (u"ࠬ࠭ଭ")
  try:
    if rep.when == bstack1lll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫମ"):
      bstack1ll1ll1ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1llll111ll_opy_:
          name = str(rep.nodeid)
          bstack1l1lll111_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଯ"), name, bstack1lll11l_opy_ (u"ࠨࠩର"), bstack1lll11l_opy_ (u"ࠩࠪ଱"), bstack1lll11l_opy_ (u"ࠪࠫଲ"), bstack1lll11l_opy_ (u"ࠫࠬଳ"))
          threading.current_thread().bstack1ll11l11_opy_ = name
          for driver in bstack111l1ll1l_opy_:
            if bstack1ll1ll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1lll111_opy_)
      except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ଴").format(str(e)))
      try:
        bstack1l1lll1lll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1lll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧଵ"):
          status = bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଶ") if rep.outcome.lower() == bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଷ") else bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩସ")
          reason = bstack1lll11l_opy_ (u"ࠪࠫହ")
          if status == bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ଺"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1lll11l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ଻") if status == bstack1lll11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ଼࠭") else bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ଽ")
          data = name + bstack1lll11l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪା") if status == bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩି") else name + bstack1lll11l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ୀ") + reason
          bstack1ll1l11l11_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ୁ"), bstack1lll11l_opy_ (u"ࠬ࠭ୂ"), bstack1lll11l_opy_ (u"࠭ࠧୃ"), bstack1lll11l_opy_ (u"ࠧࠨୄ"), level, data)
          for driver in bstack111l1ll1l_opy_:
            if bstack1ll1ll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1l11l11_opy_)
      except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୅").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭୆").format(str(e)))
  bstack11l11l111_opy_(item, call, rep)
def bstack1lll1l1ll1_opy_(framework_name):
  global bstack1l1l11l1l_opy_
  global bstack1lllll1ll1_opy_
  global bstack1ll11l11ll_opy_
  bstack1l1l11l1l_opy_ = framework_name
  logger.info(bstack111lll1l1_opy_.format(bstack1l1l11l1l_opy_.split(bstack1lll11l_opy_ (u"ࠪ࠱ࠬେ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lll11llll_opy_:
      Service.start = bstack1ll1l1l1l1_opy_
      Service.stop = bstack1111111l1_opy_
      webdriver.Remote.get = bstack1ll1lll11l_opy_
      WebDriver.close = bstack1l1ll111_opy_
      WebDriver.quit = bstack11l1ll11l_opy_
      webdriver.Remote.__init__ = bstack1l111ll1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1llll111l1_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1ll1llll11_opy_ = getAccessibilityResultsSummary
    if not bstack1lll11llll_opy_ and bstack1l1llll1ll_opy_.on():
      webdriver.Remote.__init__ = bstack1lll1l11ll_opy_
    if bstack1l1llll1ll_opy_.on():
      WebDriver.execute = bstack1ll1lll1_opy_
    bstack1lllll1ll1_opy_ = True
  except Exception as e:
    pass
  bstack111lllll1_opy_()
  if not bstack1lllll1ll1_opy_:
    bstack1l11lll1l_opy_(bstack1lll11l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨୈ"), bstack1ll111l11l_opy_)
  if bstack1llll111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111l1l1l_opy_
    except Exception as e:
      logger.error(bstack1l1ll1lll_opy_.format(str(e)))
  if bstack111l11111_opy_():
    bstack11l1lll1l_opy_(CONFIG, logger)
  if (bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ୉") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11lllll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll11111l_opy_
      except Exception as e:
        logger.warn(bstack11l111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lllll11_opy_
      except Exception as e:
        logger.debug(bstack1l11ll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack11l111lll_opy_)
    Output.end_test = bstack1ll1l11l1_opy_
    TestStatus.__init__ = bstack1l1l1l1ll_opy_
    QueueItem.__init__ = bstack111l1l111_opy_
    pabot._create_items = bstack11l11l1ll_opy_
    try:
      from pabot import __version__ as bstack1lllllllll_opy_
      if version.parse(bstack1lllllllll_opy_) >= version.parse(bstack1lll11l_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭୊")):
        pabot._run = bstack1ll111111_opy_
      elif version.parse(bstack1lllllllll_opy_) >= version.parse(bstack1lll11l_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧୋ")):
        pabot._run = bstack11l11l1l1_opy_
      else:
        pabot._run = bstack1llllll11l_opy_
    except Exception as e:
      pabot._run = bstack1llllll11l_opy_
    pabot._create_command_for_execution = bstack1lll1111ll_opy_
    pabot._report_results = bstack1ll1llll_opy_
  if bstack1lll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨୌ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack1l1ll1l11l_opy_)
    Runner.run_hook = bstack1ll1l11l_opy_
    Step.run = bstack11l1l1111_opy_
  if bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ୍ࠩ") in str(framework_name).lower():
    if not bstack1lll11llll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1lll11l1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1lll11l1l1_opy_
      Config.getoption = bstack1ll1l1l11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll11lll11_opy_
    except Exception as e:
      pass
def bstack1llll1ll1_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୎") in CONFIG and int(CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ୏")]) > 1:
    logger.warn(bstack1ll111111l_opy_)
def bstack1ll11l1l1_opy_(arg, bstack1l11l1l11_opy_, bstack1ll11lll1_opy_=None):
  global CONFIG
  global bstack1lll111l1l_opy_
  global bstack1l1l1lll_opy_
  global bstack1lll11llll_opy_
  global bstack11ll1l11l_opy_
  bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୐")
  if bstack1l11l1l11_opy_ and isinstance(bstack1l11l1l11_opy_, str):
    bstack1l11l1l11_opy_ = eval(bstack1l11l1l11_opy_)
  CONFIG = bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭୑")]
  bstack1lll111l1l_opy_ = bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ୒")]
  bstack1l1l1lll_opy_ = bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୓")]
  bstack1lll11llll_opy_ = bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ୔")]
  bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ୕"), bstack1lll11llll_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ୖ")] = bstack1ll11lllll_opy_
  os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫୗ")] = json.dumps(CONFIG)
  os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭୘")] = bstack1lll111l1l_opy_
  os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୙")] = str(bstack1l1l1lll_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ୚")] = str(True)
  if bstack11l1111l1_opy_(arg, [bstack1lll11l_opy_ (u"ࠩ࠰ࡲࠬ୛"), bstack1lll11l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫଡ଼")]) != -1:
    os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬଢ଼")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1ll11l_opy_)
    return
  bstack1l1ll1l1_opy_()
  global bstack1ll11l1ll1_opy_
  global bstack11111llll_opy_
  global bstack1ll11ll1l_opy_
  global bstack1ll11llll_opy_
  global bstack1lll111l_opy_
  global bstack1ll11l11ll_opy_
  global bstack1ll1111ll1_opy_
  arg.append(bstack1lll11l_opy_ (u"ࠧ࠳ࡗࠣ୞"))
  arg.append(bstack1lll11l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤୟ"))
  arg.append(bstack1lll11l_opy_ (u"ࠢ࠮࡙ࠥୠ"))
  arg.append(bstack1lll11l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢୡ"))
  global bstack1l1l11ll1_opy_
  global bstack111lll1l_opy_
  global bstack1111ll111_opy_
  global bstack1llll111l_opy_
  global bstack1l1lll1l11_opy_
  global bstack11l1lll1_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1lllllll11_opy_
  global bstack1llll11ll_opy_
  global bstack1lll1lll1_opy_
  global bstack1l1llllll1_opy_
  global bstack11l11l111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l11ll1_opy_ = webdriver.Remote.__init__
    bstack111lll1l_opy_ = WebDriver.quit
    bstack1lll1ll1ll_opy_ = WebDriver.close
    bstack1lllllll11_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1l1lll1ll_opy_(CONFIG) and bstack1llll11l11_opy_():
    if bstack1llll1l1_opy_() < version.parse(bstack1l1111l1l_opy_):
      logger.error(bstack111111lll_opy_.format(bstack1llll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llll11ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1lll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll1lll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1llllll1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l111111_opy_)
  try:
    from pytest_bdd import reporting
    bstack11l11l111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪୢ"))
  bstack1ll11ll1l_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧୣ"), {}).get(bstack1lll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୤"))
  bstack1ll1111ll1_opy_ = True
  bstack1lll1l1ll1_opy_(bstack11lll1lll_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭୥")] = CONFIG[bstack1lll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ୦")]
  os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ୧")] = CONFIG[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ୨")]
  os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ୩")] = bstack1lll11llll_opy_.__str__()
  from _pytest.config import main as bstack1ll11l11l1_opy_
  bstack1ll11l11l1_opy_(arg)
  if bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ୪") in multiprocessing.current_process().__dict__.keys():
    for bstack1l1111l11_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1ll11lll1_opy_.append(bstack1l1111l11_opy_)
def bstack1l1l111l_opy_(arg):
  bstack1lll1l1ll1_opy_(bstack1llll11l1_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୫")] = str(bstack1l1l1lll_opy_)
  from behave.__main__ import main as bstack1l111l1ll_opy_
  bstack1l111l1ll_opy_(arg)
def bstack1lll1lll11_opy_():
  logger.info(bstack11l1l1ll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ୬"), help=bstack1lll11l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ୭"))
  parser.add_argument(bstack1lll11l_opy_ (u"ࠧ࠮ࡷࠪ୮"), bstack1lll11l_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ୯"), help=bstack1lll11l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ୰"))
  parser.add_argument(bstack1lll11l_opy_ (u"ࠪ࠱ࡰ࠭ୱ"), bstack1lll11l_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ୲"), help=bstack1lll11l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭୳"))
  parser.add_argument(bstack1lll11l_opy_ (u"࠭࠭ࡧࠩ୴"), bstack1lll11l_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ୵"), help=bstack1lll11l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ୶"))
  bstack1ll1l1lll1_opy_ = parser.parse_args()
  try:
    bstack1ll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭୷")
    if bstack1ll1l1lll1_opy_.framework and bstack1ll1l1lll1_opy_.framework not in (bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ୸"), bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ୹")):
      bstack1ll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ୺")
    bstack1lllll1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l1l1_opy_)
    bstack1ll11l1l_opy_ = open(bstack1lllll1l1_opy_, bstack1lll11l_opy_ (u"࠭ࡲࠨ୻"))
    bstack11l1111ll_opy_ = bstack1ll11l1l_opy_.read()
    bstack1ll11l1l_opy_.close()
    if bstack1ll1l1lll1_opy_.username:
      bstack11l1111ll_opy_ = bstack11l1111ll_opy_.replace(bstack1lll11l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ୼"), bstack1ll1l1lll1_opy_.username)
    if bstack1ll1l1lll1_opy_.key:
      bstack11l1111ll_opy_ = bstack11l1111ll_opy_.replace(bstack1lll11l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ୽"), bstack1ll1l1lll1_opy_.key)
    if bstack1ll1l1lll1_opy_.framework:
      bstack11l1111ll_opy_ = bstack11l1111ll_opy_.replace(bstack1lll11l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ୾"), bstack1ll1l1lll1_opy_.framework)
    file_name = bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭୿")
    file_path = os.path.abspath(file_name)
    bstack11lll11l_opy_ = open(file_path, bstack1lll11l_opy_ (u"ࠫࡼ࠭஀"))
    bstack11lll11l_opy_.write(bstack11l1111ll_opy_)
    bstack11lll11l_opy_.close()
    logger.info(bstack1l111111l_opy_)
    try:
      os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஁")] = bstack1ll1l1lll1_opy_.framework if bstack1ll1l1lll1_opy_.framework != None else bstack1lll11l_opy_ (u"ࠨࠢஂ")
      config = yaml.safe_load(bstack11l1111ll_opy_)
      config[bstack1lll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧஃ")] = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧ஄")
      bstack1lllll1111_opy_(bstack11ll1llll_opy_, config)
    except Exception as e:
      logger.debug(bstack11llll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1ll111_opy_.format(str(e)))
def bstack1lllll1111_opy_(bstack11lllllll_opy_, config, bstack1ll1l1l111_opy_={}):
  global bstack1lll11llll_opy_
  global bstack11l1ll1l1_opy_
  if not config:
    return
  bstack1llll11111_opy_ = bstack1lllll1lll_opy_ if not bstack1lll11llll_opy_ else (
    bstack1ll1111l11_opy_ if bstack1lll11l_opy_ (u"ࠩࡤࡴࡵ࠭அ") in config else bstack1llll11lll_opy_)
  data = {
    bstack1lll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬஆ"): config[bstack1lll11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭இ")],
    bstack1lll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஈ"): config[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩஉ")],
    bstack1lll11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫஊ"): bstack11lllllll_opy_,
    bstack1lll11l_opy_ (u"ࠨࡦࡨࡸࡪࡩࡴࡦࡦࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ஋"): os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ஌"), bstack11l1ll1l1_opy_),
    bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ஍"): bstack1ll111l1l1_opy_,
    bstack1lll11l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠭எ"): bstack1ll1ll1lll_opy_(),
    bstack1lll11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨஏ"): {
      bstack1lll11l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஐ"): str(config[bstack1lll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ஑")]) if bstack1lll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨஒ") in config else bstack1lll11l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥஓ"),
      bstack1lll11l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬஔ"): bstack1ll1llllll_opy_(os.getenv(bstack1lll11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨக"), bstack1lll11l_opy_ (u"ࠧࠨ஖"))),
      bstack1lll11l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ஗"): bstack1lll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஘"),
      bstack1lll11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩங"): bstack1llll11111_opy_,
      bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬச"): config[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭஛")] if config[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧஜ")] else bstack1lll11l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ஝"),
      bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨஞ"): str(config[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩட")]) if bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ஠") in config else bstack1lll11l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ஡"),
      bstack1lll11l_opy_ (u"ࠪࡳࡸ࠭஢"): sys.platform,
      bstack1lll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ண"): socket.gethostname()
    }
  }
  update(data[bstack1lll11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨத")], bstack1ll1l1l111_opy_)
  try:
    response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"࠭ࡐࡐࡕࡗࠫ஥"), bstack1l1l1llll_opy_(bstack1ll1ll111l_opy_), data, {
      bstack1lll11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ஦"): (config[bstack1lll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஧")], config[bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬந")])
    })
    if response:
      logger.debug(bstack11ll1l1ll_opy_.format(bstack11lllllll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1ll1ll1_opy_.format(str(e)))
def bstack1ll1llllll_opy_(framework):
  return bstack1lll11l_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢன").format(str(framework), __version__) if framework else bstack1lll11l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧப").format(
    __version__)
def bstack1l1ll1l1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1lll1lll1l_opy_()
    logger.debug(bstack11l1llll_opy_.format(str(CONFIG)))
    bstack1ll1l1llll_opy_()
    bstack1l1ll11l_opy_()
  except Exception as e:
    logger.error(bstack1lll11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ஫") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1111lll_opy_
  atexit.register(bstack1llllll1ll_opy_)
  signal.signal(signal.SIGINT, bstack1ll1ll111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1ll111_opy_)
def bstack1ll1111lll_opy_(exctype, value, traceback):
  global bstack111l1ll1l_opy_
  try:
    for driver in bstack111l1ll1l_opy_:
      bstack11llll1l1_opy_(driver, bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭஬"), bstack1lll11l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ஭") + str(value))
  except Exception:
    pass
  bstack1111111ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1111111ll_opy_(message=bstack1lll11l_opy_ (u"ࠨࠩம"), bstack1lll11lll_opy_ = False):
  global CONFIG
  bstack1l111llll_opy_ = bstack1lll11l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫய") if bstack1lll11lll_opy_ else bstack1lll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩர")
  try:
    if message:
      bstack1ll1l1l111_opy_ = {
        bstack1l111llll_opy_ : str(message)
      }
      bstack1lllll1111_opy_(bstack1lll1llll1_opy_, CONFIG, bstack1ll1l1l111_opy_)
    else:
      bstack1lllll1111_opy_(bstack1lll1llll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11l1l11_opy_.format(str(e)))
def bstack11ll1lll1_opy_(bstack1lll1111l1_opy_, size):
  bstack1l1ll11l11_opy_ = []
  while len(bstack1lll1111l1_opy_) > size:
    bstack1ll11ll11l_opy_ = bstack1lll1111l1_opy_[:size]
    bstack1l1ll11l11_opy_.append(bstack1ll11ll11l_opy_)
    bstack1lll1111l1_opy_ = bstack1lll1111l1_opy_[size:]
  bstack1l1ll11l11_opy_.append(bstack1lll1111l1_opy_)
  return bstack1l1ll11l11_opy_
def bstack111l1lll1_opy_(args):
  if bstack1lll11l_opy_ (u"ࠫ࠲ࡳࠧற") in args and bstack1lll11l_opy_ (u"ࠬࡶࡤࡣࠩல") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1l11ll_opy_=None, bstack1ll11lll1_opy_=None, bstack1111ll1l1_opy_=False):
  global CONFIG
  global bstack1lll111l1l_opy_
  global bstack1l1l1lll_opy_
  global bstack11l1ll1l1_opy_
  bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"࠭ࠧள")
  bstack1l1ll111l1_opy_(bstack1l11ll1ll_opy_, logger)
  if bstack1ll1l11ll_opy_ and isinstance(bstack1ll1l11ll_opy_, str):
    bstack1ll1l11ll_opy_ = eval(bstack1ll1l11ll_opy_)
  if bstack1ll1l11ll_opy_:
    CONFIG = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧழ")]
    bstack1lll111l1l_opy_ = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩவ")]
    bstack1l1l1lll_opy_ = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫஶ")]
    bstack11ll1l11l_opy_.bstack11llll1l_opy_(bstack1lll11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬஷ"), bstack1l1l1lll_opy_)
    bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫஸ")
  if not bstack1111ll1l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1ll11l_opy_)
      return
    if sys.argv[1] == bstack1lll11l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨஹ") or sys.argv[1] == bstack1lll11l_opy_ (u"࠭࠭ࡷࠩ஺"):
      logger.info(bstack1lll11l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ஻").format(__version__))
      return
    if sys.argv[1] == bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ஼"):
      bstack1lll1lll11_opy_()
      return
  args = sys.argv
  bstack1l1ll1l1_opy_()
  global bstack1ll11l1ll1_opy_
  global bstack111ll1111_opy_
  global bstack1ll1111ll1_opy_
  global bstack11lll111_opy_
  global bstack11111llll_opy_
  global bstack1ll11ll1l_opy_
  global bstack1ll11llll_opy_
  global bstack1111ll1ll_opy_
  global bstack1lll111l_opy_
  global bstack1ll11l11ll_opy_
  global bstack1111l1lll_opy_
  bstack111ll1111_opy_ = len(CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஽")])
  if not bstack1ll11lllll_opy_:
    if args[1] == bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪா") or args[1] == bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬி"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬீ")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬு"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ூ")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௃"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௄")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௅"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬெ")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬே"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ை")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௉"):
      bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨொ")
      args = args[2:]
    else:
      if not bstack1lll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬோ") in CONFIG or str(CONFIG[bstack1lll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ௌ")]).lower() in [bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ்ࠫ"), bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭௎")]:
        bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௏")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪௐ")]).lower() == bstack1lll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௑"):
        bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௒")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௓")]).lower() == bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௔"):
        bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௕")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௖")]).lower() == bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧௗ"):
        bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௘")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௙")]).lower() == bstack1lll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௚"):
        bstack1ll11lllll_opy_ = bstack1lll11l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௛")
        args = args[1:]
      else:
        os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௜")] = bstack1ll11lllll_opy_
        bstack1l111lll_opy_(bstack11ll1l1l_opy_)
  os.environ[bstack1lll11l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ௝")] = bstack1ll11lllll_opy_
  bstack11l1ll1l1_opy_ = bstack1ll11lllll_opy_
  global bstack1ll1l11ll1_opy_
  if bstack1ll1l11ll_opy_:
    try:
      os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௞")] = bstack1ll11lllll_opy_
      bstack1lllll1111_opy_(bstack111l111l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll11l1l11_opy_.format(str(e)))
  global bstack1l1l11ll1_opy_
  global bstack111lll1l_opy_
  global bstack1lll111l1_opy_
  global bstack111111l1l_opy_
  global bstack11l11ll1_opy_
  global bstack1111ll111_opy_
  global bstack1llll111l_opy_
  global bstack111ll11ll_opy_
  global bstack1l1lll1l11_opy_
  global bstack11l1lll1_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1l1lllll_opy_
  global bstack111lll1ll_opy_
  global bstack1lllllll11_opy_
  global bstack1llll11ll_opy_
  global bstack1lll1lll1_opy_
  global bstack1l1llllll1_opy_
  global bstack111ll1l11_opy_
  global bstack11l11l111_opy_
  global bstack1lll11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l11ll1_opy_ = webdriver.Remote.__init__
    bstack111lll1l_opy_ = WebDriver.quit
    bstack1lll1ll1ll_opy_ = WebDriver.close
    bstack1lllllll11_opy_ = WebDriver.get
    bstack1lll11l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1l11ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l1lll1ll_opy_(CONFIG) and bstack1llll11l11_opy_():
    if bstack1llll1l1_opy_() < version.parse(bstack1l1111l1l_opy_):
      logger.error(bstack111111lll_opy_.format(bstack1llll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llll11ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1lll_opy_.format(str(e)))
  if bstack1ll11lllll_opy_ != bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௟") or (bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௠") and not bstack1ll1l11ll_opy_):
    bstack111ll1l1_opy_()
  if (bstack1ll11lllll_opy_ in [bstack1lll11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௡"), bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௢"), bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭௣")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11lllll1l_opy_
        bstack11l11ll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l111lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack111111l1l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11ll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack11l111lll_opy_)
    if bstack1ll11lllll_opy_ != bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௤"):
      bstack11lll1l1l_opy_()
    bstack1lll111l1_opy_ = Output.end_test
    bstack1111ll111_opy_ = TestStatus.__init__
    bstack111ll11ll_opy_ = pabot._run
    bstack1l1lll1l11_opy_ = QueueItem.__init__
    bstack11l1lll1_opy_ = pabot._create_command_for_execution
    bstack111ll1l11_opy_ = pabot._report_results
  if bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௥"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack1l1ll1l11l_opy_)
    bstack1l1lllll_opy_ = Runner.run_hook
    bstack111lll1ll_opy_ = Step.run
  if bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௦"):
    try:
      from _pytest.config import Config
      bstack1lll1lll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1llllll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l111111_opy_)
    try:
      from pytest_bdd import reporting
      bstack11l11l111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ௧"))
  if bstack1ll11lllll_opy_ in bstack11l1ll1ll_opy_:
    try:
      framework_name = bstack1lll11l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ௨") if bstack1ll11lllll_opy_ in [bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௩"), bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௪"), bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௫")] else bstack111111l11_opy_(bstack1ll11lllll_opy_)
      bstack1l1llll1ll_opy_.launch(CONFIG, {
        bstack1lll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ௬"): bstack1lll11l_opy_ (u"ࠨࡽ࠳ࢁ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ௭").format(framework_name) if bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௮") and bstack1ll11llll1_opy_() else framework_name,
        bstack1lll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௯"): bstack1lll11111_opy_(framework_name),
        bstack1lll11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௰"): __version__
      })
    except Exception as e:
      logger.debug(bstack11ll11ll_opy_.format(bstack1lll11l_opy_ (u"ࠬࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ௱"), str(e)))
  if bstack1ll11lllll_opy_ in bstack111ll111_opy_:
    try:
      framework_name = bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௲") if bstack1ll11lllll_opy_ in [bstack1lll11l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௳"), bstack1lll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௴")] else bstack1ll11lllll_opy_
      if bstack1lll11llll_opy_ and bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ௵") in CONFIG and CONFIG[bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ௶")] == True:
        if bstack1lll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ௷") in CONFIG:
          os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭௸")] = os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ௹"), json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ௺")]))
          CONFIG[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ௻")].pop(bstack1lll11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ௼"), None)
          CONFIG[bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ௽")].pop(bstack1lll11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ௾"), None)
        bstack1l1llllll_opy_, bstack1ll11l1lll_opy_ = bstack11l11llll_opy_.bstack1ll111ll1_opy_(CONFIG, bstack1ll11lllll_opy_, bstack1lll11111_opy_(framework_name))
        if not bstack1l1llllll_opy_ is None:
          os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ௿")] = bstack1l1llllll_opy_
          os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬఀ")] = str(bstack1ll11l1lll_opy_)
    except Exception as e:
      logger.debug(bstack11ll11ll_opy_.format(bstack1lll11l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఁ"), str(e)))
  if bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨం"):
    bstack1ll1111ll1_opy_ = True
    if bstack1ll1l11ll_opy_ and bstack1111ll1l1_opy_:
      bstack1ll11ll1l_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ః"), {}).get(bstack1lll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఄ"))
      bstack1lll1l1ll1_opy_(bstack11llll111_opy_)
    elif bstack1ll1l11ll_opy_:
      bstack1ll11ll1l_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨఅ"), {}).get(bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఆ"))
      global bstack111l1ll1l_opy_
      try:
        if bstack111l1lll1_opy_(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఇ")]) and multiprocessing.current_process().name == bstack1lll11l_opy_ (u"ࠧ࠱ࠩఈ"):
          bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఉ")].remove(bstack1lll11l_opy_ (u"ࠩ࠰ࡱࠬఊ"))
          bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఋ")].remove(bstack1lll11l_opy_ (u"ࠫࡵࡪࡢࠨఌ"))
          bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఍")] = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఎ")][0]
          with open(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఏ")], bstack1lll11l_opy_ (u"ࠨࡴࠪఐ")) as f:
            bstack1l1ll1111_opy_ = f.read()
          bstack11lll1111_opy_ = bstack1lll11l_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ఑").format(str(bstack1ll1l11ll_opy_))
          bstack111lllll_opy_ = bstack11lll1111_opy_ + bstack1l1ll1111_opy_
          bstack11111111_opy_ = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఒ")] + bstack1lll11l_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ఓ")
          with open(bstack11111111_opy_, bstack1lll11l_opy_ (u"ࠬࡽࠧఔ")):
            pass
          with open(bstack11111111_opy_, bstack1lll11l_opy_ (u"ࠨࡷࠬࠤక")) as f:
            f.write(bstack111lllll_opy_)
          import subprocess
          bstack1llll11l_opy_ = subprocess.run([bstack1lll11l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢఖ"), bstack11111111_opy_])
          if os.path.exists(bstack11111111_opy_):
            os.unlink(bstack11111111_opy_)
          os._exit(bstack1llll11l_opy_.returncode)
        else:
          if bstack111l1lll1_opy_(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫగ")]):
            bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఘ")].remove(bstack1lll11l_opy_ (u"ࠪ࠱ࡲ࠭ఙ"))
            bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")].remove(bstack1lll11l_opy_ (u"ࠬࡶࡤࡣࠩఛ"))
            bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")] = bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఝ")][0]
          bstack1lll1l1ll1_opy_(bstack11llll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lll11l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫట")] = bstack1lll11l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬఠ")
          mod_globals[bstack1lll11l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭డ")] = os.path.abspath(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఢ")])
          exec(open(bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lll11l_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧత").format(str(e)))
          for driver in bstack111l1ll1l_opy_:
            bstack1ll11lll1_opy_.append({
              bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭థ"): bstack1ll1l11ll_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬద")],
              bstack1lll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩధ"): str(e),
              bstack1lll11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪన"): multiprocessing.current_process().name
            })
            bstack11llll1l1_opy_(driver, bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ఩"), bstack1lll11l_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤప") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack111l1ll1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1l1lll_opy_, CONFIG, logger)
      bstack1ll11l1l1l_opy_()
      bstack1llll1ll1_opy_()
      bstack1l11l1l11_opy_ = {
        bstack1lll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఫ"): args[0],
        bstack1lll11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨబ"): CONFIG,
        bstack1lll11l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪభ"): bstack1lll111l1l_opy_,
        bstack1lll11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬమ"): bstack1l1l1lll_opy_
      }
      percy.bstack1ll111lll1_opy_()
      if bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧయ") in CONFIG:
        bstack1lll1lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1lllll_opy_ = manager.list()
        if bstack111l1lll1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨర")]):
            if index == 0:
              bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఱ")] = args
            bstack1lll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1l11_opy_, bstack1lll1lllll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪల")]):
            bstack1lll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1l11_opy_, bstack1lll1lllll_opy_)))
        for t in bstack1lll1lll_opy_:
          t.start()
        for t in bstack1lll1lll_opy_:
          t.join()
        bstack1111ll1ll_opy_ = list(bstack1lll1lllll_opy_)
      else:
        if bstack111l1lll1_opy_(args):
          bstack1l11l1l11_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫళ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll1l1ll1_opy_(bstack11llll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lll11l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫఴ")] = bstack1lll11l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬవ")
          mod_globals[bstack1lll11l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭శ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫష") or bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬస"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack11l111lll_opy_)
    bstack1ll11l1l1l_opy_()
    bstack1lll1l1ll1_opy_(bstack1ll1ll11l1_opy_)
    if bstack1lll11l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬహ") in args:
      i = args.index(bstack1lll11l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭఺"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll11l1ll1_opy_))
    args.insert(0, str(bstack1lll11l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ఻")))
    if bstack1l1llll1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11lll1l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l111ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1lll11l_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕ఼ࠥ"),
        ).parse_args(bstack11lll1l11_opy_)
        args.insert(args.index(bstack1ll1l111ll_opy_[0]), str(bstack1lll11l_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨఽ")))
        args.insert(args.index(bstack1ll1l111ll_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩా"))))
        if bstack1lll11ll1_opy_(os.environ.get(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫి"))) and str(os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫీ"), bstack1lll11l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ు"))) != bstack1lll11l_opy_ (u"ࠩࡱࡹࡱࡲࠧూ"):
          for bstack1lll1l11l1_opy_ in bstack1ll1l111ll_opy_:
            args.remove(bstack1lll1l11l1_opy_)
          bstack1l1lll1l1_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧృ")).split(bstack1lll11l_opy_ (u"ࠫ࠱࠭ౄ"))
          for bstack1111l1l11_opy_ in bstack1l1lll1l1_opy_:
            args.append(bstack1111l1l11_opy_)
      except Exception as e:
        logger.error(bstack1lll11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣ౅").format(e))
    pabot.main(args)
  elif bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧె"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack11l111lll_opy_)
    for a in args:
      if bstack1lll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ే") in a:
        bstack11111llll_opy_ = int(a.split(bstack1lll11l_opy_ (u"ࠨ࠼ࠪై"))[1])
      if bstack1lll11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭౉") in a:
        bstack1ll11ll1l_opy_ = str(a.split(bstack1lll11l_opy_ (u"ࠪ࠾ࠬొ"))[1])
      if bstack1lll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫో") in a:
        bstack1ll11llll_opy_ = str(a.split(bstack1lll11l_opy_ (u"ࠬࡀࠧౌ"))[1])
    bstack1ll11ll1l1_opy_ = None
    if bstack1lll11l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼ్ࠬ") in args:
      i = args.index(bstack1lll11l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭౎"))
      args.pop(i)
      bstack1ll11ll1l1_opy_ = args.pop(i)
    if bstack1ll11ll1l1_opy_ is not None:
      global bstack1ll1l1ll_opy_
      bstack1ll1l1ll_opy_ = bstack1ll11ll1l1_opy_
    bstack1lll1l1ll1_opy_(bstack1ll1ll11l1_opy_)
    run_cli(args)
    if bstack1lll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ౏") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1111l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11lll1_opy_.append(bstack1l1111l11_opy_)
  elif bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౐"):
    bstack11l1ll111_opy_ = bstack1ll11ll111_opy_(args, logger, CONFIG, bstack1lll11llll_opy_)
    bstack11l1ll111_opy_.bstack1llll1l1l1_opy_()
    bstack1ll11l1l1l_opy_()
    bstack11lll111_opy_ = True
    bstack1ll11l11ll_opy_ = bstack11l1ll111_opy_.bstack1ll11111ll_opy_()
    bstack11l1ll111_opy_.bstack1l11l1l11_opy_(bstack1llll111ll_opy_)
    bstack1lll111l_opy_ = bstack11l1ll111_opy_.bstack11ll11ll1_opy_(bstack1ll11l1l1_opy_, {
      bstack1lll11l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ౑"): bstack1lll111l1l_opy_,
      bstack1lll11l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭౒"): bstack1l1l1lll_opy_,
      bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ౓"): bstack1lll11llll_opy_
    })
    bstack1111l1lll_opy_ = 1 if len(bstack1lll111l_opy_) > 0 else 0
  elif bstack1ll11lllll_opy_ == bstack1lll11l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭౔"):
    try:
      from behave.__main__ import main as bstack1l111l1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11lll1l_opy_(e, bstack1l1ll1l11l_opy_)
    bstack1ll11l1l1l_opy_()
    bstack11lll111_opy_ = True
    bstack11ll11l1_opy_ = 1
    if bstack1lll11l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳౕࠧ") in CONFIG:
      bstack11ll11l1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨౖ")]
    bstack1l1ll1l1l_opy_ = int(bstack11ll11l1_opy_) * int(len(CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")]))
    config = Configuration(args)
    bstack1llll1lll1_opy_ = config.paths
    if len(bstack1llll1lll1_opy_) == 0:
      import glob
      pattern = bstack1lll11l_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩౘ")
      bstack1l1l1l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1l1l1l1_opy_)
      config = Configuration(args)
      bstack1llll1lll1_opy_ = config.paths
    bstack1lll1ll1l_opy_ = [os.path.normpath(item) for item in bstack1llll1lll1_opy_]
    bstack1lll1l1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack11lll11ll_opy_ = [item for item in bstack1lll1l1l11_opy_ if item not in bstack1lll1ll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lll11l_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬౙ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll1ll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1l11l_opy_)))
                    for bstack11l1l11l_opy_ in bstack1lll1ll1l_opy_]
    bstack1l1l1l11l_opy_ = []
    for spec in bstack1lll1ll1l_opy_:
      bstack11ll1l11_opy_ = []
      bstack11ll1l11_opy_ += bstack11lll11ll_opy_
      bstack11ll1l11_opy_.append(spec)
      bstack1l1l1l11l_opy_.append(bstack11ll1l11_opy_)
    execution_items = []
    for bstack11ll1l11_opy_ in bstack1l1l1l11l_opy_:
      for index, _ in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౚ")]):
        item = {}
        item[bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࠪ౛")] = bstack1lll11l_opy_ (u"ࠧࠡࠩ౜").join(bstack11ll1l11_opy_)
        item[bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧౝ")] = index
        execution_items.append(item)
    bstack11l1l1ll_opy_ = bstack11ll1lll1_opy_(execution_items, bstack1l1ll1l1l_opy_)
    for execution_item in bstack11l1l1ll_opy_:
      bstack1lll1lll_opy_ = []
      for item in execution_item:
        bstack1lll1lll_opy_.append(bstack111l11ll1_opy_(name=str(item[bstack1lll11l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౞")]),
                                             target=bstack1l1l111l_opy_,
                                             args=(item[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࠧ౟")],)))
      for t in bstack1lll1lll_opy_:
        t.start()
      for t in bstack1lll1lll_opy_:
        t.join()
  else:
    bstack1l111lll_opy_(bstack11ll1l1l_opy_)
  if not bstack1ll1l11ll_opy_:
    bstack1l1lll11ll_opy_()
def browserstack_initialize(bstack1ll1l11l1l_opy_=None):
  run_on_browserstack(bstack1ll1l11l1l_opy_, None, True)
def bstack1l1lll11ll_opy_():
  global CONFIG
  global bstack11l1ll1l1_opy_
  global bstack1111l1lll_opy_
  bstack1l1llll1ll_opy_.stop()
  bstack1l1llll1ll_opy_.bstack1l111l11_opy_()
  if bstack11l11llll_opy_.bstack1lll11l11l_opy_(CONFIG):
    bstack11l11llll_opy_.bstack1ll111l1l_opy_()
  [bstack11111l1ll_opy_, bstack11l1lll11_opy_] = bstack11111ll11_opy_()
  if bstack11111l1ll_opy_ is not None and bstack11111ll1l_opy_() != -1:
    sessions = bstack11lll1l1_opy_(bstack11111l1ll_opy_)
    bstack1l1lllll1l_opy_(sessions, bstack11l1lll11_opy_)
  if bstack11l1ll1l1_opy_ == bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫౠ") and bstack1111l1lll_opy_ != 0:
    sys.exit(bstack1111l1lll_opy_)
def bstack111111l11_opy_(bstack1111llll1_opy_):
  if bstack1111llll1_opy_:
    return bstack1111llll1_opy_.capitalize()
  else:
    return bstack1lll11l_opy_ (u"ࠬ࠭ౡ")
def bstack1l1ll1ll1l_opy_(bstack11l11lll1_opy_):
  if bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫౢ") in bstack11l11lll1_opy_ and bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬౣ")] != bstack1lll11l_opy_ (u"ࠨࠩ౤"):
    return bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౥")]
  else:
    bstack1l1lll11l_opy_ = bstack1lll11l_opy_ (u"ࠥࠦ౦")
    if bstack1lll11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ౧") in bstack11l11lll1_opy_ and bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ౨")] != None:
      bstack1l1lll11l_opy_ += bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭౩")] + bstack1lll11l_opy_ (u"ࠢ࠭ࠢࠥ౪")
      if bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠨࡱࡶࠫ౫")] == bstack1lll11l_opy_ (u"ࠤ࡬ࡳࡸࠨ౬"):
        bstack1l1lll11l_opy_ += bstack1lll11l_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣ౭")
      bstack1l1lll11l_opy_ += (bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ౮")] or bstack1lll11l_opy_ (u"ࠬ࠭౯"))
      return bstack1l1lll11l_opy_
    else:
      bstack1l1lll11l_opy_ += bstack111111l11_opy_(bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ౰")]) + bstack1lll11l_opy_ (u"ࠢࠡࠤ౱") + (
              bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ౲")] or bstack1lll11l_opy_ (u"ࠩࠪ౳")) + bstack1lll11l_opy_ (u"ࠥ࠰ࠥࠨ౴")
      if bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠫࡴࡹࠧ౵")] == bstack1lll11l_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨ౶"):
        bstack1l1lll11l_opy_ += bstack1lll11l_opy_ (u"ࠨࡗࡪࡰࠣࠦ౷")
      bstack1l1lll11l_opy_ += bstack11l11lll1_opy_[bstack1lll11l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ౸")] or bstack1lll11l_opy_ (u"ࠨࠩ౹")
      return bstack1l1lll11l_opy_
def bstack1llllllll1_opy_(bstack1ll1ll1l11_opy_):
  if bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ౺"):
    return bstack1lll11l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౻")
  elif bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ౼"):
    return bstack1lll11l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ౽")
  elif bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ౾"):
    return bstack1lll11l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ౿")
  elif bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢಀ"):
    return bstack1lll11l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಁ")
  elif bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦಂ"):
    return bstack1lll11l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಃ")
  elif bstack1ll1ll1l11_opy_ == bstack1lll11l_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨ಄"):
    return bstack1lll11l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಅ")
  else:
    return bstack1lll11l_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫಆ") + bstack111111l11_opy_(
      bstack1ll1ll1l11_opy_) + bstack1lll11l_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಇ")
def bstack11ll1ll1_opy_(session):
  return bstack1lll11l_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩಈ").format(
    session[bstack1lll11l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧಉ")], bstack1l1ll1ll1l_opy_(session), bstack1llllllll1_opy_(session[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪಊ")]),
    bstack1llllllll1_opy_(session[bstack1lll11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬಋ")]),
    bstack111111l11_opy_(session[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧಌ")] or session[bstack1lll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ಍")] or bstack1lll11l_opy_ (u"ࠨࠩಎ")) + bstack1lll11l_opy_ (u"ࠤࠣࠦಏ") + (session[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಐ")] or bstack1lll11l_opy_ (u"ࠫࠬ಑")),
    session[bstack1lll11l_opy_ (u"ࠬࡵࡳࠨಒ")] + bstack1lll11l_opy_ (u"ࠨࠠࠣಓ") + session[bstack1lll11l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫಔ")], session[bstack1lll11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪಕ")] or bstack1lll11l_opy_ (u"ࠩࠪಖ"),
    session[bstack1lll11l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧಗ")] if session[bstack1lll11l_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨಘ")] else bstack1lll11l_opy_ (u"ࠬ࠭ಙ"))
def bstack1l1lllll1l_opy_(sessions, bstack11l1lll11_opy_):
  try:
    bstack1lll111lll_opy_ = bstack1lll11l_opy_ (u"ࠨࠢಚ")
    if not os.path.exists(bstack1ll11lll1l_opy_):
      os.mkdir(bstack1ll11lll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11l_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬಛ")), bstack1lll11l_opy_ (u"ࠨࡴࠪಜ")) as f:
      bstack1lll111lll_opy_ = f.read()
    bstack1lll111lll_opy_ = bstack1lll111lll_opy_.replace(bstack1lll11l_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭ಝ"), str(len(sessions)))
    bstack1lll111lll_opy_ = bstack1lll111lll_opy_.replace(bstack1lll11l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪಞ"), bstack11l1lll11_opy_)
    bstack1lll111lll_opy_ = bstack1lll111lll_opy_.replace(bstack1lll11l_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬಟ"),
                                              sessions[0].get(bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩಠ")) if sessions[0] else bstack1lll11l_opy_ (u"࠭ࠧಡ"))
    with open(os.path.join(bstack1ll11lll1l_opy_, bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫಢ")), bstack1lll11l_opy_ (u"ࠨࡹࠪಣ")) as stream:
      stream.write(bstack1lll111lll_opy_.split(bstack1lll11l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ತ"))[0])
      for session in sessions:
        stream.write(bstack11ll1ll1_opy_(session))
      stream.write(bstack1lll111lll_opy_.split(bstack1lll11l_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧಥ"))[1])
    logger.info(bstack1lll11l_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧದ").format(bstack1ll11lll1l_opy_));
  except Exception as e:
    logger.debug(bstack1lll11lll1_opy_.format(str(e)))
def bstack11lll1l1_opy_(bstack11111l1ll_opy_):
  global CONFIG
  try:
    host = bstack1lll11l_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨಧ") if bstack1lll11l_opy_ (u"࠭ࡡࡱࡲࠪನ") in CONFIG else bstack1lll11l_opy_ (u"ࠧࡢࡲ࡬ࠫ಩")
    user = CONFIG[bstack1lll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಪ")]
    key = CONFIG[bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಫ")]
    bstack1ll11l1111_opy_ = bstack1lll11l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩಬ") if bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࠨಭ") in CONFIG else bstack1lll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧಮ")
    url = bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫಯ").format(user, key, host, bstack1ll11l1111_opy_,
                                                                                bstack11111l1ll_opy_)
    headers = {
      bstack1lll11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ರ"): bstack1lll11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫಱ"),
    }
    proxies = bstack1llll11l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lll11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧಲ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lll1ll1_opy_.format(str(e)))
def bstack11111ll11_opy_():
  global CONFIG
  global bstack1ll111l1l1_opy_
  try:
    if bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ಳ") in CONFIG:
      host = bstack1lll11l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ಴") if bstack1lll11l_opy_ (u"ࠬࡧࡰࡱࠩವ") in CONFIG else bstack1lll11l_opy_ (u"࠭ࡡࡱ࡫ࠪಶ")
      user = CONFIG[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩಷ")]
      key = CONFIG[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಸ")]
      bstack1ll11l1111_opy_ = bstack1lll11l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨಹ") if bstack1lll11l_opy_ (u"ࠪࡥࡵࡶࠧ಺") in CONFIG else bstack1lll11l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭಻")
      url = bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲ಼ࠬ").format(user, key, host, bstack1ll11l1111_opy_)
      headers = {
        bstack1lll11l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬಽ"): bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪಾ"),
      }
      if bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಿ") in CONFIG:
        params = {bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೀ"): CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ು")], bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೂ"): CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೃ")]}
      else:
        params = {bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫೄ"): CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೅")]}
      proxies = bstack1llll11l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1l111_opy_ = response.json()[0][bstack1lll11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫೆ")]
        if bstack1ll1l111_opy_:
          bstack11l1lll11_opy_ = bstack1ll1l111_opy_[bstack1lll11l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ೇ")].split(bstack1lll11l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩೈ"))[0] + bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬ೉") + bstack1ll1l111_opy_[
            bstack1lll11l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨೊ")]
          logger.info(bstack1ll111l11_opy_.format(bstack11l1lll11_opy_))
          bstack1ll111l1l1_opy_ = bstack1ll1l111_opy_[bstack1lll11l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩೋ")]
          bstack1lll1l11l_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪೌ")]
          if bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ್ࠪ") in CONFIG:
            bstack1lll1l11l_opy_ += bstack1lll11l_opy_ (u"ࠩࠣࠫ೎") + CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೏")]
          if bstack1lll1l11l_opy_ != bstack1ll1l111_opy_[bstack1lll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೐")]:
            logger.debug(bstack11l1lllll_opy_.format(bstack1ll1l111_opy_[bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೑")], bstack1lll1l11l_opy_))
          return [bstack1ll1l111_opy_[bstack1lll11l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ೒")], bstack11l1lll11_opy_]
    else:
      logger.warn(bstack1111l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l1lll_opy_.format(str(e)))
  return [None, None]
def bstack111l1ll1_opy_(url, bstack1lll1llll_opy_=False):
  global CONFIG
  global bstack1lllll11l1_opy_
  if not bstack1lllll11l1_opy_:
    hostname = bstack1l11llll_opy_(url)
    is_private = bstack1l1llll1l_opy_(hostname)
    if (bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ೓") in CONFIG and not bstack1lll11ll1_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ೔")])) and (is_private or bstack1lll1llll_opy_):
      bstack1lllll11l1_opy_ = hostname
def bstack1l11llll_opy_(url):
  return urlparse(url).hostname
def bstack1l1llll1l_opy_(hostname):
  for bstack1llll1llll_opy_ in bstack11l1ll11_opy_:
    regex = re.compile(bstack1llll1llll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1lll1ll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11111llll_opy_
  if not bstack11l11llll_opy_.bstack111l1111l_opy_(CONFIG, bstack11111llll_opy_):
    logger.warning(bstack1lll11l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧೕ"))
    return {}
  try:
    results = driver.execute_script(bstack1lll11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡥࡷࡧࡱࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡒࡆࡕࡓࡓࡓ࡙ࡅࠨ࠮ࠣࡪࡳ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡳࡱࡼࡥࠩࡧࡹࡩࡳࡺ࠮ࡥࡧࡷࡥ࡮ࡲ࠮ࡥࡣࡷࡥ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࡸࡨࡲࡹ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡪࡦࡥࡷࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠥࠦࠧೖ"))
    return results
  except Exception:
    logger.error(bstack1lll11l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ೗"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11111llll_opy_
  if not bstack11l11llll_opy_.bstack111l1111l_opy_(CONFIG, bstack11111llll_opy_):
    logger.warning(bstack1lll11l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ೘"))
    return {}
  try:
    bstack1l1ll11ll_opy_ = driver.execute_script(bstack1lll11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࡸࡨࡲࡹࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡇࡆࡖࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡘ࡛ࡍࡎࡃࡕ࡝ࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡱ࡯ࡺࡪ࠮ࡥࡷࡧࡱࡸ࠳ࡪࡥࡵࡣ࡬ࡰ࠳ࡹࡵ࡮࡯ࡤࡶࡾ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡘ࡛ࡍࡎࡃࡕ࡝ࡤࡘࡅࡔࡒࡒࡒࡘࡋࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨࡺࡪࡴࡴࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠣࡧࡦࡺࡣࡩࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦ࡬ࡨࡧࡹ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁ࠮ࡁࠊࠡࠢࠣࠤࠧࠨࠢ೙"))
    return bstack1l1ll11ll_opy_
  except Exception:
    logger.error(bstack1lll11l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣ೚"))
    return {}