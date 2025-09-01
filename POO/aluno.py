from POO.matriculados import Matriculados
from POO.exceptions import TipoInvalidoError, ValorInvalidoError, MaximoItensAtingidoError

class Aluno(Matriculados):
    """
    Representa um aluno, herdando de Matriculados e adicionando
    atributos e regras específicas como curso, notas e faltas.
    """

    _MAX_NOTAS = 4

    def __init__(self, nome: str, conta_ativa: bool, curso: str, faltas: int = 0, matricula_existente: str = None):
        """
        Construtor da classe Aluno.
        Parâmetros obrigatórios: nome, conta_ativa, curso.
        Parâmetros opcionais: faltas (padrão 0), matricula_existente (padrão None).
        """
        super().__init__(nome, conta_ativa, matricula_existente=matricula_existente)

        self.curso = curso
        self.faltas = faltas
        self._notas = []

    # Properties Específicas de Aluno

    @property
    def curso(self) -> str:
        return self._curso

    @curso.setter
    def curso(self, novo_curso: str):
        if not isinstance(novo_curso, str) or not novo_curso.strip():
            raise TipoInvalidoError("O nome do curso deve ser um texto não vazio.")
        self._curso = novo_curso.strip()

    @property
    def faltas(self) -> int:
        return self._faltas

    @faltas.setter
    def faltas(self, nova_quantidade: int):
        if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
            raise ValorInvalidoError("A quantidade de faltas deve ser um número inteiro não negativo.")
        self._faltas = nova_quantidade

    @property
    def notas(self) -> list:
        return self._notas.copy()

    # Métodos de Implementação Obrigatória (Abstração) 

    def get_tipo_entidade(self) -> str:
        return "Aluno"

    # Métodos Específicos de Aluno 

    def adicionar_nota(self, nota: float):
        if len(self._notas) >= self._MAX_NOTAS:
            raise MaximoItensAtingidoError(f"O aluno já possui o máximo de {self._MAX_NOTAS} notas.")

        if not isinstance(nota, (int, float)):
            raise TipoInvalidoError("A nota deve ser um valor numérico.")

        if not 0 <= nota <= 10:
            raise ValorInvalidoError("A nota deve estar no intervalo entre 0 e 10.")

        self._notas.append(float(nota))

    def calcular_media(self) -> float:
        if not self._notas:
            return 0.0
        return sum(self._notas) / len(self._notas)

    def is_aprovado(self, media_minima: float = 7.0, faltas_maximas: int = 25) -> bool:
        """Verifica se o aluno foi aprovado com base na média e faltas."""
        if self.faltas > faltas_maximas:
            return False
        return self.calcular_media() >= media_minima

    def atualizar_notas(self, lista_notas: list):
        """
        Substitui a lista de notas atual pela nova lista, aplicando validações.
        Este método é ideal para receber dados de formulários.
        """
        if not isinstance(lista_notas, list):
            raise TypeError("O valor fornecido para atualizar as notas deve ser uma lista.")

        if len(lista_notas) > self._MAX_NOTAS:
            raise ValueError(f"A lista não pode conter mais de {self._MAX_NOTAS} notas.")

        notas_validadas = []
        for nota in lista_notas:
            nota_float = float(nota)
            if not 0 <= nota_float <= 10:
                raise ValueError("Todas as notas devem estar no intervalo de 0 a 10.")
            notas_validadas.append(nota_float)

        self._notas = notas_validadas
        
    # Polimorfismo

    def __str__(self) -> str:
        info_base = super().__str__()

        media_formatada = f"{self.calcular_media():.2f}"
        info_aluno = (f"Curso: {self.curso}\n"
                      f"Notas: {self._notas}\n"
                      f"Média Final: {media_formatada}\n"
                      f"Quantidade de Faltas: {self.faltas}")

        return f"{info_base}\n{info_aluno}"