# 📌 API de Gerenciamento Escolar

Este é um projeto Flask que fornece uma API RESTful para gerenciar alunos e turmas. A API permite realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) em ambas as entidades.

## 🚀 Tecnologias Utilizadas

- Python 3
- Flask
- Requests (para testes)

## 📂 Estrutura do Projeto

```
📦 projetoFlask
├── app.py              # Configuração principal do Flask
├── BD.py               # Definição dos modelos de banco de dados
├── professores.py      # Definição das rotas da API dos professores
├── alunos.py           # Definição das rotas da API dos alunos
├── Turma.py            # Definição das rotas da API das turmas
├── testeProfessores.py # Testes dos professores
├── testeAlunos.py      # Testes dos Alunos
├── testeTurma.py       # Testes das turmas
└── README.md           # Documentação
```

## 🔧 Instalação e Configuração

1. **Clone este repositório:**

   ```sh
   git clone https://github.com/Alan-294/apis.git
   ```

2. **Instale o Flask e o requiriments:**

   ```sh
   pip install Flask
   pip install requests
   ```

3. **Inicie o servidor Flask:**
   ```sh
   python app.py
   ```
   O servidor estará rodando em `http://127.0.0.1:5000/`

## 📌 Rotas da API

### 📚 Alunos

| Método   | Rota               | Descrição                |
| -------- | ------------------ | ------------------------ |
| `GET`    | `/api/alunos`      | Retorna todos os alunos  |
| `GET`    | `/api/alunos/<id>` | Retorna um aluno pelo ID |
| `POST`   | `/api/alunos`      | Adiciona um novo aluno   |
| `PUT`    | `/api/alunos/<id>` | Atualiza um aluno        |
| `DELETE` | `/api/alunos/<id>` | Exclui um aluno          |

{

Para os métodos POST e PUT do aluno, enviar objetos json como o abaixo:

```sh
{
   "nome": "Jonas Padro",
   "data_nascimento": "2008-01-01",
   "nota_primeiro_semestre": 9.5,
   "nota_segundo_semestre": 8.0,
   "turma_id": 6
}
```

### 🎓 Turmas

| Método   | Rota              | Descrição                 |
| -------- | ----------------- | ------------------------- |
| `GET`    | `/api/turma`      | Retorna todas as turmas   |
| `GET`    | `/api/turma/<id>` | Retorna uma turma pelo ID |
| `POST`   | `/api/turma/`     | Adiciona uma nova turma   |
| `PUT`    | `/api/turma/<id>` | Atualiza uma turma        |
| `DELETE` | `/api/turma/<id>` | Exclui uma turma          |

### 🎓 Professores

| Método   | Rota               | Descrição                         |
| -------- | ------------------ | --------------------------------- |
| `GET`    | `/api/professores`      | Retorna todos os professores      |
| `GET`    | `/api/professores/<id>` | Retorna um professor pelo ID      |
| `POST`   | `/api/professores`      | Adiciona um novo professor        |
| `PUT`    | `/api/professores/<id>` | Atualiza os dados de um professor |
| `DELETE` | `/api/professores/<id>` | Exclui um professor               |

## ✅ Testando a API

Para rodar os testes automatizados, execute:

```sh
python projetoFlask/testeAlunos.py
python projetoFlask/testeTurma.py
python projetoFlask/testeProfessores.py
```
