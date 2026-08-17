# ☁️ Azure Blob Storage with Python

Aplicação web desenvolvida em **Python + Flask** para integração com o **Azure Blob Storage**.

O projeto permite realizar o **upload de imagens**, **listar os arquivos armazenados no Azure Blob Storage** e realizar o **download** dos arquivos através de uma interface web.

> Projeto desenvolvido como atividade acadêmica para demonstrar a utilização de serviços de armazenamento em nuvem com o Microsoft Azure.

---

## 📌 Funcionalidades

A aplicação possui as seguintes funcionalidades:

* 📤 Upload de imagens;
* 📋 Listagem dos arquivos armazenados no Azure Blob Storage;
* 📥 Download dos arquivos armazenados;
* ☁️ Integração com Azure Blob Storage através do SDK oficial;
* 🖥️ Interface web para gerenciamento dos arquivos;
* 🔐 Utilização de variáveis de ambiente para configuração das credenciais;
* 📁 Visualização dos arquivos através do Azure Storage Explorer.

---

## 🏗️ Arquitetura

O funcionamento da aplicação pode ser representado da seguinte forma:

```text
┌──────────────────────┐
│       Usuário        │
│     Navegador Web    │
└──────────┬───────────┘
           │
           │ HTTP
           ▼
┌──────────────────────┐
│    Flask / Python    │
│                      │
│  • Upload            │
│  • Listagem          │
│  • Download           │
└──────────┬───────────┘
           │
           │ Azure SDK
           ▼
┌──────────────────────┐
│   Azure Blob Storage │
│                      │
│  Container: imagens  │
│                      │
│  ├── imagem1.jpg     │
│  ├── imagem2.png     │
│  └── imagem3.jpeg    │
└──────────────────────┘
```

A aplicação funciona como uma camada intermediária entre o usuário e o Azure Blob Storage. O usuário interage com a interface web, enquanto o Flask realiza as operações de armazenamento utilizando o SDK do Azure.

---

## 🛠️ Tecnologias utilizadas

