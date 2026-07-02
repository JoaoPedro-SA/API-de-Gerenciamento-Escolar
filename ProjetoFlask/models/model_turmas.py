import sqlite3

from flask import jsonify, request
from config import banco_de_dados


def conectar_banco():
    conexao = sqlite3.connect(banco_de_dados)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def apiTurma(turma_id=None):
    metodo = request.method
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        if metodo == "GET":
            id_turma = turma_id or request.args.get("id")
            if id_turma:
                turma = cursor.execute(
                    "SELECT * FROM turmas WHERE id = ?",
                    (id_turma,),
                ).fetchone()
                if not turma:
                    return jsonify({"code": 404, "mensagem": "Turma nao encontrada"}), 404
                return jsonify({
                    "turma": {
                        "id": turma[0],
                        "nome": turma[1],
                        "turno": turma[2],
                        "professor_id": turma[3],
                        "ativo": turma[4],
                    }
                }), 200

            turmas = cursor.execute("SELECT * FROM turmas").fetchall()
            return jsonify([
                {
                    "id": turma[0],
                    "nome": turma[1],
                    "turno": turma[2],
                    "professor_id": turma[3],
                    "ativo": turma[4],
                }
                for turma in turmas
            ]), 200

        if metodo == "POST":
            dados = request.get_json(silent=True) or {}
            campos = ["nome", "turno", "professor_id"]
            if not all(campo in dados and dados[campo] not in ("", None) for campo in campos):
                return jsonify({"erro": "Dados incompletos"}), 400

            cursor.execute(
                "INSERT INTO turmas (nome, turno, professor_id, ativo) VALUES (?, ?, ?, ?)",
                (dados["nome"], dados["turno"], int(dados["professor_id"]), True),
            )
            conexao.commit()
            return jsonify({
                "mensagem": "Turma adicionada com sucesso",
                "turma_adicionada": {
                    "id": cursor.lastrowid,
                    "nome": dados["nome"],
                    "turno": dados["turno"],
                    "professor_id": int(dados["professor_id"]),
                    "ativo": True,
                },
            }), 201

        if metodo == "PUT":
            id_turma = turma_id or request.args.get("id")
            if not id_turma:
                return jsonify({"mensagem": "ID da turma e obrigatorio"}), 400

            dados = request.get_json(silent=True) or {}
            campos = ["nome", "turno", "professor_id", "ativo"]
            if not all(campo in dados for campo in campos):
                return jsonify({"erro": "Dados incompletos"}), 400

            cursor.execute(
                "UPDATE turmas SET nome = ?, turno = ?, professor_id = ?, ativo = ? WHERE id = ?",
                (
                    dados["nome"],
                    dados["turno"],
                    int(dados["professor_id"]),
                    bool(dados["ativo"]),
                    int(id_turma),
                ),
            )
            conexao.commit()
            if cursor.rowcount == 0:
                return jsonify({"mensagem": "Turma nao encontrada"}), 404
            return jsonify({"mensagem": "Turma atualizada com sucesso"}), 200

        if metodo == "DELETE":
            id_turma = turma_id or request.args.get("id")
            if not id_turma:
                return jsonify({"mensagem": "ID da turma e obrigatorio"}), 400

            cursor.execute("DELETE FROM turmas WHERE id = ?", (id_turma,))
            conexao.commit()
            if cursor.rowcount == 0:
                return jsonify({"mensagem": "Turma nao encontrada"}), 404
            return jsonify({"mensagem": "Turma excluida com sucesso"}), 200

        return jsonify({"mensagem": "Metodo nao permitido"}), 405
    except sqlite3.IntegrityError as e:
        conexao.rollback()
        return jsonify({"erro": "Operacao viola relacionamento do banco", "detalhe": str(e)}), 409
    finally:
        cursor.close()
        conexao.close()
