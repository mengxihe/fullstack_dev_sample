import networkx as nx

# Rhino inside部分
import rhinoinside

from data_structure.geometry_utils.mesh_utils.mesh_wrapper import QuadMesh

rhinoinside.load()
import System
import Rhino


class MeshGraph:
    def __init__(self, mesh: QuadMesh):
        self.mesh = mesh

    def convert_mesh_vertex_to_Graph(self):
        """
        根根据当前地块mesh顶点构造G
        :return:
        """
        # 创建vertex的Graph
        G = nx.Graph()
        G.add_nodes_from(list(range(self.mesh.vertices_count)))

        connected_vertices_index = []
        for i in range(self.mesh.vertices_count):
            # 和当前顶点相连的顶点的索引
            connected_vertices_index.extend(
                list(map(lambda x: (i, x), self.mesh.vertices_class.ConnectedTopologyVertices(topologyVertexIndex=System.Int32(i)))))
        G.add_edges_from(connected_vertices_index)
        return G

    def convert_mesh_centeroid_to_Graph(self):
        """
        根据quadmesh中的mesh中心点构造计算图
        :return:
        """
        # 创建vertex的Graph
        G = nx.Graph()
        G.add_nodes_from(list(range(self.mesh.mesh.Faces.Count)))

        connected_vertices_index = []
        for i in range(self.mesh.mesh.Faces.Count):
            # 和当前顶点相连的顶点的索引
            connected_vertices_index.extend(
                list(map(lambda x: (i, x),
                         self.mesh.vertices_class.ConnectedTopologyVertices(topologyVertexIndex=System.Int32(i)))))
        G.add_edges_from(connected_vertices_index)
        return G

    def get_closeness_centrality(self, G):
        """
        计算G的closeness_centrality，并按降序全排列，返回顶点序号字典
        :param G:
        :return:
        """
        # nx的分析算法
        closeness_dict = nx.closeness_centrality(G)
        # 降序排列
        descending_closeness_dict = sorted(closeness_dict.items(), key=lambda x: x[1], reverse=False)
        return descending_closeness_dict
