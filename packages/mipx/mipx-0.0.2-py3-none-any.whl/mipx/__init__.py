# -*- coding: utf-8 -*-
# @Time    : 2023/3/31 22:18
# @Author  : luyi
from .constants import Vtype, ObjType, OptimizationStatus, CmpType
# from .cpsolver import CpModel  # 暂不支持
from .lineExpr import LineExpr
from .solver import Model
from .tupledict import tupledict, multidict
from .tuplelist import tuplelist
from .utilx import name_str
from .variable import Var

P1, P2, P3, P4, P5, P6, P7, P8, P9 = 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000
