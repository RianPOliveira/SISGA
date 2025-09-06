from POO.matriculados import Matriculados
from POO.exceptions import ValorInvalidoError, MaximoItensAtingidoError, TipoInvalidoError

class Aluno(Matriculados):
    """
    Representa um aluno do sistema. Herda de Matriculados e adiciona
    atributos e métodos específicos para gestão de notas e faltas.
    """
    
    # Atributo de classe para limitar as notas
    _MAX_NOTAS = 4

    # Construtor
    def __init__(self, nome: str, conta_ativa: bool, curso: str, faltas: int = 0, matricula_existente: str = None):
        """Inicializa um objeto Aluno, chamando o construtor da classe mãe."""
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)
        self.setCurso(curso)
        self.setFaltas(faltas)
        self._notas = [] 

    # Métodos de Busca/Acesso 
    def getCurso(self) -> str:
        """Retorna o curso do aluno."""
        return self._curso

    def setCurso(self, novo_curso: str):
        """Define o curso do aluno com validação."""
        if not isinstance(novo_curso, str) or not novo_curso.strip():
            raise TipoInvalidoError("O nome do curso deve ser um texto não vazio.")
        self._curso = novo_curso.strip()

    def getFaltas(self) -> int:
        """Retorna a quantidade de faltas do aluno."""
        return self._faltas

    def setFaltas(self, nova_quantidade: int):
        """Define a quantidade de faltas do aluno com validação."""
        if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
            raise ValorInvalidoError("A quantidade de faltas deve ser um número inteiro não negativo.")
        self._faltas = nova_quantidade

    def getNotas(self) -> list:
        """Retorna uma cópia da lista de notas do aluno."""
        return self._notas.copy()
    
    # Métodos específicos da classe
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
        self._notas = notas_validadas

    def calcularMedia(self) -> float:
        """Calcula e retorna a média das notas do aluno."""
        if not self._notas:
            return 0.0
        return sum(self._notas) / len(self._notas)
        
    # Métodos Abstratos
    def getTipoEntidade(self) -> str:
        """Retorna o tipo da entidade, cumprindo o contrato da classe mãe."""
        return "Aluno"
        
    # Método de Exibição
    def imprime(self):
        """Imprime os dados completos do aluno no terminal."""
        super().imprime()
        media_formatada = f"{self.calcularMedia():.2f}"
        print(f"Curso: {self.getCurso()}")
        print(f"Notas: {self.getNotas()}")
        print(f"Média Final: {media_formatada}")
        print(f"Quantidade de Faltas: {self.getFaltas()}")