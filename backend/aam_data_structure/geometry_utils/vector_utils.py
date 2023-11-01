"""
相当于rhinocommon的二次封装
vector库
"""

# Rhino inside部分
import rhinoinside

rhinoinside.load()
import System
import Rhino

# 创建Vector类
def create_vector_by_xyz(x, y, z):
    """
    rhino中通过xyz坐标创建一个向量
    :return:
    """
    return Rhino.Geometry.Vector3d(x=x, y=y, z=z)

def create_vector_by_point(Point):
    """
    根据Point3d创建向量
    :param Point3d:
    :return:
    """
    return Rhino.Geometry.Vector3d(Point.Location)

# Vector运算类
def add_2_vector(vector1: Rhino.Geometry.Vector3d, vector2: Rhino.Geometry.Vector3d):
    """
    rhino中的两个向量相加
    :param vector1, vector2:
    :return:
    """
    return Rhino.Geometry.Vector3d.Add(vector1, vector2)

def subtract_2_vector(vector1: Rhino.Geometry.Vector3d, vector2: Rhino.Geometry.Vector3d):
    """
    rhino中的两个向量相减
    :param vector1, vector2:
    :return:
    """
    return Rhino.Geometry.Vector3d.Subtract(vector1, vector2)


def multiply_vector(vector: Rhino.Geometry.Vector3d, t: float):
    """
    rhino中的向量乘法
    :param vector, t:
    :return:
    """
    return Rhino.Geometry.Vector3d.Multiply(vector, t)

def divide_vector(vector: Rhino.Geometry.Vector3d, t:float):
    """
    rhino中的向量除法
    :param vector, t:
    :return:
    """
    return Rhino.Geometry.Vector3d.Divide(vector, t)

def angle_between_2_vector(vector1: Rhino.Geometry.Vector3d, vector2: Rhino.Geometry.Vector3d):
    """
    rhino中计算两个向量的夹角
    :param vector1:
    :param vector2:
    :return:
    """
    return Rhino.Geometry.Vector3d.VectorAngle(vector1, vector2)