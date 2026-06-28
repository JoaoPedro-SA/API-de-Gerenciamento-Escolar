import sqlite3

from flask import jsonify, request
from config import banco_de_dados


def conectar_banco():
    conexao = sqlite3.connect(banco_de_dados)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def professores():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM professores")
        resultados = cursor.fetchall()
        return jsonify([
            {"id": row[0], "nome": row[1], "disciplina": row[2]}
            for row in resultados
        ])
    finally:
        conexao.close()


def professorPorId(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM professores WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado:
            return jsonify({
                "id": resultado[0],
                "nome": resultado[1],
                "disciplina": resultado[2],
            })
        return jsonify({"mensagem": "Professor nao encontrado"}), 404
    finally:
        conexao.close()


def cria_professor():
    dados = request.get_json(silent=True) or {}
    campos = ["nome", "disciplina"]
    if not all(campo in dados and dados[campo] for campo in campos):
        return jsonify({"erro": "Dados incompletos"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO professores (nome, disciplina) VALUES (?, ?)",
            (dados["nome"], dados["disciplina"]),
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        return jsonify({
            "id": novo_id,
            "nome": dados["nome"],
            "disciplina": dados["disciplina"],
        }), 201
    finally:
        conexao.close()


def atualiza_professor(id):
    dados = request.get_json(silent=True) or {}
    campos = ["nome", "disciplina"]
    if not all(campo in dados and dados[campo] for campo in campos):
        return jsonify({"erro": "Dados incompletos"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE professores SET nome = ?, disciplina = ? WHERE id = ?",
            (dados["nome"], dados["disciplina"], id),
        )
        conexao.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Professor nao encontrado"}), 404
        return jsonify({"id": id, "nome": dados["nome"], "disciplina": dados["disciplina"]})
    finally:
        conexao.close()


def deleta_professor(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM professores WHERE id = ?", (id,))
        conexao.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Professor nao encontrado"}), 404
        return jsonify({"mensagem": "Professor deletado com sucesso"})
    except sqlite3.IntegrityError:
        return jsonify({
            "erro": "Professor possui turmas vinculadas e nao pode ser deletado"
        }), 409
    finally:
        conexao.close()
