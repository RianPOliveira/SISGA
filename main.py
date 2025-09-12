# main.py (Versão de Terminal Final e Corrigida)

import os
from POO.registro import Registro
from POO.aluno import Aluno
from POO.professor import Professor
from POO.monitor import Monitor
from POO.curso import Curso
from POO.registro_cursos import RegistroCursos
from POO.exceptions import ErroMatricula, MatriculaNaoEncontradaError, RegistroDuplicadoError

# Funções Auxiliares de Interface 
def limpar_tela():
    """Limpa a tela do terminal para uma melhor visualização."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a execução até o usuário pressionar Enter."""
    input("\nPressione Enter para voltar ao menu...")

#  Funções de Persistência de Dados 
def carregar_dados(registro, registro_cursos, nome_arquivo="registros.txt"):
    """Carrega os dados de um arquivo para o objeto de registro."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                if not linha.strip(): continue
                partes = linha.strip().split(',')
                tipo, matricula, nome, conta_ativa = partes[0], partes[1], partes[2], partes[3] == 'True'
                if tipo == 'ALUNO':
                    nome_curso, creditos, faltas = partes[4], int(partes[5]), int(partes[6])
                    # --- CORRIGIDO ---
                    curso_obj = registro_cursos.getCursoPorNome(nome_curso)
                    notas = [float(n) for n in partes[7:] if n]
                    pessoa = Aluno(nome, conta_ativa, curso_obj, creditos, faltas, matricula)
                    pessoa.atualizarNotas(notas)
                elif tipo == 'PROFESSOR':
                    salario, qtde_materias = float(partes[4]), int(partes[5])
                    pessoa = Professor(nome, conta_ativa, salario, qtde_materias, matricula)
                elif tipo == 'MONITOR':
                    valor_bolsa, carga_horaria = float(partes[4]), int(partes[5])
                    pessoa = Monitor(nome, conta_ativa, valor_bolsa, carga_horaria, matricula)
                else: 
                    continue
                registro.inserir(pessoa)
        print("Dados de pessoas carregados com sucesso!")
    except FileNotFoundError:
        print("Arquivo de registros não encontrado. Começando do zero.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os dados: {e}")

def salvar_dados(registro, nome_arquivo="registros.txt"):
    """Salva os dados do registro em um arquivo."""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            for pessoa in registro.getTodos():
                tipo = pessoa.__class__.__name__.upper()
                base_info = f"{tipo},{pessoa.getMatricula()},{pessoa.getNome()},{pessoa.getContaAtiva()}"
                if isinstance(pessoa, Aluno):
                    notas_str = ",".join(map(str, pessoa.getNotas()))
                    f.write(f"{base_info},{pessoa.getCurso().getNome()},{pessoa.getCreditos()},{pessoa.getFaltas()},{notas_str}\n")
                elif isinstance(pessoa, Professor):
                    f.write(f"{base_info},{pessoa.getSalario()},{pessoa.getQtdeMaterias()}\n")
                elif isinstance(pessoa, Monitor):
                    f.write(f"{base_info},{pessoa.getValorBolsa()},{pessoa.getCargaHoraria()}\n")
        print("Dados salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar dados: {e}")

# Funções de Menu 
def cadastrar_pessoa(registro, registro_cursos):
    """Solicita os dados para cadastrar uma nova pessoa."""
    limpar_tela(); print("--- Cadastro de Nova Pessoa ---"); print("1. Aluno\n2. Professor\n3. Monitor")
    tipo = input(">> Escolha o perfil: ")
    nome = input("Nome Completo: "); conta_ativa = True
    try:
        if tipo == '1':
            print("\nCursos Disponíveis:")
            cursos_lista = registro_cursos.getTodosOsCursos() 
            for i, curso in enumerate(cursos_lista):
                print(f"{i+1}. {curso.getNome()} ({curso.getCreditosNecessarios()} créditos)")
            
            if not cursos_lista:
                print("\nNenhum curso cadastrado. Impossível registrar aluno."); return

            escolha = int(input(">> Escolha o curso: ")) - 1
            if not 0 <= escolha < len(cursos_lista):
                print("\nOpção de curso inválida."); return
            curso_selecionado = cursos_lista[escolha]
            creditos = int(input("Créditos Cursados pelo Aluno: "))
            faltas = int(input("Quantidade de Faltas: "))
            notas = [float(input(f"Nota {i+1}: ")) for i in range(4)]
            pessoa = Aluno(nome, conta_ativa, curso_selecionado, creditos, faltas)
            pessoa.atualizarNotas(notas)
        elif tipo == '2':
            salario = float(input("Salário (R$): ")); qtde_materias = int(input("Quantidade de Matérias: "))
            pessoa = Professor(nome, conta_ativa, salario, qtde_materias)
        elif tipo == '3':
            valor_bolsa = float(input("Valor da Bolsa (R$): ")); carga_horaria = int(input("Carga Horária Semanal (h): "))
            pessoa = Monitor(nome, conta_ativa, valor_bolsa, carga_horaria)
        else: 
            print("\nOpção de perfil inválida."); return
        registro.inserir(pessoa)
        print(f"\n✅ {pessoa.getTipoEntidade()} '{pessoa.getNome()}' cadastrado com sucesso!")
        print(f"Matrícula gerada: {pessoa.getMatricula()}")
    except (ValueError, ErroMatricula) as e: print(f"\n❌ Erro de entrada ou validação: {e}")
    except Exception as e: print(f"\n❌ Ocorreu um erro inesperado: {e}")

def cadastrar_curso(registro_cursos):
    """Solicita os dados para cadastrar um novo curso."""
    limpar_tela()
    print("--- Cadastrar Novo Curso ---")
    try:
        nome_curso = input("Nome do Curso: ")
        creditos_necessarios = int(input("Créditos Necessários: "))
        novo_curso = Curso(nome_curso, creditos_necessarios)
        registro_cursos.inserirCurso(novo_curso)
        print(f"\n✅ Curso '{novo_curso.getNome()}' cadastrado com sucesso!")
    except (ValueError, ErroMatricula, RegistroDuplicadoError) as e:
        print(f"\n❌ Erro de entrada ou validação: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")

def listar_pessoas(registro, lista=None, titulo=""):
    limpar_tela(); print(f"--- {titulo} ---")
    pessoas_para_listar = lista if lista is not None else registro.getTodos()
    if not pessoas_para_listar: print("Nenhum registro encontrado.")
    else:
        for pessoa in pessoas_para_listar:
            pessoa.imprime(); print("-" * 25)

def atualizar_pessoa(registro):
    limpar_tela(); print("--- Atualizar Dados ---")
    matricula = input("Digite a matrícula da pessoa a ser atualizada: ")
    try:
        pessoa = registro.buscar(matricula)
        print(f"\nEditando: {pessoa.getNome()} ({pessoa.getTipoEntidade()})")
        novo_nome = input(f"Novo Nome (deixe em branco para manter '{pessoa.getNome()}'): ")
        if novo_nome.strip(): pessoa.setNome(novo_nome)
        
        if isinstance(pessoa, Aluno):
            print(f"Créditos Atuais: {pessoa.getCreditos()}")
            novos_creditos = input("Novos Créditos (deixe em branco para manter): ")
            if novos_creditos.strip(): pessoa.setCreditos(int(novos_creditos))
            
        print("\n✅ Dados atualizados com sucesso!")
    except (MatriculaNaoEncontradaError, ValueError, ErroMatricula) as e: print(f"\n❌ Erro: {e}")

def remover_pessoa(registro):
    limpar_tela(); print("--- Remover Pessoa ---")
    matricula = input("Digite a matrícula da pessoa a ser removida: ")
    try:
        pessoa = registro.buscar(matricula)
        confirmacao = input(f"Tem certeza que deseja remover {pessoa.getNome()} ({pessoa.getTipoEntidade()})? [s/n]: ").lower()
        if confirmacao == 's':
            registro.remover(matricula)
            print(f"\n✅ '{pessoa.getNome()}' foi removido(a) com sucesso.")
        else: 
            print("\nOperação cancelada.")
    except MatriculaNaoEncontradaError as e: print(f"\n❌ Erro ao remover: {e}")

def mostrar_filtros_alunos(registro):
    limpar_tela(); print("--- Filtros de Alunos ---"); print("1. Listar Aprovados\n2. Listar Reprovados por Média\n3. Listar Reprovados por Falta")
    opcao = input(">> Escolha uma opção: ")
    if opcao == '1': listar_pessoas(registro, registro.getAlunosPorStatus(aprovado=True), "Alunos Aprovados")
    elif opcao == '2': listar_pessoas(registro, registro.getReprovadosPorMedia(), "Alunos Reprovados por Média")
    elif opcao == '3': listar_pessoas(registro, registro.getReprovadosPorFalta(), "Alunos Reprovados por Falta")
    else: print("Opção inválida.")

# Programa Principal
if __name__ == "__main__":
    registro_cursos = RegistroCursos("cursos.txt")
    registro_principal = Registro()
    carregar_dados(registro_principal, registro_cursos)
    pausar()
    
    while True:
        limpar_tela()
        print("--- SISGA - MENU PRINCIPAL (VERSÃO TERMINAL) ---")
        print("\n1. Cadastrar Pessoa\n2. Listar Todos\n3. Atualizar Pessoa\n4. Remover Pessoa\n5. Filtros de Alunos\n6. Cadastrar Curso\n\n0. Salvar e Sair")
        opcao = input("\n>> Digite sua opção: ")

        if opcao == '1':
            cadastrar_pessoa(registro_principal, registro_cursos)
        elif opcao == '2':
            listar_pessoas(registro_principal, titulo="Lista de Todos os Registros")
        elif opcao == '3':
            atualizar_pessoa(registro_principal)
        elif opcao == '4':
            remover_pessoa(registro_principal)
        elif opcao == '5':
            mostrar_filtros_alunos(registro_principal)
        elif opcao == '6':
            cadastrar_curso(registro_cursos)
        elif opcao == '0':
            salvar_dados(registro_principal)
            # --- CORRIGIDO ---
            registro_cursos.salvarCursos()
            break
        else: 
            print("Opção inválida. Tente novamente.")
        pausar()