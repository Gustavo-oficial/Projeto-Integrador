from datetime import datetime, timezone
from flask import jsonify, request
from config.db import *
from api.models.registro import Registro
from api.services.response_adapter import setResponse, to_json_sensor