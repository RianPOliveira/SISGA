import streamlit as st
import pandas as pd
from POO.registro import Registro
from POO.aluno import Aluno
from POO.professor import Professor
from POO.monitor import Monitor
from POO.curso import Curso
from POO.registro_cursos import RegistroCursos
from POO.exceptions import ErroMatricula

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="SISGA", page_icon="🎓")
st.title("🎓 SISGA - Sistema de Gestão Acadêmica")

# --- Gerenciamento de Estado (Session State) ---
if 'registro_pessoas' not in st.session_state:
    st.session_state.registro_pessoas = Registro()
if 'registro_cursos' not in st.session_state:
    st.session_state.registro_cursos = RegistroCursos("cursos.txt")

if 'dados_carregados' not in st.session_state:
    try:
        with open("registros.txt", 'r', encoding='utf-8') as f:
            for linha in f:
                if not linha.strip(): continue
                partes = linha.strip().split(',')
                tipo, matricula, nome, conta_ativa = partes[0], partes[1], partes[2], partes[3] == 'True'
                if tipo == 'ALUNO':
                    nome_curso, creditos, faltas = partes[4], int(partes[5]), int(partes[6])
                    curso_obj = st.session_state.registro_cursos.getCursoPorNome(nome_curso)
                    notas = [float(n) for n in partes[7:] if n]
                    pessoa = Aluno(nome, conta_ativa, curso_obj, creditos, faltas, matricula)
                    pessoa.atualizarNotas(notas)
                elif tipo == 'PROFESSOR':
                    salario, qtde_materias = float(partes[4]), int(partes[5])
                    pessoa = Professor(nome, conta_ativa, salario, qtde_materias, matricula)
                elif tipo == 'MONITOR':
                    valor_bolsa, carga_horaria = float(partes[4]), int(partes[5])
                    pessoa = Monitor(nome, conta_ativa, valor_bolsa, carga_horaria, matricula)
                else: continue
                st.session_state.registro_pessoas.inserir(pessoa)
        st.session_state.dados_carregados = True
    except FileNotFoundError:
        st.session_state.dados_carregados = True
    except Exception as e:
        st.error(f"Erro crítico ao carregar registros: {e}")

if 'view' not in st.session_state: st.session_state.view = 'list_all'
if 'person_to_edit' not in st.session_state: st.session_state.person_to_edit = None

def salvar_dados_pessoas():
    try:
        with open("registros.txt", 'w', encoding='utf-8') as f:
            for pessoa in st.session_state.registro_pessoas.getTodos():
                tipo = pessoa.__class__.__name__.upper()
                base_info = f"{tipo},{pessoa.getMatricula()},{pessoa.getNome()},{pessoa.getContaAtiva()}"
                if isinstance(pessoa, Aluno):
                    notas_str = ",".join(map(str, pessoa.getNotas()))
                    f.write(f"{base_info},{pessoa.getCurso().getNome()},{pessoa.getCreditos()},{pessoa.getFaltas()},{notas_str}\n")
                elif isinstance(pessoa, Professor):
                    f.write(f"{base_info},{pessoa.getSalario()},{pessoa.getQtdeMaterias()}\n")
                elif isinstance(pessoa, Monitor):
                    f.write(f"{base_info},{pessoa.getValorBolsa()},{pessoa.getCargaHoraria()}\n")
    except IOError as e: st.error(f"Erro ao salvar dados de pessoas: {e}")

def salvar_dados_cursos():
    try:
        st.session_state.registro_cursos.salvarCursos()
    except Exception as e:
        st.error(f"Erro ao salvar cursos: {e}")


