"""
相当于rhinocommon的二次封装
point库
"""

# Rhino inside部分
import rhinoinside

rhinoinside.load()
import System
import Rhino

# 创建Point类
# Point3d
def create_pt3d(x: float, y: float, z: float):
    """
    rhino中的以三个坐标创建点
    :param x, y:
    :return:
    """
    return Rhino.Geometry.Point3d(x, y, z)

def create_pt3d_origin():
    """
    rhino中的创建原点
    :param
    :return:
    """
    return Rhino.Geometry.Point3d(0., 0., 0.)

def create_pt3d_list(points3d):
    """
    rhino中创建Point3d列表
    :param points3d:
    :return:
    """
    pt3d_list = System.Collections.Generic.List[Rhino.Geometry.Point3d]()
    for each in points3d:
        pt3d_list.Add(each)
    return pt3d_list

def convert_pt3f_to_pt(point3f):
    """
    将Point3f转换为Point
    :param point3d:
    :return:
    """
    return Rhino.Geometry.Point(Rhino.Geometry.Point3d(point3f))

# Point
def create_pt(x: float, y: float, z: float):
    """
    rhino中的以三个坐标创建点
    :param x, y:
    :return:
    """
    return Rhino.Geometry.Point(Rhino.Geometry.Point3d(x, y, z))