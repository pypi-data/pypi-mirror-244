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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111111ll_opy_, bstack1111l111l_opy_, update, bstack1lllll111_opy_,
                                       bstack1l1lll11l1_opy_, bstack1lll11l1l1_opy_, bstack1ll1l1l1l1_opy_, bstack1111111l1_opy_,
                                       bstack1l1ll111_opy_, bstack111ll1ll1_opy_, bstack1l11lll1l_opy_, bstack1lll1l1l_opy_,
                                       bstack1ll1ll1ll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1l111lll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack111l1l1ll_opy_, bstack111l11l1l_opy_, bstack1l1111l1l_opy_, bstack1lll111l11_opy_, \
    bstack11lll1lll_opy_
from bstack_utils.helper import bstack1l1111111_opy_, bstack1llll11l11_opy_, bstack11l11ll1l1_opy_, bstack11l111ll1_opy_, \
    bstack11l1111l1l_opy_, \
    bstack11l11ll1ll_opy_, bstack1llll1l1_opy_, bstack11l1111l_opy_, bstack11l1l1111l_opy_, bstack1ll11llll1_opy_, Notset, \
    bstack1lllll1l11_opy_, bstack11l11lll1l_opy_, bstack11l1l1llll_opy_, Result, bstack11l111l111_opy_, bstack11l11l111l_opy_, bstack1l11l11l11_opy_, \
    bstack1ll11ll1_opy_, bstack1lll11ll_opy_, bstack1lll11ll1_opy_
from bstack_utils.bstack111llll111_opy_ import bstack111llll1l1_opy_
from bstack_utils.messages import bstack1ll1lll1l_opy_, bstack1l11111l_opy_, bstack1llllll11_opy_, bstack1lll1l111_opy_, bstack11l111111_opy_, \
    bstack1l1ll1lll_opy_, bstack111111lll_opy_, bstack1ll111l111_opy_, bstack1llll1l11_opy_, bstack11ll11l1l_opy_, \
    bstack1ll111l11l_opy_, bstack111lll1l1_opy_
from bstack_utils.proxy import bstack11llllll_opy_, bstack1ll11l111_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack111l1lll11_opy_, bstack111l1llll1_opy_, bstack111l1lllll_opy_, bstack111ll1111l_opy_, \
    bstack111ll11l1l_opy_, bstack111ll111l1_opy_, bstack111ll111ll_opy_, bstack1l1lll1lll_opy_, bstack111ll11ll1_opy_
from bstack_utils.bstack11lll11l1_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.bstack11l1l11ll_opy_ import bstack1l11lll11_opy_, bstack111l1ll1_opy_, bstack111l111ll_opy_, \
    bstack11llll1l1_opy_, bstack11ll11lll_opy_
from bstack_utils.bstack1l1l1l1ll1_opy_ import bstack1l11l1l111_opy_
from bstack_utils.bstack1l1l11lll_opy_ import bstack1l1llll1ll_opy_
import bstack_utils.bstack1l11lll1_opy_ as bstack11l11llll_opy_
bstack1l1l11ll1_opy_ = None
bstack111lll1l_opy_ = None
bstack1111ll111_opy_ = None
bstack1llll111l_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack11l1lll1_opy_ = None
bstack1llll11ll_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack1lllllll11_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l1llllll1_opy_ = None
bstack11l11l111_opy_ = None
bstack1l1l11l1l_opy_ = bstack1lll11l_opy_ (u"ࠩࠪᒵ")
CONFIG = {}
bstack1l1l1lll_opy_ = False
bstack1lll111l1l_opy_ = bstack1lll11l_opy_ (u"ࠪࠫᒶ")
bstack1ll11ll1l_opy_ = bstack1lll11l_opy_ (u"ࠫࠬᒷ")
bstack1ll1111ll1_opy_ = False
bstack111l1ll1l_opy_ = []
bstack11l11ll1l_opy_ = bstack111l11l1l_opy_
bstack11111lll1l_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᒸ")
bstack11111l1l11_opy_ = False
bstack111ll11l1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l11ll1l_opy_,
                    format=bstack1lll11l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᒹ"),
                    datefmt=bstack1lll11l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩᒺ"),
                    stream=sys.stdout)
