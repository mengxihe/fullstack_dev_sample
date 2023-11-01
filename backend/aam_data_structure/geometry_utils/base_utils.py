# Rhino inside部分
import rhinoinside
rhinoinside.load()
import System
import Rhino

def create_enumerable_list():
    """
    创建c#可以读取的list
    :return:
    """
    return System.Collections.Generic.List[Rhino.Geometry.GeometryBase]()