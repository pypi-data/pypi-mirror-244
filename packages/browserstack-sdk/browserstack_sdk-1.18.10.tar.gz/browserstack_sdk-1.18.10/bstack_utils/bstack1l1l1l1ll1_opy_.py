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
from uuid import uuid4
from bstack_utils.helper import bstack11l111ll1_opy_, bstack11l11lll1l_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack111ll11111_opy_
class bstack1l11lllll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1l1ll1ll_opy_=None, framework=None, tags=[], scope=[], bstack1111lll1l1_opy_=None, bstack1111llll1l_opy_=True, bstack1111lll1ll_opy_=None, bstack11lllllll_opy_=None, result=None, duration=None, bstack1l1l111l1l_opy_=None, meta={}):
        self.bstack1l1l111l1l_opy_ = bstack1l1l111l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111llll1l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1l1ll1ll_opy_ = bstack1l1l1ll1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self.bstack11lllllll_opy_ = bstack11lllllll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l1l1ll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111ll1l1l_opy_(self):
        bstack111l1111ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᎣ"): bstack111l1111ll_opy_,
            bstack1lll11l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᎤ"): bstack111l1111ll_opy_,
            bstack1lll11l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᎥ"): bstack111l1111ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lll11l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᎦ") + key)
            setattr(self, key, val)
    def bstack1111ll1lll_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᎧ"): self.name,
            bstack1lll11l_opy_ (u"࠭ࡢࡰࡦࡼࠫᎨ"): {
                bstack1lll11l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᎩ"): bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᎪ"),
                bstack1lll11l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᎫ"): self.code
            },
            bstack1lll11l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᎬ"): self.scope,
            bstack1lll11l_opy_ (u"ࠫࡹࡧࡧࡴࠩᎭ"): self.tags,
            bstack1lll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᎮ"): self.framework,
            bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᎯ"): self.bstack1l1l1ll1ll_opy_
        }
    def bstack111l111l11_opy_(self):
        return {
         bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᎰ"): self.meta
        }
    def bstack1111ll1ll1_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᎱ"): {
                bstack1lll11l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭Ꮂ"): self.bstack1111lll1l1_opy_
            }
        }
    def bstack1111lll11l_opy_(self, bstack111l111ll1_opy_, details):
        step = next(filter(lambda st: st[bstack1lll11l_opy_ (u"ࠪ࡭ࡩ࠭Ꮃ")] == bstack111l111ll1_opy_, self.meta[bstack1lll11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᎴ")]), None)
        step.update(details)
    def bstack111l1111l1_opy_(self, bstack111l111ll1_opy_):
        step = next(filter(lambda st: st[bstack1lll11l_opy_ (u"ࠬ࡯ࡤࠨᎵ")] == bstack111l111ll1_opy_, self.meta[bstack1lll11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᎶ")]), None)
        step.update({
            bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᎷ"): bstack11l111ll1_opy_()
        })
    def bstack1l1l1111ll_opy_(self, bstack111l111ll1_opy_, result, duration=None):
        bstack1111lll1ll_opy_ = bstack11l111ll1_opy_()
        if self.meta.get(bstack1lll11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᎸ")):
            step = next(filter(lambda st: st[bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬᎹ")] == bstack111l111ll1_opy_, self.meta[bstack1lll11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᎺ")]), None)
            step.update({
                bstack1lll11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᎻ"): bstack1111lll1ll_opy_,
                bstack1lll11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᎼ"): duration if duration else bstack11l11lll1l_opy_(step[bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᎽ")], bstack1111lll1ll_opy_),
                bstack1lll11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᎾ"): result.result,
                bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᎿ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111l111l1l_opy_):
        if self.meta.get(bstack1lll11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏀ")):
            self.meta[bstack1lll11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏁ")].append(bstack111l111l1l_opy_)
        else:
            self.meta[bstack1lll11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᏂ")] = [ bstack111l111l1l_opy_ ]
    def bstack1111llllll_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᏃ"): self.bstack1l1l1ll111_opy_(),
            **self.bstack1111ll1lll_opy_(),
            **self.bstack1111ll1l1l_opy_(),
            **self.bstack111l111l11_opy_()
        }
    def bstack1111lllll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᏄ"): self.bstack1111lll1ll_opy_,
            bstack1lll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᏅ"): self.duration,
            bstack1lll11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᏆ"): self.result.result
        }
        if data[bstack1lll11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᏇ")] == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᏈ"):
            data[bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᏉ")] = self.result.bstack1l111l1l11_opy_()
            data[bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭Ꮚ")] = [{bstack1lll11l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᏋ"): self.result.bstack11l1ll11l1_opy_()}]
        return data
    def bstack1111ll1l11_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᏌ"): self.bstack1l1l1ll111_opy_(),
            **self.bstack1111ll1lll_opy_(),
            **self.bstack1111ll1l1l_opy_(),
            **self.bstack1111lllll1_opy_(),
            **self.bstack111l111l11_opy_()
        }
    def bstack1l11ll1ll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lll11l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᏍ") in event:
            return self.bstack1111llllll_opy_()
        elif bstack1lll11l_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᏎ") in event:
            return self.bstack1111ll1l11_opy_()
    def bstack1l1l11l111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1111lll1ll_opy_ = time if time else bstack11l111ll1_opy_()
        self.duration = duration if duration else bstack11l11lll1l_opy_(self.bstack1l1l1ll1ll_opy_, self.bstack1111lll1ll_opy_)
        if result:
            self.result = result
class bstack1l11l1l111_opy_(bstack1l11lllll1_opy_):
    def __init__(self, hooks=[], bstack1l11l11l1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l11l1l_opy_ = bstack1l11l11l1l_opy_
        super().__init__(*args, **kwargs, bstack11lllllll_opy_=bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࠨᏏ"))
    @classmethod
    def bstack111l111111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧᏐ"): id(step),
                bstack1lll11l_opy_ (u"ࠬࡺࡥࡹࡶࠪᏑ"): step.name,
                bstack1lll11l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᏒ"): step.keyword,
            })
        return bstack1l11l1l111_opy_(
            **kwargs,
            meta={
                bstack1lll11l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᏓ"): {
                    bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꮤ"): feature.name,
                    bstack1lll11l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᏕ"): feature.filename,
                    bstack1lll11l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᏖ"): feature.description
                },
                bstack1lll11l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭Ꮧ"): {
                    bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏘ"): scenario.name
                },
                bstack1lll11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏙ"): steps,
                bstack1lll11l_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᏚ"): bstack111ll11111_opy_(test)
            }
        )
    def bstack1111llll11_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᏛ"): self.hooks
        }
    def bstack111l11111l_opy_(self):
        if self.bstack1l11l11l1l_opy_:
            return {
                bstack1lll11l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᏜ"): self.bstack1l11l11l1l_opy_
            }
        return {}
    def bstack1111ll1l11_opy_(self):
        return {
            **super().bstack1111ll1l11_opy_(),
            **self.bstack1111llll11_opy_()
        }
    def bstack1111llllll_opy_(self):
        return {
            **super().bstack1111llllll_opy_(),
            **self.bstack111l11111l_opy_()
        }
    def bstack1l1l11l111_opy_(self):
        return bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᏝ")
class bstack1l1l11llll_opy_(bstack1l11lllll1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack11lllllll_opy_=bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᏞ"))
    def bstack1l11l1ll11_opy_(self):
        return self.hook_type
    def bstack1111lll111_opy_(self):
        return {
            bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᏟ"): self.hook_type
        }
    def bstack1111ll1l11_opy_(self):
        return {
            **super().bstack1111ll1l11_opy_(),
            **self.bstack1111lll111_opy_()
        }
    def bstack1111llllll_opy_(self):
        return {
            **super().bstack1111llllll_opy_(),
            **self.bstack1111lll111_opy_()
        }
    def bstack1l1l11l111_opy_(self):
        return bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᏠ")