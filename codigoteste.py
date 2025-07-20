import os
from tabulate import tabulate

qtdalunos = 30
alunoscadastrados = -1
alunos = []
notas = []


def menu():
    menu = [
        "\n1 - Cadastrar um Aluno\n",
        "2 - Remover um Aluno\n",
        "3 - Atualizar Dados\n",
        "4 - Listar Alunos Cadastrados\n",
        "5 - Listar Aprovados\n",
        "6 - Listar Reprovados por Média\n",
        "7 - Listar Reprovados por Faltas\n",
        "8 - Exibir Alunos por [..]\n",
        "9 - Apagar Todos os Dados Cadastrados\n",
        "10 - Desenvolvedores & Agradecimentos\n",
        "11 - Sair do Programa\n"
    ]
    titulo = "SISGA - Menu:"
    print(f"{linha}\n{titulo.center(100)}\n{''.join(menu)}{linha}")


def CadastroAluno():

    global alunoscadastrados

    if alunoscadastrados == qtdalunos:
        limitealunos()
    else:
        os.system('cls')
        print(linha)
        print('CADASTRO DE ALUNOS'.center(100))
        print(linha)

        while True:
            matricula = input('\n- Insira sua matrícula: ')

            if matricula in [a['Matricula'] for a in alunos]:
                os.system('cls')
                print(linha)
                print('ALUNO JÁ CADASTRADO NO SISTEMA!'.center(100))
                print(linha)
            else:
                nome = input("Insira o nome do aluno: ")
                codigo_turma = input("Insira o código da turma: ")

                notas = []
                i = 0
                while i < 4:
                    nota = float(input(f"Insira a nota {i+1} do aluno: "))
                    if nota < 0 or nota > 10:
                        os.system('cls')
                        print(linha)
                        print('NOTA INVÁLIDA!'.center(100))
                        print(linha)
                        print('- Insira um número de 0 a 10.')
                    else:
                        notas.append(nota)
                        i += 1
                media = sum(notas) / 4

                while True:
                    faltas = float(
                        input("Insira a quantidade de faltas do aluno: "))
                    if faltas > 36 or faltas < 0:
                        os.system('cls')
                        print(linha)
                        print("FREQUÊNCIA INVÁLIDA!".center(100))
                        print(linha)
                        print("- Digite o numero de faltas entre 0 a 36.")
                        print(linha)
                    else:
                        break

                alunos.append({
                    'Matricula': matricula,
                    'Nome': nome,
                    'Turma': codigo_turma,
                    'Notas': notas,
                    'Faltas': faltas,
                    'Media': media
                })
                os.system('cls')
                print(linha)
                print('ALUNO CADASTRADO COM SUCESSO!'.center(100))
                alunoscadastrados += 1
                EscreverAlunos()
                break


def RemoveAluno():
    os.system('cls')
    global alunoscadastrados

    if alunoscadastrados == -1:
        semalunos()
    else:
        print(linha)
        print('REMOÇÃO DE ALUNO'.center(100))
        print(linha)

        removmatricula = input("\nDigite o número da matricula: ")
        matricula_encontrada = False

        for i in range(len(alunos)):
            if alunos[i]['Matricula'] == removmatricula:
                os.system('cls')
                del alunos[i]
                alunoscadastrados -= 1
                print(linha)
                EscreverAlunos()
                print('ALUNO REMOVIDO COM SUCESSO!'.center(100))
                matricula_encontrada = True
                break

            if not matricula_encontrada:
                os.system('cls')
                print(linha)
                print('MATRICULA INEXISTEMTE!'.center(100))


