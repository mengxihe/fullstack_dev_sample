# 写入3dm文件
import os.path
from typing import Union, List
# rhino inside
import rhinoinside

from aam_data_structure.data_structure_core.base_element import PartElement
from aam_data_structure.rhino_module.rhino_file_constant import \
    MODEL_TEMPLATE_FILE_NAME
from aam_data_structure.rhino_module.rhino_file_reader import RhinoFileReader
from master_plan_algorithm.simple_spoiler_generator import SimpleSpoilerGenerator

rhinoinside.load()
import System
import Rhino

class RhinoFileWriter:

    def __init__(self, template_ops: int):
        self.template_ops = template_ops
        self.doc = None
        self._create_empty_doc()

    def _create_empty_doc(self):
        doc = Rhino.RhinoDoc.Create(modelTemplateFileName=MODEL_TEMPLATE_FILE_NAME[self.template_ops])
        self.doc = doc

    def _export_data_element_file(self, data:Union[PartElement]):
        """
        写入物件部件模型
        :param data:
        :return:
        """
        # 定位点图层
        anchor_pt_layer = Rhino.DocObjects.Layer()
        anchor_pt_layer.Name = 'anchor_pt'
        anchor_pt_layer.Visible = True
        anchor_pt_layer.Color = System.Drawing.Color.FromArgb(255, 255, 255, 0)
        self.doc.Layers.Add(anchor_pt_layer)
        # 几何物件图层
        geometry_layer = Rhino.DocObjects.Layer()
        geometry_layer.Name = 'geometry'
        geometry_layer.Visible = True
        geometry_layer.Color = System.Drawing.Color.FromArgb(255, 0, 0, 0)
        self.doc.Layers.Add(geometry_layer)

        # 将物件放到对应的图层
        for g in data.geometry:
            # 创建物件属性
            cur_attr = self.doc.CreateDefaultAttributes()
            cur_attr.LayerIndex = 1
            #TODO 有一些物件类型需要转换

            # 将物件对象存入到doc中
            self.doc.Objects.Add(g, cur_attr)

    def _export_any_data_file(self, data:List[Rhino.Geometry.GeometryBase]):
        """
        将任意的
        :param data:
        :return:
        """
        layer = Rhino.DocObjects.Layer()
        layer.Name = 'default'
        layer.Visible = True
        layer.Color = System.Drawing.Color.FromArgb(255, 0, 0, 0)
        self.doc.Layers.Add(layer)

        # 将物件放到对应的图层
        for g in data:
            # 创建物件属性
            cur_attr = self.doc.CreateDefaultAttributes()
            cur_attr.LayerIndex = 0
            # TODO 有一些物件类型需要转换


            # 将物件对象存入到doc中
            self.doc.Objects.Add(g, cur_attr)


    def write_3dm_file(self, data:Union[PartElement, List],file_dir:str, file_name:str, type:int, rhino_version:int=7):
        """
        根据type类型写入3dm文件
        0为compose graph
        1为data element文件
        2为记录所有的物件
        :param file_path:
        :param file_name:
        :return:
        """
        # 文件路径
        path = file_dir + '/' + file_name
        # 设置Options
        options = Rhino.FileIO.FileWriteOptions()
        options.FileVersion = rhino_version

        if type == 0:
            self._export_data_element_file(data=data)
        else:
            self._export_any_data_file(data=data)

        self.doc.Write3dmFile(path=path, options=options)
        self.doc.Finalize()
        self.doc.Dispose()
        print(f"{path}文件已成功写入！")

if __name__ == "__main__":
    # test
    # file_dir = r'E:\pix_projects\nev_spoiler_generative_algorithm\input_models\additive_type\compose_graphs'
    # file_name = 'spoiler_compose_graph.3dm'
    file_dir = r'C:\Users\mengx\Dropbox\MENGXI\pix_moving\AAM_20220608\_AAM_Training\aam_final_assignment\aam_smallapp\backend\master_plan_algorithm\input_models'
    file_name = 'cube.3dm'

    file_reader = RhinoFileReader()
    data = file_reader.read_3dm_file(file_dir=file_dir, file_name=file_name, read_type='model')

    # output_dir =r'E:\pix_projects\nev_spoiler_generative_algorithm\input_models\additive_type\compose_graphs'
    # output_name = 'test.3dm'
    # file_writer = RhinoFileWriter(template_ops=2)
    # file_writer.write_3dm_file(data=data, file_dir=output_dir, file_name=output_name, type=0, rhino_version=7)

    output_dir =r'C:\Users\mengx\Dropbox\MENGXI\pix_moving\AAM_20220608\_AAM_Training\aam_final_assignment\aam_smallapp\backend\master_plan_algorithm\input_models\tests'
    output_name = 'test.3dm'
    file_writer = RhinoFileWriter(template_ops=2)
    print(data.geometry)
    # file_writer.write_3dm_file(data=data, file_dir=output_dir, file_name=output_name, type=1, rhino_version=7)

    file_reader = RhinoFileReader()
    spoiler_generator = SimpleSpoilerGenerator(file_reader=file_reader, params={
        'building_height': 14.0,
        'l1_road_width': 7.0,
        'l2_road_width': 3.0,
        'l4_road_width': 3.0,
        'trees_density': 5,
    })
    default_spoiler = spoiler_generator.generate_simple_spoiler()
    geoList = []
    for part in default_spoiler:
        geo = part.geometry
        geoList.append(geo)
    print(geoList)
    result = [j for sub in geoList for j in sub]
    print(result)
    file_writer.write_3dm_file(data=result, file_dir=output_dir, file_name=output_name, type=1, rhino_version=7)
    print(result)