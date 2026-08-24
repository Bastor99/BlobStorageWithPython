from flask import Flask, render_template, request, redirect, send_file
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from azure.data.tables import TableServiceClient
from datetime import datetime
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

table_client = table_service_client.get_table_client(
    table_name=table_name
)

try:
    table_client.create_table()
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


if __name__ == "__main__":
    app.run(debug=True)