def AtualizaDados():
    global alunoscadastrados

    if alunoscadastrados == -1:
        semalunos()
    else:
        os.system('cls')
        print(linha)
        print('ATUALIZAR DADOS DO ALUNO'.center(100))
        print(linha)
        indicealuno = -1
        matriculatemp = input('\n- Insira a matrícula: ')
        matriculaencontrada = False
        cabecalho = ['MATRICULAS', 'NOMES',
                     'TURMAS', 'NOTAS', 'FALTAS', 'MEDIAS']

        for i in range(len(alunos)):
            if alunos[i]['Matricula'] == matriculatemp:
                indicealuno = i
                os.system('cls')
                print(linha)
                print('ALUNO ENCONTRADO!'.center(100))
                print(linha)
                print(tabulate([alunos[i]], headers=dict.fromkeys(
                    cabecalho), tablefmt='fancy_grid'))
                print(linha)
                while True:

                    print('QUAL DADO DESEJA ALTERAR?'.center(100))
                    print(linha)
                    print(
                        '1- Nome | 2- Codigo da Turma | 3- Notas | 4- Faltas  | 5- Retornar ao Menu Principal'.center(100))
                    menuopcoes2 = input("\n- Insira uma opção válida: ")
                    while not menuopcoes2.isdigit():
                        mensagemerro()
                        print(linha)
                        print('QUAL DADO DESEJA ALTERAR?'.center(100))
                        print(linha)
                        print(
                            '1- Nome | 2- Codigo da Turma | 3- Notas | 4- Faltas  | 5- Retornar ao Menu Principal'.center(100))
                        menuopcoes2 = input("\n- Insira uma opção válida: ")
                    menuopcoes2 = int(menuopcoes2)
                    if menuopcoes2 < 1 or menuopcoes2 > 5:
                        mensagemerro()
                        print(linha)
                    if menuopcoes2 == 1:
                        os.system('cls')
                        nome = input("Insira o nome do aluno: ")
                        alunos[i]['Nome'] = nome
                        print(linha)
                        EscreverAlunos()
                        print('NOME ATUALIZADO COM SUCESSO!'.center(100))
                        matriculaencontrada = True

                    elif menuopcoes2 == 2:
                        os.system('cls')
                        codigo_turma = input("Insira o código da turma: ")
                        alunos[i]['Turma'] = codigo_turma
                        print(linha)
                        EscreverAlunos()
                        print('TURMA ATUALIZADA COM SUCESSO!'.center(100))
                        matriculaencontrada = True
                    elif menuopcoes2 == 3:
                        os.system('cls')
                        i = 0
                        while i < 4:
                            nota = float(
                                input(f"Insira a nota {i+1} do aluno: "))
                            if nota < 0 or nota > 10:
                                os.system('cls')
                                print(linha)
                                print('NOTA INVÁLIDA!'.center(100))
                                print(linha)
                                print('- Insira um número de 0 a 10.')
                            else:
                                notas.append(nota)
                                i += 1

                        media = sum(notas) / 4

                        alunos[indicealuno]['Notas'] = notas
                        alunos[indicealuno]['Media'] = media

                        print(linha)
                        EscreverAlunos()
                        print('NOTAS ATUALIZADAS COM SUCESSO!'.center(100))
                        matriculaencontrada = True
                    elif menuopcoes2 == 4:
                        os.system('cls')
                        while True:
                            faltas = int(
                                input("Insira a quantidade de faltas do aluno: "))
                            if faltas > 36 or faltas < 0:
                                os.system('cls')
                                print(linha)
                                print("FREQUÊNCIA INVÁLIDA!".center(100))
                                print(linha)
                                print("- Digite o numero de faltas entre 0 a 36.")
                                print(linha)
                            else:
                                break
                        alunos[indicealuno]['Faltas'] = faltas
                        print(linha)
                        EscreverAlunos()
                        print('FREQUÊNCIA ATUALIZADa COM SUCESSO!'.center(100))
                        matriculaencontrada = True
                    elif menuopcoes2 == 5:
                        os.system('cls')
                        break
            if not matriculaencontrada:
                os.system('cls')
                print(linha)
                print('MATRICULA INEXISTEMTE!'.center(100))


def AlunosCadastrados():
    os.system('cls')
    global alunoscadastrados

    cabecalho = ['MATRICULAS', 'NOMES', 'TURMAS', 'NOTAS', 'FALTAS', 'MEDIAS']

    if alunoscadastrados == qtdalunos:
        limitealunos()
    elif alunoscadastrados == -1:
        semalunos()
    else:
        print(tabulate(alunos, headers=dict.fromkeys(
            cabecalho), tablefmt='fancy_grid'))


