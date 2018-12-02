import os
import json

from flask import jsonify
from part_data import PartData
from flask import Flask, g
from flask import Blueprint, abort, g, render_template, redirect, request, url_for
from slugify import slugify
from tree_engine_cfg_generator import generate_engine_tree
from tree_parts_cfg_generator import generate_parts_tree
from ecm_engines_cfg_generator import generate_ecm_engines
from ecm_parts_cfg_generator import generate_ecm_parts
from identical_parts_cfg_generator import generate_identical_parts

part_data = PartData()

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/api/part_data')
    def all_part_data():
        return jsonify({"data": part_data.parts})
    
    @app.route('/api/unique_values_for_column/<column_name>')
    def unique_values_for_column(column_name):
        sorted_values = list(part_data.unique_values_for_columns[column_name])
        sorted_values.sort()
        return jsonify({"data": sorted_values})
    
    @app.route('/api/export_to_json')
    def export_to_json():
        for mod in part_data.unique_values_for_columns['mod']:
            parts_for_mod = list(filter(lambda x: x['mod'] == mod, part_data.parts))
            text_file = open("data/" + make_safe_filename(mod)  + ".json", "w")
            text_file.write(json.dumps(parts_for_mod, sort_keys=True, indent=4, separators=(',', ': ')))
            text_file.close()
        return "true"
    @app.route('/api/generate_tree_engine_configs')
    def generate_tree_engine_configs():
        generate_engine_tree(part_data.parts)
        return "true"
    
    @app.route('/api/generate_tree_parts_configs')
    def generate_tree_parts_configs():
        generate_parts_tree(part_data.parts)
        return "true"
    
    @app.route('/api/generate_ecm_engines_configs')
    def generate_ecm_engines_configs():
        generate_ecm_engines(part_data.parts)
        return "true"
        
    @app.route('/api/generate_ecm_parts_configs')
    def generate_ecm_parts_configs():
        generate_ecm_parts(part_data.parts)
        return "true"
        
    @app.route('/api/generate_identical_parts_configs')
    def generate_identical_parts_configs():
        generate_identical_parts(part_data.parts)
        return "true"
    
    app.register_blueprint(bp)
    app.run()    
    return app
    
def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")
    
bp = Blueprint("part", __name__, url_prefix="/")

@bp.route("/")
def index():
    """
    Render the homepage.
    """
    parts = []
    parts_final = []
    
    return render_template("browser/index.html", parts=parts_final)


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """
    Render the dashboard page.
    """
    if request.method == "GET":
        return render_template("browser/dashboard.html", parts=part_data.parts)

    return render_template("browser/dashboard.html", parts=part_data.parts)


@bp.route("/<name>")
def view_part(name):
    """View a part."""
    part = part_data.get_part_by_name(name)
    if not part:
        abort(404)

    return render_template("browser/part.html", part=part)


@bp.route("/<name>/edit", methods=["GET", "POST"])
def edit_part(name):
    """Edit a post."""
    
    return redirect(url_for(".view_part", name=name))


if __name__ == "__main__":
    create_app()