from POO.matriculados import Matriculados
from POO.exceptions import TipoInvalidoError, ValorInvalidoError

class Monitor(Matriculados):
    """
    Representa um monitor, herdando de Matriculados e adicionando
    informações sobre bolsa e carga horária.
    """


    def __init__(self, nome: str, conta_ativa: bool, valor_bolsa: float, carga_horaria: int, matricula_existente: str = None):
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.valor_bolsa = valor_bolsa
        self.carga_horaria = carga_horaria

    # Propriedades Específicas de Monitor 

    @property
    def valor_bolsa(self) -> float:
        return self._valor_bolsa

    @valor_bolsa.setter
    def valor_bolsa(self, novo_valor: float):
        if not isinstance(novo_valor, (int, float)) or novo_valor < 0:
            raise ValorInvalidoError("O valor da bolsa deve ser um número não negativo.")
        self._valor_bolsa = float(novo_valor)

    @property
    def carga_horaria(self) -> int:
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, nova_carga: int):
        if not isinstance(nova_carga, int) or nova_carga <= 0:
            raise ValorInvalidoError("A carga horária deve ser um número inteiro positivo.")
        self._carga_horaria = nova_carga

    # Métodos de Abstração

    def get_tipo_entidade(self) -> str:
        return "Monitor"

    # Polimorfismo

    def __str__(self) -> str:
        info_base = super().__str__()
        valor_bolsa_formatado = f"R$ {self.valor_bolsa:.2f}"
        info_monitor = (f"Valor da Bolsa: {valor_bolsa_formatado}\n"
                        f"Carga Horária: {self.carga_horaria}h semanais")

        return f"{info_base}\n{info_monitor}"