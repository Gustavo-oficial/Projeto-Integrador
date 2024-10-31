from config.endpoint_base import *
from api.endpoints.sensor import app, mybd

mqtt_dados = {}

@app.route("/dados", methods=["GET"])
def get_data(id):
    registro = Registro.query.filter_by(id=id).first()
    
    return jsonify(mqtt_dados)


@app.route("/dados", methods=["POST"])
def create_data():
    try:
        data = request.get_json()

        if not data:
            return setResponse(400, "data", (), "Nenhum dado fornecido")


        print(f"Dados recebidos: {data}")
        temperatura = data.get("temperatura")
        pressao = data.get("pressao")
        altitude = data.get("altitude")
        umidade = data.get("umidade")
        co2 = data.get("co2")
        poeira = data.get("poeira")
        timestamp_unix = data.get("tempo_registro")

        try:
            tempo_oficial = datetime.fromtimestamp(int(timestamp_unix), tz=timezone.utc)
        except Exception as e:
            print("Erro", e)
            return setResponse(400, "error", (), "Timestamp invalido")

        novo_registro = Registro(
            temperatura=temperatura,
            pressao=pressao,
            altitude=altitude,
            umidade=umidade,
            co2=co2,
            poeira=poeira,
            tempo_registro=tempo_oficial
        )

        mybd.session.add(novo_registro)
        print("Adicionando um novo registro")
        
        mybd.session.commit()
        print("Dados inseridos no banco de dados com sucesso")
        
        return setResponse(201, "data", novo_registro, "Dados recebidos com sucesso")
    
    except Exception as e:
        print("Erro", e)
        mybd.session.rollback()

        return setResponse(500, "data", (), "Falha ao processar os dados")