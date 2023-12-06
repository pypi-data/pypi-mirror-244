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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l1111111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111llll1l1_opy_:
    def __init__(self, handler):
        self._11l1111l11_opy_ = {}
        self._11l111111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l1111l11_opy_[bstack1lll11l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬኯ")] = Module._inject_setup_function_fixture
        self._11l1111l11_opy_[bstack1lll11l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫኰ")] = Module._inject_setup_module_fixture
        self._11l1111l11_opy_[bstack1lll11l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ኱")] = Class._inject_setup_class_fixture
        self._11l1111l11_opy_[bstack1lll11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ኲ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack111lll1ll1_opy_(bstack1lll11l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩኳ"))
        Module._inject_setup_module_fixture = self.bstack111lll1ll1_opy_(bstack1lll11l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨኴ"))
        Class._inject_setup_class_fixture = self.bstack111lll1ll1_opy_(bstack1lll11l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨኵ"))
        Class._inject_setup_method_fixture = self.bstack111lll1ll1_opy_(bstack1lll11l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ኶"))
    def bstack111llll1ll_opy_(self, bstack111llllll1_opy_, hook_type):
        meth = getattr(bstack111llllll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l111111l_opy_[hook_type] = meth
            setattr(bstack111llllll1_opy_, hook_type, self.bstack111lllll11_opy_(hook_type))
    def bstack111llll11l_opy_(self, instance, bstack111lllll1l_opy_):
        if bstack111lllll1l_opy_ == bstack1lll11l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ኷"):
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧኸ"))
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤኹ"))
        if bstack111lllll1l_opy_ == bstack1lll11l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢኺ"):
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨኻ"))
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥኼ"))
        if bstack111lllll1l_opy_ == bstack1lll11l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤኽ"):
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣኾ"))
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧ኿"))
        if bstack111lllll1l_opy_ == bstack1lll11l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዀ"):
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧ዁"))
            self.bstack111llll1ll_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤዂ"))
    @staticmethod
    def bstack111lllllll_opy_(hook_type, func, args):
        if hook_type in [bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧዃ"), bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫዄ")]:
            _11l1111111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111lllll11_opy_(self, hook_type):
        def bstack11l11111l1_opy_(arg=None):
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪዅ"))
            result = None
            exception = None
            try:
                self.bstack111lllllll_opy_(hook_type, self._11l111111l_opy_[hook_type], (arg,))
                result = Result(result=bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ዆"))
            except Exception as e:
                result = Result(result=bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ዇"), exception=e)
                self.handler(hook_type, bstack1lll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬወ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ዉ"), result)
        def bstack11l11111ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨዊ"))
            result = None
            exception = None
            try:
                self.bstack111lllllll_opy_(hook_type, self._11l111111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዋ"))
            except Exception as e:
                result = Result(result=bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዌ"), exception=e)
                self.handler(hook_type, bstack1lll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪው"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዎ"), result)
        if hook_type in [bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬዏ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩዐ")]:
            return bstack11l11111ll_opy_
        return bstack11l11111l1_opy_
    def bstack111lll1ll1_opy_(self, bstack111lllll1l_opy_):
        def bstack111lll1lll_opy_(this, *args, **kwargs):
            self.bstack111llll11l_opy_(this, bstack111lllll1l_opy_)
            self._11l1111l11_opy_[bstack111lllll1l_opy_](this, *args, **kwargs)
        return bstack111lll1lll_opy_