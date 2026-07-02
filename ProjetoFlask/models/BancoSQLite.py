import os
import sqlite3

from config import banco_de_dados


def inicializar_banco():
    db_dir = os.path.dirname(os.path.abspath(banco_de_dados))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conexao = sqlite3.connect(banco_de_dados)
    conexao.execute("PRAGMA foreign_keys = ON")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT NOT NULL,
            professor_id INTEGER NOT NULL,
            ativo BOOLEAN NOT NULL,
            FOREIGN KEY (professor_id) REFERENCES professores (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            nota_primeiro_semestre REAL,
            nota_segundo_semestre REAL,
            media_final REAL,
            FOREIGN KEY (turma_id) REFERENCES turmas (id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM professores")
    if cursor.fetchone()[0] == 0:
        professores = [
            ("Joao Silva", "Matematica"),
            ("Maria Oliveira", "Historia"),
            ("Carlos Souza", "Fisica"),
            ("Ana Lima", "Quimica"),
            ("Fernanda Costa", "Biologia"),
        ]
        cursor.executemany(
            "INSERT INTO professores (nome, disciplina) VALUES (?, ?)",
            professores,
        )

    cursor.execute("SELECT id FROM professores ORDER BY id")
    professores_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) FROM turmas")
    if cursor.fetchone()[0] == 0 and len(professores_ids) >= 5:
        turmas = [
            ("Turma A", "Manha", professores_ids[0], True),
            ("Turma B", "Tarde", professores_ids[1], True),
            ("Turma C", "Noite", professores_ids[2], True),
            ("Turma D", "Manha", professores_ids[3], True),
            ("Turma E", "Tarde", professores_ids[4], True),
        ]
        cursor.executemany(
            "INSERT INTO turmas (nome, turno, professor_id, ativo) VALUES (?, ?, ?, ?)",
            turmas,
        )

    cursor.execute("SELECT COUNT(*) FROM alunos")
    if cursor.fetchone()[0] == 0:
        alunos = [
            ("Pedro Santos", 15, 1, 8.0, 7.5, 7.75),
            ("Julia Almeida", 16, 2, 9.0, 8.5, 8.75),
            ("Lucas Pereira", 14, 3, 7.0, 6.5, 6.75),
            ("Mariana Rocha", 17, 4, 10.0, 9.5, 9.75),
            ("Gabriel Nunes", 15, 5, 6.0, 5.5, 5.75),
        ]
        cursor.executemany(
            """
            INSERT INTO alunos
                (nome, idade, turma_id, nota_primeiro_semestre, nota_segundo_semestre, media_final)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            alunos,
        )

    conexao.commit()
    conexao.close()
    print("Banco de dados inicializado com sucesso!")