store = {
    bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᒻ"): []
}
def bstack1ll1l1llll_opy_():
    global CONFIG
    global bstack11l11ll1l_opy_
    if bstack1lll11l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᒼ") in CONFIG:
        bstack11l11ll1l_opy_ = bstack111l1l1ll_opy_[CONFIG[bstack1lll11l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᒽ")]]
        logging.getLogger().setLevel(bstack11l11ll1l_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1l1ll11l_opy_ = {}
current_test_uuid = None
def bstack1111l11ll_opy_(page, bstack1111lll11_opy_):
    try:
        page.evaluate(bstack1lll11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᒾ"),
                      bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᒿ") + json.dumps(
                          bstack1111lll11_opy_) + bstack1lll11l_opy_ (u"ࠨࡽࡾࠤᓀ"))
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᓁ"), e)
def bstack1ll1l111l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1lll11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᓂ"), bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧᓃ") + json.dumps(
            message) + bstack1lll11l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ᓄ") + json.dumps(level) + bstack1lll11l_opy_ (u"ࠫࢂࢃࠧᓅ"))
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣᓆ"), e)
def pytest_configure(config):
    bstack11ll1l11l_opy_ = Config.get_instance()
    config.args = bstack1l1llll1ll_opy_.bstack1111l1l1l1_opy_(config.args)
    bstack11ll1l11l_opy_.bstack1l1l11l1_opy_(bstack1lll11ll1_opy_(config.getoption(bstack1lll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᓇ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11111l1ll1_opy_ = item.config.getoption(bstack1lll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᓈ"))
    plugins = item.config.getoption(bstack1lll11l_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤᓉ"))
    report = outcome.get_result()
    bstack11111111l1_opy_(item, call, report)
    if bstack1lll11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢᓊ") not in plugins or bstack1ll11llll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1lll11l_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦᓋ"), None)
    page = getattr(item, bstack1lll11l_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥᓌ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack111111l1ll_opy_(item, report, summary, bstack11111l1ll1_opy_)
    if (page is not None):
        bstack11111lllll_opy_(item, report, summary, bstack11111l1ll1_opy_)
def bstack111111l1ll_opy_(item, report, summary, bstack11111l1ll1_opy_):
    if report.when == bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᓍ") and report.skipped:
        bstack111ll11ll1_opy_(report)
    if report.when in [bstack1lll11l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓎ"), bstack1lll11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓏ")]:
        return
    if not bstack11l11ll1l1_opy_():
        return
    try:
        if (str(bstack11111l1ll1_opy_).lower() != bstack1lll11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᓐ")):
            item._driver.execute_script(
                bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧᓑ") + json.dumps(
                    report.nodeid) + bstack1lll11l_opy_ (u"ࠪࢁࢂ࠭ᓒ"))
        os.environ[bstack1lll11l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᓓ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1lll11l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧᓔ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᓕ")))
    bstack1l1lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠢࠣᓖ")
    bstack111ll11ll1_opy_(report)
    if not passed:
        try:
            bstack1l1lll1l1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lll11l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᓗ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1lll1l1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᓘ")))
        bstack1l1lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠥࠦᓙ")
        if not passed:
            try:
                bstack1l1lll1l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll11l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᓚ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1lll1l1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᓛ")
                    + json.dumps(bstack1lll11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢᓜ"))
                    + bstack1lll11l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᓝ")
                )
            else:
                item._driver.execute_script(
                    bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᓞ")
                    + json.dumps(str(bstack1l1lll1l1l_opy_))
                    + bstack1lll11l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᓟ")
                )
        except Exception as e:
            summary.append(bstack1lll11l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣᓠ").format(e))
def bstack111111lll1_opy_(test_name, error_message):
    try:
        bstack111111l11l_opy_ = []
        bstack1ll1ll11_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᓡ"), bstack1lll11l_opy_ (u"ࠬ࠶ࠧᓢ"))
        bstack1ll1lllll_opy_ = {bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᓣ"): test_name, bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᓤ"): error_message, bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᓥ"): bstack1ll1ll11_opy_}
        bstack1111111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᓦ"))
        if os.path.exists(bstack1111111ll1_opy_):
            with open(bstack1111111ll1_opy_) as f:
                bstack111111l11l_opy_ = json.load(f)
        bstack111111l11l_opy_.append(bstack1ll1lllll_opy_)
        with open(bstack1111111ll1_opy_, bstack1lll11l_opy_ (u"ࠪࡻࠬᓧ")) as f:
            json.dump(bstack111111l11l_opy_, f)
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩᓨ") + str(e))
def bstack11111lllll_opy_(item, report, summary, bstack11111l1ll1_opy_):
    if report.when in [bstack1lll11l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓩ"), bstack1lll11l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓪ")]:
        return
    if (str(bstack11111l1ll1_opy_).lower() != bstack1lll11l_opy_ (u"ࠧࡵࡴࡸࡩࠬᓫ")):
        bstack1111l11ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᓬ")))
    bstack1l1lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠤࠥᓭ")
    bstack111ll11ll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1lll1l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll11l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᓮ").format(e)
                )
        try:
            if passed:
                bstack11ll11lll_opy_(getattr(item, bstack1lll11l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᓯ"), None), bstack1lll11l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᓰ"))
            else:
                error_message = bstack1lll11l_opy_ (u"࠭ࠧᓱ")
                if bstack1l1lll1l1l_opy_:
                    bstack1ll1l111l1_opy_(item._page, str(bstack1l1lll1l1l_opy_), bstack1lll11l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᓲ"))
                    bstack11ll11lll_opy_(getattr(item, bstack1lll11l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᓳ"), None), bstack1lll11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᓴ"), str(bstack1l1lll1l1l_opy_))
                    error_message = str(bstack1l1lll1l1l_opy_)
                else:
                    bstack11ll11lll_opy_(getattr(item, bstack1lll11l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᓵ"), None), bstack1lll11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᓶ"))
                bstack111111lll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1lll11l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤᓷ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1lll11l_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᓸ"), default=bstack1lll11l_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᓹ"), help=bstack1lll11l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᓺ"))
    parser.addoption(bstack1lll11l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᓻ"), default=bstack1lll11l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᓼ"), help=bstack1lll11l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᓽ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1lll11l_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢᓾ"), action=bstack1lll11l_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧᓿ"), default=bstack1lll11l_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢᔀ"),
                         help=bstack1lll11l_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢᔁ"))
def bstack1l11ll1111_opy_(log):
    if not (log[bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔂ")] and log[bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔃ")].strip()):
        return
    active = bstack1l11ll1l11_opy_()
    log = {
        bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᔄ"): log[bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᔅ")],
        bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᔆ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"࡛ࠧࠩᔇ"),
        bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔈ"): log[bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔉ")],
    }
    if active:
        if active[bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨᔊ")] == bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᔋ"):
            log[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔌ")] = active[bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔍ")]
        elif active[bstack1lll11l_opy_ (u"ࠧࡵࡻࡳࡩࠬᔎ")] == bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᔏ"):
            log[bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔐ")] = active[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔑ")]
    bstack1l1llll1ll_opy_.bstack1l11l1l1l1_opy_([log])
def bstack1l11ll1l11_opy_():
    if len(store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔒ")]) > 0 and store[bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔓ")][-1]:
        return {
            bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫᔔ"): bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᔕ"),
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔖ"): store[bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᔗ")][-1]
        }
    if store.get(bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔘ"), None):
        return {
            bstack1lll11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᔙ"): bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࠪᔚ"),
            bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔛ"): store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔜ")]
        }
    return None
