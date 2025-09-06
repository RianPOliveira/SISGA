from POO.exceptions import TipoInvalidoError, ValorInvalidoError

class Curso:
    """
    Representa um curso oferecido no sistema.
    """
    def __init__(self, nome: str, creditos_necessarios: int):
        """Inicializa um objeto Curso."""
        self.setNome(nome)
        self.setCreditosNecessarios(creditos_necessarios)

    def getNome(self) -> str:
        """Retorna o nome do curso."""
        return self.__nome

    def setNome(self, novo_nome: str):
        """Define o nome do curso com validação."""
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise TipoInvalidoError("O nome do curso deve ser um texto não vazio.")
        self.__nome = novo_nome.strip()

    def getCreditosNecessarios(self) -> int:
        """Retorna a quantidade de créditos necessários para o curso."""
        return self.__creditos_necessarios

    def setCreditosNecessarios(self, nova_quantidade: int):
        """Define a quantidade de créditos do curso com validação."""
        if not isinstance(nova_quantidade, int) or nova_quantidade <= 0:
            raise ValorInvalidoError("A quantidade de créditos deve ser um número inteiro positivo.")
        self.__creditos_necessarios = nova_quantidade

    def imprime(self):
        """Imprime os dados do curso no console."""
        print(f"Curso: {self.getNome()}")
        print(f"Créditos Necessários: {self.getCreditosNecessarios()}")
