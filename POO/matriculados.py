from random import randint 
from abc import ABC, abstractmethod

class Matriculados(ABC):
    """
    Classe base abstrata que representa todas as entidades matriculadas.
    Possui funcionalidades comuns para gerenciamento de nomes, 
    status de conta e números de matrícula exclusivos.
    """
    
    def __init__(self, nome: str, conta_ativa: bool, matricula_existente: str = None):
        self.setNome(nome)
        self.setContaAtiva(conta_ativa)
        
        if matricula_existente:
            self.__matricula = matricula_existente
        else:
            self.__gerar_matricula()
            
        self.__tipo_entidade = self.getTipoEntidade()
      
    # Método Privado  
    def __gerar_matricula(self) -> str:
        """
        Gera uma nova matrícula única baseada no ano e em um número aleatório.
        """
        ano_atual = "2025"
        id_aleatorio = randint(1000, 9999) 
        nova_matricula = f"{ano_atual}{id_aleatorio}"
        self.__matricula = nova_matricula

    # Métodos de Acesso
    def getNome(self) -> str:
        return self.__nome

    def setNome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome deve ser um texto não vazio.")
        self.__nome = novo_nome.strip()

    def getContaAtiva(self) -> bool:
        return self.__conta_ativa

    def setContaAtiva(self, status: bool):
        if not isinstance(status, bool):
            raise TypeError("O status da conta deve ser um valor booleano (True/False).")
        self.__conta_ativa = status

    def getMatricula(self) -> str:
        return self.__matricula
    
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
