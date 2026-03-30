class Atendimento:
    def __init__(self, paciente_id, data, tipo, observacoes, status, id=None):
        self.id = id
        self.paciente_id = paciente_id
        self.data = data
        self.tipo = tipo
        self.observacoes = observacoes
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "data": self.data,
            "tipo": self.tipo,
            "observacoes": self.observacoes,
            "status": self.status
            }