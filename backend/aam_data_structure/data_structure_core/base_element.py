# 单独的部件数据结构

from dataclasses import dataclass, field
import uuid
from typing import *
from typing import List, AnyStr, Tuple, Dict, Union
import math

import rhinoinside
import networkx as nx
from networkx import Graph

from aam_data_structure.data_structure_core.points import InstallPoint, RotatePoint


rhinoinside.load()
import System
import Rhino


@dataclass(order=True)
class BaseElement:
    # geometry attributes
    geometry: List = field(default_factory=list)  # 可以包括rhinocommon的geometry
    link_elements: Dict = field(default_factory=dict)  # 与该element链接的element的id
    parent_element: AnyStr = field(default=None)  # 上级节点
    anchor_pt: Rhino.Geometry = field(default=None)  # 如果是具体的零部件，则需要有对应的anchor pt
    install_pts: List = field(default_factory=list)  # 用于安装其他零部件的安装点
    rotate_pts: List = field(default_factory=list)  # 用于锚定旋转的点
    # semantics attributes
    id: AnyStr = field(default=None)
    object_type: AnyStr = field(default=None)  # 物件类型，属于是哪个位置的部件（用于按类型分类构件）
    object_name: AnyStr = field(default=None)  # 物件名称，物件具体的名称
    compose_graph: Graph = field(default=nx.Graph())  # 组合图
    # 自定义语义
    custom_semantics: Dict = field(default_factory=dict)

    def __post_init__(self):
        """
        要先将自己的id加入到compose graph中
        :return:
        """
        self.id = str(uuid.uuid1())
        self.compose_graph.add_node(self.id)

    # 标记需要与该物件链接的物件，可以是PartElement或SectionElement
    def link(self, elements: List):
        """
        用于生成链接记录
        :param element:
        :return:
        """
        if not isinstance(elements, List):
            elements = [elements]
        for each in elements:
            if isinstance(each, PartElement) or isinstance(each, SectionElement):
                if each.id not in list(self.link_elements.keys()):
                    self.link_elements[each.id]=each
                    each.parent_element = self.id

    # 直接提取所有的几何对象，用于输出测试
    # 需要将所有的link elements展开到一个表上
    def export_all_geometry(self):
        """
        提取所有的对象，用于测试等
        anchor_pt, install_pts, rotate_pts不会被提取
        :return:
        """
        res = []
        res.extend([e for e in self.geometry])
        if len(self.link_elements)>0:
            for key, value in self.link_elements.items():
                res.extend(value.export_all_geometry())
        res = list(set(res))
        return res

    # 递归获取所有的link element中的所有对应的物件
    def extract_all_link_elements(self):
        """
        递归获取所有的link elements
        :return:
        """
        res = []
        if len(self.link_elements)>0:
            for each in self.link_elements.values():
                res.extend(each.extract_all_link_elements()+[self])
        else:
            res.append(self)
        return res

    def assemble_part_element(self, element_list: List):
        """
        用多个part element 组装成一个part element
        并在compose graph中构建对应的部件连接图
        :return:
        """
        self.object_type = 'compose_object'
        # 先合并graph，然后再在part elements and section elements 中只加入与
        # all_graph = nx.compose_all([each.compose_graph for each in part_element_list])

        # 将所有没有父亲节点的过滤出来
        valid_elements = list(filter(lambda each:each.parent_element is None, element_list))

        # 只连接没有父节点的物件，其他物件会随着父节点联动
        self.link(elements=valid_elements)

        # TODO draw graph test
        # nx.draw(all_graph)
        # plt.pause(0)


    # 选择点
    def select_pt_by_layer_name(self, layer_name: AnyStr) -> Union[InstallPoint, RotatePoint]:
        """
        通过图层名选择对应的对象
        :param layer_name:
        :return:
        """
        if 'install' in layer_name:
            return list(filter(lambda each: each.layer == layer_name, self.install_pts))[0]
        elif 'rotate' in layer_name:
            return list(filter(lambda each: each.layer == layer_name, self.rotate_pts))[0]


@dataclass(order=True)
class PartElement(BaseElement):
    def __int__(self):
        pass

    def duplicate(self, object_name: AnyStr):
        """
        做一个复制，rhino.geometry不能使用deepcopy
        :return:
        """
        cur = PartElement()
        # 处理geometry
        cur.geometry = [g.Duplicate() for g in self.geometry]
        # 处理anchor pt
        cur.anchor_pt = self.anchor_pt.Duplicate() if self.anchor_pt != None else None
        # 处理install pts
        if len(self.install_pts) > 0:
            for _ in self.install_pts:
                cur.install_pts.append(_.duplicate())
        # 处理rotate pts
        if len(self.rotate_pts) > 0:
            for _ in self.rotate_pts:
                cur.rotate_pts.append(_.duplicate())
        # 处理link elements以及父节点
        if len(self.link_elements)>0:
            for key, val in self.link_elements.items():
                cur.link_elements[key] = val.duplicate()
        cur.parent_element = self.parent_element
        # semantics attributes
        cur.object_type = self.object_type
        cur.object_name = object_name
        cur.compose_graph = self.compose_graph
        cur.custom_semantics = self.custom_semantics
        return cur

@dataclass(order=True)
class SectionElement(BaseElement):
    def __int__(self):
        pass

    def duplicate(self, object_name: AnyStr):
        """
        做一个复制，rhino.geometry不能使用deepcopy
        :return:
        """
        cur = SectionElement()
        # 处理geometry
        cur.geometry = [g.Duplicate() for g in self.geometry]
        # 处理anchor pt
        cur.anchor_pt = self.anchor_pt.Duplicate() if self.anchor_pt != None else None
        # 处理install pts
        if len(self.install_pts) > 0:
            for _ in self.install_pts:
                cur.install_pts.append(_.duplicate())
        # 处理rotate pts
        if len(self.rotate_pts) > 0:
            for _ in self.rotate_pts:
                cur.rotate_pts.append(_.duplicate())
        # 处理link elements以及父节点
        if len(self.link_elements) > 0:
            for key, val in self.link_elements.items():
                cur.link_elements[key] = val.duplicate()
        cur.parent_element = self.parent_element
        # semantics attributes
        cur.object_type = self.object_type
        cur.object_name = object_name
        cur.compose_graph = self.compose_graph
        cur.custom_semantics = self.custom_semantics
        return cur