"""
相当于rhinocommon的二次封装
curve库
"""
from typing import List
# Rhino inside部分
import rhinoinside

from aam_data_structure.geometry_utils.point_geometry_utils import create_pt3d
from aam_data_structure.geometry_utils.surface_geometry_utils import \
    create_horizontal_plane

rhinoinside.load()
import System
import Rhino


# 创建Curve类
def create_line(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    """
    rhino中的以两点坐标创建直线段
    :param x1, y1, z1, x2, y2, z2:
    :return:
    """
    pt_from = create_pt3d(x1, y1, z1)
    pt_to = create_pt3d(x2, y2, z2)
    return Rhino.Geometry.Line(pt_from, pt_to)


def create_line_by_two_pt3d(pt_from: Rhino.Geometry.Point3d, pt_to: Rhino.Geometry.Point3d) -> Rhino.Geometry.Line:
    """
    rhino中的以两个point3d坐标创建直线段
    :param pt1:
    :param pt2:
    :return:
    """
    return Rhino.Geometry.Line(pt_from, pt_to)


def create_line_by_vector(start: Rhino.Geometry.Point3d, direction: Rhino.Geometry.Vector3d):
    """
    rhino中的以起始点和给定方形创建直线段
    :param start:
    :param direction:
    :return:
    """
    return Rhino.Geometry.Line(start=start, span=direction)


def create_polyline_curve(pline_pts):
    """
    rhino中的以点创建多段线polyline
    :param pline_pts:
    :return:
    """
    pts_list = System.Collections.Generic.List[Rhino.Geometry.Point3d]()
    for each in pline_pts:
        pts_list.Add(each)
    return Rhino.Geometry.Polyline(pts_list).ToPolylineCurve()


def create_polyline_curve_list(curves):
    """
    rhino中创建polyline_curve曲线列表
    :param :
    :return:
    """
    crv_list = System.Collections.Generic.List[Rhino.Geometry.PolylineCurve]()
    for each in curves:
        crv_list.Add(each)
    return crv_list


def create_polyline(pline_pts):
    """
    rhino中的以点创建多段线polyline
    :param pline_pts:
    :return:
    """
    pts_list = System.Collections.Generic.List[Rhino.Geometry.Point3d]()
    for each in pline_pts:
        pts_list.Add(each)
    return Rhino.Geometry.Polyline(pts_list).ToPolylineCurve()


def create_curve_list(curves):
    """
    rhino中创建Curve曲线列表
    :param :
    :return:
    """
    crv_list = System.Collections.Generic.List[Rhino.Geometry.Curve]()
    for each in curves:
        crv_list.Add(each)
    return crv_list


# 操作Curve类
def get_curve_curve_intersections(curveA, curveB):
    """
    rhino中求两条曲线交点
    :param curveA，curveB:
    :return:
    """
    intersections = Rhino.Geometry.Intersect.Intersection.CurveCurve(curveA=curveA, curveB=curveB, tolerance=0.,
                                                                     overlapTolerance=1.)
    return intersections


def join_curves(inputCurves, joinTolerance: float = 1.0):
    """
    rhino中合并多条曲线
    :param inputCurves:
    :return:
    """
    joined_crv = Rhino.Geometry.Curve.JoinCurves(inputCurves=inputCurves, joinTolerance=joinTolerance)
    # 改了这里
    if not joined_crv[0].IsClosed:
        joined_crv[0].MakeClosed(tolerance=System.Double(0.0))
    return joined_crv[0]


def generate_floor_curve(curve: Rhino.Geometry.Curve, floor_height: float, geometry_height: float) -> List[
    Rhino.Geometry.Curve]:
    """
    根据高度，每层偏移的高度，以及总高度自动生成楼层线
    :param curve:
    :param floor_height:
    :param geometry_height:
    :return:
    """
    res = [curve]
    floor_count = int(geometry_height / floor_height)
    vector = Rhino.Geometry.Vector3d(.0, .0, float(floor_height))
    for i in range(floor_count):
        new = res[-1].Duplicate()
        new.Translate(translationVector=vector)
        res.append(new)
    res.pop()
    return res


def specific_offset_curve_by_distance(curve: Rhino.Geometry, distance: float, ops: int) -> Rhino.Geometry.Curve:
    """
    偏移曲线一定距离，可返回向内（0）， 向外（1），向内向外（2）的偏移曲线
    :param curve:
    :param distance:
    :return:
    """
    # 建立基础平面
    plane = create_horizontal_plane()
    # 偏移
    offset_curve_1 = join_curves(
        inputCurves=curve.Offset(plane=plane, distance=System.Double(float(distance)), tolerance=0.01, cornerStyle=1),
        joinTolerance=1.0)
    offset_curve_2 = join_curves(
        inputCurves=curve.Offset(plane=plane, distance=System.Double((-1.0) * distance), tolerance=0.01, cornerStyle=1),
        joinTolerance=1.0)

    if ops == 0:
        return list(filter(lambda x: x.GetLength() < curve.GetLength(), [offset_curve_1, offset_curve_2]))[0]
    elif ops == 1:
        return list(filter(lambda x: x.GetLength() > curve.GetLength(), [offset_curve_1, offset_curve_2]))[0]
    elif ops == 2:
        return [offset_curve_1, offset_curve_2]


def judge_point_containment(point: Rhino.Geometry.Point3d, curve: Rhino.Geometry.Curve) -> str:
    """
    判断一个点和曲线的包含关系
    :param point:
    :return:
    """
    containment = curve.Contains(testPoint=point)
    if containment == 0:
        return "unset"
    elif containment == 1:
        return "in"
    elif containment == 2:
        return "out"
    elif containment == 3:
        return "on"