st.sidebar.header("Menu de Opções")
st.sidebar.subheader("Gerenciar Pessoas"); 
if st.sidebar.button("Cadastrar Pessoa", use_container_width=True): st.session_state.view = 'add_person'; st.session_state.person_to_edit = None
if st.sidebar.button("Atualizar Pessoa", use_container_width=True): st.session_state.view = 'update_person'; st.session_state.person_to_edit = None
if st.sidebar.button("Remover Pessoa", use_container_width=True): st.session_state.view = 'remove_person'; st.session_state.person_to_edit = None
st.sidebar.subheader("Gerenciar Cursos"); 
if st.sidebar.button("Listar Cursos", use_container_width=True): st.session_state.view = 'list_courses'
if st.sidebar.button("Cadastrar Curso", use_container_width=True): st.session_state.view = 'add_course'
st.sidebar.subheader("Filtros de Alunos"); 
if st.sidebar.button("Listar Todos", use_container_width=True, type="primary"): st.session_state.view = 'list_all'; st.session_state.person_to_edit = None
if st.sidebar.button("Mostrar Aprovados", use_container_width=True): st.session_state.view = 'list_approved'; st.session_state.person_to_edit = None
if st.sidebar.button("Mostrar Reprovados por Média", use_container_width=True): st.session_state.view = 'list_failed_grade'; st.session_state.person_to_edit = None
if st.sidebar.button("Mostrar Reprovados por Falta", use_container_width=True): st.session_state.view = 'list_failed_absence'; st.session_state.person_to_edit = None

# Renderização da Página Principal 

if st.session_state.view in ['list_all', 'list_approved', 'list_failed_grade', 'list_failed_absence']:
    st.header("Visão Geral dos Registros")
    lista_atual = []
    if st.session_state.view == 'list_all': lista_atual = st.session_state.registro_pessoas.getTodos()
    elif st.session_state.view == 'list_approved': lista_atual = st.session_state.registro_pessoas.getAlunosPorStatus(aprovado=True)
    elif st.session_state.view == 'list_failed_grade': lista_atual = st.session_state.registro_pessoas.getReprovadosPorMedia()
    elif st.session_state.view == 'list_failed_absence': lista_atual = st.session_state.registro_pessoas.getReprovadosPorFalta()
    if not lista_atual: st.info("Nenhum registro encontrado para este filtro.")
    else:
        dados_para_tabela = []
        for p in lista_atual:
            info = { "Matrícula": p.getMatricula(), "Nome": p.getNome(), "Função": p.getTipoEntidade()}
            if isinstance(p, Aluno):
                info["Curso"] = p.getCurso().getNome(); info["Créditos"] = f"{p.getCreditos()}/{p.getCurso().getCreditosNecessarios()}"; info["Média"] = f"{p.calcularMedia():.2f}"
            dados_para_tabela.append(info)
        df = pd.DataFrame(dados_para_tabela); st.dataframe(df, use_container_width=True, hide_index=True)

elif st.session_state.view == 'list_courses':
    st.header("Cursos Disponíveis")
    cursos = st.session_state.registro_cursos.getTodosOsCursos()
    if not cursos: st.info("Nenhum curso cadastrado.")
    else:
        dados_cursos = [{"Nome do Curso": c.getNome(), "Créditos para Formatura": c.getCreditosNecessarios()} for c in cursos]
        df_cursos = pd.DataFrame(dados_cursos); st.dataframe(df_cursos, use_container_width=True, hide_index=True)

elif st.session_state.view == 'add_course':
    st.header("Cadastrar Novo Curso")
    with st.form("course_form", clear_on_submit=True):
        nome_curso = st.text_input("Nome do Curso"); creditos = st.number_input("Créditos Necessários", min_value=1, step=1)
        if st.form_submit_button("Salvar Curso"):
            try:
                novo_curso = Curso(nome_curso, creditos)
                # --- CORREÇÃO AQUI ---
                st.session_state.registro_cursos.inserirCurso(novo_curso)
                salvar_dados_cursos()
                st.success(f"Curso '{nome_curso}' adicionado com sucesso!")
            except Exception as e: st.error(f"Erro ao salvar curso: {e}")

