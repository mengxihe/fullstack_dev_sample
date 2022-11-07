from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import server_constant
from aam_data_structure.rhino_module.rhino_file_reader import RhinoFileReader
from aam_data_structure.rhino_module.rhino_file_writer import RhinoFileWriter
from aam_data_structure.frontend_data_exchange.export_to_frontend import \
    FrontendExporter
import master_plan_algorithm.spoiler_algorithm_constant as constant
from master_plan_algorithm.simple_spoiler_generator import SimpleSpoilerGenerator

def create_app():
    app = Flask(__name__)
    # allow cross-domain
    CORS(app, resources={r'/*':{'origins':"*"}})
    return app


app = create_app()
app.debug = server_constant.DEBUG_MODE

@app.route('/', methods=['GET'])
def connect_test():
    return 'the connection is stable'


@app.route("/test", methods=['GET', 'POST'])
def greetings():
    print('received a request from frontend')
    return jsonify({"name": "tom", "age": 10})

@app.route("/getSpoiler", methods=['GET', 'POST'])
def getspoiler():
    """
    :param:
    :return: jsonify(export_data)
    """
    params = {
        'building_height': 14.0,
        'l1_road_width': 7.0,
        'l2_road_width': 3.0,
        'l4_road_width': 3.0,
        'trees_density': 5,
    }
    print('received a request from frontend')
    exporter = FrontendExporter()
    fileReader = RhinoFileReader()
    spoiler = SimpleSpoilerGenerator(fileReader, params)
    simpleSpoiler = spoiler.generate_simple_spoiler()
    export_data = exporter.export_element_to_frontend(elements=simpleSpoiler)
    return jsonify(export_data)

@app.route('/generate_building', methods=['POST'])
def generate_building():
    """
    根据参数生成building
    :return:
    """
    params = json.loads(request.data)['params']
    params = {
        'building_height': params['buildingHight'],  
        'l1_road_width': params['l1RoadWidth'],  
        'l2_road_width': params['l2RoadWidth'],  
        'l4_road_width': float(params['l4RoadWidth']),  
        'trees_density': params['treeDensity'],  
    }
    print('received a request from frontend')
    exporter = FrontendExporter()
    fileReader = RhinoFileReader()
    spoiler = SimpleSpoilerGenerator(fileReader, params)
    simpleSpoiler = spoiler.generate_simple_spoiler()
    export_data = exporter.export_element_to_frontend(elements=simpleSpoiler)
    return jsonify(export_data)


@app.route('/save_file', methods=['POST'])
def save_3dm():
    """
    save file when click
    :param
    :return:
    """
    params = json.loads(request.data)['param']
    params = {
        'building_height': params['buildingHight'],  #
        'l1_road_width': params['l1RoadWidth'],  #
        'l2_road_width': params['l2RoadWidth'],  #
        'l4_road_width': float(params['l4RoadWidth']),  #
        'trees_density': params['treeDensity'],  #
    }
    print('received a request from frontend')

    file_reader = RhinoFileReader()
    spoiler = SimpleSpoilerGenerator(file_reader, params)
    simpleSpoiler = spoiler.generate_simple_spoiler()

    file_writer = RhinoFileWriter(template_ops=2)
    output_dir = r'C:\Users\mengx\Dropbox\MENGXI\pix_moving\AAM_20220608\_AAM_Training\aam_final_assignment\aam_smallapp\backend\master_plan_algorithm\input_models\tests'
    output_name = 'test.3dm'
    geoList = []
    for part in simpleSpoiler:
        geo = part.geometry
        geoList.append(geo)

    result = [j for sub in geoList for j in sub]
    file_writer.write_3dm_file(data=result, file_dir=output_dir, file_name=output_name, type=1, rhino_version=7)

    return jsonify(output_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
