from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)
f = open("dados.json")
dados = json.load(f)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('searched_key', type=int, required=True)


@app.route("/")
def welcome_message():
    msg = {
        "buscar por distrito": {"Url": "/moz-cep-api/distrito"},
        "buscar por cidade": {"Url": "/moz-cep-api/cidade/nome_da_cidade"},
        "buscar por provincia": {"Url": "/moz-cep-api/provincia/nome_da_provincia"},
        "buscar todos": {"Url": "/moz-cep-api/todos/"}
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
                if searched_key == dados[key]["posto administrativo"]:
                    j = {"provincia": dados[key]["provincia"],
                         "distrito": dados[key]["distrito"],
                         "posto administrativo": dados[key]["posto administrativo"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
        if len(t) == 0:
            t.append({"mensagem": "nenhum registro foi achado"})

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
            t.append({"mensagem": f"nenhum registro referentes a cidade de {searched_key} foi achado"})
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
            t.append({"mensagem": f"nenhum registro referentes a provincia de {searched_key} foi achado"})
        return jsonify(t)


class Get_by_administrative_post(Resource):
    def get(self, searched_key):
        t = []
        for key, value in enumerate(dados):
            try:
                if searched_key == dados[key]["posto administrativo"]:
                    j = {"cidade": dados[key]["cidade"],
                         "distrito": dados[key]["distrito"],
                         "bairro": dados[key]["bairro"],
                         "cep": dados[key]["cep"]
                         }
                    t.append(j)
            except:
                pass
        if len(t) == 0:
            t.append({"mensagem": f"nenhum registro referentes ao posto administrativo de {searched_key} foi achado"})
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


api.add_resource(Get_by_name, "/moz-cep-api/distrito/<searched_key>")
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
