import os
from POO.registro import Registro
from POO.aluno import Aluno
from POO.professor import Professor
from POO.monitor import Monitor
from POO.exceptions import ErroMatricula, MatriculaNaoEncontradaError

def limpar_tela():
    """Limpa a tela do terminal para uma melhor visualização."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a execução até o usuário pressionar Enter."""
    input("\nPressione Enter para voltar ao menu...")

def carregar_dados(registro, nome_arquivo="registros.txt"):
    """Carrega os dados de um arquivo para o objeto de registro."""
    try:
        with open(nome_arquivo, 'r') as f:
            for linha in f:
                if not linha.strip(): continue
                partes = linha.strip().split(',')
                tipo, matricula, nome, conta_ativa = partes[0], partes[1], partes[2], partes[3] == 'True'
                
                if tipo == 'ALUNO':
                    curso, faltas = partes[4], int(partes[5])
                    notas = [float(n) for n in partes[6:] if n]
                    pessoa = Aluno(nome=nome, conta_ativa=conta_ativa, curso=curso, faltas=faltas, matricula_existente=matricula)
                    pessoa.atualizar_notas(notas)
                elif tipo == 'PROFESSOR':
                    salario, qtde_materias = float(partes[4]), int(partes[5])
                    pessoa = Professor(nome=nome, conta_ativa=conta_ativa, salario=salario, qtde_materias=qtde_materias, matricula_existente=matricula)
                elif tipo == 'MONITOR':
                    valor_bolsa, carga_horaria = float(partes[4]), int(partes[5])
                    pessoa = Monitor(nome=nome, conta_ativa=conta_ativa, valor_bolsa=valor_bolsa, carga_horaria=carga_horaria, matricula_existente=matricula)
                else: continue
                registro.inserir(pessoa)
        print("Dados carregados com sucesso!")
    except FileNotFoundError:
        print("Arquivo de registros não encontrado. Começando com um registro vazio.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os dados: {e}")

def salvar_dados(registro, nome_arquivo="registros.txt"):
    """Salva os dados do registro em um arquivo."""
    try:
        with open(nome_arquivo, 'w') as f:
            for pessoa in registro.get_todos():
                tipo = pessoa.__class__.__name__.upper()
                base_info = f"{tipo},{pessoa.matricula},{pessoa.nome},{pessoa.conta_ativa}"
                if isinstance(pessoa, Aluno):
                    notas_str = ",".join(map(str, pessoa.notas))
                    f.write(f"{base_info},{pessoa.curso},{pessoa.faltas},{notas_str}\n")
                elif isinstance(pessoa, Professor):
                    f.write(f"{base_info},{pessoa.salario},{pessoa.qtde_materias}\n")
                elif isinstance(pessoa, Monitor):
                    f.write(f"{base_info},{pessoa.valor_bolsa},{pessoa.carga_horaria}\n")
        print("Dados salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar dados: {e}")


def cadastrar_pessoa(registro):
    limpar_tela()
    print("--- Cadastro de Nova Pessoa ---")
    print("1. Aluno")
    print("2. Professor")
    print("3. Monitor")
    tipo = input(">> Escolha o perfil: ")
    
    try:
        nome = input("Nome Completo: ")
        conta_ativa = True #
        
        if tipo == '1':
            curso = input("Curso: ")
            faltas = int(input("Quantidade de Faltas: "))
            notas = [float(input(f"Nota {i+1}: ")) for i in range(4)]
            pessoa = Aluno(nome, conta_ativa, curso, faltas)
            pessoa.atualizar_notas(notas)
        elif tipo == '2':
            salario = float(input("Salário (R$): "))
            qtde_materias = int(input("Quantidade de Matérias: "))
            pessoa = Professor(nome, conta_ativa, salario, qtde_materias)
        elif tipo == '3':
            valor_bolsa = float(input("Valor da Bolsa (R$): "))
            carga_horaria = int(input("Carga Horária Semanal (h): "))
            pessoa = Monitor(nome, conta_ativa, valor_bolsa, carga_horaria)
        else:
            print("\nOpção de perfil inválida.")
            return

        registro.inserir(pessoa)
        print(f"\n✅ {pessoa.get_tipo_entidade()} '{nome}' cadastrado com sucesso!")
        print(f"Matrícula gerada: {pessoa.matricula}")

    except (ValueError, ErroMatricula) as e:
        print(f"\n❌ Erro de entrada ou validação: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")

def listar_pessoas(registro, lista=None, titulo=""):
    limpar_tela()
    print(f"--- {titulo} ---")
    
    pessoas_para_listar = lista if lista is not None else registro.get_todos()

    if not pessoas_para_listar:
        print("Nenhum registro encontrado.")
    else:
        for pessoa in pessoas_para_listar:
            print(str(pessoa))
            print("-" * 25)

