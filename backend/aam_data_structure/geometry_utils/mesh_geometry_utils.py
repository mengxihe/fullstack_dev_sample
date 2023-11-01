"""
mesh的几何操作封装
"""
import os
from typing import Dict, List

# Rhino inside部分
import rhinoinside

from nev_spoiler_generative_algorithm.aam_data_structure.common_utils.common_ops import flatten_list
from nev_spoiler_generative_algorithm.aam_data_structure.geometry_utils.geometry_analysis_utils import get_mesh_area

rhinoinside.load()
import System
import Rhino

def get_all_edges(mesh:Rhino.Geometry.Mesh)->List[Rhino.Geometry.Curve]:
    """
    求当前mesh中所有的edge
    :return:
    """
    a = mesh.TopologyEdges
    res = [a.EdgeLine(topologyEdgeIndex=idx).ToNurbsCurve() for idx in range(a.Count)]
    return res

def get_sub_mesh_index_index(mesh:Rhino.Geometry.Mesh)->List[int]:
    """
    返回该mesh下所有的faces的index list
    :param mesh:
    :return:
    """
    face_list = mesh.Faces
    index_list = [list(face_list.GetEnumerator()).index(m) for m in face_list]
    return index_list

def get_meshface_by_index(mesh: Rhino.Geometry.Mesh, index: int)-> Rhino.Geometry.MeshFace:
    """
    根据index获取mesh中对应的meshface
    :param mesh:
    :param index:
    :return:
    """
    return mesh.Faces.GetFace(index=index)

def get_mesh_by_index(mesh: Rhino.Geometry.Mesh, index)-> Rhino.Geometry.Mesh:
    """
    根据index获取mesh中对应的mesh，原平面会被切割
    :param mesh:
    :param index:
    :return:
    """
    return mesh.Faces.ExtractFaces(faceIndices=index)

def create_mesh_index_list(index_list:list)->System.Collections.Generic.IEnumerable[System.Int32]:
    """
    创建一组meshface序号列表
    :param index_list:
    :return:
    """
    index = System.Collections.Generic.List[System.Int32]()
    for i in index_list:
        index.Add(i)
    return index

def get_adjacent_faces_index(index: int, mesh: Rhino.Geometry.Mesh):
    """
    取mesh中某个面的相邻面序号
    :param index:
    :param mesh:
    :return:
    """
    return mesh.Faces.AdjacentFaces(faceIndex=index)

def get_mesh_face_center_by_index(index: int, mesh:Rhino.Geometry.Mesh):
    """
    获取mesh中某个面的中心点
    :param index:
    :param mesh:
    :return:
    """
    return mesh.Faces.GetFaceCenter(faceIndex=index)

def get_mesh_face_area(index:int,mesh:Rhino.Geometry.Mesh)->float:
    """
    求mesh中某个face的面积
    :param index:
    :param mesh:
    :return:
    """
    face = mesh.Duplicate().Faces.ExtractFaces(faceIndices=index)
    return float(get_mesh_area(mesh=face))

# quad mesh 神奇操作类
def get_quad_index_by_type(quadmesh: Rhino.Geometry.Mesh, ops: int):
    """
    获取quad各种类型的编号：所有类型（0），三角面（1），悬置格（2），角格（3）、边格（4）、内部（5）、外沿（6）其中不同类型的四边面编号
    :param quadmesh:
    :return:
    """
    tri_quad_index = []
    dangling_quad_index = []
    corner_quad_index = []
    side_quad_index = []
    interior_quad_index = []
    exterior_quad_index = []
    # 筛选
    for index in range(quadmesh.Faces.Count):
        cur_face = get_meshface_by_index(mesh=quadmesh, index=index)
        adjacent_faces_count = len(quadmesh.Faces.AdjacentFaces(faceIndex=index))
        # 如果当前面为四边面
        if cur_face.IsQuad:
            if adjacent_faces_count ==1 :
                dangling_quad_index.append(index)
            elif adjacent_faces_count == 2:
                corner_quad_index.append(index)
                exterior_quad_index.append(index)
            elif adjacent_faces_count == 3:
                side_quad_index.append(index)
                exterior_quad_index.append(index)
            elif adjacent_faces_count == 4:
                interior_quad_index.append(index)
        # 如果当前面为三角面
        else:
            tri_quad_index.append(index)
            exterior_quad_index.append(index)


    if ops == 0:
        # 返回所有类型的序号
        return tri_quad_index, dangling_quad_index, corner_quad_index, side_quad_index, interior_quad_index, exterior_quad_index
    elif ops == 1:
        return tri_quad_index
    elif ops == 2:
        return dangling_quad_index
    elif ops == 3:
        return corner_quad_index
    elif ops == 4:
        return side_quad_index
    elif ops == 5:
        return interior_quad_index
    elif ops == 6:
        return exterior_quad_index

def filter_adjacent_face_by_target_index_list(input_face_index:int, filter_list:List[int], mesh:Rhino.Geometry.Mesh)->List[int]:
    """
    找到与输入面连接，但一定在过滤list中的face的index
    :param input_face_index:
    :param filter_list:
    :param mesh:
    :return:
    """
    all_adjacent_faces_index=mesh.Faces.AdjacentFaces(faceIndex=input_face_index)
    res = list(filter(lambda each:each in filter_list, all_adjacent_faces_index))
    return res

def merge_brep_into_mesh(brep_list:List[Rhino.Geometry.Brep])->Rhino.Geometry.Mesh:
    """
    把一个list中
    :param brep_list:
    :return:
    """
    new_mesh = Rhino.Geometry.Mesh()
    if len(brep_list) > 0:
        for each in brep_list:
            cur_mesh = Rhino.Geometry.Mesh()
            mesh_params = Rhino.Geometry.MeshingParameters()
            res_mesh_list = cur_mesh.CreateFromBrep(brep=each, meshingParameters=mesh_params)
            for m in res_mesh_list:
                new_mesh.Append(m)
    new_mesh.MergeAllCoplanarFaces(System.Double(.1))
    return new_mesh

def merge_listMesh_into_mesh(mesh_list:List[Rhino.Geometry.Mesh])->Rhino.Geometry.Mesh:
    """
    将很多个mesh合并成一个mesh
    :param mesh_list:
    :return:
    """
    mesh_list = flatten_list(input_list=mesh_list)
    new_mesh = Rhino.Geometry.Mesh()
    for m in mesh_list:
        new_mesh.Append(m)
    new_mesh.MergeAllCoplanarFaces(System.Double(.1))
    return new_mesh