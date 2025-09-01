from POO.matriculados import Matriculados
from POO.aluno import Aluno
from POO.exceptions import (
    TipoInvalidoError,
    MatriculaNaoEncontradaError,
    RegistroDuplicadoError,
)

class Registro:
    """
    Classe para gerenciar uma coleção de objetos Matriculados.
    Utiliza um dicionário para acesso rápido e garantir matrículas únicas.
    """
    def __init__(self):
        self._registros = {}

    # Métodos Especiais para comportamento de coleção 

    def __len__(self) -> int:
        """Permite usar a função `len(registro)`."""
        return len(self._registros)

    def __contains__(self, matricula: str) -> bool:
        """Permite usar o operador `in` (ex: `if matricula in registro:`)."""
        return matricula in self._registros

    def __iter__(self):
        """Permite iterar sobre os objetos do registro (ex: `for pessoa in registro:`)."""
        return iter(self._registros.values())

    # Métodos de Gerenciamento (com tratamento de erros) 

    def inserir(self, pessoa: Matriculados):
        """Adiciona uma pessoa ao registro, usando a matrícula como chave."""
        if not isinstance(pessoa, Matriculados):
            raise TipoInvalidoError("O objeto a ser inserido não é um tipo válido de Matriculado.")

        if pessoa.matricula in self._registros:
            raise RegistroDuplicadoError(f"A matrícula {pessoa.matricula} já existe no registro.")

        self._registros[pessoa.matricula] = pessoa

    def remover(self, matricula: str) -> Matriculados:
        """Remove uma pessoa do registro pela matrícula e retorna o objeto removido."""
        if matricula not in self._registros:
            raise MatriculaNaoEncontradaError(f"A matrícula {matricula} não foi encontrada.")

        return self._registros.pop(matricula)

    def buscar(self, matricula: str) -> Matriculados:
        """Busca e retorna uma pessoa pela matrícula."""
        if matricula not in self._registros:
             raise MatriculaNaoEncontradaError(f"A matrícula {matricula} não foi encontrada.")
        return self._registros[matricula]

    # Métodos de Lógica (retornam dados) 

    def get_todos(self) -> list:
        """Retorna uma lista com todos os objetos matriculados."""
        return list(self._registros.values())

    def get_ordenado_por(self, chave: str = 'nome') -> list:
        """Retorna uma NOVA LISTA de matriculados, ordenada pelo critério."""
        if chave not in ['nome', 'matricula']:
            raise ValueError("Chave de ordenação inválida. Use 'nome' ou 'matricula'.")

        return sorted(self._registros.values(), key=lambda pessoa: getattr(pessoa, chave))

    def get_alunos_por_status(self, aprovado: bool = True) -> list:
        """Retorna uma lista de alunos filtrados por status (aprovado/reprovado)."""
        alunos_filtrados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno):
                if pessoa.is_aprovado() == aprovado:
                    alunos_filtrados.append(pessoa)
        return alunos_filtrados

    def get_reprovados_por_media(self) -> list:
        """Retorna uma lista de alunos com média inferior a 5.0."""
        reprovados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno) and pessoa.calcular_media() < 5.0:
                reprovados.append(pessoa)
        return reprovados

    def get_reprovados_por_falta(self) -> list:
        """Retorna uma lista de alunos com mais de 9 faltas."""
        from POO.aluno import Aluno
        reprovados = []
        for pessoa in self._registros.values():
            if isinstance(pessoa, Aluno) and pessoa.faltas > 9:
                reprovados.append(pessoa)
        return reprovados

    def listar_todos(self):
        """Imprime os dados de todos os registros."""
        print("\n--- LISTA DE REGISTROS ---")
        if not self._registros:
            print("Nenhum registro encontrado.")
        else:
            for pessoa in self.get_ordenado_por('nome'):
                print(pessoa)
                print("-" * 15)
        print("--- FIM DA LISTA ---\n")

    def listar_alunos_por_status(self, aprovado: bool = True):
        """Lista todos os alunos aprovados ou reprovados."""
        status_str = "APROVADOS" if aprovado else "REPROVADOS"
        print(f"\n--- ALUNOS {status_str} ---")

        lista_alunos = self.get_alunos_por_status(aprovado=aprovado)

        if not lista_alunos:
            print(f"Nenhum aluno {status_str.lower()} encontrado.")
        else:
            for aluno in lista_alunos:
                print(aluno)
                print("-" * 15)
        print(f"--- FIM DA LISTA DE {status_str} ---\n")