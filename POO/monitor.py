from POO.matriculados import Matriculados
from POO.exceptions import ValorInvalidoError

class Monitor(Matriculados):
    """
    Representa um monitor do sistema. Herda de Matriculados e adiciona
    atributos específicos de bolsa e carga horária.
    """
    
    # Construtor
    def __init__(self, nome: str, conta_ativa: bool, valor_bolsa: float, carga_horaria: int, matricula_existente: str = None):
        """Inicializa um objeto Monitor, chamando o construtor da classe mãe."""
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.setValorBolsa(valor_bolsa)
        self.setCargaHoraria(carga_horaria)

    # Métodos de Busca/Acesso
    def getValorBolsa(self) -> float:
        """Retorna o valor da bolsa do monitor."""
        return self.__valor_bolsa

    def setValorBolsa(self, novo_valor: float):
        """Define o valor da bolsa do monitor com validação."""
        if not isinstance(novo_valor, (int, float)) or novo_valor < 0:
            raise ValorInvalidoError("O valor da bolsa deve ser um número não negativo.")
        self.__valor_bolsa = float(novo_valor)

    def getCargaHoraria(self) -> int:
        """Retorna a carga horária do monitor."""
        return self.__carga_horaria

    def setCargaHoraria(self, nova_carga: int):
        """Define a carga horária do monitor com validação."""
        if not isinstance(nova_carga, int) or nova_carga <= 0:
            raise ValorInvalidoError("A carga horária deve ser um número inteiro positivo.")
        self.__carga_horaria = nova_carga

    # Implementação de Métodos Abstratos 
    def getTipoEntidade(self) -> str:
        """Retorna o tipo da entidade, cumprindo o contrato da classe mãe."""
        return "Monitor"
    
    # Método de Exibição 
    def imprime(self):
        """Imprime os dados completos do monitor no console."""
        super().imprime()
        valor_bolsa_formatado = f"R$ {self.getValorBolsa():.2f}"
        print(f"Valor da Bolsa: {valor_bolsa_formatado}")
        print(f"Carga Horária: {self.getCargaHoraria()}h semanais")