bstack1l1l11111l_opy_ = bstack1l1l111lll_opy_(bstack1l11ll1111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack11111l1l11_opy_
        if bstack11111l1l11_opy_:
            driver = getattr(item, bstack1lll11l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᔝ"), None)
            bstack1ll1l11111_opy_ = bstack11l11llll_opy_.bstack1l11lllll_opy_(CONFIG, bstack11l11ll1ll_opy_(item.own_markers))
            item._a11y_started = bstack11l11llll_opy_.bstack1l1ll1l11_opy_(driver, bstack1ll1l11111_opy_)
        if not bstack1l1llll1ll_opy_.on() or bstack11111lll1l_opy_ != bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᔞ"):
            return
        global current_test_uuid, bstack1l1l11111l_opy_
        bstack1l1l11111l_opy_.start()
        bstack1l11l11ll1_opy_ = {
            bstack1lll11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᔟ"): uuid4().__str__(),
            bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᔠ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠬࡠࠧᔡ")
        }
        current_test_uuid = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᔢ")]
        store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔣ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᔤ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1l1ll11l_opy_[item.nodeid] = {**_1l1l1ll11l_opy_[item.nodeid], **bstack1l11l11ll1_opy_}
        bstack11111ll1ll_opy_(item, _1l1l1ll11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᔥ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬᔦ"), str(err))
def pytest_runtest_setup(item):
    if bstack11l1l1111l_opy_():
        atexit.register(bstack1llllll1ll_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1lll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᔧ")
    try:
        if not bstack1l1llll1ll_opy_.on():
            return
        bstack1l1l11111l_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l11ll1_opy_ = {
            bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᔨ"): uuid,
            bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᔩ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"࡛ࠧࠩᔪ"),
            bstack1lll11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᔫ"): bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᔬ"),
            bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᔭ"): bstack1lll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᔮ"),
            bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᔯ"): bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᔰ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᔱ")] = item
        store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᔲ")] = [uuid]
        if not _1l1l1ll11l_opy_.get(item.nodeid, None):
            _1l1l1ll11l_opy_[item.nodeid] = {bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᔳ"): [], bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᔴ"): []}
        _1l1l1ll11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᔵ")].append(bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᔶ")])
        _1l1l1ll11l_opy_[item.nodeid + bstack1lll11l_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭ᔷ")] = bstack1l11l11ll1_opy_
        bstack11111lll11_opy_(item, bstack1l11l11ll1_opy_, bstack1lll11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᔸ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᔹ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111ll11l1_opy_
        if getattr(item, bstack1lll11l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᔺ"), False):
            logger.info(bstack1lll11l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥᔻ"))
            driver = getattr(item, bstack1lll11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᔼ"), None)
            bstack11ll1l1111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l11llll_opy_.bstack1l1111lll_opy_(driver, bstack11ll1l1111_opy_, item.name, item.module.__name__, item.path, bstack111ll11l1_opy_)
        if not bstack1l1llll1ll_opy_.on():
            return
        bstack1l11l11ll1_opy_ = {
            bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᔽ"): uuid4().__str__(),
            bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᔾ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"࡛ࠧࠩᔿ"),
            bstack1lll11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᕀ"): bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᕁ"),
            bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᕂ"): bstack1lll11l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᕃ"),
            bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᕄ"): bstack1lll11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᕅ")
        }
        _1l1l1ll11l_opy_[item.nodeid + bstack1lll11l_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᕆ")] = bstack1l11l11ll1_opy_
        bstack11111lll11_opy_(item, bstack1l11l11ll1_opy_, bstack1lll11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᕇ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨᕈ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1llll1ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack111ll1111l_opy_(fixturedef.argname):
        store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᕉ")] = request.node
    elif bstack111ll11l1l_opy_(fixturedef.argname):
        store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᕊ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᕋ"): fixturedef.argname,
            bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᕌ"): bstack11l1111l1l_opy_(outcome),
            bstack1lll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᕍ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack111111llll_opy_ = store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᕎ")]
        if not _1l1l1ll11l_opy_.get(bstack111111llll_opy_.nodeid, None):
            _1l1l1ll11l_opy_[bstack111111llll_opy_.nodeid] = {bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᕏ"): []}
        _1l1l1ll11l_opy_[bstack111111llll_opy_.nodeid][bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᕐ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᕑ"), str(err))
if bstack1ll11llll1_opy_() and bstack1l1llll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1l1ll11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᕒ")].bstack111l1111l1_opy_(id(step))
        except Exception as err:
            print(bstack1lll11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫᕓ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1l1ll11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᕔ")].bstack1l1l1111ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᕕ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1l1l1ll1_opy_: bstack1l11l1l111_opy_ = _1l1l1ll11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᕖ")]
            bstack1l1l1l1ll1_opy_.bstack1l1l1111ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᕗ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111lll1l_opy_
        try:
            if not bstack1l1llll1ll_opy_.on() or bstack11111lll1l_opy_ != bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᕘ"):
                return
            global bstack1l1l11111l_opy_
            bstack1l1l11111l_opy_.start()
            if not _1l1l1ll11l_opy_.get(request.node.nodeid, None):
                _1l1l1ll11l_opy_[request.node.nodeid] = {}
            bstack1l1l1l1ll1_opy_ = bstack1l11l1l111_opy_.bstack111l111111_opy_(
                scenario, feature, request.node,
                name=bstack111ll111l1_opy_(request.node, scenario),
                bstack1l1l1ll1ll_opy_=bstack11l111ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1lll11l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᕙ"),
                tags=bstack111ll111ll_opy_(feature, scenario)
            )
            _1l1l1ll11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᕚ")] = bstack1l1l1l1ll1_opy_
            bstack11111llll1_opy_(bstack1l1l1l1ll1_opy_.uuid)
            bstack1l1llll1ll_opy_.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᕛ"), bstack1l1l1l1ll1_opy_)
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᕜ"), str(err))
def bstack11111l1lll_opy_(bstack11111l11ll_opy_):
    if bstack11111l11ll_opy_ in store[bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᕝ")]:
        store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᕞ")].remove(bstack11111l11ll_opy_)
def bstack11111llll1_opy_(bstack111111l111_opy_):
    store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᕟ")] = bstack111111l111_opy_
    threading.current_thread().current_test_uuid = bstack111111l111_opy_
@bstack1l1llll1ll_opy_.bstack1111l11l11_opy_
def bstack11111111l1_opy_(item, call, report):
    global bstack11111lll1l_opy_
    try:
        if report.when == bstack1lll11l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᕠ"):
            bstack1l1l11111l_opy_.reset()
        if report.when == bstack1lll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᕡ"):
            if bstack11111lll1l_opy_ == bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᕢ"):
                _1l1l1ll11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᕣ")] = bstack11l111l111_opy_(report.stop)
                bstack11111ll1ll_opy_(item, _1l1l1ll11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᕤ"), report, call)
                store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᕥ")] = None
            elif bstack11111lll1l_opy_ == bstack1lll11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᕦ"):
                bstack1l1l1l1ll1_opy_ = _1l1l1ll11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᕧ")]
                bstack1l1l1l1ll1_opy_.set(hooks=_1l1l1ll11l_opy_[item.nodeid].get(bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᕨ"), []))
                exception, bstack1l11lll1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11lll1ll_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l1l1l1ll1_opy_.stop(time=bstack11l111l111_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11lll1ll_opy_=bstack1l11lll1ll_opy_))
                bstack1l1llll1ll_opy_.bstack1l1l11l1l1_opy_(bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᕩ"), _1l1l1ll11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᕪ")])
        elif report.when in [bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᕫ"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᕬ")]:
            bstack1l1l1l11ll_opy_ = item.nodeid + bstack1lll11l_opy_ (u"ࠫ࠲࠭ᕭ") + report.when
            if report.skipped:
                hook_type = bstack1lll11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᕮ") if report.when == bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᕯ") else bstack1lll11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᕰ")
                _1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_] = {
                    bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᕱ"): uuid4().__str__(),
                    bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᕲ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬᕳ"),
                    bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᕴ"): hook_type
                }
            _1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᕵ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1lll11l_opy_ (u"࡚࠭ࠨᕶ")
            bstack11111l1lll_opy_(_1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕷ")])
            bstack11111lll11_opy_(item, _1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_], bstack1lll11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᕸ"), report, call)
            if report.when == bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᕹ"):
                if report.outcome == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᕺ"):
                    bstack1l11l11ll1_opy_ = {
                        bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᕻ"): uuid4().__str__(),
                        bstack1lll11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᕼ"): bstack11l111ll1_opy_(),
                        bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᕽ"): bstack11l111ll1_opy_()
                    }
                    _1l1l1ll11l_opy_[item.nodeid] = {**_1l1l1ll11l_opy_[item.nodeid], **bstack1l11l11ll1_opy_}
                    bstack11111ll1ll_opy_(item, _1l1l1ll11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᕾ"))
                    bstack11111ll1ll_opy_(item, _1l1l1ll11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᕿ"), report, call)
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᖀ"), str(err))
def bstack11111ll11l_opy_(test, bstack1l11l11ll1_opy_, result=None, call=None, bstack11lllllll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1l1l1ll1_opy_ = {
        bstack1lll11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖁ"): bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᖂ")],
        bstack1lll11l_opy_ (u"ࠬࡺࡹࡱࡧࠪᖃ"): bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࠫᖄ"),
        bstack1lll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᖅ"): test.name,
        bstack1lll11l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᖆ"): {
            bstack1lll11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᖇ"): bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᖈ"),
            bstack1lll11l_opy_ (u"ࠫࡨࡵࡤࡦࠩᖉ"): inspect.getsource(test.obj)
        },
        bstack1lll11l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᖊ"): test.name,
        bstack1lll11l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᖋ"): test.name,
        bstack1lll11l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᖌ"): bstack1l1llll1ll_opy_.bstack1l1l1l1l11_opy_(test),
        bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᖍ"): file_path,
        bstack1lll11l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᖎ"): file_path,
        bstack1lll11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᖏ"): bstack1lll11l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᖐ"),
        bstack1lll11l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᖑ"): file_path,
        bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᖒ"): bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᖓ")],
        bstack1lll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᖔ"): bstack1lll11l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᖕ"),
        bstack1lll11l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᖖ"): {
            bstack1lll11l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᖗ"): test.nodeid
        },
        bstack1lll11l_opy_ (u"ࠬࡺࡡࡨࡵࠪᖘ"): bstack11l11ll1ll_opy_(test.own_markers)
    }
    if bstack11lllllll_opy_ in [bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᖙ"), bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᖚ")]:
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᖛ")] = {
            bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᖜ"): bstack1l11l11ll1_opy_.get(bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᖝ"), [])
        }
    if bstack11lllllll_opy_ == bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᖞ"):
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᖟ")] = bstack1lll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᖠ")
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖡ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖢ")]
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᖣ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᖤ")]
    if result:
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᖥ")] = result.outcome
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᖦ")] = result.duration * 1000
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᖧ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖨ")]
        if result.failed:
            bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᖩ")] = bstack1l1llll1ll_opy_.bstack1l111l1l11_opy_(call.excinfo.typename)
            bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᖪ")] = bstack1l1llll1ll_opy_.bstack1111l1l11l_opy_(call.excinfo, result)
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖫ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᖬ")]
    if outcome:
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᖭ")] = bstack11l1111l1l_opy_(outcome)
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᖮ")] = 0
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖯ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᖰ")]
        if bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᖱ")] == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᖲ"):
            bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᖳ")] = bstack1lll11l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᖴ")  # bstack11111l1l1l_opy_
            bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᖵ")] = [{bstack1lll11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᖶ"): [bstack1lll11l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᖷ")]}]
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖸ")] = bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖹ")]
    return bstack1l1l1l1ll1_opy_
