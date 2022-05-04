from flask import Flask
from flask import render_template
from flask import redirect
from flask import jsonify
from flask import g
from flask import request
from jsonschema import ValidationError
from dicttoxml import dicttoxml
from pandas import DataFrame
from tzlocal import get_localzone
from unicodedata import normalize
from unicodedata import category
from apscheduler.schedulers.background import BackgroundScheduler

from .modules.database import Database
from .modules.parser import parse
from .modules.schemas import validate_schema

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
localzone = get_localzone().__str__()
app.scheduler = BackgroundScheduler(timezone=localzone, daemon=True)
app.scheduler.start()


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g._database = Database()
    return g._database


def strip_accents(s):
    return ''.join(c for c in normalize('NFD', s)
                   if category(c) != 'Mn')


def search_by_arrondissement(arrondissement):
    db = get_db()
    installations = db.read_all_installations_arrondissement(arrondissement)
    return [installation.to_dictionary() for installation in installations]


def search_by_installation(installation):
    db = get_db()
    installations = db.read_installation_nom(installation)
    return installations.to_dictionary()

def search_by_arrondissement(arrondissement):
    db = get_db()
    installations = db.read_all_installations_arrondissement(arrondissement)
    return [installation.to_dictionary() for installation in installations]


def search_by_installation(installation):
    db = get_db()
    installations = db.read_installation_nom(installation)
    r

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="404"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title="500"), 500


@app.errorhandler(ValidationError)
def validation_error(e):
    return jsonify({'error': e.message}), 400


# Initialiser la base de donnees avant le premier request
@app.before_first_request
@app.scheduler.scheduled_job(trigger='cron', day='*', hour=0, minute=0)
def init_database():
    with app.app_context():
        # print("--------------- Test importation des donnees ---------------")
        parse(get_db())


@app.route('/')
def index():
    return redirect('/doc', code=302)


@app.route('/doc')
def documentation():
    return render_template("doc.html"), 200


@app.route('/rechercher')
def rechercher():
    installations = get_db().read_all_noms()
    return render_template("index.html", title="Index",
                           installations=installations), 200


# Retourner les installations disponibles
@app.route('/api/installations', methods=['GET'])
def installations():
    # Rechercher par nom d'arrondissement
    arrondissement = request.args.get('arrondissement')
    if arrondissement is not None and len(arrondissement) != 0:
        installations = search_by_arrondissement(arrondissement)
        # Verifier si l'arrondissement existe
        if len(installations) == 0:
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
        return jsonify(installations)
    # Rechercher par nom d'installation
    installation = request.args.get('installation')
    if installation is not None and len(installation) != 0:
        try:
            installations = search_by_installation(installation)
        except TypeError:
            # Retourner 404 si le nom de l'installation n'existe pas
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
        return jsonify(installations), 200
    # Retourner toutes les installations
    installations = get_db().read_all_installations()
    installations = sorted(installations, key=lambda i: strip_accents(i.nom))
    return jsonify([installation.to_dictionary()
                    for installation in installations]), 200


# Retouner une version xml des installations
@app.route('/api/installations/xml', methods=['GET'])
def installation_xml():
    # Rechercher par nom d'installation
    installation = request.args.get('installation')
    if installation is not None and len(installation) != 0:
        try:
            installation = get_db().read_installation_nom(installation)
            xml = dicttoxml([installation.to_dictionary()])
            return Response(xml, mimetype='text/xml'), 200
        except TypeError:
            # Retourner 404 si le nom de l'installation n'existe pas
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
    # Rechercher toutes les installations
    installations = get_db().read_all_installations()
    installations = sorted(installations, key=lambda i: strip_accents(i.nom))
    xml = dicttoxml([installation.to_dictionary()
                     for installation in installations])
    return Response(xml, mimetype='text/xml'), 200


# Retouner une version csv des installations
@app.route('/api/installations/csv', methods=['GET'])
def installation_csv():
    # Rechercher par nom d'installation
    installation = request.args.get('installation')
    if installation is not None and len(installation) != 0:
        try:
            installation = get_db().read_installation_nom(installation)
            csv = DataFrame([installation.to_dictionary()]).to_csv(index=False)
            return Response(csv, mimetype='text/csv'), 200
        except TypeError:
            # Retourner 404 si le nom de l'installation n'existe pas
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
    # Rechercher toutes les installations
    installations = get_db().read_all_installations()
    installations = sorted(installations, key=lambda i: strip_accents(i.nom))
    csv = DataFrame([installation.to_dictionary()
                     for installation in installations]).to_csv(index=False)
    return Response(csv, mimetype='text/csv'), 200


# Modifier une installation
@app.route('/api/installations/modifier', methods=["PUT"])
def modify_glissade():
    # Recherche par nom
    nom = request.args.get('installation')
    if nom is not None and len(nom) != 0:
        try:
            db = get_db()
            installation = db.read_installation_nom(nom)
            informations = validate_schema(installation.type,
                                           request.get_json())
            installation.update_informations(informations)
            db.update_installation(installation)
            return jsonify(installation.to_dictionary()), 201
        except TypeError:
            # Retourner 404 si le nom de l'installation n'existe pas
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
    # Retourner 404 si le nom de l'installation n'existe pas
    erreur = "Aucune installation trouvée."
    return render_template("404.html", title="404", erreur=erreur), 404


# Supprimer une installation
@app.route('/api/installations/supprimer', methods=["DELETE"])
def delete_installation():
    # Recherche par nom
    nom = request.args.get('installation')
    if nom is not None and len(nom) != 0:
        try:
            db = get_db()
            installation = db.read_installation_nom(nom)
            db.delete_installation(installation)
            return jsonify("Succès"), 200
        except TypeError:
            # Retourner 404 si le nom de la installation n'existe pas
            erreur = "Aucune installation trouvée."
            return render_template("404.html", title="404", erreur=erreur), 404
    # Retourner 404 si le nom de la installation n'existe pas
    erreur = "Aucune installation trouvée."
    return render_template("404.html", title="404", erreur=erreur), 404
