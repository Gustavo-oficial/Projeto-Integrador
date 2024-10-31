import json
import os
from config.endpoint_base import *
from api.endpoints.sensor import app, mybd

def connection_sensor(cliente, userdata, flags, rc):
    load_dotenv()

    subscribe_path = os.getenv("SUBSCRIBEPATH")
    cliente.subscribe(subscribe_path)

def msg_sensor(client, userdata, msg):
    global mqtt_dados
    valor = msg.payload.decode('utf-8')
    mqtt_dados = json.loads(valor)
    

    print(f'Mensagem Recebida: {mqtt_dados}')

    with app.app_context():
        try:
            temperatura = mqtt_dados.get('temperature')
            pressao = mqtt_dados.get('pressure')
            altitude = mqtt_dados.get('altitude')
            umidade = mqtt_dados.get('humidity')
            co2 = mqtt_dados.get('co2')
            poeira  = 0
            tempo_registro = mqtt_dados.get('timestamp')
        
            if tempo_registro is None:
                print('Timestamp não encontrado')
                return
            
            try:
                tempo_oficial = datetime.fromtimestamp(int
                (tempo_registro), tz=timezone.utc)


            except Exception as ex:
                print(f'Erro ao converter timestamp: {str(ex)}')
                return

            novos_dados = Registro(
                temperatura = temperatura,
                pressao = pressao,
                altitude = altitude,
                umidade = umidade,
                co2 = co2,
                poeira = poeira,
                tempo_registro = tempo_registro
            )

            mybd.session.add(novos_dados)
            mybd.session.commit()
            print('Dados foram inseridos com sucesso no banco de dados!')

        except Exception as e:
            print(f'Erro ao processar os dados do MQTT {str(e)}')
            mybd.session.rollback()