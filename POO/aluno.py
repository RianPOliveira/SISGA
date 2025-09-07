from POO.matriculados import Matriculados
from POO.exceptions import ValorInvalidoError, MaximoItensAtingidoError, TipoInvalidoError
from POO.curso import Curso

class Aluno(Matriculados):
    """
    Representa um aluno do sistema. Herda de Matriculados e adiciona
    atributos e métodos específicos para gestão de notas, faltas e créditos.
    """
    
    _MAX_NOTAS = 4

    def __init__(self, nome: str, conta_ativa: bool, curso: Curso, creditos: int, faltas: int = 0, matricula_existente: str = None):
        """Inicializa um objeto Aluno, chamando o construtor da classe mãe."""
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.setCurso(curso)
        self.setCreditos(creditos)
        self.setFaltas(faltas)
        self.__notas = [] 

    def getCurso(self) -> Curso:
        """Retorna o objeto curso do aluno."""
        return self.__curso

    def setCurso(self, novo_curso: Curso):
        """Define o curso do aluno, esperando um objeto da classe Curso."""
        if not isinstance(novo_curso, Curso):
            raise TipoInvalidoError("O curso deve ser um objeto da classe Curso.")
        self.__curso = novo_curso

    def getCreditos(self) -> int:
        """Retorna a quantidade de créditos que o aluno possui."""
        return self.__creditos

    def setCreditos(self, nova_quantidade: int):
        """Define a quantidade de créditos do aluno com validação."""
        if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
            raise ValorInvalidoError("A quantidade de créditos deve ser um número inteiro não negativo.")
        self.__creditos = nova_quantidade

    def getFaltas(self) -> int:
        """Retorna a quantidade de faltas do aluno."""
        return self.__faltas

    def setFaltas(self, nova_quantidade: int):
        """Define a quantidade de faltas do aluno com validação."""
        if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
            raise ValorInvalidoError("A quantidade de faltas deve ser um número inteiro não negativo.")
        self.__faltas = nova_quantidade

    def getNotas(self) -> list:
        """Retorna uma cópia da lista de notas do aluno."""
        return self.__notas.copy()
    
    def atualizarNotas(self, lista_notas: list):
        """Substitui a lista de notas atual pela nova lista, com validação."""
        if not isinstance(lista_notas, list) or len(lista_notas) > self._MAX_NOTAS:
            raise ValueError(f"A lista de notas é inválida ou excede o máximo de {self._MAX_NOTAS} notas.")
        
        notas_validadas = []
        for nota in lista_notas:
            nota_float = float(nota)
            if not 0 <= nota_float <= 10:
                raise ValorInvalidoError("Todas as notas devem estar no intervalo de 0 a 10.")
            notas_validadas.append(nota_float)
        self.__notas = notas_validadas

    def calcularMedia(self) -> float:
        """Calcula e retorna a média das notas do aluno."""
        if not self.__notas:
            return 0.0
        return sum(self.__notas) / len(self.__notas)
        
    def getTipoEntidade(self) -> str:
        """Retorna o tipo da entidade, cumprindo o contrato da classe mãe."""
        return "Aluno"
        
    def imprime(self):
        """Imprime os dados completos do aluno no terminal."""
        super().imprime()
        media_formatada = f"{self.calcularMedia():.2f}"
        print(f"Curso: {self.getCurso().getNome()}")
        print(f"Créditos: {self.getCreditos()} / {self.getCurso().getCreditosNecessarios()}")
        print(f"Notas: {self.getNotas()}")
        print(f"Média Final: {media_formatada}")
        print(f"Quantidade de Faltas: {self.getFaltas()}")
