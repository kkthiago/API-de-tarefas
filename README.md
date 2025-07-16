# 📋 API de Tarefas com FastAPI + Docker + Poetry

Bem-vindo à **API de Tarefas**! 🚀  
Este projeto foi desenvolvido com o objetivo de fornecer uma API REST robusta e segura para o gerenciamento de tarefas.  
Você poderá **adicionar**, **listar**, **atualizar** e **deletar** tarefas, além de filtrar por páginas. Tudo isso com autenticação básica.

---

## 🧠 Tecnologias Utilizadas

- 🐍 **Python 3.11**
- ⚡ **FastAPI** — Web Framework assíncrono
- 🛢️ **SQLite** — Banco de dados leve e prático
- 🔐 **HTTP Basic Auth** — Autenticação simples e segura
- 📦 **Poetry** — Gerenciador de dependências moderno
- 🐳 **Docker + Docker Compose** — Ambientes reprodutíveis com isolamento
- 🛠️ **SQLAlchemy** — ORM para manipulação do banco de dados

---

## 📁 Estrutura do Projeto

```

tarefas-api/
│
├── app/
│   └── main.py               # Código principal da API
│
├── Dockerfile                # Imagem da aplicação
├── docker-compose.yml        # Orquestração com Docker Compose
├── pyproject.toml            # Dependências do projeto via Poetry
├── poetry.lock               # Versões fixas das dependências
├── .env                      # Variáveis de ambiente
└── README.md                 # Documentação do projeto

````

---

## 🚀 Como Executar a Aplicação

### 1️⃣ Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2️⃣ Clone o Repositório

```bash
git clone https://github.com/seuusuario/tarefas-api.git
cd tarefas-api
````

### 3️⃣ Configure o arquivo `.env`

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
meu_user=admin
meu_login=123456
DATABASE_URL=sqlite:///./tarefas.db
```

🔐 **Importante:** esses dados são utilizados para autenticação básica e conexão com o banco.

### 4️⃣ Rode o Docker Compose

```bash
docker-compose up --build -d
```

O servidor FastAPI será iniciado em:

> 📡 [http://localhost:8000](http://localhost:8000)

Documentação automática da API:

> 📄 [http://localhost:8000/docs](http://localhost:8000/docs)
> 🔍 [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5️⃣ Parar a aplicação

```bash
docker-compose down
```

---

## 🧪 Endpoints Disponíveis

🔐 **Todos os endpoints exigem autenticação básica!**

| Método | Rota                      | Descrição                     |
| ------ | ------------------------- | ----------------------------- |
| GET    | `/tarefas?page=1&limit=5` | Lista tarefas paginadas       |
| POST   | `/adiciona`               | Adiciona uma nova tarefa      |
| PUT    | `/atualizar/{id_tarefa}`  | Atualiza uma tarefa existente |
| DELETE | `/deletar/{id_tarefa}`    | Remove uma tarefa do sistema  |

---

## 📤 Exemplo de Payload para Adicionar Tarefa

```json
{
  "id_tarefa": 1,
  "nome_tarefa": "Estudar FastAPI",
  "descricao_tarefa": "Ler a documentação e fazer testes.",
  "concluso_tarefa": false
}
```

---

## 🔐 Autenticação Básica

Todos os endpoints exigem autenticação via HTTP Basic.

Exemplo com `curl`:

```bash
curl -u admin:123456 http://localhost:8000/tarefas?page=1&limit=5
```
## 👨‍💻 Autor

Desenvolvido por **Thiago Alves Soares**
📧 [thiagobrsoares3011@gmail.com](mailto:thiagobrsoares3011@gmail.com)

Sinta-se à vontade para contribuir, dar um ⭐ no repositório, ou abrir uma *issue* com dúvidas e sugestões!

---

## 📜 Licença

Distribuído sob a licença MIT.
Veja `LICENSE` para mais informações.

```

---

Esse README está:

- **Responsivo e visualmente amigável**
- **Com exemplos reais e comandos claros**
- **Documentado para rodar localmente ou em servidores**
- **Pronto para GitHub, GitLab ou qualquer repositório remoto**

