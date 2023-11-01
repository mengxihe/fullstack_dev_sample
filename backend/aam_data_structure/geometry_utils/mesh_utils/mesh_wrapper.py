
# Rhino inside部分
import rhinoinside

from data_structure.geometry_utils.curve_geometry_utils import judge_point_containment
from data_structure.geometry_utils.point_geometry_utils import convert_pt3f_to_pt

rhinoinside.load()
import System
import Rhino

from typing import List


class QuadMesh:
    def __init__(self, mesh):
        self.mesh = mesh
        # edges相关
        self.edges_class = self.mesh.TopologyEdges
        self.edges_count = self.mesh.TopologyEdges.Count
        self.edges = None

        # vertices相关
        self.vertices_class = self.mesh.TopologyVertices
        self.vertices_list = self.get_vertices_list()
        self.vertices_count = self.vertices_class.Count

        # faces相关
        self.faces_class = self.mesh.Faces

    # edges相关
    def get_edges_class(self) -> Rhino.Geometry.Collections.MeshTopologyEdgeList:
        """
        获取MeshTopologyEdgeList类对象
        """
        return self.edges_class

    def get_edges_count(self):
        """
        获取所有edges的数量
        :return:
        """
        return self.edges_count

    def get_edge_by_index(self, edge_index):
        """
        根据edge索引返回特定的edge
        :param edge_index:
        :return:
        """
        return self.edges_class.EdgeLine(topologyEdgeIndex=edge_index)

    def get_edges(self)->List[Rhino.Geometry.NurbsCurve]:
        """
        返回所有的edges
        :return:
        """
        self.edges = list(
            map(lambda index: self.get_edge_by_index(edge_index=index).ToNurbsCurve(), list(range(self.edges_count))))
        return self.edges

    def get_edge_index_by_vertex_index(self, index1: int, index2: int)->int:
        """
        根据edge顶点编号求当前edge编号
        :param index1:
        :param index2:
        :return:
        """
        return self.edges_class.GetEdgeIndex(topologyVertex1=index1, topologyVertex2=index2)

    # vertices相关
    def get_vertices_class(self):
        """
        获取MeshTopologyVertexList类对象，每一项元素为Rhino.Geometry.Point3f
        :return:
        """
        return self.vertices_class

    def get_vertices_list(self):
        """
        获取vertices列表，每一项元素为Rhino.Geometry.Point
        :return:
        """
        return list(map(lambda pt3f: convert_pt3f_to_pt(pt3f), list(self.vertices_class.GetEnumerator())))

    def get_vertices_count(self):
        """
        获取所有vertices的数量
        :return:
        """
        return self.vertices_count

    def get_vertices_index_by_face_index(self, face_index: int)->List[int]:
        """
        根据当前面编号获取该面上顶点的编号
        :param face_index:
        :return:
        """
        return list(self.faces_class.GetTopologicalVertices(faceIndex=face_index))

    def get_vertices_index_by_type(self, ops):
        """
        根据各个顶点相邻的面的数量将其分类，并选取特定种类的顶点，以顶点序号形式返回
        :return:
        """
        # STEP1 预处理
        # 遍历顶点序号，求每个顶点邻面数量
        connected_faces_count = [self.get_connected_faces_count_by_vertex_index(index) for index in list(range(self.vertices_count))]
        # 所有三分点
        all_triple_vertices_index = [index for index, count in enumerate(connected_faces_count) if count == 3]
        # mesh边界线
        outline = list(self.mesh.GetNakedEdges())[0]

        # STEP2 分类
        # 凸角点
        corner_vertices_index = [index for index, count in enumerate(connected_faces_count) if count == 1]
        # 边点（边界上除凸角点、凹角点外的点）
        side_vertices_index = [index for index, count in enumerate(connected_faces_count) if count == 2]
        # 三分点
        triple_vertices_index = list(filter(lambda i: judge_point_containment(curve=outline.ToNurbsCurve(), point=self.vertices_list[i].Location) == "in", all_triple_vertices_index))
        # 凹角点
        concave_vertices_index = list(filter(lambda x: x not in triple_vertices_index, all_triple_vertices_index))
        # 四分点
        grid_vertices_index = [index for index, count in enumerate(connected_faces_count) if count == 4]
        # 五分点
        penta_vertices_index = [index for index, count in enumerate(connected_faces_count) if count == 5]

        # STEP3 返回各类型顶点序号
        if ops == "corner":
            return corner_vertices_index
        elif ops == "side":
            return side_vertices_index
        elif ops == "concave":
            return concave_vertices_index
        elif ops == "triple":
            return triple_vertices_index
        elif ops == "grid":
            return grid_vertices_index
        elif ops == "penta":
            return penta_vertices_index
        # 外缘点 = 凸角点 + 边点 + 凹角点
        elif ops == "exterior":
            return corner_vertices_index + side_vertices_index + concave_vertices_index
        # 内部点 = 四分点 + 三分点 + 五分点
        elif ops == "interior":
            return grid_vertices_index + triple_vertices_index + penta_vertices_index
        # 所有点 = 外缘点 + 内部点
        elif ops == "all":
            return list(range(self.vertices_count))

    def get_vertices_by_type(self, ops)->List[Rhino.Geometry.Point]:
        """
        根据各个顶点相邻的面的数量将其分类，并选取特定种类的顶点，以Point列表返回
        :return:
        """
        selected_vertices_index = self.mesh.get_vertices_index_by_type(ops=ops)
        return [self.mesh.vertices_list[i] for i in selected_vertices_index]

    # faces相关
    def get_connected_faces_index_by_vertex_index(self, vertex_index):
        """
        根据顶点编号获取其邻面编号
        :param vertex_index:
        :return:
        """
        return self.vertices_class.ConnectedFaces(topologyVertexIndex=vertex_index)

    def get_connected_faces_count_by_vertex_index(self, vertex_index):
        """
        获取顶点编号获取其邻面数量
        :param vertex_index:
        :return:
        """
        return len(self.vertices_class.ConnectedFaces(topologyVertexIndex=vertex_index))

    def get_faces_index_by_edge_index(self, edge_index: int)->List[int]:
        """
        根据当前edge编号获取其邻面编号
        :param edge_index:
        :return:
        """
        return list(self.edges_class.GetConnectedFaces(topologyEdgeIndex=edge_index))

    def get_all_single_face(self)->List[Rhino.Geometry.Mesh]:
        """
        获取当前quadmesh中每一个单独的面
        :return:
        """
        face_list = []
        for i in range(self.mesh.Faces.Count):
            idx_list = System.Collections.Generic.List[System.Int32]()
            idx_list.Add(i)
            cur_mesh = self.mesh.Duplicate()
            face_list.append(cur_mesh.Faces.ExtractFaces(faceIndices=idx_list))
        return face_list

    def get_faces_by_index(self,idx_list:List[int], is_selected:bool=False)->Rhino.Geometry.Mesh:
        """
        根据index的列表获取face,
        is_selected是true时，返回选中的idx的face，false返回不在idx list中的face列表
        :return:
        """
        all_idx = [i for i in range(self.mesh.Faces.Count)]
        idxs = System.Collections.Generic.List[System.Int32]()
        for idx in all_idx:
            if is_selected:
                if idx in idx_list:
                    idxs.Add(idx)
            else:
                if idx not in idx_list:
                    idxs.Add(idx)
        cur_mesh = self.mesh.Duplicate()
        return cur_mesh.Faces.ExtractFaces(faceIndices=idxs)


if __name__ == '__main__':
    print('yes')
