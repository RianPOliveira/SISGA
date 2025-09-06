from POO.matriculados import Matriculados
from POO.exceptions import ValorInvalidoError

class Professor(Matriculados):
    """
    Representa um professor do sistema. Herda de Matriculados e adiciona
    atributos específicos de salário e matérias.
    """

    # Construtor
    def __init__(self, nome: str, conta_ativa: bool, salario: float, qtde_materias: int, matricula_existente: str = None):
        """Inicializa um objeto Professor, chamando o construtor da classe mãe."""
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.setSalario(salario)
        self.setQtdeMaterias(qtde_materias)

    # Métodos de Busca/Acesso 
    def getSalario(self) -> float:
        """Retorna o salário do professor."""
        return self._salario

    def setSalario(self, novo_salario: float):
        """Define o salário do professor com validação."""
        if not isinstance(novo_salario, (int, float)) or novo_salario < 0:
            raise ValorInvalidoError("O salário deve ser um valor numérico não negativo.")
        self._salario = float(novo_salario)

    def getQtdeMaterias(self) -> int:
        """Retorna a quantidade de matérias do professor."""
        return self._qtde_materias

    def setQtdeMaterias(self, nova_qtde: int):
        """Define a quantidade de matérias do professor com validação."""
        if not isinstance(nova_qtde, int) or nova_qtde < 0:
            raise ValorInvalidoError("A quantidade de matérias deve ser um número inteiro não negativo.")
        self._qtde_materias = nova_qtde

    # Método Abstrato
    def getTipoEntidade(self) -> str:
        """Retorna o tipo da entidade, cumprindo o contrato da classe mãe."""
        return "Professor"
    
    # Método de Exibição 
    def imprime(self):
        """Imprime os dados completos do professor no console."""
        super().imprime()
        salario_formatado = f"R$ {self.getSalario():.2f}"
        print(f"Salário: {salario_formatado}")
        print(f"Quantidade de Matérias: {self.getQtdeMaterias()}")