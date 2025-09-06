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

if 'view' not in st.session_state:
    st.session_state.view = 'list_all' 
if 'person_to_edit' not in st.session_state:
    st.session_state.person_to_edit = None

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

# Barra Lateral 
st.sidebar.header("Menu de Opções")

st.sidebar.subheader("Gerenciamento")
if st.sidebar.button("Cadastrar Nova Pessoa", use_container_width=True):
    st.session_state.view = 'add_person'
    st.session_state.person_to_edit = None 

if st.sidebar.button("Atualizar Pessoa", use_container_width=True):
    st.session_state.view = 'update_person'
    st.session_state.person_to_edit = None

if st.sidebar.button("Remover Pessoa", use_container_width=True):
    st.session_state.view = 'remove_person'
    st.session_state.person_to_edit = None

st.sidebar.subheader("Filtros e Visualização")
if st.sidebar.button("Listar Todos", use_container_width=True, type="primary"):
    st.session_state.view = 'list_all'
    st.session_state.person_to_edit = None

if st.sidebar.button("Mostrar Aprovados", use_container_width=True):
    st.session_state.view = 'list_approved'
    st.session_state.person_to_edit = None

if st.sidebar.button("Mostrar Reprovados por Média", use_container_width=True):
    st.session_state.view = 'list_failed_grade'
    st.session_state.person_to_edit = None

if st.sidebar.button("Mostrar Reprovados por Falta", use_container_width=True):
    st.session_state.view = 'list_failed_absence'
    st.session_state.person_to_edit = None

# Página Principal 
if 'list' in st.session_state.view:
    st.header("Visão Geral dos Registros")
    
    lista_atual = []
    if st.session_state.view == 'list_all':
        lista_atual = st.session_state.registro.get_todos()
    elif st.session_state.view == 'list_approved':
        lista_atual = st.session_state.registro.get_alunos_por_status(aprovado=True)
    elif st.session_state.view == 'list_failed_grade':
        lista_atual = st.session_state.registro.get_reprovados_por_media()
    elif st.session_state.view == 'list_failed_absence':
        lista_atual = st.session_state.registro.get_reprovados_por_falta()
    
    if not lista_atual:
        st.info("Nenhum registro encontrado para este filtro.")
    else:
        dados_para_tabela = []
        for p in lista_atual:
            info = { "Matrícula": p.matricula, "Nome": p.nome, "Função": p.get_tipo_entidade(), "Conta Ativa": "Sim" if p.conta_ativa else "Não" }
            if isinstance(p, Aluno):
                info["Média Final"] = f"{p.calcular_media():.2f}"
                info["Faltas"] = p.faltas
            dados_para_tabela.append(info)
        df = pd.DataFrame(dados_para_tabela)
        st.dataframe(df, use_container_width=True, hide_index=True)

elif st.session_state.view == 'add_person':
    st.header("Cadastro de Nova Pessoa")
    tipo_pessoa = st.selectbox("Selecione o Perfil", ["Aluno", "Professor", "Monitor"])
    
    if tipo_pessoa == "Aluno":
        with st.form(key="aluno_add_form", clear_on_submit=True):
            nome = st.text_input("Nome do Aluno"); curso = st.text_input("Curso")
            cols = st.columns(4)
            n1 = cols[0].number_input("Nota 1", 0.0, 10.0, 0.0, 0.5); n2 = cols[1].number_input("Nota 2", 0.0, 10.0, 0.0, 0.5)
            n3 = cols[2].number_input("Nota 3", 0.0, 10.0, 0.0, 0.5); n4 = cols[3].number_input("Nota 4", 0.0, 10.0, 0.0, 0.5)
            faltas = st.number_input("Faltas", 0, step=1)
            if st.form_submit_button("Cadastrar Aluno"):
                try:
                    aluno = Aluno(nome=nome, conta_ativa=True, curso=curso, faltas=faltas); aluno.atualizar_notas([n1,n2,n3,n4])
                    st.session_state.registro.inserir(aluno); salvar_dados()
                    st.success(f"Aluno {nome} cadastrado!"); st.session_state.view = 'list_all'
                except Exception as e: st.error(f"Erro: {e}")

    elif tipo_pessoa == "Professor":
        with st.form(key="prof_add_form", clear_on_submit=True):
            nome = st.text_input("Nome do Professor")
            salario = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
            qtde_materias = st.number_input("Quantidade de Matérias", min_value=0, step=1)
            if st.form_submit_button("Cadastrar Professor"):
                try:
                    prof = Professor(nome=nome, conta_ativa=True, salario=salario, qtde_materias=qtde_materias)
                    st.session_state.registro.inserir(prof); salvar_dados()
                    st.success(f"Professor {nome} cadastrado!"); st.session_state.view = 'list_all'
                except Exception as e: st.error(f"Erro: {e}")
    
    elif tipo_pessoa == "Monitor":
        with st.form(key="monitor_add_form", clear_on_submit=True):
            nome = st.text_input("Nome do Monitor")
            valor_bolsa = st.number_input("Valor da Bolsa (R$)", min_value=0.0, step=50.0)
            carga_horaria = st.number_input("Carga Horária Semanal (h)", min_value=0, step=1)
            if st.form_submit_button("Cadastrar Monitor"):
                try:
                    monitor = Monitor(nome=nome, conta_ativa=True, valor_bolsa=valor_bolsa, carga_horaria=carga_horaria)
                    st.session_state.registro.inserir(monitor); salvar_dados()
                    st.success(f"Monitor {nome} cadastrado!"); st.session_state.view = 'list_all'
                except Exception as e: st.error(f"Erro: {e}")

