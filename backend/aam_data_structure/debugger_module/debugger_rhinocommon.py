from typing import List
import os
import rhinoinside
from uuid import uuid1
rhinoinside.load()
import System
import Rhino


def debugger_some_objects(objects):
    """
    专门用来debugger任意的物件
    生产的文件在当前模块的文件夹下
    :param List:
    :return:
    """
    # 路径
    path = r'D:\arp_projects\arp_kool_urban_tool_v1_server\debugger_module\result'
    path = os.path.abspath(path)
    # 创建data model
    data_model = DataModel(mode='RhinoCommon')
    data_model.name = f'debugger_mode_{str(uuid1())}'
    data_model.id = 'None'
    data_model.elements = []
    # 插入
    for obj in objects:
        create_data_element(geometry=obj, layer_name='0', data_model=data_model)
    # 写入文件
    template_ops = 2  # '大模型 - 米.3dm'
    rhino_file_writer = RhinoFileWriter(data_model=data_model, template_ops=template_ops)
    rhino_file_writer.write_3dm_file(file_path=path, file_name=data_model.name)
    print('写入一个debugger.....')