"""
读取对应的rhino3dm文件，并转换成对应的数据结构
"""
import re
import os
import json
from uuid import uuid1
from typing import Dict, List, Union, AnyStr

# Rhino inside部分
import rhinoinside

from aam_data_structure.data_structure_core.base_element import PartElement, \
    SectionElement
from aam_data_structure.data_structure_core.points import InstallPoint, RotatePoint

rhinoinside.load()
import System
import Rhino

class RhinoFileReader:
    # 以下为RhinoCommon格式转换模块
    AllRhinoObjectType = {
        0: 'None',
        1: 'Point',
        2: 'PointSet',
        4: 'Curve',
        8: 'Surface',
        16: 'Brep',
        32: 'Mesh',
        256: 'Light',
        512: 'Annotation',
        2048: 'InstanceDefinition',
        4096: 'InstanceReference',
        8192: 'TextDot',
        16384: 'Grip',
        32768: 'Detail',
        65536: 'Hatch',
        131072: 'MorphControl',
        262144: 'SubD',
        524288: 'BrepLoop',
        1048576: 'BrepVertex',
        2097152: 'PolysrfFilter',
        4194304: 'EdgeFilter',
        8388608: 'PolyedgeFilter',
        16777216: 'MeshVertex',
        33554432: 'MeshEdge',
        67108864: 'MeshFace',
        134217728: 'Cage',
        268435456: 'Phantom',
        536870912: 'ClipPlane',
        1073741824: 'Extrusion',
        4294967295: 'AnyObject'
    }

    def __init__(self):
        self.file3dm = None

    def _read_file3dm(self, file_path)->Rhino.FileIO.File3dm:
        """
        读取文件的file3dm
        :param file_path:
        :return:
        """
        print(f'正在读取3dm文件，路径：{file_path}')
        file3dm = Rhino.FileIO.File3dm()
        return file3dm.Read(file_path)

    def _extract_layer_name_file3dm(self, file3dm: Rhino.FileIO.File3dm) -> Dict:
        """
        用fileIO的方法读取文件
        :param file3dm:
        :return:
        """
        return {each.Index: each.Name for each in file3dm.Layers}

    def _extract_file_to_part_element(self, file3dm:Rhino.FileIO.File3dm, layers:Dict, name:str)->PartElement:
        """
        将文件转换成PartElement
        :param file_name:
        :param layers:
        :param name:
        :return:
        """
        cur_data_element = PartElement()
        cur_data_element.id = uuid1()
        cur_data_element.object_name = name
        for each in file3dm.Objects:
            if layers[each.Attributes.get_LayerIndex()] == 'anchor_pt':
                cur_data_element.anchor_pt = each.Geometry
            elif 'install_' in layers[each.Attributes.get_LayerIndex()]:
                cur_install_pt = InstallPoint()
                cur_install_pt.pt = each.Geometry
                cur_install_pt.layer = layers[each.Attributes.get_LayerIndex()]
                cur_data_element.install_pts.append(cur_install_pt)
            elif 'rotate_' in layers[each.Attributes.get_LayerIndex()]:
                cur_rotate_pt = RotatePoint()
                cur_rotate_pt.pt = each.Geometry
                cur_rotate_pt.layer = layers[each.Attributes.get_LayerIndex()]
                cur_data_element.rotate_pts.append(cur_rotate_pt)
            elif layers[each.Attributes.get_LayerIndex()] == 'geometry':
                cur_data_element.geometry.append(each.Geometry)
        cur_data_element.object_type = 'PartElement'
        return cur_data_element

    def _extract_file_to_section_element(self, file3dm:Rhino.FileIO.File3dm, layers:Dict, name:str)->SectionElement:
        """
        将文件转换成PartElement
        :param file_name:
        :param layers:
        :param name:
        :return:
        """
        cur_section_element = SectionElement()
        cur_section_element.id = uuid1()
        cur_section_element.object_name = name
        for each in file3dm.Objects:
            if layers[each.Attributes.get_LayerIndex()] == 'anchor_pt':
                cur_section_element.anchor_pt = each.Geometry
            elif 'install_' in layers[each.Attributes.get_LayerIndex()]:
                cur_install_pt = InstallPoint()
                cur_install_pt.pt = each.Geometry
                cur_install_pt.layer = layers[each.Attributes.get_LayerIndex()]
                cur_section_element.install_pts.append(cur_install_pt)
            elif 'rotate_' in layers[each.Attributes.get_LayerIndex()]:
                cur_rotate_pt = RotatePoint()
                cur_rotate_pt.pt = each.Geometry
                cur_rotate_pt.layer = layers[each.Attributes.get_LayerIndex()]
                cur_section_element.rotate_pts.append(cur_rotate_pt)
            elif layers[each.Attributes.get_LayerIndex()] == 'section':
                cur_section_element.geometry.append(each.Geometry)
        cur_section_element.object_type = 'SectionElement'
        return cur_section_element

    def read_3dm_file(self, file_dir: str, file_name: str, read_type:str) -> Union[PartElement, SectionElement,None]:
            """
            读取3dm文件，并转换成对应的数据结构
            :param file_dir:
            :param file_name:
            :return:
            """
            # 拼接然后读取传入的3dm文件
            file_path = os.path.join(os.path.abspath(file_dir), file_name)
            print(f'当前文件路径{file_path}')
            # 读取文件
            file3dm = self._read_file3dm(file_path=file_path)
            layers = self._extract_layer_name_file3dm(file3dm=file3dm)
            name = file_name.split('.')[0]
            if read_type == 'model':
                return self._extract_file_to_part_element(file3dm=file3dm, layers=layers, name=name)
            elif read_type == 'section':
                return self._extract_file_to_section_element(file3dm=file3dm,layers=layers, name=name)
            else:
                return None

if __name__ == '__main__':
    file_reader = RhinoFileReader()

    file_dir = r'D:\NEV\nev_spoiler_generative_algorithm\input_models\normal_type\parts'
    spoiler_model_file = 'spoiler_base_model.3dm'
    spoiler_model = file_reader.read_3dm_file(file_dir=file_dir, file_name=spoiler_model_file, read_type='model')

    print(spoiler_model)
    # print(spoiler_model)
    # spoiler_compose_graph_file = 'spoiler_compose_graph.3dm'
    # spoiler_compose_graph = file_reader.read_3dm_file(file_dir=file_dir, file_name=spoiler_compose_graph_file, read_type='graph')
