from config.endpoint_base import *

@app.route("/registro", methods=["GET"])
def seleciona_registro():
    objects = Registro.query.all()
    result = [registro.to_json() for registro in objects]

    return setResponse(200, "registro", result)

@app.route("/registro/<id>", methods=["GET"])
def get_registro_by_id(id):
    objects = Registro.query.filter_by(id=id).first()

    if objects:
        result = objects.to_json()

        return setResponse(200, "registro", result)
    
    else:
        return setResponse(404, "registro", (), "Registro nao encontrado")
    
@app.route("/registro/<id>", methods=["GET"])
def delete_registro(id):
    registro = Registro.query.filter_by(id=id).first()

    if registro:
        try:
            mybd.session.delete(registro)
            mybd.session.commit()

            return setResponse(200, "registro", registro.to_json(), "Registro deletado com sucesso")
        except Exception as e:
            print("Erro", e)
            mybd.session.rollback()

            return setResponse(404, "registro", (), "Erro ao deletar")
    else:
        return setResponse(404, "registro", (), "Registro nao encontrado")
