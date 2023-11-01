"""
相当于rhinocommon的二次封装
"""
import os
from typing import Dict, List

# Rhino inside部分
import rhinoinside


rhinoinside.load()
import System
import Rhino

# 创建surface类
def create_horizontal_plane()->Rhino.Geometry.Plane:
    """
    创建一个z=0的xy基准水平面
    :return:
    """
    return Rhino.Geometry.Plane(0., 0., 1., 0.)

def create_horizontal_plane_by_point(pt:Rhino.Geometry.Point3d):
    """
    基于一个点在其上创建一个xy基准面
    :return:
    """
    vector = Rhino.Geometry.Vector3d(Rhino.Geometry.Point3d(x=.0, y=.0, z=.1))
    return Rhino.Geometry.Plane(origin=pt, normal=vector)

def create_plane(a, b, c):
    # 建立基础平面
    center_point = Rhino.Geometry.Point3d(a, b, 0.0)
    zaxis = Rhino.Geometry.Vector3d()
    zaxis.Z = 1.0
    plane = Rhino.Geometry.Plane(origin=center_point, normal=zaxis)
    plane.ZAxis = zaxis
    return plane

def create_planner_surface_by_lines(lines):
    """
    rhino中的以平面曲线建立曲面，自动挖空中心
    :param lines:
    :return:
    """
    geometry_list = System.Collections.Generic.List[Rhino.Geometry.Curve]()
    for each in lines:
        geometry_list.Add(each)
    surface = Rhino.Geometry.Brep().CreatePlanarBreps(geometry_list)
    mesh = [Rhino.Geometry.Mesh().CreateFromBrep(brep=g)[0] for g in surface]
    return mesh

def create_brep_by_boundary(boundary):
    """
    rhino中的以封闭平面曲线创建brep
    :param boundary:
    :return:
    """
    return Rhino.Geometry.Brep().CreatePlanarBreps(inputLoop=boundary)[0]


def create_mesh_by_boudnary(boundary):
    """
    rhino中的以封闭平面曲线创建mesh
    :param boundary:
    :return:
    """
    mesh = Rhino.Geometry.Mesh().CreateFromPlanarBoundary(boundary=boundary, parameters=Rhino.Geometry.MeshingParameters(), tolerance=0.)
    return mesh

def create_mesh_by_brep(brep):
    """
    rhino中的以brep创建mesh
    :param brep:
    :return:
    """
    return Rhino.Geometry.Mesh.CreateFromBrep(brep=brep)[0]

# 编辑surface类
def quad_remesh(mesh: Rhino.Geometry.Mesh, unit:float):
    """
    rhino中按特定尺度对mesh进行quadRemesh
    :param mesh, unit:
    :return:
    """
    # 设置QuadRemesh参数
    para = Rhino.Geometry.QuadRemeshParameters()
    para.AdaptiveQuadCount = True  # 自适应网格数
    para.DetectHardEdges = True  # When enabled the hard edges in models will be retained
    para.PreserveMeshArrayEdgesMode = 2  # 0=off, 1=On(Smart), 2=On(Strict) 使用曲面边缘
    area = Rhino.Geometry.AreaMassProperties.Compute(mesh).Area
    para.TargetQuadCount = int(area / unit**2)  # 目标mesh数量（当勾选自适应网格和设置自适应大小时该数值为参考值）
    print('当前mesh面积：',round(area, 2), para.TargetQuadCount)
    return mesh.QuadRemesh(parameters=para)


def quad_remesh_by_specific_area(mesh: Rhino.Geometry.Mesh, min_quad_area:float):
    """
    rhino中按特定尺度对mesh进行quadRemesh
    :param mesh, unit:
    :return:
    """
    # 设置QuadRemesh参数
    para = Rhino.Geometry.QuadRemeshParameters()
    para.AdaptiveQuadCount = False  # 自适应网格数
    para.DetectHardEdges = True  # When enabled the hard edges in models will be retained
    para.PreserveMeshArrayEdgesMode = 2  # 0=off, 1=On(Smart), 2=On(Strict) 使用曲面边缘
    area = Rhino.Geometry.AreaMassProperties.Compute(mesh).Area
    para.TargetQuadCount = area / min_quad_area  # 目标mesh数量（当勾选自适应网格和设置自适应大小时该数值为参考值）

    return mesh.QuadRemesh(parameters=para)