def AlunosAprovados():
    os.system('cls')
    global alunoscadastrados
    cabecalho = ['MATRICULAS', 'NOMES', 'TURMAS', 'NOTAS', 'FALTAS', 'MEDIAS']

    if alunoscadastrados == -1:
        semalunos()
    else:
        alunos_aprovados = []
        for i in range(len(alunos)):
            if alunos[i]['Media'] >= 7 and alunos[i]['Faltas'] <= 21.6:
                alunos_aprovados.append(alunos[i])
        if len(alunos_aprovados) > 0:
            print(linha)
            print('ALUNOS APROVADOS'.center(100))
            print(linha)
            print('- OS ALUNOS ABAIXO (SE HOUVER) FORAM APROVADOS POR TEREM UMA MÉDIA \nSUPERIOR OU IGUAL A 7 PONTOS E FREQUÊNCIA MAIOR OU IGUAL A 60 %.\n')
            print(tabulate(alunos_aprovados, headers=dict.fromkeys(
                cabecalho), tablefmt='fancy_grid'))
        else:
            print(linha)
            print('NÃO HÁ ALUNOS APROVADOS NO SISTEMA'.center(100))


def ReprovadosMedia():
    os.system('cls')
    global alunoscadastrados
    cabecalho = ['MATRICULAS', 'NOMES', 'TURMAS', 'NOTAS', 'FALTAS', 'MEDIAS']

    if alunoscadastrados == -1:
        semalunos()
    else:
        alunosreprovados = []
        for i in range(len(alunos)):
            if alunos[i]['Media'] < 7:
                alunosreprovados.append(alunos[i])
        if len(alunosreprovados) > 0:
            print(linha)
            print('ALUNOS REPROVADOS POR MÉDIA'.center(100))
            print(linha)
            print(
                '- OS ALUNOS ABAIXO (SE HOUVER) FORAM REPROVADOS POR TEREM UMA MÉDIA INFERIOR A 7 PONTOS.\n')
            print(tabulate(alunosreprovados, headers=dict.fromkeys(
                cabecalho), tablefmt='fancy_grid'))
        else:
            print(linha)
            print('NÃO HÁ ALUNOS REPROVADOS PELA MÉDIA NO SISTEMA'.center(100))


def ReprovadosFaltas():
    os.system('cls')
    global alunoscadastrados
    cabecalho = ['MATRICULAS', 'NOMES', 'TURMAS', 'NOTAS', 'FALTAS', 'MEDIAS']

    if alunoscadastrados == -1:
        semalunos()
    else:
        alunosreprovadosfaltas = []
        for i in range(len(alunos)):
            if alunos[i]['Faltas'] > 21.6:
                alunosreprovadosfaltas.append(alunos[i])
        if len(alunosreprovadosfaltas) > 0:
            print(linha)
            print('ALUNOS REPROVADOS POR MÉDIA'.center(100))
            print(linha)
            print(
                '- OS ALUNOS ABAIXO (SE HOUVER) FORAM REPROVADOS POR TEREM FREQUÊNCIA ABAIXO DE 60 %.\n')
            print(tabulate(alunosreprovadosfaltas, headers=dict.fromkeys(
                cabecalho), tablefmt='fancy_grid'))
        else:
            print(linha)
            print('NÃO HÁ ALUNOS REPROVADOS POR FALTAS NO SISTEMA'.center(100))


