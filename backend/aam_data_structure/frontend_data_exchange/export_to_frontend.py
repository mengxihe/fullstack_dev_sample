# 将数据转换成前端可以读取的bytes
# systematic
import base64
from typing import List, Union, AnyStr
import rhinoinside

from aam_data_structure.data_structure_core.base_element import PartElement, \
    SectionElement

rhinoinside.load()
import System
import Rhino

class FrontendExporter:

    def __init__(self):
        pass

    def _get_layer_index_by_layer_name(self, file3dm:Rhino.FileIO.File3dm, layer_name:AnyStr)->int:
        """
        传入一个file3dm 文件，通过图层名返回index
        :param file3dm:
        :return:
        """
        layer_dict = {each.Name: each.Index for each in file3dm.Layers}
        return layer_dict[layer_name]

    def _add_object_to_file3dm(self, file3dm:Rhino.FileIO.File3dm,geo:Rhino.Geometry.GeometryBase, obj_attr:Rhino.DocObjects.ObjectAttributes):
        """
        将物件对应插入到file3dm中
        :param geo:
        :param layer_idx:
        :return:
        """
        if geo.ObjectType == 0:
            print('None cannot add to file3dm')
        elif geo.ObjectType == 1:
            if isinstance(geo, Rhino.Geometry.Point):
                cur_id = file3dm.Objects.AddPoint(point=geo.Location, attributes=obj_attr)
                cur_obj = file3dm.Objects.FindId(id=cur_id)
                cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
            else:
                file3dm.Objects.AddPoint(point=geo, attributes=obj_attr)
        elif geo.ObjectType == 2:
            print('PointSet cannot add to file3dm')
        elif geo.ObjectType == 4:
            cur_id = file3dm.Objects.AddCurve(curve=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 8:
            cur_id = file3dm.Objects.AddSurface(surface=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 16:
            cur_id = file3dm.Objects.AddBrep(brep=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 32:
            cur_id = file3dm.Objects.AddMesh(mesh=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 256:
            print('Light cannot add to file3dm')
        elif geo.ObjectType == 512:
            print('Annotation cannot add to file3dm')
        elif geo.ObjectType == 2048:
            cur_id = file3dm.Objects.AddInstanceObject(instanceReference=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 4096:
            cur_id = file3dm.Objects.AddInstanceObject(instanceReference=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 8192:
            cur_id = file3dm.Objects.AddTextDot(dot=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 16384:
            print('Grip cannot add to file3dm')
        elif geo.ObjectType == 32768:
            print('Detail cannot add to file3dm')
        elif geo.ObjectType == 65536:
            cur_id = file3dm.Objects.AddHatch(hatch=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 131072:
            print('MorphControl cannot add to file3dm')
        elif geo.ObjectType == 262144:
            cur_id = file3dm.Objects.AddSubD(subd=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 524288:
            print('BrepLoop cannot add to file3dm')
        elif geo.ObjectType == 1048576:
            print('BrepVertex cannot add to file3dm')
        elif geo.ObjectType == 2097152:
            print('PolysrfFilter cannot add to file3dm')
        elif geo.ObjectType == 4194304:
            print('EdgeFilter cannot add to file3dm')
        elif geo.ObjectType == 8388608:
            print('PolyedgeFilter cannot add to file3dm')
        elif geo.ObjectType == 16777216:
            print('MeshVertex cannot add to file3dm')
        elif geo.ObjectType == 33554432:
            print('MeshEdge cannot add to file3dm')
        elif geo.ObjectType == 67108864:
            print('MeshFace cannot add to file3dm')
        elif geo.ObjectType == 134217728:
            print('Cage cannot add to file3dm')
        elif geo.ObjectType == 268435456:
            print('Phantom cannot add to file3dm')
        elif geo.ObjectType == 536870912:
            print('ClipPlane cannot add to file3dm')
        elif geo.ObjectType == 1073741824:
            cur_id = file3dm.Objects.AddExtrusion(extrusion=geo, attributes=obj_attr)
            cur_obj = file3dm.Objects.FindId(id=cur_id)
            cur_obj.Attributes.set_LayerIndex(obj_attr.LayerIndex)
        elif geo.ObjectType == 4294967295:
            print('AnyObject cannot add to file3dm')

    def _add_layer_to_file3dm(self,file3dm:Rhino.FileIO.File3dm, name:AnyStr):
        """
        增加图层到对应的file3dm中
        :return:
        """
        file3dm.AllLayers.AddLayer(name=name, color=System.Drawing.Color())

    def _convert_file3dm_to_base64(self, file3dm)->AnyStr:
        """
        将file3dm转换成base64的byte array
        :param file3dm:
        :return:
        """
        file3dm = System.Convert.ToBase64String(file3dm.ToByteArray())
        data = base64.b64decode(file3dm)
        data = base64.b64encode(data)
        return str(data, 'utf-8')

    def _convert_invalid_to_mesh(self, geometry:Rhino.Geometry.GeometryBase)->Rhino.Geometry.Mesh:
        """
        将一些没法识别的类型转换成mesh
        :param geometry:
        :return:
        """
        if geometry.ObjectType == 1073741824:
            geometry = geometry.ToBrep()
            print(f'{geometry.ObjectType}---------------->Rhino.Geometry.brep')
        if geometry.ObjectType == 16:
            cur_mesh_list = Rhino.Geometry.Mesh().CreateFromBrep(brep=geometry, meshingParameters=Rhino.Geometry.MeshingParameters())
            res_mesh = Rhino.Geometry.Mesh()
            res_mesh.Append(meshes=cur_mesh_list)
            res_mesh.MergeAllCoplanarFaces(tolerance=2.0)
            geometry = res_mesh
            print(f'{geometry.ObjectType}---------------->Rhino.Geometry.Mesh')
        return geometry

    def export_single_base_element(self, ele:Union[PartElement, SectionElement])->List:
        """
        将一个base element类转换成包含file3dm byte以及其他信息的dict
        :param ele:
        :return:
        """
        cur_file3dm = Rhino.FileIO.File3dm()
        # 建立geometry图层以及写入对应的内容
        self._add_layer_to_file3dm(file3dm=cur_file3dm,name='geometry')
        for g in ele.geometry:
            g = self._convert_invalid_to_mesh(geometry=g)
            idx = self._get_layer_index_by_layer_name(file3dm=cur_file3dm, layer_name='geometry')
            obj_attr = Rhino.DocObjects.ObjectAttributes()
            obj_attr.LayerIndex = System.Int32(idx)
            self._add_object_to_file3dm(file3dm=cur_file3dm,geo=g, obj_attr=obj_attr)
        # anchor_pt 图层以及写入对应内容
        if ele.anchor_pt != None:
            self._add_layer_to_file3dm(file3dm=cur_file3dm, name='anchor_pt')
            idx = self._get_layer_index_by_layer_name(file3dm=cur_file3dm, layer_name='anchor_pt')
            obj_attr = Rhino.DocObjects.ObjectAttributes()
            obj_attr.LayerIndex = System.Int32(idx)
            self._add_object_to_file3dm(file3dm=cur_file3dm, geo=ele.anchor_pt, obj_attr=obj_attr)
        # install_pt 图层以及写入对应内容
        if len(ele.install_pts) > 0:
            for pt in ele.install_pts:
                self._add_layer_to_file3dm(file3dm=cur_file3dm, name=pt.layer)
                idx = self._get_layer_index_by_layer_name(file3dm=cur_file3dm, layer_name=pt.layer)
                obj_attr = Rhino.DocObjects.ObjectAttributes()
                obj_attr.LayerIndex = System.Int32(idx)
                self._add_object_to_file3dm(file3dm=cur_file3dm, geo=pt.pt, obj_attr=obj_attr)
        # rotate_pt 图层以及写入对应内容
        if len(ele.rotate_pts) > 0:
            for pt in ele.rotate_pts:
                self._add_layer_to_file3dm(file3dm=cur_file3dm, name=pt.layer)
                idx = self._get_layer_index_by_layer_name(file3dm=cur_file3dm, layer_name=pt.layer)
                obj_attr = Rhino.DocObjects.ObjectAttributes()
                obj_attr.LayerIndex = System.Int32(idx)
                self._add_object_to_file3dm(file3dm=cur_file3dm, geo=pt.pt, obj_attr=obj_attr)
        # 如果有链接的物件，以树状结构来组建字典
        link_elements = []
        if len(ele.link_elements)>0:
            for sub_ele in ele.link_elements.values():
                link_elements.extend(self.export_single_base_element(ele=sub_ele))



        # 父节点
        element_dict = {
            'file3dm':self._convert_file3dm_to_base64(file3dm=cur_file3dm),
            'link_element':link_elements,
            'parent_element':ele.parent_element,
            # semantics attributes
            'id':ele.id,
            'object_type':ele.object_type,
            'object_name':ele.object_name,
            'custom_semantics':ele.custom_semantics,
        }
        return [element_dict]

    def export_element_to_frontend(self, elements:List[Union[PartElement, SectionElement]]):
        """
        输出对应的data element到前端
        :param elements:
        :return:
        """
        res_list = []
        for each in elements:
            cur_res = self.export_single_base_element(ele=each)
            res_list.extend(cur_res)
        return res_list



if __name__ == '__main__':
    exporter = FrontendExporter()
    exporter.export_element_to_frontend([])

