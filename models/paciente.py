class Paciente:
    def __init__(self, nome, data_nascimento, telefone, email, cpf, id=None):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf
        }