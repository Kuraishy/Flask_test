from flask import blueprint, render_template

second = Blueprint("second",__name__, static_folder = "static", template_folder="templates")