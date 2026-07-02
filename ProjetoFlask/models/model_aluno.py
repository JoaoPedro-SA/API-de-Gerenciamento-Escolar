import sqlite3

from flask import jsonify
from config import banco_de_dados


def conectar_banco():
    conexao = sqlite3.connect(banco_de_dados)
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    return conexao


def _validar_aluno(aluno):
    if not aluno:
        return "JSON invalido ou ausente"

    campos = ["nome", "idade", "turma_id", "nota_primeiro_semestre", "nota_segundo_semestre"]
    for campo in campos:
        if campo not in aluno:
            return f"Campo obrigatorio ausente: {campo}"

    try:
        idade = int(aluno["idade"])
        turma_id = int(aluno["turma_id"])
        nota1 = float(aluno["nota_primeiro_semestre"])
        nota2 = float(aluno["nota_segundo_semestre"])
    except (TypeError, ValueError):
        return "Idade, turma_id e notas devem ser numeros validos"

    return {
        "nome": aluno["nome"],
        "idade": idade,
        "turma_id": turma_id,
        "nota_primeiro_semestre": nota1,
        "nota_segundo_semestre": nota2,
        "media_final": (nota1 + nota2) / 2,
    }


def adiciona_aluno(aluno):
    dados = _validar_aluno(aluno)
    if isinstance(dados, str):
        return jsonify({"erro": dados}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO alunos
                (nome, idade, turma_id, nota_primeiro_semestre, nota_segundo_semestre, media_final)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                dados["nome"],
                dados["idade"],
                dados["turma_id"],
                dados["nota_primeiro_semestre"],
                dados["nota_segundo_semestre"],
                dados["media_final"],
            ),
        )
        conexao.commit()
        dados["id"] = cursor.lastrowid
        return jsonify(dados), 201
    except sqlite3.IntegrityError as e:
        conexao.rollback()
        return jsonify({"erro": "Turma informada nao existe", "detalhe": str(e)}), 409
    finally:
        conexao.close()


def lista_alunos():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM alunos")
        return jsonify([dict(row) for row in cursor.fetchall()])
    finally:
        conexao.close()


def consulta_aluno(aluno_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = cursor.fetchone()
        if aluno:
            return jsonify(dict(aluno)), 200
        return jsonify({"mensagem": "Aluno nao encontrado"}), 404
    finally:
        conexao.close()


def update_aluno(id_aluno, novo_aluno):
    dados = _validar_aluno(novo_aluno)
    if isinstance(dados, str):
        return jsonify({"erro": dados}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome = ?, idade = ?, turma_id = ?, nota_primeiro_semestre = ?,
                nota_segundo_semestre = ?, media_final = ?
            WHERE id = ?
            """,
            (
                dados["nome"],
                dados["idade"],
                dados["turma_id"],
                dados["nota_primeiro_semestre"],
                dados["nota_segundo_semestre"],
                dados["media_final"],
                id_aluno,
            ),
        )
        conexao.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Aluno nao encontrado"}), 404
        return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200
    except sqlite3.IntegrityError as e:
        conexao.rollback()
        return jsonify({"erro": "Turma informada nao existe", "detalhe": str(e)}), 409
    finally:
        conexao.close()


def deletar_aluno(aluno_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
        conexao.commit()
        if cursor.rowcount > 0:
            return jsonify({"mensagem": "Aluno removido com sucesso"})
        return jsonify({"mensagem": "Aluno nao encontrado"}), 404
    finally:
        conexao.close()
