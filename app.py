from flask import Flask, render_template, request, redirect, send_file
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from azure.data.tables import TableServiceClient
from datetime import datetime, timedelta
import uuid
import os
import io

load_dotenv()

app = Flask(__name__)

# =========================
# Configurações do Azure
# =========================

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
table_name = os.getenv("AZURE_TABLE_NAME")
acessos_table_name = os.getenv("AZURE_ACCESS_TABLE_NAME")
acessos_date_table_name = os.getenv("AZURE_ACCESS_DATE_TABLE_NAME")

# =========================
# Conexão com Blob Storage
# =========================

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)

# =========================
# Conexão com Table Storage
# =========================

table_service_client = TableServiceClient.from_connection_string(
    connection_string
)

# =========================
# Tabela de Logs
# =========================

table_client = table_service_client.get_table_client(
    table_name=table_name
)

try:
    table_client.create_table()
except:
    pass


# =========================
# Tabela de Acessos Físicos
# =========================

acessos_table_client = table_service_client.get_table_client(
    table_name=acessos_table_name
)

try:
    acessos_table_client.create_table()
except:
    pass


# =========================
# Tabela de Acessos por Data
# =========================

acessos_date_table_client = table_service_client.get_table_client(
    table_name=acessos_date_table_name
)

try:
    acessos_date_table_client.create_table()
except:
    pass

# =========================
# Registro de logs 
# =========================

def registrar_log(operacao, arquivo):
    log = {
        "PartitionKey": "arquivos",
        "RowKey": str(uuid.uuid4()),
        "Operacao": operacao,
        "Arquivo": arquivo,
        "DataHora": datetime.now().isoformat()
    }

    table_client.create_entity(entity=log)

# =========================
# Registro de acessos físicos 
# =========================

def registrar_acesso(id_usuario, id_local):

    agora = datetime.now()

    timestamp = int(datetime.now().timestamp() * 1000)

    inverted_timestamp = 9999999999999 - timestamp

     # =========================
    # Registro por usuário
    # =========================

    acesso_usuario = {
        "PartitionKey": id_usuario,
        "RowKey": f"{inverted_timestamp}_{id_local}",
        "IdUsuario": id_usuario,
        "IdLocal": id_local,
        "DataHora": agora.isoformat()
    }

    acessos_table_client.create_entity(
        entity=acesso_usuario
    )

    # =========================
    # Registro por data
    # =========================

    data = agora.strftime("%Y-%m-%d")

    acesso_data = {
        "PartitionKey": data,
        "RowKey": f"{timestamp}_{id_usuario}_{id_local}",
        "IdUsuario": id_usuario,
        "IdLocal": id_local,
        "DataHora": agora.isoformat()
    }

    acessos_date_table_client.create_entity(
        entity=acesso_data
    )
# =========================
# Consulta dos Acessos nos últimos 30 dias por usuário
# =========================

def consultar_acessos_usuario(id_usuario):
    agora = int(datetime.now().timestamp() * 1000)

    trinta_dias_atras = int(
        (datetime.now() - timedelta(days=30)).timestamp() * 1000
    )

    inverted_agora = 9999999999999 - agora

    inverted_trinta_dias = 9999999999999 - trinta_dias_atras

    rowkey_inicio = f"{inverted_agora}_"

    rowkey_fim = f"{inverted_trinta_dias}_\uffff"

    filtro = (
        f"PartitionKey eq '{id_usuario}' "
        f"and RowKey ge '{rowkey_inicio}' "
        f"and RowKey lt '{rowkey_fim}'"
    )

    return list(
        acessos_table_client.query_entities(
            query_filter=filtro
        )
    )

# =========================
# Consulta dos Acessos de Hoje
# =========================
def consultar_acessos_hoje():

    hoje = datetime.now().strftime("%Y-%m-%d")

    filtro = f"PartitionKey eq '{hoje}'"

    return list(
        acessos_date_table_client.query_entities(
            query_filter=filtro
        )
    )

# =========================
# Rotas
# =========================

@app.route("/")
def index():
    blobs = container_client.list_blobs()

    arquivos = [blob.name for blob in blobs]

    return render_template(
        "index.html",
        arquivos=arquivos
    )


@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files["arquivo"]

    if arquivo:
        blob_client = container_client.get_blob_client(
            arquivo.filename
        )

        blob_client.upload_blob(
            arquivo,
            overwrite=True
        )

        registrar_log(
            "Upload", 
            arquivo.filename
        )

    return redirect("/")


@app.route("/download/<nome>")
def download(nome):
    blob_client = container_client.get_blob_client(nome)

    blob_data = blob_client.download_blob().readall()

    registrar_log(
        "Download",
        nome
    )

    return send_file(
        io.BytesIO(blob_data),
        download_name=nome,
        as_attachment=True
    )


# =========================
# Registrar acesso físico
# =========================

@app.route("/acesso", methods=["POST"])
def acesso():

    id_usuario = request.form["id_usuario"]

    id_local = request.form["id_local"]

    registrar_acesso(
        id_usuario,
        id_local
    )

    return redirect("/")


# =========================
# Consultar acessos de usuário
# =========================

@app.route("/acessos/<id_usuario>")
def acessos_usuario(id_usuario):

    acessos = consultar_acessos_usuario(
        id_usuario
    )

    return render_template(
        "acessos.html",
        acessos=acessos,
        id_usuario=id_usuario
    )


# =========================
# Consultar acessos de hoje
# =========================

@app.route("/acessos-hoje")
def acessos_hoje():

    acessos = consultar_acessos_hoje()

    hoje = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        "acessos_hoje.html",
        acessos=acessos,
        hoje=hoje
    )

if __name__ == "__main__":
    app.run(debug=True)