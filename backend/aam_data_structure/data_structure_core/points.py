# 点
import uuid
from dataclasses import dataclass, field
from uuid import uuid1
from typing import *
from typing import List, AnyStr,Tuple,Dict
from networkx import Graph
import math
import rhinoinside

rhinoinside.load()
import System
import Rhino

@dataclass(order=True)
class BasePoint:
    """
    点的基类
    """
    pt: Rhino.Geometry.Point = field(default=None)
    layer: AnyStr = field(default="")  # 图层名


# 零件的安装点
@dataclass(order=True)
class InstallPoint(BasePoint):
    def __int__(self):
        pass

    def duplicate(self):
        cur = InstallPoint()
        cur.pt = self.pt.Duplicate() if isinstance(self.pt, Rhino.Geometry.Point) else None
        cur.layer = self.layer
        return cur

# 零件的旋转锚点
@dataclass(order=True)
class RotatePoint(BasePoint):
    def __int__(self):
        pass

    def duplicate(self):
        cur = RotatePoint()
        cur.pt = self.pt.Duplicate() if isinstance(self.pt, Rhino.Geometry.Point) else None
        cur.layer = self.layer
        return cur