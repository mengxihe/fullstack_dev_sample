"""
相当于rhinocommon的二次封装
用于测算面积、求取质心等操作
"""

# Rhino inside部分
from typing import List

import rhinoinside


rhinoinside.load()
import System
import Rhino

# 距离类
def get_two_point_distance(pt1:Rhino.Geometry.Point3d, pt2:Rhino.Geometry.Point3d)->float:
    """
    计算点的距离
    :param pt1:
    :param pt2:
    :return:
    """
    distance = pt1.DistanceTo(other=pt2)
    return distance

def get_point_curve_shortest_distance(curve:Rhino.Geometry.NurbsCurve, pt:Rhino.Geometry.Point3d)->float:
    """
    计算点与线之间的最短距离
    :param curve:
    :param pt:
    :return:
    """
    t = System.Double(.0)
    _, t=curve.ClosestPoint(testPoint=pt, t=t)
    curve_pt = Rhino.Geometry.Point3d(curve.PointAt(t=t))
    return get_two_point_distance(pt1=pt, pt2=curve_pt)


def get_two_closed_curve_closest_pts(thisCurve, otherCurve):
    """
    rhino求两条曲线的相互最近点
    :param thisCurve:
    :param otherCurve:
    :return:
    """
    succ, pt_on_thisCurve, pt_on_otherCurve = thisCurve.ClosestPoints(otherCurve=otherCurve,
                                                                      pointOnThisCurve=Rhino.Geometry.Point3d(),
                                                                      pointOnOtherCurve=Rhino.Geometry.Point3d())
    return pt_on_thisCurve, pt_on_otherCurve

def get_two_curve_distance(curve1, curve2)->float:
    """
    两个线之间的距离
    :param curve1:
    :param curve2:
    :return:
    """
    pt1, pt2 = get_two_closed_curve_closest_pts(thisCurve=curve1, otherCurve=curve2)
    distance = get_two_point_distance(pt1=pt1, pt2=pt2)
    return distance

def get_two_closed_curve_square_distance(thisCurve, otherCurve):
    """
    rhino求两根闭合曲线之间的最小平方距离
    :param thisCurve:
    :param otherCurve:
    :return:
    """
    # 求两条曲线的最近点
    pt_on_thisCurve, pt_on_otherCurve = get_two_closed_curve_closest_pts(thisCurve, otherCurve)
    return pt_on_thisCurve.DistanceToSquared(other=pt_on_otherCurve)

def get_two_point3d_square_distance(pointA:Rhino.Geometry.Point3d, pointB:Rhino.Geometry.Point3d)->float:
    """
    rhino求两个point3d之间的平方距离
    :param pointA:
    :param pointB:
    :return:
    """
    return pointA.DistanceToSquared(other=pointB)

# 面积类
def get_closed_curve_area(closedPlanarCurve):
    """
    rhino求封闭平面曲线面积
    :param closedPlanarCurve:
    :return:
    """
    if not closedPlanarCurve.IsClosed:
        closedPlanarCurve.MakeClosed(tolerance=System.Double(0.1))
    area_mass = Rhino.Geometry.AreaMassProperties.Compute(closedPlanarCurve=closedPlanarCurve)
    return area_mass.Area



def get_brep_area(brep):
    """
    rhino求brep面积
    :param brep:
    :return:
    """
    return Rhino.Geometry.AreaMassProperties.Compute(brep=brep).Area

def get_mesh_area(mesh):
    """
    rhino求mesh面积
    :param mesh:
    :return:
    """
    return Rhino.Geometry.AreaMassProperties.Compute(mesh=mesh).Area

# 质心类
def get_closed_curve_centroid(closedPlanarCurve):
    """
    rhino求封闭平面曲线的质心
    :param closedPlanarCurve:
    :return:
    """
    return Rhino.Geometry.AreaMassProperties.Compute(closedPlanarCurve=closedPlanarCurve).Centroid

def get_brep_centroid(brep):
    """
    rhino求brep的质心
    :param brep:
    :return:
    """
    return Rhino.Geometry.AreaMassProperties.Compute(brep=brep).Centroid

def get_mesh_centroid(mesh):
    """
    rhino求mesh的质心
    :param mesh:
    :return:
    """
    return Rhino.Geometry.AreaMassProperties.Compute(mesh=mesh).Centroid

def get_curve_end_pt(curve:Rhino.Geometry.Curve, ops:int)->List[Rhino.Geometry.Point3d]:
    """
    ops=0返回起点
    ops=1返回终点
    ops=2返回两个点
    :param curve:
    :param ops:
    :return:
    """
    start_pt = curve.PointAtStart
    end_pt = curve.PointAtEnd
    if ops==0:
        return [start_pt]
    elif ops==1:
        return [end_pt]
    elif ops==2:
        return [start_pt, end_pt]