### Backend

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Azure Storage Blob SDK for Python](https://pypi.org/project/azure-storage-blob/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

### Frontend

* HTML5
* CSS3

### Cloud

* Microsoft Azure
* Azure Blob Storage
* Azure Storage Explorer

---

## 📁 Estrutura do projeto

```text
BlobStorageWithPython/
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

### Descrição dos arquivos

| Arquivo                | Descrição                                             |
| ---------------------- | ----------------------------------------------------- |
| `app.py`               | Aplicação Flask e integração com o Azure Blob Storage |
| `templates/index.html` | Interface HTML da aplicação                           |
| `static/style.css`     | Estilos da interface                                  |
| `.env.example`         | Modelo das variáveis de ambiente necessárias          |
| `.gitignore`           | Arquivos que não devem ser enviados ao Git            |
| `requirements.txt`     | Dependências Python utilizadas no projeto             |
| `README.md`            | Documentação do projeto                               |

---

# ☁️ Configuração do Azure

Para executar o projeto, é necessário possuir um **Storage Account** no Microsoft Azure.

Dentro do Storage Account, deve ser criado um **Blob Container** para armazenar as imagens.

Neste projeto, o container utilizado como exemplo é:

```text
imagens
```

## 1. Criar o Storage Account

No [Portal do Microsoft Azure](https://portal.azure.com/):

1. Procure por **Storage accounts**;
2. Clique em **Create**;
3. Selecione ou crie um **Resource Group**;
4. Defina um nome único para o Storage Account;
5. Selecione uma região disponível;
6. Utilize o desempenho **Standard**;
7. Para um projeto acadêmico, pode ser utilizada a redundância **LRS**;
8. Finalize a criação do recurso.

---

## 2. Criar o container

Após criar o Storage Account, acesse:

```text
Storage Account
    ↓
Data storage
    ↓
Containers
    ↓
+ Container
```

Crie um container chamado:

```text
imagens
```

O nome do container pode ser alterado, desde que o mesmo nome seja configurado na variável `AZURE_CONTAINER_NAME`.

---

# 🔐 Configuração das credenciais

A aplicação utiliza uma **Connection String** para se conectar ao Azure Blob Storage.

Por motivos de segurança, a Connection String real **não é armazenada no repositório**.

O projeto possui um arquivo:

```text
.env.example
```

Esse arquivo serve apenas como modelo para indicar quais variáveis precisam ser configuradas.

## 1. Criar o arquivo `.env`

Faça uma cópia do `.env.example`.

### Windows

No PowerShell:

```powershell
Copy-Item .env.example .env
```

Ou no CMD:

```cmd
copy .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

---

## 2. Configurar o `.env`

Abra o arquivo `.env` e preencha as variáveis:

```env
AZURE_STORAGE_CONNECTION_STRING="SUA_CONNECTION_STRING"
AZURE_CONTAINER_NAME="imagens"
```

A `AZURE_STORAGE_CONNECTION_STRING` pode ser encontrada no Azure Portal em:

```text
Storage Account
    ↓
Security + networking
    ↓
Access keys
    ↓
Connection string
```

A Connection String terá uma estrutura semelhante a:

```text
DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
```

> ⚠️ **Nunca publique sua Connection String no GitHub.** Ela contém credenciais que podem permitir acesso ao seu Storage Account.

O arquivo `.env` está incluído no `.gitignore` e, portanto, não deve ser enviado para o repositório.

---

# 📦 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/Bastor99/BlobStorageWithPython.git
```

Entre na pasta:

```bash
cd BlobStorageWithPython
```

---

## 2. Criar um ambiente virtual

No Windows:

```powershell
python -m venv venv
```

Ative o ambiente virtual:

```powershell
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```

As principais dependências utilizadas são:

```text
Flask
azure-storage-blob
python-dotenv
```

---

# ▶️ Executando a aplicação

Depois de configurar o `.env` e instalar as dependências, execute:

```bash
python app.py
```

A aplicação será iniciada localmente.

Acesse no navegador:

```text
http://127.0.0.1:5000
```

ou:

```text
http://localhost:5000
```

---

# 📤 Upload de imagens

Na página inicial existe uma área para selecionar uma imagem.

O fluxo do upload ocorre da seguinte maneira:

```text
Usuário seleciona uma imagem
          ↓
Formulário envia o arquivo
          ↓
Flask recebe o arquivo
          ↓
Azure Blob Storage SDK
          ↓
Container "imagens"
          ↓
Imagem armazenada no Azure
```

Depois do upload, o arquivo passa a aparecer na lista de imagens armazenadas.

---

# 📋 Listagem dos arquivos

A aplicação consulta o container do Azure Blob Storage e obtém os arquivos armazenados.

Esses arquivos são apresentados na interface web.

Exemplo:

```text
Imagens armazenadas

🖼️ cachorro.jpg       [Download]
🖼️ paisagem.png       [Download]
🖼️ foto.jpeg          [Download]
```

A aplicação também apresenta a quantidade de arquivos armazenados.

---

# 📥 Download

Cada arquivo listado possui um botão **Download**.

Quando o usuário seleciona essa opção:

```text
Usuário
   ↓
Clica em "Download"
   ↓
Flask
   ↓
Azure Blob Storage
   ↓
Arquivo recuperado
   ↓
Navegador
   ↓
Download
```

O arquivo é recuperado do Blob Storage e enviado ao navegador para ser baixado.

---

# 🗂️ Azure Storage Explorer

O **Azure Storage Explorer** pode ser utilizado para visualizar os arquivos armazenados no Azure.

Após conectar sua conta Azure, navegue até:

```text
Storage Accounts
    ↓
Seu Storage Account
    ↓
Blob Containers
    ↓
imagens
```

Os arquivos enviados pela aplicação estarão disponíveis dentro do container.

Por exemplo:

```text
imagens
│
├── cachorro.jpg
├── gato.jpg
└── paisagem.png
```

O Storage Explorer é especialmente útil para verificar se os arquivos enviados pela aplicação realmente foram armazenados no Azure Blob Storage.

Mais informações:

[Azure Storage Explorer](https://azure.microsoft.com/products/storage/storage-explorer/)

---

# 🔄 Fluxo das principais operações

## Upload

```text
┌───────────────┐
│    Usuário    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Seleciona     │
│ uma imagem    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Flask         │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Azure Blob    │
│ Storage       │
└───────────────┘
```

## Listagem

```text
Flask
  │
  ▼
Azure Blob Storage
  │
  ▼
Lista de Blobs
  │
  ▼
Interface Web
```

## Download

```text
Usuário
  │
  ▼
Download
  │
  ▼
Flask
  │
  ▼
Azure Blob Storage
  │
  ▼
Arquivo
  │
  ▼
Navegador
```

---

# 🔒 Segurança

As credenciais utilizadas para acessar o Azure não devem ser armazenadas diretamente no código-fonte.

Por isso, o projeto utiliza variáveis de ambiente:

```env
AZURE_STORAGE_CONNECTION_STRING="..."
AZURE_CONTAINER_NAME="imagens"
```

O arquivo:

```text
.env
```

não deve ser enviado ao GitHub.

O arquivo:

```text
.env.example
```

é disponibilizado no repositório apenas como um modelo de configuração e **não deve conter credenciais reais**.

Para aplicações em produção, recomenda-se utilizar mecanismos mais seguros para gerenciamento de credenciais, como:

* Azure Key Vault;
* Managed Identity;
* Microsoft Entra ID;
* Azure RBAC.

---

# 🎓 Contexto acadêmico

O projeto foi desenvolvido para demonstrar, de forma prática, a utilização de um serviço de **Cloud Computing** para armazenamento de arquivos.

O **Azure Blob Storage** permite que a aplicação utilize um armazenamento disponibilizado na nuvem, evitando a necessidade de manter os arquivos exclusivamente no sistema de arquivos local da máquina.

A atividade demonstra principalmente os conceitos de:

* Cloud Computing;
* Object Storage;
* Azure Blob Storage;
* Containers;
* Upload e download de arquivos;
* Integração entre aplicações e serviços de nuvem;
* Gerenciamento de credenciais através de variáveis de ambiente.

---

# 👨‍💻 Autor

**Vitor Bastos**

GitHub: [@Bastor99](https://github.com/Bastor99)

Repositório: [BlobStorageWithPython](https://github.com/Bastor99/BlobStorageWithPython)

---

## 📚 Referências

* [Microsoft Azure](https://azure.microsoft.com/)
* [Azure Blob Storage](https://azure.microsoft.com/products/storage/blobs/)
* [Azure Storage Explorer](https://azure.microsoft.com/products/storage/storage-explorer/)
* [Azure Storage Blob SDK for Python](https://pypi.org/project/azure-storage-blob/)
* [Flask](https://flask.palletsprojects.com/)
* [Python](https://www.python.org/)
