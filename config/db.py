import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db_uri = os.getenv("DATABASEURI")

app = Flask('registro')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
mybd = SQLAlchemy(app)

import mysql.connector
import pandas as pd

def conexao(query):
    load_dotenv()

    db_name = os.getenv("DB")
    host = os.getenv("DBHOST")
    password = os.getenv("DBPASSWORD")

    conn = mysql.connector.connect(
        host = host,
        port = 3306,
        user = "root",
        password = password,
        db = db_name
    )

    dataframe = pd.read_sql_query(query, conn)

    conn.close()

    return dataframe