from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
api = Api(app)
f = open("dados.json")
dados = json.load(f)

parser = reqparse.RequestParser(bundle_errors=True)

SWAGGER_URL = '/moz-cep-api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/documentacao.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Moz-Cep-API"
    }
)

app.register_blueprint(swaggerui_blueprint)

@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'erro': 'Incompreensivel'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'erro': 'Nao autorizado'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'erro': 'Nao foi achado'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'erro': 'Erro do servidor'}), 500)

@app.route("/")
def welcome_message():
    msg = {
        "buscar todos": {"Url": "/moz-cep-api/todos/"},
        "buscar por distrito": {"Url": "/moz-cep-api/distrito"},
        "buscar por cidade": {"Url": "/moz-cep-api/cidade/nome_da_cidade"},
        "buscar por provincia": {"Url": "/moz-cep-api/provincia/nome_da_provincia"},
        "buscar por posto administrativo": {"Url": "/moz-cep-api/posto-admin/nome_do_posto_administrativo"}
    }
    return jsonify(msg)


def abort_if_name_doesnt_exist(searched_key):
    if searched_key not in dados:
        abort(404, message=f"O nome {searched_key} nao existe")


class Get_by_name(Resource):
    def get(self, searched_key):
        t = []
        for key, value in enumerate(dados):
            try:
                if searched_key == dados[key]["bairro"]:
                    j = {"cidade": dados[key]["cidade"],
                         "distrito": dados[key]["distrito"],
                         "bairro": dados[key]["bairro"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
            except:
                pass
        if len(t) == 0:
            t.append({"mensagem": f"nenhum registro referentes ao bairro de {searched_key} foi achado"})

        return jsonify(t)


class Get_by_city(Resource):
    def get(self, searched_key):
        t = []
        for key, value in enumerate(dados):
            try:
                if searched_key == dados[key]["cidade"]:
                    j = {"cidade": dados[key]["cidade"],
                         "distrito": dados[key]["distrito"],
                         "bairro": dados[key]["bairro"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
            except:
                pass
        if len(t) == 0:
            t.append({"mensagem": f"nenhum registro referente a cidade de {searched_key} foi achado"})
        return jsonify(t)


class Get_by_province(Resource):
    def get(self, searched_key):
        t = []
        for key, value in enumerate(dados):
            try:
                if searched_key == dados[key]["provincia"]:
                    j = {"provincia": dados[key]["provincia"],
                         "distrito": dados[key]["distrito"],
                         "posto administrativo": dados[key]["posto administrativo"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
            except:
                pass
        if len(t) == 0:
            t.append({"mensagem": f"nenhum registro referente a provincia de {searched_key} foi achado"})
        return jsonify(t)


class Get_by_administrative_post(Resource):
    def get(self, searched_key):
        t = []
        for key, value in enumerate(dados):
            try:
                if searched_key == dados[key]["posto administrativo"]:
                    j = {"provincia": dados[key]["provincia"],
                         "distrito": dados[key]["distrito"],
                         "posto administrativo": dados[key]["posto administrativo"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
            except:
                pass
        if len(t) == 0:
            t.append({"mensagem": f"nenhum registro referente ao posto administrativo de {searched_key} foi achado"})
        return jsonify(t)


class Get_all(Resource):
    def get(self):
        return jsonify(dados)


class Get_by_name_error(Resource):
    def get(self):
        msg = {"msg": "deve incluir um parametro na URL"}
        return jsonify(msg)

class Get_by_city_error(Resource):
    def get(self):
        msg = {"msg": "deve incluir um parametro na URL"}
        return jsonify(msg)

class Get_by_province_error(Resource):
    def get(self):
        msg = {"msg": "deve incluir um parametro na URL"}
        return jsonify(msg)

class Get_by_administrative_post_error(Resource):
    def get(self):
        msg = {"msg": "deve incluir um parametro na URL"}
        return jsonify(msg)


api.add_resource(Get_by_name, "/moz-cep-api/bairro/<searched_key>")
api.add_resource(Get_by_city, "/moz-cep-api/cidade/<searched_key>")
api.add_resource(Get_by_province, "/moz-cep-api/provincia/<searched_key>")
api.add_resource(Get_by_administrative_post, "/moz-cep-api/posto-admin/<searched_key>")
api.add_resource(Get_all, "/moz-cep-api/todos/")
api.add_resource(Get_by_name_error, "/moz-cep-api/distrito/")
api.add_resource(Get_by_city_error, "/moz-cep-api/cidade/")
api.add_resource(Get_by_province_error, "/moz-cep-api/")
api.add_resource(Get_by_administrative_post_error, "/moz-cep-api/posto-admin")
if __name__ == "__main__":
    app.run()