def Ordenacao():
    os.system('cls')
    global alunoscadastrados

    if alunoscadastrados == -1:
        semalunos()
    else:
        print(linha)
        print('ORDENAÇÃO DE ALUNOS'.center(100))
        print(linha)

        while True:
            print("- Escolha uma das opções abaixo caso deseje ordenar os dados cadastrados \nem ordem crescente ou alfabética pelos seguintes parâmetros:")
            print(linha)
            print("1 - Exibir por Matrícula\n2 - Exibir por Nome\n3 - Exibir por Turma\n4 - Exibir por Faltas\n5 - Exibir por Média \n6 - Retornar ao Menu Principal")
            print(linha)
            opcaoord = input("- Insira uma opção válida: ")
            while not opcaoord.isdigit():
                mensagemerro()
                print(linha)
                print('COMO DESEJA ORDENAR OS ALUNOS?'.center(100))
                print(linha)
                print("1 - Exibir por Matrícula\n2 - Exibir por Nome\n3 - Exibir por Turma\n4 - Exibir por Faltas\n5 - Exibir por Média \n6 - Retornar ao Menu Principal")
                print(linha)
                opcaoord = input("- Insira uma opção válida: ")
            opcaoord = int(opcaoord)
            if opcaoord < 1 or opcaoord > 6:
                mensagemerro()
                print(linha)
            elif opcaoord == 1:
                OrdenacaoMatricula()
            elif opcaoord == 2:
                OrdenacaoNome()
            elif opcaoord == 3:
                OrdenacaoTurma()
            elif opcaoord == 4:
                OrdenacaoFaltas()
            elif opcaoord == 5:
                OrdenacaoMedia()
            elif opcaoord == 6:
                os.system('cls')
                break


def OrdenacaoMatricula():
    os.system('cls')
    global alunos
    alunos = sorted(alunos, key=lambda x: x['Matricula'])
    print(linha)
    print('ALUNOS ORDENADOS PELA MATRÍCULA COM SUCESSO!'.center(100))
    print(linha)


def OrdenacaoNome():
    os.system('cls')
    global alunos
    alunos = sorted(alunos, key=lambda x: x['Nome'])
    print(linha)
    print('ALUNOS ORDENADOS PELO NOME COM SUCESSO!'.center(100))
    print(linha)


def OrdenacaoTurma():
    os.system('cls')
    global alunos
    alunos = sorted(alunos, key=lambda x: x['Nome'])
    print(linha)
    print('ALUNOS ORDENADOS PELA TURMA COM SUCESSO!'.center(100))
    print(linha)


def OrdenacaoMedia():
    os.system('cls')
    global alunos
    alunos = sorted(alunos, key=lambda x: x['Media'])
    print(linha)
    print('ALUNOS ORDENADOS PELA MÉDIA COM SUCESSO!'.center(100))
    print(linha)


def OrdenacaoFaltas():
    os.system('cls')
    global alunos
    alunos = sorted(alunos, key=lambda x: x['Faltas'])
    print(linha)
    print('ALUNOS ORDENADOS PELAS FALTAS COM SUCESSO!'.center(100))
    print(linha)


def LerDados():
    global alunos
    global arquivo
    global alunoscadastrados

    if os.path.exists('alunos.txt'):
        arquivo = open('alunos.txt', 'r')
    else:
        arquivo = open('alunos.txt', 'w+')

    for linha in arquivo:
        alunos.append({
            'Matricula': linha.strip().split(',')[0],
            'Nome': linha.strip().split(',')[1],
            'Turma': linha.strip().split(',')[2],
            'Notas': [float(nota) for nota in linha.strip().split(',')[3].split(';')],
            'Faltas': float(linha.strip().split(',')[4]),
            'Media': float(linha.strip().split(',')[5])
        })
    for i in range(len(alunos)):
        alunoscadastrados = i


def EscreverAlunos():
    global alunos
    global arquivo
    global alunoscadastrados

    with open('alunos.txt', 'w+') as arquivo:
        for aluno in alunos:
            linha = f"{aluno['Matricula']},{aluno['Nome']},{aluno['Turma']},{';'.join(map(str, aluno['Notas']))},{aluno['Faltas']},{aluno['Media']:.2f}\n"
            arquivo.write(linha)


