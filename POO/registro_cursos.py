from POO.curso import Curso

class RegistroCursos:
    """
    Esta classe gerencia a coleção de todos os cursos disponíveis,
    carregando-os a partir de um arquivo de texto.
    """
    def __init__(self, nome_arquivo="cursos.txt"):
        """Inicializa o registro de cursos e carrega os dados."""
        self._cursos = {}
        self.carregar_cursos(nome_arquivo)

    def carregar_cursos(self, nome_arquivo):
        """Carrega os dados dos cursos a partir de um arquivo."""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    nome, creditos = linha.strip().split(',')
                    curso = Curso(nome, int(creditos))
                    self._cursos[nome] = curso
        except FileNotFoundError:
            print(f"Aviso: Arquivo '{nome_arquivo}' não encontrado. Nenhum curso foi carregado.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar os cursos: {e}")

    def get_curso_por_nome(self, nome: str) -> Curso:
        """Busca e retorna um objeto Curso pelo seu nome."""
        curso = self._cursos.get(nome)
        if not curso:
            raise ValueError(f"O curso '{nome}' não foi encontrado no registro.")
        return curso

    def get_todos_os_cursos(self) -> list:
        """Retorna uma lista com todos os objetos Curso registrados."""
        return list(self._cursos.values())
    
    def get_nomes_dos_cursos(self) -> list:
        """Retorna uma lista com os nomes de todos os cursos."""
        return list(self._cursos.keys())