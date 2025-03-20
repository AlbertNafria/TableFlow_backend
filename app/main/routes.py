from flask import render_template
from app.main import bp

# Routes
# Página web home para ver la documentación de la api
@bp.route("/")
@bp.route("/index")
def home():
    return render_template("index.html")