def ApagarDados():
    os.system('cls')
    global alunoscadastrados
    global arquivo
    global alunos
    global notas

    if alunoscadastrados == -1:
        semalunos()
    else:
        while True:
            print(linha)
            print('DESEJA EXCLUIR TODOS OS DADOS CADASTRADOS?'.center(100))
            print(linha)
            print("1 - SIM | 2 - NÃO".center(100))
            print(linha)
            opcaoord = input("- Insira uma opção válida: ")
            while not opcaoord.isdigit():
                mensagemerro()
                print(linha)
                print('DESEJA EXCLUIR TODOS OS DADOS CADASTRADOS?'.center(100))
                print(linha)
                print("1 - SIM | 2 - NÃO".center(100))
                print(linha)
                opcaoord = input("- Insira uma opção válida: ")
            opcaoord = int(opcaoord)
            if opcaoord < 1 or opcaoord > 5:
                mensagemerro()
                print(linha)
            elif opcaoord == 1:
                os.system('cls')
                with open("alunos.txt", "w") as arquivo:
                    arquivo.truncate(0)
                alunos = []
                notas = []
                print(linha)
                print('TODOS OS ALUNOS FORAM DELETADOS COM SUCESSO!'.center(100))
                alunoscadastrados = -1
                break
            elif opcaoord == 2:
                os.system('cls')
                break


def Agradecimentos():
    os.system('cls')

    print(linha)
    print('DESENVOLVEDORES E AGRADECIMENTOS'.center(100))
    print(linha)

    print("- Uma seção especial dedicada a todos que ajudaram e contribuiram "
          "com o desenvolvimento, ideias e\n tudo que se foi necessário para que "
          "este programa ganhasse vida e, posterioremente,\n tendo sua utilidade "
          "para as mais diversas finalidades no meio escolar ou acadêmico.\n"
          " Segue a listagem abaixo:\n")

    print("• RIAN PURIFICAÇÃO DE OLIVEIRA | Desenvolvedor Principal")
    print("• RENÊ PEREIRA DE GUSMÃO | Professor & Orientador")
    print("• JOSÉ EDUARDO SANTANA MACEDO | Monitor de Programação - UFS")
    print('\n', linha)
    print('SISGA - 2023 Ⓡ.'.center(100))


def mensagemerro():
    os.system('cls')
    print(linha)
    print('OPÇÃO INVÁLIDA!'.center(100))


def fimdoprograma():
    os.system('cls')
    print(linha)
    print('OBRIGADO POR UTILIZAR NOSSOS SERVIÇOS. ATÉ A PRÓXIMA!'.center(100))
    print('SISGA - 2023 Ⓡ.'.center(100))
    print(linha)


def limitealunos():
    os.system('cls')
    print(linha)
    print('LIMITE MÁXIMO DE 30 MATRICULAS ATINGIDO!'.center(100))


def semalunos():
    os.system('cls')
    print(linha)
    print('NÃO HÁ ALUNOS CADASTRADOS NO SISTEMA!'.center(100))


# Inicio do programa
LerDados()

linha = '-' * 100

print(linha)
print(
    '\nBem vindo ao SISGA - Sistema Simplificado para Gestão de Alunos.\nEscolha a opção desejada de acordo com a numeração [1 - 8] no menu abaixo:\n'.center(100))

while True:
    menu()
    menuopcoes = input("Insira uma opção válida: ")
    while not menuopcoes.isdigit():
        mensagemerro()
        menu()
        menuopcoes = input("Insira uma opção válida: ")
    menuopcoes = int(menuopcoes)
    if menuopcoes < 1 or menuopcoes > 11:
        mensagemerro()

    if menuopcoes == 1:
        CadastroAluno()
    elif menuopcoes == 2:
        RemoveAluno()
    elif menuopcoes == 3:
        AtualizaDados()
    elif menuopcoes == 4:
        AlunosCadastrados()
    elif menuopcoes == 5:
        AlunosAprovados()
    elif menuopcoes == 6:
        ReprovadosMedia()
    elif menuopcoes == 7: 
        ReprovadosFaltas()
    elif menuopcoes == 8:
        Ordenacao()
    elif menuopcoes == 9:
        ApagarDados()
    elif menuopcoes == 10:
        Agradecimentos()
    elif menuopcoes == 11:
        fimdoprograma()
        break