elif st.session_state.view == 'update_person':
    st.header("Atualizar Dados de Pessoa")
    matricula_para_editar = st.text_input("Digite a Matrícula da pessoa que deseja editar:", key="update_matricula_input")
    
    if matricula_para_editar:
        try:
            pessoa = st.session_state.registro.buscar(matricula_para_editar)
            st.session_state.person_to_edit = pessoa
        except Exception:
            st.warning("Matrícula não encontrada.")
            st.session_state.person_to_edit = None
            
    if st.session_state.person_to_edit:
        pessoa = st.session_state.person_to_edit
        st.subheader(f"Editando: {pessoa.nome} ({pessoa.get_tipo_entidade()})")
        
        if isinstance(pessoa, Aluno):
            with st.form(key="aluno_edit_form"):
                nome = st.text_input("Nome", value=pessoa.nome); curso = st.text_input("Curso", value=pessoa.curso)
                cols = st.columns(4)
                notas_atuais = pessoa.notas + [0.0] * (4 - len(pessoa.notas))
                n1 = cols[0].number_input("Nota 1", 0.0, 10.0, float(notas_atuais[0]), 0.5)
                n2 = cols[1].number_input("Nota 2", 0.0, 10.0, float(notas_atuais[1]), 0.5)
                n3 = cols[2].number_input("Nota 3", 0.0, 10.0, float(notas_atuais[2]), 0.5)
                n4 = cols[3].number_input("Nota 4", 0.0, 10.0, float(notas_atuais[3]), 0.5)
                faltas = st.number_input("Faltas", 0, value=pessoa.faltas, step=1)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        pessoa.nome = nome; pessoa.curso = curso; pessoa.faltas = faltas; pessoa.atualizar_notas([n1, n2, n3, n4])
                        salvar_dados(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")

        elif isinstance(pessoa, Professor):
            with st.form(key="prof_edit_form"):
                nome = st.text_input("Nome", value=pessoa.nome)
                salario = st.number_input("Salário (R$)", min_value=0.0, value=float(pessoa.salario), step=100.0)
                qtde_materias = st.number_input("Quantidade de Matérias", min_value=0, value=pessoa.qtde_materias, step=1)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        pessoa.nome = nome; pessoa.salario = salario; pessoa.qtde_materias = qtde_materias
                        salvar_dados(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")

        elif isinstance(pessoa, Monitor):
            with st.form(key="monitor_edit_form"):
                nome = st.text_input("Nome", value=pessoa.nome)
                valor_bolsa = st.number_input("Valor da Bolsa (R$)", min_value=0.0, value=float(pessoa.valor_bolsa), step=50.0)
                carga_horaria = st.number_input("Carga Horária Semanal (h)", min_value=0, value=pessoa.carga_horaria, step=1)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        pessoa.nome = nome; pessoa.valor_bolsa = valor_bolsa; pessoa.carga_horaria = carga_horaria
                        salvar_dados(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")

elif st.session_state.view == 'remove_person':
    st.header("Remover Pessoa")
    matricula_para_remover = st.text_input("Digite a Matrícula da pessoa que deseja remover:")
    if matricula_para_remover:
        try:
            pessoa = st.session_state.registro.buscar(matricula_para_remover)
            st.warning(f"Você tem certeza que deseja remover **{pessoa.nome} ({pessoa.get_tipo_entidade()})**?")
            if st.button("Sim, remover", type="primary"):
                st.session_state.registro.remover(matricula_para_remover)
                salvar_dados(); st.success(f"{pessoa.nome} foi removido(a)."); st.session_state.view = 'list_all'; st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")