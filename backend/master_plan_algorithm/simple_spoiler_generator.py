from typing import Dict
from aam_data_structure.data_structure_core.base_element import SectionElement, PartElement
from aam_data_structure.geometry_utils.brep_geometry_utils import extrude_brep, create_brep_from_loft_simple, create_brep_list
from aam_data_structure.geometry_utils.surface_geometry_utils import create_brep_by_boundary
from aam_data_structure.geometry_utils.curve_geometry_utils import specific_offset_curve_by_distance, judge_point_containment
from aam_data_structure.geometry_utils.geometry_analysis_utils import get_closed_curve_area
from aam_data_structure.rhino_module.rhino_file_reader import RhinoFileReader
import master_plan_algorithm.spoiler_algorithm_constant as constant
from aam_data_structure.frontend_data_exchange.export_to_frontend import \
    FrontendExporter
import random
import rhinoinside

rhinoinside.load()
import Rhino
import System


class SimpleSpoilerGenerator:

    def __init__(self, file_reader: RhinoFileReader, params: Dict):
        self.file_reader = file_reader
        self.params = params
        self.outlines = None
        self.buildings = None
        self.river_bank = None
        self.grass_good = None
        self.grass_better = None
        self.l1_road = None
        self.l2_road = None
        self.l4_road = None

    def _load_init_files(self):
        # read all 3dm files
        self.outline = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='outline.3dm', read_type='section')
        self.buildings = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='buildings.3dm', read_type='section')
        self.river_bank = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='river_bank.3dm', read_type='section')
        self.grass_good = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='grass_good.3dm', read_type='section')
        self.grass_better = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='grass_better.3dm', read_type='section')
        self.l1_road = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='l1_road.3dm', read_type='section')
        self.l2_road = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='l2_road.3dm', read_type='section')
        self.l4_road = self.file_reader.read_3dm_file(file_dir=constant.SIMPLE_ADDITIVE_TYPE_DIR, file_name='l4_road.3dm', read_type='section')

    def _generate_elements(self, file_layer_geometry: list, height: float, layer_name: str):
        """
        generate part elements from read file geometries
        """
        model_list = []
        test_element = PartElement()
        for geo in file_layer_geometry:
            boundary = create_brep_by_boundary(geo)
            boundary_face = boundary.Faces[0]
            boundary_model = extrude_brep(boundary_face, height, True)
            test_element.geometry.append(boundary_model)
            test_element.object_name = layer_name
        return test_element

    def _generate_trees(self):
        """
        generate trees geometries
        """
        alltrunks = []
        alltrunks_test = []
        for crv in self.grass_better.geometry:
            planer_brep = create_brep_by_boundary(crv)
            srf = planer_brep.Faces[0]
            domU = srf.Domain(0)
            domV = srf.Domain(1)
            curve_area = get_closed_curve_area(crv)
            trunks_test = PartElement()
            if curve_area > 399:
                while len(trunks_test.geometry) < self.params['trees_density']:
                    # print(curve_area)
                    u = random.uniform(domU[0], domV[1])
                    v = random.uniform(domV[0], domV[1])
                    point = srf.PointAt(u,v)
                    interior = Rhino.Geometry.PointFaceRelation.Interior
                    if srf.IsPointOnFace(u,v) == interior:
                        circle = Rhino.Geometry.Circle(point, 0.5)
                        ccurve = Rhino.Geometry.NurbsCurve.CreateFromCircle(circle)
                        planer = create_brep_by_boundary(ccurve)
                        face = planer.Faces[0]
                        truck = extrude_brep(face, 7.0, True)
                        trunks_test.geometry.append(truck)
                        trunks_test.object_name = 'truck_test'
            else:
                while len(trunks_test.geometry) <= 1:
                    # print(curve_area)
                    u = random.uniform(domU[0], domV[1])
                    v = random.uniform(domV[0], domV[1])
                    point = srf.PointAt(u,v)
                    interior = Rhino.Geometry.PointFaceRelation.Interior
                    if srf.IsPointOnFace(u,v) == interior:
                        circle = Rhino.Geometry.Circle(point, 0.5)
                        ccurve = Rhino.Geometry.NurbsCurve.CreateFromCircle(circle)
                        planer = create_brep_by_boundary(ccurve)
                        face = planer.Faces[0]
                        truck = extrude_brep(face, 7.0, True)
                        trunks_test.geometry.append(truck)
                        trunks_test.object_name = 'truck_test'
            alltrunks_test.append(trunks_test)
        # result = [j for sub in alltrunks for j in sub]
        return alltrunks_test


    def _operate_road(self, file_layer_geometry: list, height: float, road_width: float, layer_name: str):
        """
        create elements for the lines/roads
        :param file_layer_geometry: height: road_width: layer_name
        :return
        """
        road_model_list = []
        road_model_test = []
        for geo in file_layer_geometry:
            offset_distance = road_width/2
            lines = specific_offset_curve_by_distance(geo, offset_distance, 2)
            road_loft = create_brep_from_loft_simple(lines, closed=False, loft_type=Rhino.Geometry.LoftType.Straight, is_cap=False)
            road_face = road_loft.Faces[0]
            road_model = extrude_brep(road_face, height, layer_name)
            road_element = PartElement()
            road_element.geometry.append(road_model)
            road_element.object_name = layer_name
            road_model_list.append(road_element)
        return road_model_list

    def _operate_model(self):
        """
        :param:
        :return big_model:
        """
        self.outline_model = self._generate_elements(self.outline.geometry, 1.0, 'outlines')
        self.buildings_model = self._generate_elements(self.buildings.geometry, self.params['building_height'], 'buildings')
        self.river_bank_model = self._generate_elements(self.river_bank.geometry, 1.2, 'river_bank')
        self.grass_good_model = self._generate_elements(self.grass_good.geometry, 2.2, 'grass_good')
        self.grass_better_model = self._generate_elements(self.grass_better.geometry, 2.2, 'grass_better')
        self.l1_road_model = self._operate_road(self.l1_road.geometry, 4.0, self.params['l1_road_width'], 'l1_road')
        self.l2_road_model = self._operate_road(self.l2_road.geometry, 3.0, self.params['l2_road_width'], 'l2_road')
        self.l4_road_model = self._operate_road(self.l4_road.geometry, 4.0, self.params['l4_road_width'], 'l4_road')
        self.trees_model = self._generate_trees()

        big_model = [self.outline_model, self.buildings_model, self.river_bank_model, self.grass_better_model, self.grass_good_model]+self.l1_road_model + self.l2_road_model +self.l4_road_model+self.trees_model
        return big_model

    def generate_simple_spoiler(self):
        self._load_init_files()
        whole_spoiler = self._operate_model()
        return whole_spoiler


if __name__ == '__main__':
    exporter = FrontendExporter()
    file_reader = RhinoFileReader()
    spoiler_generator = SimpleSpoilerGenerator(file_reader=file_reader, params = {
        'building_height': 14.0,
        'l1_road_width': 7.0,
        'l2_road_width': 3.0,
        'l4_road_width': 3.0,
        'trees_density': 5,
    })
    default_spoiler = spoiler_generator.generate_simple_spoiler()
