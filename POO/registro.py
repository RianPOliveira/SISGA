from POO.matriculados import Matriculados
from POO.aluno import Aluno
from POO.exceptions import TipoInvalidoError, MatriculaNaoEncontradaError, RegistroDuplicadoError

class Registro:
    """
    Esta classe gerencia a coleção de todas as pessoas matriculadas (Alunos, Professores, Monitores).
    Ela é responsável por inserir, remover, buscar e filtrar os registros.
    """
    
    # Construtor
    def __init__(self):
        """Inicializa o registro com um dicionário vazio para armazenar os dados."""
        self._registros = {}

    # Gerenciamento do Registro
    def inserir(self, pessoa: Matriculados):
        """Adiciona uma pessoa (Aluno, Professor ou Monitor) ao registro."""
        if not isinstance(pessoa, Matriculados):
            raise TipoInvalidoError("O objeto a ser inserido não é um tipo válido de Matriculado.")
        
        matricula = pessoa.getMatricula()
        if self.contemMatricula(matricula):
            raise RegistroDuplicadoError(f"A matrícula {matricula} já existe no registro.")
            
        self._registros[matricula] = pessoa

    def remover(self, matricula: str) -> Matriculados:
        """Remove uma pessoa do registro pela matrícula e retorna o objeto removido."""
        if not self.contemMatricula(matricula):
            raise MatriculaNaoEncontradaError(f"A matrícula {matricula} não foi encontrada.")
        
        return self._registros.pop(matricula)

    # Métodos de Busca/Acesso 
    def buscar(self, matricula: str) -> Matriculados:
        """Busca e retorna uma pessoa pela matrícula."""
        if not self.contemMatricula(matricula):
             raise MatriculaNaoEncontradaError(f"A matrícula {matricula} não foi encontrada.")
        return self._registros[matricula]

    def getTodos(self) -> list:
        """Retorna uma lista com todos os objetos matriculados."""
        return list(self._registros.values())
        
    def getQuantidade(self) -> int:
        """Retorna a quantidade total de pessoas registradas."""
        return len(self._registros)

    def contemMatricula(self, matricula: str) -> bool:
        """Verifica se uma matrícula já existe no registro."""
        return matricula in self._registros

    # Métodos de Filtragem de Alunos
    def getAlunosPorStatus(self, aprovado: bool = True) -> list:
        """Retorna uma lista de alunos filtrados por status (aprovado/reprovado)."""
        alunos_filtrados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno):
                if (pessoa.calcularMedia() >= 5 and pessoa.getFaltas() <= 9) == aprovado:
                    alunos_filtrados.append(pessoa)
        return alunos_filtrados

    def getReprovadosPorMedia(self) -> list:
        """Retorna uma lista de alunos com média inferior a 5.0."""
        reprovados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno) and pessoa.calcularMedia() < 5.0:
                reprovados.append(pessoa)
        return reprovados

    def getReprovadosPorFalta(self) -> list:
        """Retorna uma lista de alunos com mais de 9 faltas."""
        reprovados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno) and pessoa.getFaltas() > 9:
                reprovados.append(pessoa)
        return reprovados