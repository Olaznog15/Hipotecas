# -*- coding: utf-8 -*-
from flask import Blueprint, Flask, render_template
from Controllers import SimulacionController, ClienteController
from flask_restx import Api

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

apiBlPrint = Blueprint("api",__name__)
api = Api(apiBlPrint,
          title="Hipotecas API",
          description="API simple con python para dar de alta y modificar clientes y calcular las cuotas de su hipoteca",
          version ="1.0",
          doc="/swagger/",
          validate =True)

app.register_blueprint(apiBlPrint)
api.add_namespace(ClienteController.ClienteCtrl)
api.add_namespace(SimulacionController.SimulacionCtrl)



import os
os.environ['SERVER_HOST'] = 'localhost'  # Establecer el host
os.environ['SERVER_PORT'] = '8086'  # Establecer el puerto

HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
PORT = int(os.environ.get('SERVER_PORT', '8086'))

app.run(host=HOST, port=PORT)