def atualizar_pessoa(registro):
    limpar_tela()
    print("--- Atualizar Dados ---")
    matricula = input("Digite a matrícula da pessoa a ser atualizada: ")
    try:
        pessoa = registro.buscar(matricula)
        print(f"\nEditando: {pessoa.nome} ({pessoa.get_tipo_entidade()})")
        
        # Lógica de atualização específica para cada tipo
        if isinstance(pessoa, Aluno):
            pessoa.nome = input(f"Nome Atual: {pessoa.nome}\nNovo Nome: ") or pessoa.nome
            pessoa.curso = input(f"Curso Atual: {pessoa.curso}\nNovo Curso: ") or pessoa.curso
            pessoa.faltas = int(input(f"Faltas Atuais: {pessoa.faltas}\nNovas Faltas: ") or pessoa.faltas)
            novas_notas = [float(input(f"Nota {i+1} Atual: {pessoa.notas[i] if i < len(pessoa.notas) else 'N/A'}\nNova Nota {i+1}: ") or (pessoa.notas[i] if i < len(pessoa.notas) else 0.0)) for i in range(4)]
            pessoa.atualizar_notas(novas_notas)
        elif isinstance(pessoa, Professor):
            pessoa.nome = input(f"Nome Atual: {pessoa.nome}\nNovo Nome: ") or pessoa.nome
            pessoa.salario = float(input(f"Salário Atual: {pessoa.salario}\nNovo Salário: ") or pessoa.salario)
            pessoa.qtde_materias = int(input(f"Qtd. Matérias Atual: {pessoa.qtde_materias}\nNova Qtd: ") or pessoa.qtde_materias)
        elif isinstance(pessoa, Monitor):
            pessoa.nome = input(f"Nome Atual: {pessoa.nome}\nNovo Nome: ") or pessoa.nome
            pessoa.valor_bolsa = float(input(f"Bolsa Atual: {pessoa.valor_bolsa}\nNovo Valor: ") or pessoa.valor_bolsa)
            pessoa.carga_horaria = int(input(f"Carga Horária Atual: {pessoa.carga_horaria}\nNova Carga: ") or pessoa.carga_horaria)
            
        print("\n✅ Dados atualizados com sucesso!")
    except (MatriculaNaoEncontradaError, ValueError) as e:
        print(f"\n❌ Erro: {e}")

def remover_pessoa(registro):
    limpar_tela()
    print("--- Remover Pessoa ---")
    matricula = input("Digite a matrícula da pessoa a ser removida: ")
    try:
        pessoa = registro.buscar(matricula)
        confirmacao = input(f"Tem certeza que deseja remover {pessoa.nome} ({pessoa.get_tipo_entidade()})? [s/n]: ").lower()
        if confirmacao == 's':
            registro.remover(matricula)
            print(f"\n✅ '{pessoa.nome}' foi removido(a) com sucesso.")
        else:
            print("\nOperação cancelada.")
    except MatriculaNaoEncontradaError as e:
        print(f"\n❌ Erro ao remover: {e}")

def mostrar_filtros_alunos(registro):
    limpar_tela()
    print("--- Filtros de Alunos ---")
    print("1. Listar Aprovados")
    print("2. Listar Reprovados por Média")
    print("3. Listar Reprovados por Falta")
    opcao = input(">> Escolha uma opção: ")

    if opcao == '1':
        listar_pessoas(registro, registro.get_alunos_por_status(aprovado=True), "Alunos Aprovados")
    elif opcao == '2':
        listar_pessoas(registro, registro.get_reprovados_por_media(), "Alunos Reprovados por Média")
    elif opcao == '3':
        listar_pessoas(registro, registro.get_reprovados_por_falta(), "Alunos Reprovados por Falta")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    registro_principal = Registro()
    carregar_dados(registro_principal)
    pausar()
    
    while True:
        limpar_tela()
        print("--- SISGA - MENU PRINCIPAL (VERSÃO TERMINAL) ---")
        print("\n1. Cadastrar Nova Pessoa")
        print("2. Listar Todos os Registros")
        print("3. Atualizar Dados de uma Pessoa")
        print("4. Remover Pessoa")
        print("5. Filtros de Alunos")
        print("\n0. Salvar e Sair")

        opcao = input("\n>> Digite sua opção: ")

        if opcao == '1':
            cadastrar_pessoa(registro_principal)
        elif opcao == '2':
            listar_pessoas(registro_principal, titulo="Lista de Todos os Registros")
        elif opcao == '3':
            atualizar_pessoa(registro_principal)
        elif opcao == '4':
            remover_pessoa(registro_principal)
        elif opcao == '5':
            mostrar_filtros_alunos(registro_principal)
        elif opcao == '0':
            salvar_dados(registro_principal)
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        pausar()