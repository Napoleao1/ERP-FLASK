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

---

## 🏆 Desafios para Prática Independente (Modo Hardcore)

Agora que você tem uma base de produção sólida, é hora de voar sozinho! Escolha um ou mais desafios abaixo para implementar e elevar suas habilidades para o nível Sênior.

### 🥉 Desafio 1: Dashboard de Métricas (Nível: Iniciante)

Atualmente, a rota `/` (raiz) redireciona diretamente para a lista de produtos.

* **Sua missão:** Crie uma nova rota no `web_bp` e um template `dashboard.html`. Esta página deve exibir 3 "Cards" mostrando a contagem total de Produtos, Categorias e Usuários cadastrados no banco de dados.

### 🥈 Desafio 2: Paginação de Dados (Nível: Intermediário)

Se a sua empresa cadastrar 5.000 produtos, a página web vai travar ao tentar listar todos de uma vez.

* **Sua missão:** Utilize o método `.paginate()` do Flask-SQLAlchemy nos *Controllers* em vez do `.all()`. Atualize o Jinja2 para exibir botões de "Próxima Página" e "Página Anterior" na listagem.

### 🥇 Desafio 3: Documentação de API com Swagger (Nível: Intermediário)

Os desenvolvedores front-end que forem consumir a sua API não sabem quais dados enviar.

* **Sua missão:** Instale a biblioteca `flasgger`. Crie arquivos `.yaml` descrevendo os endpoints dentro da pasta `/app/docs` e configure o Swagger na sua Application Factory. A documentação deve aparecer na rota `/apidocs/`.

### 💎 Desafio 4: Autenticação de Usuários (Nível: Avançado)

Atualmente, qualquer pessoa que acessar a URL do sistema consegue apagar e cadastrar produtos.

* **Sua missão:** Implemente um sistema de Login real. Crie uma tela de login e utilize a biblioteca `Flask-Login` ou manipulação de `session` do Flask para proteger os endpoints do Blueprint `web_bp`. Se o usuário não estiver logado, redirecione-o para a tela de login.

### 🚀 Desafio 5: Soft Delete (Nível: Expert)

Em sistemas reais de ERP, nunca excluímos registros financeiros ou cadastros com a instrução `DELETE` do banco (o que estamos fazendo no momento), pois isso quebra históricos.

* **Sua missão:** Adicione uma coluna booleana `ativo = db.Column(db.Boolean, default=True)` em todas as suas Models. Ao clicar no botão "Excluir", altere este valor para `False` em vez de deletar o registro fisicamente. Modifique todas as listagens para mostrar apenas itens onde `ativo == True`.

---

**Desenvolvido na Prática Guiada de ERP Completa - Arquitetura de Software em Flask.**