elif st.session_state.view == 'add_person':
    st.header("Cadastro de Nova Pessoa")
    tipo_pessoa = st.selectbox("Selecione o Perfil", ["Aluno", "Professor", "Monitor"])
    
    if tipo_pessoa == "Aluno":
        cursos_disponiveis = st.session_state.registro_cursos.getNomesDosCursos()
        if not cursos_disponiveis: st.warning("Nenhum curso cadastrado. Por favor, cadastre um curso antes de adicionar um aluno.")
        else:
            with st.form(key="aluno_add_form"):
                nome = st.text_input("Nome do Aluno"); curso_selecionado_nome = st.selectbox("Curso", options=cursos_disponiveis)
                creditos = st.number_input("Créditos Cursados", min_value=0, step=1); faltas = st.number_input("Faltas", 0, step=1)
                st.markdown("---"); cols = st.columns(4)
                n1 = cols[0].number_input("Nota 1", 0.0, 10.0, 0.0, 0.5); n2 = cols[1].number_input("Nota 2", 0.0, 10.0, 0.0, 0.5)
                n3 = cols[2].number_input("Nota 3", 0.0, 10.0, 0.0, 0.5); n4 = cols[3].number_input("Nota 4", 0.0, 10.0, 0.0, 0.5)
                if st.form_submit_button("Cadastrar Aluno"):
                    try:
                        curso_obj = st.session_state.registro_cursos.getCursoPorNome(curso_selecionado_nome)
                        aluno = Aluno(nome, True, curso_obj, creditos, faltas); aluno.atualizarNotas([n1,n2,n3,n4])
                        st.session_state.registro_pessoas.inserir(aluno); salvar_dados_pessoas()
                        st.success(f"Aluno {nome} cadastrado!"); st.session_state.view = 'list_all'; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")
    elif tipo_pessoa == "Professor":
        with st.form(key="prof_add_form", clear_on_submit=True):
            nome = st.text_input("Nome do Professor"); salario = st.number_input("Salário (R$)", min_value=0.0, step=100.0)
            qtde_materias = st.number_input("Quantidade de Matérias", min_value=0, step=1)
            if st.form_submit_button("Cadastrar Professor"):
                try:
                    prof = Professor(nome, True, salario, qtde_materias); st.session_state.registro_pessoas.inserir(prof); salvar_dados_pessoas()
                    st.success(f"Professor {nome} cadastrado!"); st.session_state.view = 'list_all'; st.rerun()
                except Exception as e: st.error(f"Erro: {e}")
    elif tipo_pessoa == "Monitor":
        with st.form(key="monitor_add_form", clear_on_submit=True):
            nome = st.text_input("Nome do Monitor"); valor_bolsa = st.number_input("Valor da Bolsa (R$)", min_value=0.0, step=50.0)
            carga_horaria = st.number_input("Carga Horária Semanal (h)", min_value=0, step=1)
            if st.form_submit_button("Cadastrar Monitor"):
                try:
                    monitor = Monitor(nome, True, valor_bolsa, carga_horaria); st.session_state.registro_pessoas.inserir(monitor); salvar_dados_pessoas()
                    st.success(f"Monitor {nome} cadastrado!"); st.session_state.view = 'list_all'; st.rerun()
                except Exception as e: st.error(f"Erro: {e}")

