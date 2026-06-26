# 🚀 ERP Modular Avançado - Flask Full Stack

Este é o projeto definitivo da nossa **Prática Guiada de ERP Completa**. Ele demonstra como fazer uma **Arquitetura de Produção Híbrida e Modular**, pronta para escalar.

O sistema atua em duas frentes:

1. **Frontend Interno (Web):** Painel administrativo gerado no servidor usando Jinja2 e Bootstrap 5 para gestão (CRUD completo) de Usuários, Categorias e Produtos.
2. **Backend Externo (API):** Endpoints RESTful em JSON, protegidos contra CORS, para consumo por aplicações externas (React, Vue, Mobile).

---

## 🏗️ Arquitetura do Projeto (Padrão MVC + Application Factory)

A estrutura de diretórios adota a separação de responsabilidades para evitar problemas como *Circular Imports* e código macarrônico:

```text
/sistema_erp_avancado
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente (não versionado)
├── run.py                # Ponto de inicialização do servidor
└── app/          
    ├── __init__.py       # Application Factory (cria o app)
    ├── extensions.py     # Inicialização de extensões (SQLAlchemy, CORS)
    ├── models/           # Entidades do Banco de Dados (Tabelas)
    ├── controllers/      # Regras de Negócio e Validações
    ├── rotas/            # Blueprints (api_bp.py e web_bp.py)
    └── templates/        # Telas do sistema usando Herança (Jinja2)
```

---

## ⚙️ Como Executar o Projeto Localmente

### 1. Pré-requisitos

* Python 3.10+ instalado.
* Git para clonar o repositório.

### 2. Configuração do Ambiente Virtual

Crie e ative um ambiente virtual para isolar as dependências:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 4. Configuração das Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves:

```env
FLASK_DEBUG=True
DATABASE_URL=sqlite:///sistema_erp.db
SECRET_KEY=sua_chave_super_secreta_aqui
CORS_ORIGINS=http://localhost:3000,[http://127.0.0.1:8080](http://127.0.0.1:8080)
```

### 5. Rodando a Aplicação

Inicie o servidor Flask:

```bash
python run.py
```

* **Painel Web (HTML):** Acesse `http://localhost:5000/`
* **API de Produtos (JSON):** Acesse `http://localhost:5000/api/produtos`
