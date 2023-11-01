import random


# Rhino inside部分
import rhinoinside

from typing import List

from data_structure.geometry_utils.mesh_utils.mesh_wrapper import QuadMesh

rhinoinside.load()
import System
import Rhino


class MeshWireframe:
    def __init__(self, mesh: QuadMesh, G):
        self.mesh = mesh
        self.G = G
        self.wireframe_index_list = []
        # 边点序号
        self.side_vertices_index = self.mesh.get_vertices_index_by_type(ops="side")
        # 外缘点序号
        self.exterior_vertices_index = self.mesh.get_vertices_index_by_type(ops="exterior")
        # 三分点序号
        self.triple_vertices_index= self.mesh.get_vertices_index_by_type(ops="triple")

    def _go_first_step(self, start_index) -> int:
        """
        以边点为起始点，往垂直于边界的方向走一步，返回第一步顶点的序号
        :param start_index:
        :return:
        """
        start_neighbors_index = [n for n in self.G.neighbors(start_index)]
        target_index = list(filter(lambda x: x not in self.exterior_vertices_index, start_neighbors_index))
        # print(start_neighbors_index)
        # print(self.exterior_vertices_index)
        return target_index[0]

    def _go_straight_one_step(self, last_index: int, source_index: int):
        """
        根据来向顶点和当前顶点序号，求下一步顶点序号
        :param last_index:
        :param source_index:
        :return:
        """
        # 来向顶点和当前顶点所在edge的编号
        cur_edge_index = self.mesh.get_edge_index_by_vertex_index(last_index, source_index)
        # edge两个邻面编号
        edge_connected_faces_index = self.mesh.get_faces_index_by_edge_index(cur_edge_index)

        # 取出两个邻面上的顶点编号，作为被排除的点序列
        excluded_index = []
        for face_index in edge_connected_faces_index:
            excluded_index.extend(self.mesh.get_vertices_index_by_face_index(face_index=face_index))
        # 去重
        excluded_index = list(set(excluded_index))

        # 当前起始点的相邻点编号
        source_neighbors_index = [n for n in self.G.neighbors(source_index)]

        # 在这四个相邻点中排除掉来向点、两翼点。注意排除凹点的特殊情况。
        target_index = list(filter(lambda index: index not in excluded_index, source_neighbors_index))

        # 如果剔除的结果不为空，即存在下一步：
        if len(target_index) > 0:
            # 下一步终点的编号，返回作为下一次迭代的起始点编号
            return target_index[0]
        # 剔除的结果为空，即找不到下一步：
        else:
            return None

    def _get_single_wireframe(self, start_index) -> List[int]:
        """
        以边点为起始点，提取过该点的结构线，以顶点序号列表形式返回
        :param start_index:
        :return:
        """
        # 定义结构线顶点序号列表，将首个点序号添加进去
        wireframe_index = [start_index]

        try:
            # 先往垂直于边界的方向走一步
            source_index = self._go_first_step(start_index=start_index)
            wireframe_index.append(source_index)

            # 设定递归初始条件
            last_index = start_index
            target_index = [source_index]

            # 只要下一步的终点未碰到边界（外缘点），就不停向前走
            while target_index is not None:
                # 向前走一步
                target_index = self._go_straight_one_step(last_index=last_index, source_index=source_index)
                # 如果存在下一步
                if target_index is not None:
                    # 将下一步顶点序号添加到结构线顶线序号列表中
                    wireframe_index.append(target_index)
                    # 更新递归条件
                    last_index = source_index
                    source_index = target_index
                # 如果下一步编号为空，且当前点为三分点编号，则在当前点相邻点编号中（去除来向点编号）任选一个作为下一步
                elif source_index in self.triple_vertices_index:
                    source_neighbors_index = [n for n in self.G.neighbors(source_index)]
                    candidate_neighbors_index = list(filter(lambda x: x != last_index, source_neighbors_index))
                    target_index = random.sample(candidate_neighbors_index, 1)[0]
                    # 将下一步顶点序号添加到结构线顶线序号列表中
                    wireframe_index.append(target_index)
                    # 更新递归条件
                    last_index = source_index
                    source_index = target_index
                # 如果下一步编号为空，且当前点为边缘点
                elif source_index in self.exterior_vertices_index:
                    break
        except Exception as e:
            print("某些结构线未被成功提取！")
        return wireframe_index

    def extract_mesh_wireframe_as_index_list(self) -> List[int]:
        """
        提取mesh的所有结构线，以结构线上的顶点序号列表返回
        :return:
        """
        # 遍历边点作为起始点
        for start_index in self.side_vertices_index:
            # 先统计已提取出的结构线的终点序号
            wireframe_endpoints_index = [each[-1] for each in self.wireframe_index_list]
            # 如果当前起点序号没有被提取过，求结构线
            if start_index not in wireframe_endpoints_index:
                cur_wireframe = self._get_single_wireframe(start_index=start_index)
                self.wireframe_index_list.append(cur_wireframe)
            # 如果当前起点已经在结构线集合的终点中，不计算
            else:
                pass
        return self.wireframe_index_list


if __name__ == '__main__':
    print('yes')