elif st.session_state.view == 'update_person':
    st.header("Atualizar Dados de Pessoa")
    matricula_para_editar = st.text_input("Digite a Matrícula da pessoa que deseja editar:", key="update_matricula_input")
    if matricula_para_editar:
        try: st.session_state.person_to_edit = st.session_state.registro_pessoas.buscar(matricula_para_editar)
        except Exception: st.warning("Matrícula não encontrada."); st.session_state.person_to_edit = None
            
    if st.session_state.person_to_edit:
        pessoa = st.session_state.person_to_edit
        st.subheader(f"Editando: {pessoa.getNome()} ({pessoa.getTipoEntidade()})")
        if isinstance(pessoa, Aluno):
            with st.form(key="aluno_edit_form"):
                nome = st.text_input("Nome", value=pessoa.getNome()); 
                cursos_disponiveis = st.session_state.registro_cursos.getNomesDosCursos()
                curso_atual_index = cursos_disponiveis.index(pessoa.getCurso().getNome()) if pessoa.getCurso().getNome() in cursos_disponiveis else 0
                curso_selecionado_nome = st.selectbox("Curso", options=cursos_disponiveis, index=curso_atual_index)
                creditos = st.number_input("Créditos Cursados", min_value=0, value=pessoa.getCreditos(), step=1); faltas = st.number_input("Faltas", 0, value=pessoa.getFaltas(), step=1)
                st.markdown("---"); cols = st.columns(4)
                notas_atuais = pessoa.getNotas() + [0.0] * (4 - len(pessoa.getNotas()))
                n1=cols[0].number_input("Nota 1",0.0,10.0,float(notas_atuais[0]),0.5); n2=cols[1].number_input("Nota 2",0.0,10.0,float(notas_atuais[1]),0.5)
                n3=cols[2].number_input("Nota 3",0.0,10.0,float(notas_atuais[2]),0.5); n4=cols[3].number_input("Nota 4",0.0,10.0,float(notas_atuais[3]),0.5)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        curso_obj = st.session_state.registro_cursos.getCursoPorNome(curso_selecionado_nome)
                        pessoa.setNome(nome); pessoa.setCurso(curso_obj); pessoa.setCreditos(creditos); pessoa.setFaltas(faltas); pessoa.atualizarNotas([n1, n2, n3, n4])
                        salvar_dados_pessoas(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")
        elif isinstance(pessoa, Professor):
            with st.form(key="prof_edit_form"):
                nome = st.text_input("Nome", value=pessoa.getNome()); salario = st.number_input("Salário (R$)", min_value=0.0, value=float(pessoa.getSalario()), step=100.0)
                qtde_materias = st.number_input("Quantidade de Matérias", min_value=0, value=pessoa.getQtdeMaterias(), step=1)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        pessoa.setNome(nome); pessoa.setSalario(salario); pessoa.setQtdeMaterias(qtde_materias)
                        salvar_dados_pessoas(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")
        elif isinstance(pessoa, Monitor):
            with st.form(key="monitor_edit_form"):
                nome = st.text_input("Nome", value=pessoa.getNome()); valor_bolsa = st.number_input("Valor da Bolsa (R$)", min_value=0.0, value=float(pessoa.getValorBolsa()), step=50.0)
                carga_horaria = st.number_input("Carga Horária Semanal (h)", min_value=0, value=pessoa.getCargaHoraria(), step=1)
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        pessoa.setNome(nome); pessoa.setValorBolsa(valor_bolsa); pessoa.setCargaHoraria(carga_horaria)
                        salvar_dados_pessoas(); st.success(f"Dados de {nome} atualizados!"); st.session_state.view = 'list_all'; st.session_state.person_to_edit = None; st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")

elif st.session_state.view == 'remove_person':
    st.header("Remover Pessoa")
    matricula_para_remover = st.text_input("Digite a Matrícula da pessoa que deseja remover:")
    if matricula_para_remover:
        try:
            pessoa = st.session_state.registro_pessoas.buscar(matricula_para_remover)
            st.warning(f"Você tem certeza que deseja remover **{pessoa.getNome()} ({pessoa.getTipoEntidade()})**?")
            if st.button("Sim, remover", type="primary"):
                st.session_state.registro_pessoas.remover(matricula_para_remover)
                salvar_dados_pessoas(); st.success(f"{pessoa.getNome()} foi removido(a)."); st.session_state.view = 'list_all'; st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")