def bstack11111ll111_opy_(test, bstack1l11l1lll1_opy_, bstack11lllllll_opy_, result, call, outcome, bstack1111111l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᖺ")]
    hook_name = bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᖻ")]
    hook_data = {
        bstack1lll11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖼ"): bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖽ")],
        bstack1lll11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖾ"): bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᖿ"),
        bstack1lll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᗀ"): bstack1lll11l_opy_ (u"ࠫࢀࢃࠧᗁ").format(bstack111l1llll1_opy_(hook_name)),
        bstack1lll11l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᗂ"): {
            bstack1lll11l_opy_ (u"࠭࡬ࡢࡰࡪࠫᗃ"): bstack1lll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᗄ"),
            bstack1lll11l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᗅ"): None
        },
        bstack1lll11l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᗆ"): test.name,
        bstack1lll11l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᗇ"): bstack1l1llll1ll_opy_.bstack1l1l1l1l11_opy_(test, hook_name),
        bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᗈ"): file_path,
        bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᗉ"): file_path,
        bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗊ"): bstack1lll11l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᗋ"),
        bstack1lll11l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᗌ"): file_path,
        bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᗍ"): bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᗎ")],
        bstack1lll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᗏ"): bstack1lll11l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᗐ") if bstack11111lll1l_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᗑ") else bstack1lll11l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᗒ"),
        bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᗓ"): hook_type
    }
    bstack11111l1111_opy_ = bstack1l11l1llll_opy_(_1l1l1ll11l_opy_.get(test.nodeid, None))
    if bstack11111l1111_opy_:
        hook_data[bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᗔ")] = bstack11111l1111_opy_
    if result:
        hook_data[bstack1lll11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᗕ")] = result.outcome
        hook_data[bstack1lll11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᗖ")] = result.duration * 1000
        hook_data[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗗ")] = bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᗘ")]
        if result.failed:
            hook_data[bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᗙ")] = bstack1l1llll1ll_opy_.bstack1l111l1l11_opy_(call.excinfo.typename)
            hook_data[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᗚ")] = bstack1l1llll1ll_opy_.bstack1111l1l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1lll11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗛ")] = bstack11l1111l1l_opy_(outcome)
        hook_data[bstack1lll11l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᗜ")] = 100
        hook_data[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗝ")] = bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗞ")]
        if hook_data[bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗟ")] == bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗠ"):
            hook_data[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᗡ")] = bstack1lll11l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᗢ")  # bstack11111l1l1l_opy_
            hook_data[bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᗣ")] = [{bstack1lll11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᗤ"): [bstack1lll11l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᗥ")]}]
    if bstack1111111l1l_opy_:
        hook_data[bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗦ")] = bstack1111111l1l_opy_.result
        hook_data[bstack1lll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᗧ")] = bstack11l11lll1l_opy_(bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᗨ")], bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗩ")])
        hook_data[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗪ")] = bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗫ")]
        if hook_data[bstack1lll11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᗬ")] == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗭ"):
            hook_data[bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᗮ")] = bstack1l1llll1ll_opy_.bstack1l111l1l11_opy_(bstack1111111l1l_opy_.exception_type)
            hook_data[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᗯ")] = [{bstack1lll11l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗰ"): bstack11l1l1llll_opy_(bstack1111111l1l_opy_.exception)}]
    return hook_data
def bstack11111ll1ll_opy_(test, bstack1l11l11ll1_opy_, bstack11lllllll_opy_, result=None, call=None, outcome=None):
    bstack1l1l1l1ll1_opy_ = bstack11111ll11l_opy_(test, bstack1l11l11ll1_opy_, result, call, bstack11lllllll_opy_, outcome)
    driver = getattr(test, bstack1lll11l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᗱ"), None)
    if bstack11lllllll_opy_ == bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᗲ") and driver:
        bstack1l1l1l1ll1_opy_[bstack1lll11l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᗳ")] = bstack1l1llll1ll_opy_.bstack1l11ll111l_opy_(driver)
    if bstack11lllllll_opy_ == bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᗴ"):
        bstack11lllllll_opy_ = bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᗵ")
    bstack1l1l111111_opy_ = {
        bstack1lll11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᗶ"): bstack11lllllll_opy_,
        bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᗷ"): bstack1l1l1l1ll1_opy_
    }
    bstack1l1llll1ll_opy_.bstack1l11lll1l1_opy_(bstack1l1l111111_opy_)
def bstack11111lll11_opy_(test, bstack1l11l11ll1_opy_, bstack11lllllll_opy_, result=None, call=None, outcome=None, bstack1111111l1l_opy_=None):
    hook_data = bstack11111ll111_opy_(test, bstack1l11l11ll1_opy_, bstack11lllllll_opy_, result, call, outcome, bstack1111111l1l_opy_)
    bstack1l1l111111_opy_ = {
        bstack1lll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᗸ"): bstack11lllllll_opy_,
        bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᗹ"): hook_data
    }
    bstack1l1llll1ll_opy_.bstack1l11lll1l1_opy_(bstack1l1l111111_opy_)
def bstack1l11l1llll_opy_(bstack1l11l11ll1_opy_):
    if not bstack1l11l11ll1_opy_:
        return None
    if bstack1l11l11ll1_opy_.get(bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗺ"), None):
        return getattr(bstack1l11l11ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᗻ")], bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᗼ"), None)
    return bstack1l11l11ll1_opy_.get(bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᗽ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1llll1ll_opy_.on():
            return
        places = [bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᗾ"), bstack1lll11l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᗿ"), bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘀ")]
        bstack1l1l1l1lll_opy_ = []
        for bstack111111ll1l_opy_ in places:
            records = caplog.get_records(bstack111111ll1l_opy_)
            bstack11111l11l1_opy_ = bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘁ") if bstack111111ll1l_opy_ == bstack1lll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᘂ") else bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘃ")
            bstack111111l1l1_opy_ = request.node.nodeid + (bstack1lll11l_opy_ (u"ࠨࠩᘄ") if bstack111111ll1l_opy_ == bstack1lll11l_opy_ (u"ࠩࡦࡥࡱࡲࠧᘅ") else bstack1lll11l_opy_ (u"ࠪ࠱ࠬᘆ") + bstack111111ll1l_opy_)
            bstack111111l111_opy_ = bstack1l11l1llll_opy_(_1l1l1ll11l_opy_.get(bstack111111l1l1_opy_, None))
            if not bstack111111l111_opy_:
                continue
            for record in records:
                if bstack11l11l111l_opy_(record.message):
                    continue
                bstack1l1l1l1lll_opy_.append({
                    bstack1lll11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᘇ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1lll11l_opy_ (u"ࠬࡠࠧᘈ"),
                    bstack1lll11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘉ"): record.levelname,
                    bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘊ"): record.message,
                    bstack11111l11l1_opy_: bstack111111l111_opy_
                })
        if len(bstack1l1l1l1lll_opy_) > 0:
            bstack1l1llll1ll_opy_.bstack1l11l1l1l1_opy_(bstack1l1l1l1lll_opy_)
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᘋ"), str(err))
def bstack1ll1ll11ll_opy_(driver_command, response):
    if driver_command == bstack1lll11l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᘌ"):
        bstack1l1llll1ll_opy_.bstack1l1lllll11_opy_({
            bstack1lll11l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᘍ"): response[bstack1lll11l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᘎ")],
            bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘏ"): store[bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᘐ")]
        })
