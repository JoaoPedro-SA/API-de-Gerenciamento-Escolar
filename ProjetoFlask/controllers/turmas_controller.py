from flask import Blueprint, request
from models import model_turmas

turmas_bp = Blueprint('turma', __name__)

# GET /api/turma - Lista todas as turmas
@turmas_bp.route('/api/turma', methods=['GET'])
def consulta_turmas():
    return model_turmas.apiTurma()

# GET /api/turma/<int:turma_id> - Consulta uma turma específica
@turmas_bp.route('/api/turma/<int:turma_id>', methods=['GET'])
def consulta_turma(turma_id):
    return model_turmas.apiTurma(turma_id)

# POST /api/turma - Cria uma nova turma
@turmas_bp.route('/api/turma', methods=['POST'])
def cria_turma():
    return model_turmas.apiTurma()

# PUT /api/turma - Atualiza uma turma existente
@turmas_bp.route('/api/turma', methods=['PUT'])
@turmas_bp.route('/api/turma/<int:turma_id>', methods=['PUT'])
def atualiza_turma(turma_id=None):
    return model_turmas.apiTurma(turma_id)

# DELETE /api/turma - Deleta uma turma existente
@turmas_bp.route('/api/turma', methods=['DELETE'])
@turmas_bp.route('/api/turma/<int:turma_id>', methods=['DELETE'])
def deleta_turma(turma_id=None):
    return model_turmas.apiTurma(turma_id)
