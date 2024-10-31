import json
from flask import Response

def setResponse(status, keyContent, content, msg=False):
    body={}
    body[keyContent] = content

    if msg:
        body["mensagem"] = msg

    return Response(json.dumps(body), status=status, mimeType="application/json")

def to_json_sensor(self):
    return {
        "id": self.id,
        "temperatura": float(self.temperatura),
        "pressao": float(self.pressao),
        "altitude": float(self.altitude),
        "umidade": float(self.umidade),
        "co2": float(self.co2),
        "poeira": float(self.poeira),
        "tempo_registro": self.tempo_registro.strftime("%Y-%m-%d %H:%S") if self.tempo_registro else None
    }
