from random import randint 
from abc import ABC, abstractmethod

class Matriculados(ABC):
    
    def __init__(self, nome: str, conta_ativa: bool, matricula_existente: str = None):
        self.setNome(nome)
        self.setContaAtiva(conta_ativa)
        
        if matricula_existente:
            self._matricula = matricula_existente
        else:
            self._matricula = self.__gerar_matricula()
            
        self._tipo_entidade = self.getTipoEntidade()
      
    # Método Privado  
    def __gerar_matricula(self) -> str:
        """
        Gera uma nova matrícula única baseada no ano e em um número aleatório.
        """
        ano_atual = "2025"
        id_aleatorio = randint(1000, 9999) 
        nova_matricula = f"{ano_atual}{id_aleatorio}"
        return nova_matricula

    # Métodos de Acesso
    def getNome(self) -> str:
        return self._nome

    def setNome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome deve ser um texto não vazio.")
        self._nome = novo_nome.strip()

    def getContaAtiva(self) -> bool:
        return self._conta_ativa

    def setContaAtiva(self, status: bool):
        if not isinstance(status, bool):
            raise TypeError("O status da conta deve ser um valor booleano (True/False).")
        self._conta_ativa = status

    def getMatricula(self) -> str:
        return self._matricula
    
    # Métodos abstratos
    @abstractmethod 
    def getTipoEntidade(self) -> str:
        pass
    
    # Exibir no Terminal
    def imprime(self):
        """Imprime os dados básicos da pessoa no console."""
        status = "Sim" if self.getContaAtiva() else "Não"
        print(f"Nome: {self.getNome()}")
        print(f"Matrícula: {self.getMatricula()}")
        print(f"Função: {self.getTipoEntidade()}")
        print(f"Conta Ativa: {status}")