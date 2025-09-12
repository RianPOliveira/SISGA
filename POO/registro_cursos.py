from POO.curso import Curso
from POO.exceptions import RegistroDuplicadoError

class RegistroCursos:
    """
    Esta classe gerencia a coleção de todos os cursos disponíveis,
    carregando-os a partir de um arquivo de texto.
    """
    def __init__(self, nome_arquivo="cursos.txt"):
        """Inicializa o registro de cursos e carrega os dados."""
        self.__cursos = {}
        self.nome_arquivo = nome_arquivo
        self.carregar__cursos(nome_arquivo)

    def carregar__cursos(self, nome_arquivo):
        """Carrega os dados dos cursos a partir de um arquivo."""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    nome, creditos = linha.strip().split(',')
                    curso = Curso(nome, int(creditos))
                    self.__cursos[nome] = curso
        except FileNotFoundError:
            print(f"Aviso: Arquivo '{nome_arquivo}' não encontrado. Nenhum curso foi carregado.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar os cursos: {e}")

    def salvar__cursos(self):
        """Salva a lista de cursos no arquivo de texto."""
        try:
            with open(self.nome_arquivo, 'w', encoding='utf-8') as f:
                for curso in self.__cursos.values():
                    f.write(f"{curso.getNome()},{curso.getCreditosNecessarios()}\n")
            print("Cursos salvos com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar cursos: {e}")

    def inserir_curso(self, curso: Curso):
        """Adiciona um novo curso ao registro."""
        if curso.getNome() in self.__cursos:
            raise RegistroDuplicadoError(f"O curso '{curso.getNome()}' já existe no registro.")
        self.__cursos[curso.getNome()] = curso

    def get_curso_por_nome(self, nome: str) -> Curso:
        """Busca e retorna um objeto Curso pelo seu nome."""
        curso = self.__cursos.get(nome)
        if not curso:
            raise ValueError(f"O curso '{nome}' não foi encontrado no registro.")
        return curso

    def get_todos_os_cursos(self) -> list:
        """Retorna uma lista com todos os objetos Curso registrados."""
        return list(self.__cursos.values())
    
    def get_nomes_dos_cursos(self) -> list:
        """Retorna uma lista com os nomes de todos os cursos."""
        return list(self.__cursos.keys())
