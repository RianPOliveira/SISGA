import datetime
from abc import ABC, abstractmethod
from POO.exceptions import TipoInvalidoError, ValorInvalidoError

class Matriculados(ABC):
    """
    Classe abstrata base para qualquer pessoa matriculada na instituição.
    Implementa validação de dados e geração automática de matrícula.
    """

    # Atributo de classe
    _numero_sequencial = 0

    def __init__(self, nome: str, conta_ativa: bool, matricula_existente: str = None):
        self.nome = nome
        self.conta_ativa = conta_ativa

        if matricula_existente:
            self._matricula = matricula_existente 
        else:
            self._matricula = self._gerar_matricula() 

        self._tipo_entidade = self.get_tipo_entidade()


    def _gerar_matricula(self) -> str:
        """
        Gera uma nova matrícula única baseada no ano e em um contador sequencial.
        """
        ano_atual = "2025"  
        Matriculados._numero_sequencial += 1
        id_sequencial = Matriculados._numero_sequencial
        nova_matricula = f"{ano_atual}{id_sequencial:03d}"
        return nova_matricula
        
    # Encapsulamento 

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise TipoInvalidoError("O nome deve ser um texto não vazio.")
        self._nome = novo_nome.strip()

    @property
    def conta_ativa(self) -> bool:
        return self._conta_ativa

    @conta_ativa.setter
    def conta_ativa(self, status: bool):
        if not isinstance(status, bool):
            raise TipoInvalidoError("O status da conta deve ser um valor booleano (True/False).")
        self._conta_ativa = status

    @property
    def matricula(self) -> str:
        return self._matricula

    # Métodos Abstratos 

    @abstractmethod
    def get_tipo_entidade(self) -> str:
        """
        Método abstrato que força as classes filhas a implementarem
        sua própria identificação de tipo.
        """
        pass

    def __gerar_matricula(self) -> str:
        """
        Método privado que gera uma nova matrícula única.
        Formato: ANO + ID sequencial de 4 dígitos.
        """
        ano_atual = datetime.datetime.now().strftime("%Y")
        Matriculados._numero_sequencial += 1
        id_sequencial = Matriculados._numero_sequencial
        nova_matricula = f"{ano_atual}{id_sequencial:04d}"
        return nova_matricula

    def __str__(self) -> str:
        """
        Método especial para representação em string do objeto (Polimorfismo).
        """
        status = "SIM" if self._conta_ativa else "NÃO"
        return (f"Nome: {self.nome}\n"
                f"Matrícula: {self.matricula}\n"
                f"Função: {self._tipo_entidade}\n"
                f"Conta Ativa: {status}")