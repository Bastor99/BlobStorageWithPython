from flask import Flask, render_template, request, redirect, send_file
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import io

load_dotenv()

app = Flask(__name__)

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)


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

    return redirect("/")


@app.route("/download/<nome>")
def download(nome):
    blob_client = container_client.get_blob_client(nome)

    blob_data = blob_client.download_blob().readall()

    return send_file(
        io.BytesIO(blob_data),
        download_name=nome,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)