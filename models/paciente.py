class Paciente:
    def __init__(self, nome, data_nascimento, telefone, email, doc, tipo_documento,id=None):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.doc = doc
        self.tipo_documento = tipo_documento

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "email": self.email,
            "doc": self.doc,
            "tipo_documento": self.tipo_documento}