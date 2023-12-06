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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1l1llll_opy_, bstack1l1111l1_opy_
class bstack1lll111ll_opy_:
  working_dir = os.getcwd()
  bstack111ll1lll_opy_ = False
  config = {}
  binary_path = bstack1lll11l_opy_ (u"ࠪࠫහ")
  bstack11ll1ll1l1_opy_ = bstack1lll11l_opy_ (u"ࠫࠬළ")
  bstack11llll1l1l_opy_ = False
  bstack11lll1l111_opy_ = None
  bstack11lll11l1l_opy_ = {}
  bstack11lll1111l_opy_ = 300
  bstack11lllll1l1_opy_ = False
  logger = None
  bstack1l111111ll_opy_ = False
  bstack1l1111ll11_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭ෆ")
  bstack1l1111l1ll_opy_ = {
    bstack1lll11l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭෇") : 1,
    bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ෈") : 2,
    bstack1lll11l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭෉") : 3,
    bstack1lll11l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ්ࠩ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11lll1lll1_opy_(self):
    bstack1l11111l1l_opy_ = bstack1lll11l_opy_ (u"ࠪࠫ෋")
    bstack1l11111ll1_opy_ = sys.platform
    bstack1l11111lll_opy_ = bstack1lll11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ෌")
    if re.match(bstack1lll11l_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧ෍"), bstack1l11111ll1_opy_) != None:
      bstack1l11111l1l_opy_ = bstack11llll1l11_opy_ + bstack1lll11l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢ෎")
      self.bstack1l1111ll11_opy_ = bstack1lll11l_opy_ (u"ࠧ࡮ࡣࡦࠫා")
    elif re.match(bstack1lll11l_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨැ"), bstack1l11111ll1_opy_) != None:
      bstack1l11111l1l_opy_ = bstack11llll1l11_opy_ + bstack1lll11l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥෑ")
      bstack1l11111lll_opy_ = bstack1lll11l_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨි")
      self.bstack1l1111ll11_opy_ = bstack1lll11l_opy_ (u"ࠫࡼ࡯࡮ࠨී")
    else:
      bstack1l11111l1l_opy_ = bstack11llll1l11_opy_ + bstack1lll11l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣු")
      self.bstack1l1111ll11_opy_ = bstack1lll11l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ෕")
    return bstack1l11111l1l_opy_, bstack1l11111lll_opy_
  def bstack11lll1l1l1_opy_(self):
    try:
      bstack11lllll1ll_opy_ = [os.path.join(expanduser(bstack1lll11l_opy_ (u"ࠢࡿࠤූ")), bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ෗")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11lllll1ll_opy_:
        if(self.bstack11lll1ll11_opy_(path)):
          return path
      raise bstack1lll11l_opy_ (u"ࠤࡘࡲࡦࡲࡢࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨෘ")
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧෙ").format(e))
  def bstack11lll1ll11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11ll1lllll_opy_(self, bstack1l11111l1l_opy_, bstack1l11111lll_opy_):
    try:
      bstack11ll1ll1ll_opy_ = self.bstack11lll1l1l1_opy_()
      bstack11ll1lll11_opy_ = os.path.join(bstack11ll1ll1ll_opy_, bstack1lll11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧේ"))
      bstack1l1111l111_opy_ = os.path.join(bstack11ll1ll1ll_opy_, bstack1l11111lll_opy_)
      if os.path.exists(bstack1l1111l111_opy_):
        self.logger.info(bstack1lll11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢෛ").format(bstack1l1111l111_opy_))
        return bstack1l1111l111_opy_
      if os.path.exists(bstack11ll1lll11_opy_):
        self.logger.info(bstack1lll11l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦො").format(bstack11ll1lll11_opy_))
        return self.bstack1l11111111_opy_(bstack11ll1lll11_opy_, bstack1l11111lll_opy_)
      self.logger.info(bstack1lll11l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧෝ").format(bstack1l11111l1l_opy_))
      response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠨࡉࡈࡘࠬෞ"), bstack1l11111l1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11ll1lll11_opy_, bstack1lll11l_opy_ (u"ࠩࡺࡦࠬෟ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1111l1l1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡢࡪࡰࡤࡶࡾࡥࡺࡪࡲࡢࡴࡦࡺࡨࡾࠤ෠"))
        return self.bstack1l11111111_opy_(bstack11ll1lll11_opy_, bstack1l11111lll_opy_)
      else:
        raise(bstack1l1111l1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࡸࡥࡴࡲࡲࡲࡸ࡫࠮ࡴࡶࡤࡸࡺࡹ࡟ࡤࡱࡧࡩࢂࠨ෡"))
    except:
      self.logger.error(bstack1lll11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤ෢"))
  def bstack11lll1ll1l_opy_(self, bstack1l11111l1l_opy_, bstack1l11111lll_opy_):
    try:
      bstack1l1111l111_opy_ = self.bstack11ll1lllll_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_)
      bstack11lllllll1_opy_ = self.bstack1l11111l11_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_, bstack1l1111l111_opy_)
      return bstack1l1111l111_opy_, bstack11lllllll1_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥ෣").format(e))
    return bstack1l1111l111_opy_, False
  def bstack1l11111l11_opy_(self, bstack1l11111l1l_opy_, bstack1l11111lll_opy_, bstack1l1111l111_opy_, bstack11llllll1l_opy_ = 0):
    if bstack11llllll1l_opy_ > 1:
      return False
    if bstack1l1111l111_opy_ == None or os.path.exists(bstack1l1111l111_opy_) == False:
      self.logger.warn(bstack1lll11l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ෤"))
      bstack1l1111l111_opy_ = self.bstack11ll1lllll_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_)
      self.bstack1l11111l11_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_, bstack1l1111l111_opy_, bstack11llllll1l_opy_+1)
    bstack1l1111lll1_opy_ = bstack1lll11l_opy_ (u"ࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼࡠ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠳ࡢࡤࠬ࠰࡟ࡨ࠰ࠨ෥")
    command = bstack1lll11l_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෦").format(bstack1l1111l111_opy_)
    bstack1l1111ll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1l1111lll1_opy_, bstack1l1111ll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1lll11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤ෧"))
      bstack1l1111l111_opy_ = self.bstack11ll1lllll_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_)
      self.bstack1l11111l11_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_, bstack1l1111l111_opy_, bstack11llllll1l_opy_+1)
  def bstack1l11111111_opy_(self, bstack11ll1lll11_opy_, bstack1l11111lll_opy_):
    try:
      working_dir = os.path.dirname(bstack11ll1lll11_opy_)
      shutil.unpack_archive(bstack11ll1lll11_opy_, working_dir)
      bstack1l1111l111_opy_ = os.path.join(working_dir, bstack1l11111lll_opy_)
      os.chmod(bstack1l1111l111_opy_, 0o755)
      return bstack1l1111l111_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧ෨"))
  def bstack11lll11ll1_opy_(self):
    try:
      percy = str(self.config.get(bstack1lll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ෩"), bstack1lll11l_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧ෪"))).lower()
      if percy != bstack1lll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧ෫"):
        return False
      self.bstack11llll1l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ෬").format(e))
  def init(self, bstack111ll1lll_opy_, config, logger):
    self.bstack111ll1lll_opy_ = bstack111ll1lll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11lll11ll1_opy_():
      return
    self.bstack11lll11l1l_opy_ = config.get(bstack1lll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ෭"), {})
    try:
      bstack1l11111l1l_opy_, bstack1l11111lll_opy_ = self.bstack11lll1lll1_opy_()
      bstack1l1111l111_opy_, bstack11lllllll1_opy_ = self.bstack11lll1ll1l_opy_(bstack1l11111l1l_opy_, bstack1l11111lll_opy_)
      if bstack11lllllll1_opy_:
        self.binary_path = bstack1l1111l111_opy_
        thread = Thread(target=self.bstack1l1111l11l_opy_)
        thread.start()
      else:
        self.bstack1l111111ll_opy_ = True
        self.logger.error(bstack1lll11l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢ෮").format(bstack1l1111l111_opy_))
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ෯").format(e))
  def bstack11lll111ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡨࠩ෰"), bstack1lll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩ෱"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1lll11l_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦෲ").format(logfile))
      self.bstack11ll1ll1l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤෳ").format(e))
  def bstack1l1111l11l_opy_(self):
    bstack11lll11lll_opy_ = self.bstack11lll1l11l_opy_()
    if bstack11lll11lll_opy_ == None:
      self.bstack1l111111ll_opy_ = True
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧ෴"))
      return False
    command_args = [bstack1lll11l_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦ෵") if self.bstack111ll1lll_opy_ else bstack1lll11l_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨ෶")]
    bstack11llll1lll_opy_ = self.bstack11llll11l1_opy_()
    if bstack11llll1lll_opy_ != None:
      command_args.append(bstack1lll11l_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦ෷").format(bstack11llll1lll_opy_))
    env = os.environ.copy()
    env[bstack1lll11l_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦ෸")] = bstack11lll11lll_opy_
    bstack11ll1llll1_opy_ = [self.binary_path]
    self.bstack11lll111ll_opy_()
    self.bstack11lll1l111_opy_ = self.bstack1l1111llll_opy_(bstack11ll1llll1_opy_ + command_args, env)
    self.logger.debug(bstack1lll11l_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣ෹"))
    bstack11llllll1l_opy_ = 0
    while self.bstack11lll1l111_opy_.poll() == None:
      bstack11llllll11_opy_ = self.bstack11lll11111_opy_()
      if bstack11llllll11_opy_:
        self.logger.debug(bstack1lll11l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ෺"))
        self.bstack11lllll1l1_opy_ = True
        return True
      bstack11llllll1l_opy_ += 1
      self.logger.debug(bstack1lll11l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ෻").format(bstack11llllll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1lll11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣ෼").format(bstack11llllll1l_opy_))
    self.bstack1l111111ll_opy_ = True
    return False
  def bstack11lll11111_opy_(self, bstack11llllll1l_opy_ = 0):
    try:
      if bstack11llllll1l_opy_ > 10:
        return False
      bstack11ll1lll1l_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫ෽"), bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭෾"))
      bstack11llll1111_opy_ = bstack11ll1lll1l_opy_ + bstack11lll1llll_opy_
      response = requests.get(bstack11llll1111_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11lll1l11l_opy_(self):
    bstack11lllll111_opy_ = bstack1lll11l_opy_ (u"࠭ࡡࡱࡲࠪ෿") if self.bstack111ll1lll_opy_ else bstack1lll11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ฀")
    bstack11llll111l_opy_ = bstack1lll11l_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠢก").format(self.config[bstack1lll11l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧข")], bstack11lllll111_opy_)
    uri = bstack1l1l1llll_opy_(bstack11llll111l_opy_)
    try:
      response = bstack1l1111l1_opy_(bstack1lll11l_opy_ (u"ࠪࡋࡊ࡚ࠧฃ"), uri, {}, {bstack1lll11l_opy_ (u"ࠫࡦࡻࡴࡩࠩค"): (self.config[bstack1lll11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧฅ")], self.config[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩฆ")])})
      if response.status_code == 200:
        bstack11lllll11l_opy_ = response.json()
        if bstack1lll11l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨง") in bstack11lllll11l_opy_:
          return bstack11lllll11l_opy_[bstack1lll11l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢจ")]
        else:
          raise bstack1lll11l_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩฉ").format(bstack11lllll11l_opy_)
      else:
        raise bstack1lll11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥช").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧซ").format(e))
  def bstack11llll11l1_opy_(self):
    bstack11llllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣฌ"))
    try:
      if bstack1lll11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧญ") not in self.bstack11lll11l1l_opy_:
        self.bstack11lll11l1l_opy_[bstack1lll11l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨฎ")] = 2
      with open(bstack11llllllll_opy_, bstack1lll11l_opy_ (u"ࠨࡹࠪฏ")) as fp:
        json.dump(self.bstack11lll11l1l_opy_, fp)
      return bstack11llllllll_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤฐ").format(e))
  def bstack1l1111llll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1l1111ll11_opy_ == bstack1lll11l_opy_ (u"ࠪࡻ࡮ࡴࠧฑ"):
        bstack1l1111111l_opy_ = [bstack1lll11l_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬฒ"), bstack1lll11l_opy_ (u"ࠬ࠵ࡣࠨณ")]
        cmd = bstack1l1111111l_opy_ + cmd
      cmd = bstack1lll11l_opy_ (u"࠭ࠠࠨด").join(cmd)
      self.logger.debug(bstack1lll11l_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦต").format(cmd))
      with open(self.bstack11ll1ll1l1_opy_, bstack1lll11l_opy_ (u"ࠣࡣࠥถ")) as bstack1l111l1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1l111l1111_opy_, text=True, stderr=bstack1l111l1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1l111111ll_opy_ = True
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦท").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11lllll1l1_opy_:
        self.logger.info(bstack1lll11l_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦธ"))
        cmd = [self.binary_path, bstack1lll11l_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢน")]
        self.bstack1l1111llll_opy_(cmd)
        self.bstack11lllll1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧบ").format(cmd, e))
  def bstack1ll111lll1_opy_(self):
    if not self.bstack11llll1l1l_opy_:
      return
    try:
      bstack11llll1ll1_opy_ = 0
      while not self.bstack11lllll1l1_opy_ and bstack11llll1ll1_opy_ < self.bstack11lll1111l_opy_:
        if self.bstack1l111111ll_opy_:
          self.logger.info(bstack1lll11l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦป"))
          return
        time.sleep(1)
        bstack11llll1ll1_opy_ += 1
      os.environ[bstack1lll11l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ผ")] = str(self.bstack11llll11ll_opy_())
      self.logger.info(bstack1lll11l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤฝ"))
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥพ").format(e))
  def bstack11llll11ll_opy_(self):
    if self.bstack111ll1lll_opy_:
      return
    try:
      bstack11lll1l1ll_opy_ = [platform[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨฟ")].lower() for platform in self.config.get(bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧภ"), [])]
      bstack11lll11l11_opy_ = sys.maxsize
      bstack1l111111l1_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭ม")
      for browser in bstack11lll1l1ll_opy_:
        if browser in self.bstack1l1111l1ll_opy_:
          bstack11lll111l1_opy_ = self.bstack1l1111l1ll_opy_[browser]
        if bstack11lll111l1_opy_ < bstack11lll11l11_opy_:
          bstack11lll11l11_opy_ = bstack11lll111l1_opy_
          bstack1l111111l1_opy_ = browser
      return bstack1l111111l1_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢย").format(e))