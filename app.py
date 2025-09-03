import streamlit as st
import pandas as pd
from POO.registro import Registro
from POO.aluno import Aluno
from POO.professor import Professor
from POO.monitor import Monitor

st.set_page_config(layout="wide", page_title="SISGA", page_icon="🎓")
st.title("🎓 SISGA - Sistema de Gestão Acadêmica")

if 'registro' not in st.session_state:
    st.session_state.registro = Registro()
    try:
        with open("registros.txt", 'r') as f:
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
                st.session_state.registro.inserir(pessoa)
    except FileNotFoundError:
        pass 

def salvar_dados():
    """Função para salvar os dados no arquivo."""
    try:
        with open("registros.txt", 'w') as f:
            for pessoa in st.session_state.registro.get_todos():
                tipo = pessoa.__class__.__name__.upper()
                base_info = f"{tipo},{pessoa.matricula},{pessoa.nome},{pessoa.conta_ativa}"
                if isinstance(pessoa, Aluno):
                    notas_str = ",".join(map(str, pessoa.notas))
                    f.write(f"{base_info},{pessoa.curso},{pessoa.faltas},{notas_str}\n")
                elif isinstance(pessoa, Professor):
                    f.write(f"{base_info},{pessoa.salario},{pessoa.qtde_materias}\n")
                elif isinstance(pessoa, Monitor):
                    f.write(f"{base_info},{pessoa.valor_bolsa},{pessoa.carga_horaria}\n")
    except IOError as e:
        st.error(f"Erro ao salvar dados: {e}")


st.sidebar.header("Menu de Opções")
acao = st.sidebar.selectbox("O que deseja fazer?", ["Listar Todos", "Cadastrar Nova Pessoa", "Remover Pessoa"])

if acao == "Cadastrar Nova Pessoa":
    st.sidebar.subheader("Formulário de Cadastro")
    tipo_pessoa = st.sidebar.selectbox("Selecione o Perfil", ["Aluno", "Professor", "Monitor"])

    with st.sidebar.form(key="cadastro_form", clear_on_submit=True):
        if tipo_pessoa == "Aluno":
            nome = st.text_input("Nome do Aluno")
            curso = st.text_input("Curso")
            n1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
            n2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
            n3 = st.number_input("Nota 3", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
            n4 = st.number_input("Nota 4", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
            faltas = st.number_input("Faltas", min_value=0, step=1, value=0)
            
            if st.form_submit_button("Cadastrar Aluno"):
                try:
                    novo_aluno = Aluno(nome=nome, conta_ativa=True, curso=curso, faltas=faltas)
                    novo_aluno.atualizar_notas([n1, n2, n3, n4])
                    st.session_state.registro.inserir(novo_aluno)
                    salvar_dados()
                    st.success(f"Aluno {nome} cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")

        elif tipo_pessoa == "Professor":
            nome = st.text_input("Nome do Professor")
            salario = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
            qtde_materias = st.number_input("Quantidade de Matérias", min_value=0, step=1)
            
            if st.form_submit_button("Cadastrar Professor"):
                try:
                    novo_prof = Professor(nome=nome, conta_ativa=True, salario=salario, qtde_materias=qtde_materias)
                    st.session_state.registro.inserir(novo_prof)
                    salvar_dados()
                    st.success(f"Professor {nome} cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")
        
        elif tipo_pessoa == "Monitor":
            nome = st.text_input("Nome do Monitor")
            valor_bolsa = st.number_input("Valor da Bolsa (R$)", min_value=0.0, step=50.0)
            carga_horaria = st.number_input("Carga Horária Semanal (h)", min_value=0, step=1)

            if st.form_submit_button("Cadastrar Monitor"):
                try:
                    novo_monitor = Monitor(nome=nome, conta_ativa=True, valor_bolsa=valor_bolsa, carga_horaria=carga_horaria)
                    st.session_state.registro.inserir(novo_monitor)
                    salvar_dados()
                    st.success(f"Monitor {nome} cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")

elif acao == "Remover Pessoa":
    st.sidebar.subheader("Remover por Matrícula")
    matricula_para_remover = st.sidebar.text_input("Digite a Matrícula")
    if st.sidebar.button("Remover"):
        try:
            pessoa_removida = st.session_state.registro.remover(matricula_para_remover)
            salvar_dados()
            st.success(f"{pessoa_removida.get_tipo_entidade()} '{pessoa_removida.nome}' foi removido(a).")
        except Exception as e:
            st.error(f"Erro ao remover: {e}")

st.header("Visão Geral")

todos = st.session_state.registro.get_todos()
if not todos:
    st.info("Nenhum registro encontrado. Cadastre uma nova pessoa na barra lateral.")
else:
    dados_para_tabela = []
    for p in todos:
        info = {
            "Matrícula": p.matricula,
            "Nome": p.nome,
            "Função": p.get_tipo_entidade(),
            "Conta Ativa": "Sim" if p.conta_ativa else "Não"
        }
        if isinstance(p, Aluno):
            info["Média Final"] = f"{p.calcular_media():.2f}"
            info["Faltas"] = p.faltas
        dados_para_tabela.append(info)

    df = pd.DataFrame(dados_para_tabela)
    st.dataframe(df, use_container_width=True)