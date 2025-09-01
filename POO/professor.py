from POO.matriculados import Matriculados
from POO.exceptions import ValorInvalidoError, TipoInvalidoError

class Professor(Matriculados):
    """
    Representa um professor, herdando de Matriculados e adicionando
    atributos como salário e quantidade de matérias.
    """
    def __init__(self, nome: str, conta_ativa: bool, salario: float, qtde_materias: int, matricula_existente: str = None):
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.salario = salario
        self.qtde_materias = qtde_materias

    # Properties Específicas de Professor 

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, novo_salario: float):
        if not isinstance(novo_salario, (int, float)) or novo_salario < 0:
            raise ValorInvalidoError("O salário deve ser um valor numérico não negativo.")
        self._salario = float(novo_salario)

    @property
    def qtde_materias(self) -> int:
        return self._qtde_materias

    @qtde_materias.setter
    def qtde_materias(self, nova_qtde: int):
        if not isinstance(nova_qtde, int) or nova_qtde < 0:
            raise ValorInvalidoError("A quantidade de matérias deve ser um número inteiro não negativo.")
        self._qtde_materias = nova_qtde

    # Métodos de Abstração

    def get_tipo_entidade(self) -> str:
        return "Professor"

    # Polimorfismo

    def __str__(self) -> str:
        info_base = super().__str__()
        salario_formatado = f"R$ {self.salario:.2f}"
        info_professor = (f"Salário: {salario_formatado}\n"
                          f"Quantidade de Matérias: {self.qtde_materias}")

        return f"{info_base}\n{info_professor}"