import os
from typing import List, Tuple, Union
import rhinoinside

from aam_data_structure.data_structure_core.base_element import PartElement
from aam_data_structure.data_structure_core.points import InstallPoint, RotatePoint
from aam_data_structure.data_structure_core.base_element import SectionElement

rhinoinside.load()
import System
import Rhino

def flatten_list(input_list:List)->List:
    """
    递归拍平list
    :param input_list:
    :return:
    """
    output_list = []
    for _ in input_list:
        if isinstance(_, list):
            output_list+=flatten_list(input_list=_)
        else:
            output_list.append(_)
    return output_list

def make_list_right(input_list:List)->List:
    """
    检查list是否有None或空
    :param input_list:
    :return:
    """
    input_list = list(filter(lambda each:each is not None, input_list))
    return input_list

def export_all_data_into_list(input_list:List)->List:
    """
    将一堆数据结构的东西放进去，自动变成一堆rhino geometry的list
    主要是用于快速输出结果
    :param input_list:
    :return:
    """
    res = []
    for each in input_list:
        if isinstance(each, PartElement) or isinstance(each, SectionElement):
            res.extend(each.export_all_geometry())
        if isinstance(each,InstallPoint) or isinstance(each, RotatePoint):
            res.append(each.pt)
        if isinstance(each, Rhino.Geometry.GeometryBase):
            res.append(each)
        else:
            pass

    return res

if __name__ == "__main__":
    a = [[1,2,3,[12,56],[5,6,8]], [123], [234, [234, [56]]]]
    a = flatten_list(input_list=a)
    print(a)