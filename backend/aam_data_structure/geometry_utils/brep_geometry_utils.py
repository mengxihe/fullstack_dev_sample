"""
相当于rhinocommon的二次封装
brep库
"""
from typing import List
# Rhino inside部分
import rhinoinside

from aam_data_structure.geometry_utils.curve_geometry_utils import join_curves, \
    get_curve_curve_intersections, create_polyline, create_curve_list
from aam_data_structure.geometry_utils.point_geometry_utils import create_pt3d_origin, \
    create_pt3d, create_pt3d_list

rhinoinside.load()
import System
import Rhino


def get_brep_complete_boundary(brep, join_tolerance):
    """
    返回该brep合并之后的外边线
    :param brep:
    :param join_tolerance:
    :return:
    """
    return join_curves(inputCurves=brep.Curves3D, joinTolerance=join_tolerance)

def test_brep_boundary_intersects_curve(brep, test_curve):
    """
    测试该brep的边线是否与测试的curve相交
    :param brep:
    :param test_curve:
    :return:
    """
    res = get_curve_curve_intersections(get_brep_complete_boundary(brep=brep, join_tolerance=1.0), test_curve)
    return res.Count

def create_brep_from_mesh(mesh:Rhino.Geometry.Mesh, trimmedTriangles:System.Boolean)->Rhino.Geometry.Brep:
    """
    从mesh构建一个brep
    :param mesh:
    :param trimmedTriangles:
    :return:
    """
    brep = Rhino.Geometry.Brep()
    return brep.CreateFromMesh(mesh=mesh, trimmedTriangles=trimmedTriangles)

def extrude_brep(brepface: Rhino.Geometry.BrepFace, height: float, cap:System.Boolean)->Rhino.Geometry.Brep:
    """
    按对应高度挤出brepface
    :param brep:
    :param height:
    :return:
    """
    points3d = []
    # 构造挤出高度方向polyline
    points3d.extend([create_pt3d_origin(), create_pt3d(0., 0., float(height))])
    pathCurve = create_polyline(pline_pts=create_pt3d_list(points3d))
    return brepface.CreateExtrusion(pathCurve=pathCurve, cap=True)

def split_brep_by_curves(brep: Rhino.Geometry.Brep, cutting_curves:List):
    """
    用curve切割brep
    :param brep:
    :param cutting_curves:
    :return:
    """
    cutting_curves = create_curve_list(cutting_curves)
    return brep.Split(cutters=cutting_curves, intersectionTolerance=5.)


def create_brep_list(breps:List):
    """
    创建brep列表
    :param :
    :return:
    """
    brep_list = System.Collections.Generic.List[Rhino.Geometry.Brep]()
    for each in breps:
        brep_list.Add(each)
    return brep_list

def create_brep_from_loft_simple(curves:List[Rhino.Geometry.Curve], loft_type:Rhino.Geometry.LoftType, closed:bool, is_cap:bool):
    """
    简单放样一个brep
    :param curves:
    :param loft_type:
    :param closed:
    :param is_cap:
    :return:
    """
    curves_list = System.Collections.Generic.List[Rhino.Geometry.Curve]()
    for _ in curves:
        curves_list.Add(_)
    is_close = System.Boolean(1) if closed is True else System.Boolean(0)
    res_brep = Rhino.Geometry.Brep().CreateFromLoft(curves=curves_list, start=Rhino.Geometry.Point3d.Unset, end=Rhino.Geometry.Point3d.Unset,loftType=loft_type, closed=is_close)[0]
    if res_brep.IsValid:
        if is_cap:
            res_brep = res_brep.CapPlanarHoles(tolerance=System.Double(0.1))
        return res_brep
    else:
        print('放样生成Brep失败.....')
        return None

def create_brep_from_loft_by_2_pts(curves:List[Rhino.Geometry.Curve], start_pt:Rhino.Geometry.Point, end_pt:Rhino.Geometry.Point, loft_type:Rhino.Geometry.LoftType,closed:bool, is_cap:bool):
    """
    放样构建一个brep
    :param curves:
    :param start_pt:
    :param end_pt:
    :param loft_type:
    :param closed:
    :return:
    """
    curves_list = System.Collections.Generic.List[Rhino.Geometry.Curve]()
    for _ in curves:
        curves_list.Add(_)
    is_close = System.Boolean(1) if closed is True else System.Boolean(0)
    res_brep = Rhino.Geometry.Brep().CreateFromLoft(curves=curves_list, start=start_pt.Location, end=end_pt.Location, loftType=loft_type, closed=is_close)[0]
    if res_brep.IsValid:
        if is_cap:
            res_brep = res_brep.CapPlanarHoles(tolerance=System.Double(0.1))
        return res_brep
    else:
        print('放样生成Brep失败.....')
        return None