def bstack1llllll1ll_opy_():
    global bstack111l1ll1l_opy_
    bstack1l1llll1ll_opy_.bstack1l1l11ll1l_opy_()
    for driver in bstack111l1ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l11ll_opy_(self, *args, **kwargs):
    bstack1lll1111_opy_ = bstack1l1l11ll1_opy_(self, *args, **kwargs)
    bstack1l1llll1ll_opy_.bstack11l111l1_opy_(self)
    return bstack1lll1111_opy_
def bstack1lll1l1ll1_opy_(framework_name):
    global bstack1l1l11l1l_opy_
    global bstack1lllll1ll1_opy_
    bstack1l1l11l1l_opy_ = framework_name
    logger.info(bstack111lll1l1_opy_.format(bstack1l1l11l1l_opy_.split(bstack1lll11l_opy_ (u"ࠧ࠮ࠩᘑ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l11ll1l1_opy_():
            Service.start = bstack1ll1l1l1l1_opy_
            Service.stop = bstack1111111l1_opy_
            webdriver.Remote.__init__ = bstack1l111ll1_opy_
            webdriver.Remote.get = bstack1ll1lll11l_opy_
            if not isinstance(os.getenv(bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩᘒ")), str):
                return
            WebDriver.close = bstack1l1ll111_opy_
            WebDriver.quit = bstack11l1ll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1llll111l1_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1ll1llll11_opy_ = getAccessibilityResultsSummary
        if not bstack11l11ll1l1_opy_() and bstack1l1llll1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1lll1l11ll_opy_
        bstack1lllll1ll1_opy_ = True
    except Exception as e:
        pass
    bstack111lllll1_opy_()
    if os.environ.get(bstack1lll11l_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧᘓ")):
        bstack1lllll1ll1_opy_ = eval(os.environ.get(bstack1lll11l_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨᘔ")))
    if not bstack1lllll1ll1_opy_:
        bstack1l11lll1l_opy_(bstack1lll11l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨᘕ"), bstack1ll111l11l_opy_)
    if bstack1llll111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack111l1l1l_opy_
        except Exception as e:
            logger.error(bstack1l1ll1lll_opy_.format(str(e)))
    if bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᘖ") in str(framework_name).lower():
        if not bstack11l11ll1l1_opy_():
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
def bstack11l1ll11l_opy_(self):
    global bstack1l1l11l1l_opy_
    global bstack1ll1ll1ll_opy_
    global bstack111lll1l_opy_
    try:
        if bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᘗ") in bstack1l1l11l1l_opy_ and self.session_id != None and bstack1l1111111_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᘘ"), bstack1lll11l_opy_ (u"ࠨࠩᘙ")) != bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᘚ"):
            bstack1lll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᘛ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘜ")
            bstack1lll11ll_opy_(logger, True)
            if self != None:
                bstack11llll1l1_opy_(self, bstack1lll1l1l1_opy_, bstack1lll11l_opy_ (u"ࠬ࠲ࠠࠨᘝ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack1lll11l_opy_ (u"࠭ࠧᘞ")
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣᘟ") + str(e))
    bstack111lll1l_opy_(self)
    self.session_id = None
def bstack1l111ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1ll1ll_opy_
    global bstack1lllll11ll_opy_
    global bstack1ll1111ll1_opy_
    global bstack1l1l11l1l_opy_
    global bstack1l1l11ll1_opy_
    global bstack111l1ll1l_opy_
    global bstack1lll111l1l_opy_
    global bstack1ll11ll1l_opy_
    global bstack11111l1l11_opy_
    global bstack111ll11l1_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᘠ")] = str(bstack1l1l11l1l_opy_) + str(__version__)
    command_executor = bstack11l1111l_opy_(bstack1lll111l1l_opy_)
    logger.debug(bstack1lll1l111_opy_.format(command_executor))
    proxy = bstack1ll1ll1ll1_opy_(CONFIG, proxy)
    bstack1ll1ll11_opy_ = 0
    try:
        if bstack1ll1111ll1_opy_ is True:
            bstack1ll1ll11_opy_ = int(os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᘡ")))
    except:
        bstack1ll1ll11_opy_ = 0
    bstack11ll1ll1l_opy_ = bstack111111ll_opy_(CONFIG, bstack1ll1ll11_opy_)
    logger.debug(bstack1ll111l111_opy_.format(str(bstack11ll1ll1l_opy_)))
    bstack111ll11l1_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘢ"))[bstack1ll1ll11_opy_]
    if bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᘣ") in CONFIG and CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᘤ")]:
        bstack111l111ll_opy_(bstack11ll1ll1l_opy_, bstack1ll11ll1l_opy_)
    if desired_capabilities:
        bstack1l1lll11_opy_ = bstack1111l111l_opy_(desired_capabilities)
        bstack1l1lll11_opy_[bstack1lll11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᘥ")] = bstack1lllll1l11_opy_(CONFIG)
        bstack1l1ll1ll_opy_ = bstack111111ll_opy_(bstack1l1lll11_opy_)
        if bstack1l1ll1ll_opy_:
            bstack11ll1ll1l_opy_ = update(bstack1l1ll1ll_opy_, bstack11ll1ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack111ll1ll1_opy_(options, bstack11ll1ll1l_opy_)
    if not options:
        options = bstack1lllll111_opy_(bstack11ll1ll1l_opy_)
    if bstack11l11llll_opy_.bstack111l1111l_opy_(CONFIG, bstack1ll1ll11_opy_) and bstack11l11llll_opy_.bstack1l1ll111l_opy_(bstack11ll1ll1l_opy_, options):
        bstack11111l1l11_opy_ = True
        bstack11l11llll_opy_.set_capabilities(bstack11ll1ll1l_opy_, CONFIG)
    if proxy and bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᘦ")):
        options.proxy(proxy)
    if options and bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᘧ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll1l1_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᘨ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll1ll1l_opy_)
    logger.info(bstack1llllll11_opy_)
    if bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᘩ")):
        bstack1l1l11ll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᘪ")):
        bstack1l1l11ll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᘫ")):
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
        bstack1ll11111l_opy_ = bstack1lll11l_opy_ (u"࠭ࠧᘬ")
        if bstack1llll1l1_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨᘭ")):
            bstack1ll11111l_opy_ = self.caps.get(bstack1lll11l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᘮ"))
        else:
            bstack1ll11111l_opy_ = self.capabilities.get(bstack1lll11l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤᘯ"))
        if bstack1ll11111l_opy_:
            bstack1ll11ll1_opy_(bstack1ll11111l_opy_)
            if bstack1llll1l1_opy_() <= version.parse(bstack1lll11l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᘰ")):
                self.command_executor._url = bstack1lll11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᘱ") + bstack1lll111l1l_opy_ + bstack1lll11l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᘲ")
            else:
                self.command_executor._url = bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᘳ") + bstack1ll11111l_opy_ + bstack1lll11l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᘴ")
            logger.debug(bstack1l11111l_opy_.format(bstack1ll11111l_opy_))
        else:
            logger.debug(bstack1ll1lll1l_opy_.format(bstack1lll11l_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᘵ")))
    except Exception as e:
        logger.debug(bstack1ll1lll1l_opy_.format(e))
    bstack1ll1ll1ll_opy_ = self.session_id
    if bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᘶ") in bstack1l1l11l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l1llll1ll_opy_.bstack11l111l1_opy_(self)
    bstack111l1ll1l_opy_.append(self)
    if bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘷ") in CONFIG and bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᘸ") in CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᘹ")][bstack1ll1ll11_opy_]:
        bstack1lllll11ll_opy_ = CONFIG[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘺ")][bstack1ll1ll11_opy_][bstack1lll11l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᘻ")]
    logger.debug(bstack11ll11l1l_opy_.format(bstack1ll1ll1ll_opy_))
def bstack1ll1lll11l_opy_(self, url):
    global bstack1lllllll11_opy_
    global CONFIG
    try:
        bstack111l1ll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1llll1l11_opy_.format(str(err)))
    try:
        bstack1lllllll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1llllllll_opy_ = str(e)
            if any(err_msg in bstack1llllllll_opy_ for err_msg in bstack1lll111l11_opy_):
                bstack111l1ll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1llll1l11_opy_.format(str(err)))
        raise e
def bstack1ll1111ll_opy_(item, when):
    global bstack1l1llllll1_opy_
    try:
        bstack1l1llllll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11lll11_opy_(item, call, rep):
    global bstack11l11l111_opy_
    global bstack111l1ll1l_opy_
    name = bstack1lll11l_opy_ (u"ࠨࠩᘼ")
    try:
        if rep.when == bstack1lll11l_opy_ (u"ࠩࡦࡥࡱࡲࠧᘽ"):
            bstack1ll1ll1ll_opy_ = threading.current_thread().bstackSessionId
            bstack11111l1ll1_opy_ = item.config.getoption(bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᘾ"))
            try:
                if (str(bstack11111l1ll1_opy_).lower() != bstack1lll11l_opy_ (u"ࠫࡹࡸࡵࡦࠩᘿ")):
                    name = str(rep.nodeid)
                    bstack1l1lll111_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙀ"), name, bstack1lll11l_opy_ (u"࠭ࠧᙁ"), bstack1lll11l_opy_ (u"ࠧࠨᙂ"), bstack1lll11l_opy_ (u"ࠨࠩᙃ"), bstack1lll11l_opy_ (u"ࠩࠪᙄ"))
                    os.environ[bstack1lll11l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᙅ")] = name
                    for driver in bstack111l1ll1l_opy_:
                        if bstack1ll1ll1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1lll111_opy_)
            except Exception as e:
                logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᙆ").format(str(e)))
            try:
                bstack1l1lll1lll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1lll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᙇ"):
                    status = bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᙈ") if rep.outcome.lower() == bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᙉ") else bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᙊ")
                    reason = bstack1lll11l_opy_ (u"ࠩࠪᙋ")
                    if status == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙌ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1lll11l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᙍ") if status == bstack1lll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙎ") else bstack1lll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᙏ")
                    data = name + bstack1lll11l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩᙐ") if status == bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᙑ") else name + bstack1lll11l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬᙒ") + reason
                    bstack1ll1l11l11_opy_ = bstack1l11lll11_opy_(bstack1lll11l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᙓ"), bstack1lll11l_opy_ (u"ࠫࠬᙔ"), bstack1lll11l_opy_ (u"ࠬ࠭ᙕ"), bstack1lll11l_opy_ (u"࠭ࠧᙖ"), level, data)
                    for driver in bstack111l1ll1l_opy_:
                        if bstack1ll1ll1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1l11l11_opy_)
            except Exception as e:
                logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᙗ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬᙘ").format(str(e)))
    bstack11l11l111_opy_(item, call, rep)
notset = Notset()
def bstack1ll1l1l11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll1lll1_opy_
    if str(name).lower() == bstack1lll11l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᙙ"):
        return bstack1lll11l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᙚ")
    else:
        return bstack1lll1lll1_opy_(self, name, default, skip)
def bstack111l1l1l_opy_(self):
    global CONFIG
    global bstack1llll11ll_opy_
    try:
        proxy = bstack11llllll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1lll11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᙛ")):
                proxies = bstack1ll11l111_opy_(proxy, bstack11l1111l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll11l11_opy_ = proxies.popitem()
                    if bstack1lll11l_opy_ (u"ࠧࡀ࠯࠰ࠤᙜ") in bstack1lll11l11_opy_:
                        return bstack1lll11l11_opy_
                    else:
                        return bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᙝ") + bstack1lll11l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1lll11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦᙞ").format(str(e)))
    return bstack1llll11ll_opy_(self)
def bstack1llll111_opy_():
    return (bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᙟ") in CONFIG or bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᙠ") in CONFIG) and bstack1llll11l11_opy_() and bstack1llll1l1_opy_() >= version.parse(
        bstack1l1111l1l_opy_)
def bstack1lll11ll1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lllll11ll_opy_
    global bstack1ll1111ll1_opy_
    global bstack1l1l11l1l_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᙡ")] = str(bstack1l1l11l1l_opy_) + str(__version__)
    bstack1ll1ll11_opy_ = 0
    try:
        if bstack1ll1111ll1_opy_ is True:
            bstack1ll1ll11_opy_ = int(os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᙢ")))
    except:
        bstack1ll1ll11_opy_ = 0
    CONFIG[bstack1lll11l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᙣ")] = True
    bstack11ll1ll1l_opy_ = bstack111111ll_opy_(CONFIG, bstack1ll1ll11_opy_)
    logger.debug(bstack1ll111l111_opy_.format(str(bstack11ll1ll1l_opy_)))
    if CONFIG.get(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᙤ")):
        bstack111l111ll_opy_(bstack11ll1ll1l_opy_, bstack1ll11ll1l_opy_)
    if bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙥ") in CONFIG and bstack1lll11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙦ") in CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᙧ")][bstack1ll1ll11_opy_]:
        bstack1lllll11ll_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᙨ")][bstack1ll1ll11_opy_][bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᙩ")]
    import urllib
    import json
    bstack111l1l11_opy_ = bstack1lll11l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧᙪ") + urllib.parse.quote(json.dumps(bstack11ll1ll1l_opy_))
    browser = self.connect(bstack111l1l11_opy_)
    return browser
def bstack111lllll1_opy_():
    global bstack1lllll1ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll11ll1l_opy_
        bstack1lllll1ll1_opy_ = True
    except Exception as e:
        pass
def bstack11111111ll_opy_():
    global CONFIG
    global bstack1l1l1lll_opy_
    global bstack1lll111l1l_opy_
    global bstack1ll11ll1l_opy_
    global bstack1ll1111ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬᙫ")))
    bstack1l1l1lll_opy_ = eval(os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᙬ")))
    bstack1lll111l1l_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ᙭"))
    bstack1lll1l1l_opy_(CONFIG, bstack1l1l1lll_opy_)
    bstack1ll1l1llll_opy_()
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
    if (bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᙮") in CONFIG or bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᙯ") in CONFIG) and bstack1llll11l11_opy_():
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
        logger.debug(bstack1lll11l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬᙰ"))
    bstack1ll11ll1l_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙱ"), {}).get(bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᙲ"))
    bstack1ll1111ll1_opy_ = True
    bstack1lll1l1ll1_opy_(bstack11lll1lll_opy_)
if (bstack11l1l1111l_opy_()):
    bstack11111111ll_opy_()
@bstack1l11l11l11_opy_(class_method=False)
def bstack1111111lll_opy_(hook_name, event, bstack11111l111l_opy_=None):
    if hook_name not in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᙳ"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᙴ"), bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᙵ"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᙶ"), bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᙷ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᙸ"), bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᙹ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᙺ")]:
        return
    node = store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᙻ")]
    if hook_name in [bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᙼ"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᙽ")]:
        node = store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᙾ")]
    elif hook_name in [bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᙿ"), bstack1lll11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ ")]:
        node = store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᚁ")]
    if event == bstack1lll11l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᚂ"):
        hook_type = bstack111l1lllll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l1lll1_opy_ = {
            bstack1lll11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚃ"): uuid,
            bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚄ"): bstack11l111ll1_opy_(),
            bstack1lll11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᚅ"): bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᚆ"),
            bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᚇ"): hook_type,
            bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᚈ"): hook_name
        }
        store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᚉ")].append(uuid)
        bstack1111111l11_opy_ = node.nodeid
        if hook_type == bstack1lll11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᚊ"):
            if not _1l1l1ll11l_opy_.get(bstack1111111l11_opy_, None):
                _1l1l1ll11l_opy_[bstack1111111l11_opy_] = {bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᚋ"): []}
            _1l1l1ll11l_opy_[bstack1111111l11_opy_][bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᚌ")].append(bstack1l11l1lll1_opy_[bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚍ")])
        _1l1l1ll11l_opy_[bstack1111111l11_opy_ + bstack1lll11l_opy_ (u"࠭࠭ࠨᚎ") + hook_name] = bstack1l11l1lll1_opy_
        bstack11111lll11_opy_(node, bstack1l11l1lll1_opy_, bstack1lll11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᚏ"))
    elif event == bstack1lll11l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᚐ"):
        bstack1l1l1l11ll_opy_ = node.nodeid + bstack1lll11l_opy_ (u"ࠩ࠰ࠫᚑ") + hook_name
        _1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚒ")] = bstack11l111ll1_opy_()
        bstack11111l1lll_opy_(_1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_][bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᚓ")])
        bstack11111lll11_opy_(node, _1l1l1ll11l_opy_[bstack1l1l1l11ll_opy_], bstack1lll11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᚔ"), bstack1111111l1l_opy_=bstack11111l111l_opy_)
def bstack111111ll11_opy_():
    global bstack11111lll1l_opy_
    if bstack1ll11llll1_opy_():
        bstack11111lll1l_opy_ = bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᚕ")
    else:
        bstack11111lll1l_opy_ = bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᚖ")
@bstack1l1llll1ll_opy_.bstack1111l11l11_opy_
def bstack11111ll1l1_opy_():
    bstack111111ll11_opy_()
    if bstack1llll11l11_opy_():
        bstack1ll1l1ll1l_opy_(bstack1ll1ll11ll_opy_)
    bstack111llll111_opy_ = bstack111llll1l1_opy_(bstack1111111lll_opy_)
bstack11111ll1l1_opy_()