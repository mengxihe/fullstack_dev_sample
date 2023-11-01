# 针对数据结构的操作
from typing import List, AnyStr, Tuple, Dict, Union
import math

import rhinoinside

from aam_data_structure.data_structure_core.base_element import BaseElement, \
    PartElement, SectionElement
from aam_data_structure.data_structure_core.points import RotatePoint, InstallPoint

rhinoinside.load()
import System
import Rhino

def filter_duplicate_sub_element(eles:List[Union[BaseElement, PartElement, SectionElement]]):
    """
    提取所有的子元素，并将重复的子元素去掉
    :param ele:
    :return:
    """
    # 将所有重复的元素先排除
    valid_elements = []
    elements_id = []
    for _ in eles:
        if _.id not in elements_id:
            valid_elements.append(_)
            elements_id.append(_.id)
    return valid_elements

# 移动BaseElement类
def translate_element(ele:Union[BaseElement, PartElement, SectionElement], deltaX: float, deltaY: float, deltaZ: float, is_sync: bool):
    """
    整体移动当前的整个element
    :param ele:
    :return:
    """
    # 看是否需要将所有要联动的物件进行联动
    if is_sync:
        valid_elements = filter_duplicate_sub_element(eles=ele.extract_all_link_elements())
    else:
        valid_elements = [ele]

    # 做移动
    deltaX = float(deltaX)
    deltaY = float(deltaY)
    deltaZ = float(deltaZ)
    for each in valid_elements:
        # 找到所有要移动的物件
        if len(each.geometry) > 0:
            for g in each.geometry:
                g.Translate(x=deltaX, y=deltaY, z=deltaZ)
        if each.anchor_pt != None:
            each.anchor_pt.Translate(x=deltaX, y=deltaY, z=deltaZ)
        for _ in each.install_pts + each.rotate_pts:
            _.pt.Translate(x=deltaX, y=deltaY, z=deltaZ)


def translate_element_by_pt(ele:Union[BaseElement, SectionElement, PartElement], ref_pt: Rhino.Geometry.Point, target_pt: Rhino.Geometry.Point, is_sync: bool):
    """
    给定一个参考点以及一个目标点
    将整个模型按照参考点与目标点的translate矩阵进行位移
    :param target_pt:
    :return:
    """
    if isinstance(ref_pt, RotatePoint) or isinstance(ref_pt, InstallPoint):
        ref_pt = ref_pt.pt
    if isinstance(target_pt, RotatePoint) or isinstance(target_pt, InstallPoint):
        target_pt = target_pt.pt
    # 先计算移动距离
    deltaX = target_pt.Location.X - ref_pt.Location.X
    deltaY = target_pt.Location.Y - ref_pt.Location.Y
    deltaZ = target_pt.Location.Z - ref_pt.Location.Z

    # 将所有元素进行移动
    translate_element(ele=ele,deltaX=deltaX, deltaY=deltaY, deltaZ=deltaZ, is_sync=is_sync)

# 旋转BaseElement类
def rotate_element(ele:Union[BaseElement, PartElement, SectionElement], rotate_center: Rhino.Geometry.Point, radians: float, axis: Rhino.Geometry.Vector3d, is_sync: bool):
    """
    旋转
    :param rotate_center:
    :param angle:
    :param axis:
    :return:
    """
    # 看是否需要将所有要联动的物件进行联动
    if is_sync:
        valid_elements = filter_duplicate_sub_element(eles=ele.extract_all_link_elements())
    else:
        valid_elements = [ele]
    for each in valid_elements:
        for g in each.geometry:
            g.Rotate(angleRadians=System.Double(radians), rotationAxis=axis, rotationCenter=rotate_center.pt.Location)
        for _ in each.install_pts + each.rotate_pts:
            _.pt.Rotate(angleRadians=radians, rotationAxis=axis, rotationCenter=rotate_center.pt.Location)
        each.anchor_pt.Rotate(angleRadians=radians, rotationAxis=axis, rotationCenter=rotate_center.pt.Location)

def rotate_element_by_pt(ele:Union[BaseElement, PartElement, SectionElement], rotate_center: Rhino.Geometry.Point, angle: float, axis_plane: int, is_sync: bool):
    """
    根据旋转中心旋转整个data element
    :param rotate_center:
    :param angle:
    :param axis_plane:
    :return:
    """
    radians = angle * (math.pi / 180)
    if axis_plane == 0:  # 绕z轴旋转
        rotate_element(ele=ele,rotate_center=rotate_center, radians=radians, axis=Rhino.Geometry.Vector3d().ZAxis,
                            is_sync=is_sync)
    elif axis_plane == 1:  # 绕y轴旋转
        rotate_element(ele=ele,rotate_center=rotate_center, radians=radians, axis=Rhino.Geometry.Vector3d().YAxis,
                            is_sync=is_sync)
    elif axis_plane == 2:  # 绕x轴旋转
        rotate_element(ele=ele,rotate_center=rotate_center, radians=radians, axis=Rhino.Geometry.Vector3d().XAxis,
                            is_sync=is_sync)

# 缩放BaseElement类
def scale_element_by_pt(ele:Union[BaseElement, PartElement, SectionElement], anchor_pt: Rhino.Geometry.Point, factor: float, is_sync: bool):
    """
    指定某个点进行缩放
    :param anchor_pt:
    :param factor:
    :return:
    """
    matrix = Rhino.Geometry.Transform().Scale(anchor=anchor_pt.Location, scaleFactor=factor)
    # 看是否需要将所有要联动的物件进行联动
    if is_sync:
        valid_elements = filter_duplicate_sub_element(eles=ele.extract_all_link_elements())
    else:
        valid_elements = [ele]
    for each in valid_elements:
        for g in each.geometry:
            g.Transform(xform=matrix)
        for _ in each.install_pts + each.rotate_pts:
            _.pt.Transform(xform=matrix)