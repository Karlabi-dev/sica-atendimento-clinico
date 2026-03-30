class Response:
    def __init__(self, sucesso, mensagem=None, dados=None, erro=None):
        self.sucesso = sucesso
        self.mensagem = mensagem
        self.dados = dados
        self.erro = erro

    def to_dict(self):
        return {
            "sucesso": self.sucesso,
            "mensagem": self.mensagem,
            "dados": self.dados,
            "erro": self.erro
        }