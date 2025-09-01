# interface_grafica.py (Versão com Notas e Média na Tabela)

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox

from POO.aluno import Aluno
from POO.professor import Professor
from POO.monitor import Monitor
from POO.registro import Registro
from POO.exceptions import ErroMatricula, MatriculaNaoEncontradaError

class SisgaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SISGA - Sistema de Gestão Acadêmica")
        # Aumentei um pouco a largura para caber as novas colunas
        self.root.geometry("1200x600") 
        self.registro = Registro()
        self.arquivo_dados = "registros.txt"
        self._carregar_dados()
        self._criar_widgets()
        self.listar_todos()

    def _criar_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(20, 20))
        main_frame.pack(fill='both', expand=True)

        actions_frame = ttk.LabelFrame(main_frame, text="Menu de Opções", padding=(15, 15))
        actions_frame.pack(side='left', fill='y', padx=(0, 20))

        # ... (Os botões continuam os mesmos) ...
        ttk.Button(actions_frame, text="Cadastrar Pessoa", command=self._janela_selecionar_perfil, bootstyle="primary").pack(fill='x', pady=6)
        ttk.Button(actions_frame, text="Atualizar Pessoa", command=self._janela_atualizar, bootstyle="info-outline").pack(fill='x', pady=6)
        ttk.Button(actions_frame, text="Remover Pessoa", command=self._janela_remover, bootstyle="danger-outline").pack(fill='x', pady=6)
        ttk.Separator(actions_frame, orient='horizontal').pack(fill='x', pady=12)
        student_actions_frame = ttk.LabelFrame(actions_frame, text="Filtros de Alunos", padding=(10,10))
        student_actions_frame.pack(fill='x', pady=10)
        ttk.Button(student_actions_frame, text="Listar Aprovados", command=self.listar_aprovados, bootstyle="success").pack(fill='x', pady=5)
        ttk.Button(student_actions_frame, text="Reprovados por Média", command=self.listar_reprovados_media, bootstyle="warning").pack(fill='x', pady=5)
        ttk.Button(student_actions_frame, text="Reprovados por Falta", command=self.listar_reprovados_falta, bootstyle="warning").pack(fill='x', pady=5)
        ttk.Button(actions_frame, text="Listar Todos", command=self.listar_todos, bootstyle="secondary").pack(fill='x', side='bottom', pady=10)
        ttk.Button(actions_frame, text="Sair", command=self._sair, bootstyle="danger").pack(fill='x', side='bottom', pady=6)

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(side='right', fill='both', expand=True)

        # --- ALTERAÇÃO 1: NOVAS COLUNAS ---
        self.colunas = ('matricula', 'nome', 'funcao', 'n1', 'n2', 'n3', 'n4', 'media', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=self.colunas, show='headings', bootstyle="primary")

        # --- ALTERAÇÃO 2: NOVOS CABEÇALHOS E LARGURAS ---
        col_map = {
            'matricula': 'Matrícula', 'nome': 'Nome', 'funcao': 'Função', 
            'n1': 'Nota 1', 'n2': 'Nota 2', 'n3': 'Nota 3', 'n4': 'Nota 4',
            'media': 'Média Final', 'status': 'Conta Ativa'
        }
        for col in self.colunas: self.tree.heading(col, text=col_map[col])

        # Ajustando larguras para melhor visualização
        self.tree.column('matricula', width=80, anchor='center')
        self.tree.column('nome', width=250, anchor='w')
        self.tree.column('funcao', width=80, anchor='center')
        self.tree.column('n1', width=60, anchor='center')
        self.tree.column('n2', width=60, anchor='center')
        self.tree.column('n3', width=60, anchor='center')
        self.tree.column('n4', width=60, anchor='center')
        self.tree.column('media', width=80, anchor='center')
        self.tree.column('status', width=90, anchor='center')

        self.tree.bind("<Double-1>", self._mostrar_detalhes)
        self.tree.pack(fill='both', expand=True)

    # --- ALTERAÇÃO 3: LÓGICA DE ATUALIZAÇÃO DA TABELA ---
    def _atualizar_tabela(self, lista_pessoas):
        self.tree.delete(*self.tree.get_children())
        for pessoa in lista_pessoas:
            # Informações base, comuns a todos
            matricula = pessoa.matricula
            nome = pessoa.nome
            funcao = pessoa.get_tipo_entidade()
            status = "Sim" if pessoa.conta_ativa else "Não"

            # Informações específicas de Aluno
            if isinstance(pessoa, Aluno):
                # Pega as notas e preenche com '-' se tiver menos de 4
                notas = pessoa.notas + ['-'] * (4 - len(pessoa.notas))
                n1, n2, n3, n4 = notas[0], notas[1], notas[2], notas[3]
                media = f"{pessoa.calcular_media():.2f}"
            else:
                # Para Professor e Monitor, preenche com '-'
                n1, n2, n3, n4, media = '-', '-', '-', '-', '-'

            # Monta a tupla de valores na ordem correta das colunas
            valores = (matricula, nome, funcao, n1, n2, n3, n4, media, status)
            self.tree.insert('', 'end', values=valores)

    # O restante do arquivo (funções de salvar, carregar, cadastrar, atualizar, etc.)
    # permanece exatamente o mesmo da versão anterior.
    # ... (Cole aqui o restante das suas funções sem alteração) ...

    def _salvar_dados(self):
        try:
            with open(self.arquivo_dados, 'w') as f:
                for pessoa in self.registro.get_todos():
                    tipo = pessoa.__class__.__name__.upper()
                    base_info = f"{tipo},{pessoa.matricula},{pessoa.nome},{pessoa.conta_ativa}"
                    if isinstance(pessoa, Aluno):
                        notas_str = ",".join(map(str, pessoa.notas))
                        f.write(f"{base_info},{pessoa.curso},{pessoa.faltas},{notas_str}\n")
                    elif isinstance(pessoa, Professor):
                        f.write(f"{base_info},{pessoa.salario},{pessoa.qtde_materias}\n")
                    elif isinstance(pessoa, Monitor):
                        f.write(f"{base_info},{pessoa.valor_bolsa},{pessoa.carga_horaria}\n")
        except IOError as e: Messagebox.show_error(f"Não foi possível salvar: {e}", "Erro de Arquivo")


    def _carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r') as f:
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
                    self.registro.inserir(pessoa)
        except FileNotFoundError: pass
        except Exception as e: Messagebox.show_error(f"Não foi possível carregar os dados: {e}", "Erro de Arquivo")

    def _mostrar_detalhes(self, event):
        if not self.tree.focus(): return
        try:
            matricula = self.tree.item(self.tree.focus(), 'values')[0]
            pessoa = self.registro.buscar(matricula)
            Messagebox.show_info(str(pessoa), f"Detalhes de {pessoa.nome}")
        except (MatriculaNaoEncontradaError, IndexError) as e:
            Messagebox.show_warning(str(e), "Atenção")

    def listar_todos(self): self._atualizar_tabela(self.registro.get_todos())
    def listar_aprovados(self): self._atualizar_tabela(self.registro.get_alunos_por_status(aprovado=True))
    def listar_reprovados_media(self): self._atualizar_tabela(self.registro.get_reprovados_por_media())
    def listar_reprovados_falta(self): self._atualizar_tabela(self.registro.get_reprovados_por_falta())

    def _criar_formulario(self, master, fields, data={}):
        entries = {}
        for i, field_text in enumerate(fields):
            ttk.Label(master, text=field_text).grid(row=i, column=0, padx=10, pady=8, sticky='w')
            entry = ttk.Entry(master, width=30)
            entry.grid(row=i, column=1, padx=10, pady=8)
            if field_text in data: entry.insert(0, data[field_text])
            entries[field_text] = entry
        return entries

    def _janela_selecionar_perfil(self):
        win = ttk.Toplevel(self.root)
        win.title("Selecionar Perfil"); win.geometry("300x200")
        frame = ttk.Frame(win, padding=(20, 20)); frame.pack(expand=True, fill='both')
        ttk.Label(frame, text="Qual perfil cadastrar?", font=("-size", 12)).pack(pady=10)
        def open_win(func): win.destroy(); func()
        ttk.Button(frame, text="Aluno", command=lambda: open_win(self._janela_cadastrar_aluno)).pack(fill='x', pady=5)
        ttk.Button(frame, text="Professor", command=lambda: open_win(self._janela_cadastrar_professor)).pack(fill='x', pady=5)
        ttk.Button(frame, text="Monitor", command=lambda: open_win(self._janela_cadastrar_monitor)).pack(fill='x', pady=5)

    def _janela_cadastrar_aluno(self):
        win = ttk.Toplevel(self.root); win.title("Cadastrar Aluno")
        frame = ttk.Frame(win, padding=(20, 10)); frame.pack(expand=True, fill='both')
        fields = ["Nome", "Curso", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Faltas"]
        entries = self._criar_formulario(frame, fields)
        def on_save():
            try:
                aluno = Aluno(nome=entries["Nome"].get(), conta_ativa=True, curso=entries["Curso"].get(), faltas=int(entries["Faltas"].get() or 0))
                notas = [float(entries[f"Nota {i}"].get() or 0) for i in range(1, 5)]
                aluno.atualizar_notas(notas)
                self.registro.inserir(aluno)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info(f"Aluno {aluno.nome} cadastrado!\nMatrícula: {aluno.matricula}", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar", command=on_save, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)


    def _janela_cadastrar_professor(self):
        win = ttk.Toplevel(self.root); win.title("Cadastrar Professor")
        frame = ttk.Frame(win, padding=(20, 10)); frame.pack(expand=True, fill='both')
        fields = ["Nome", "Salário (R$)", "Qtd. de Matérias"]
        entries = self._criar_formulario(frame, fields)
        def on_save():
            try:
                prof = Professor(nome=entries["Nome"].get(), conta_ativa=True, salario=float(entries["Salário (R$)"].get() or 0), qtde_materias=int(entries["Qtd. de Matérias"].get() or 0))
                self.registro.inserir(prof)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info(f"Professor {prof.nome} cadastrado!\nMatrícula: {prof.matricula}", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar", command=on_save, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)


    def _janela_cadastrar_monitor(self):
        win = ttk.Toplevel(self.root); win.title("Cadastrar Monitor")
        frame = ttk.Frame(win, padding=(20, 10)); frame.pack(expand=True, fill='both')
        fields = ["Nome", "Valor da Bolsa (R$)", "Carga Horária (h)"]
        entries = self._criar_formulario(frame, fields)
        def on_save():
            try:
                monitor = Monitor(nome=entries["Nome"].get(), conta_ativa=True, valor_bolsa=float(entries["Valor da Bolsa (R$)"].get() or 0), carga_horaria=int(entries["Carga Horária (h)"].get() or 0))
                self.registro.inserir(monitor)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info(f"Monitor {monitor.nome} cadastrado!\nMatrícula: {monitor.matricula}", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar", command=on_save, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)

    def _janela_atualizar(self):
        matricula = Querybox.get_string("Digite a matrícula da pessoa:", "Buscar para Atualizar")
        if not matricula: return
        try:
            pessoa = self.registro.buscar(matricula)
            if isinstance(pessoa, Aluno): self._janela_editar_aluno(pessoa)
            elif isinstance(pessoa, Professor): self._janela_editar_professor(pessoa)
            elif isinstance(pessoa, Monitor): self._janela_editar_monitor(pessoa)
        except MatriculaNaoEncontradaError as e:
            Messagebox.show_warning(str(e), "Não Encontrado")

    def _janela_editar_aluno(self, aluno):
        win = ttk.Toplevel(self.root); win.title(f"Editando Aluno: {aluno.nome}")
        frame = ttk.Frame(win, padding=(20,10)); frame.pack(fill='both', expand=True)
        dados_atuais = {
            "Nome": aluno.nome, "Curso": aluno.curso, "Faltas": aluno.faltas,
            "Nota 1": aluno.notas[0] if len(aluno.notas) > 0 else "", "Nota 2": aluno.notas[1] if len(aluno.notas) > 1 else "",
            "Nota 3": aluno.notas[2] if len(aluno.notas) > 2 else "", "Nota 4": aluno.notas[3] if len(aluno.notas) > 3 else ""
        }
        fields = ["Nome", "Curso", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Faltas"]
        entries = self._criar_formulario(frame, fields, dados_atuais)
        def on_update():
            try:
                aluno.nome = entries["Nome"].get()
                aluno.curso = entries["Curso"].get()
                aluno.faltas = int(entries["Faltas"].get() or 0)
                notas = [float(entries[f"Nota {i}"].get() or 0) for i in range(1, 5)]
                aluno.atualizar_notas(notas)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info("Dados do aluno atualizados!", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar Alterações", command=on_update, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)

    def _janela_editar_professor(self, prof):
        win = ttk.Toplevel(self.root); win.title(f"Editando Professor: {prof.nome}")
        frame = ttk.Frame(win, padding=(20,10)); frame.pack(fill='both', expand=True)
        dados_atuais = {"Nome": prof.nome, "Salário (R$)": prof.salario, "Qtd. de Matérias": prof.qtde_materias}
        fields = ["Nome", "Salário (R$)", "Qtd. de Matérias"]
        entries = self._criar_formulario(frame, fields, dados_atuais)
        def on_update():
            try:
                prof.nome = entries["Nome"].get()
                prof.salario = float(entries["Salário (R$)"].get() or 0)
                prof.qtde_materias = int(entries["Qtd. de Matérias"].get() or 0)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info("Dados do professor atualizados!", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar Alterações", command=on_update, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)

    def _janela_editar_monitor(self, monitor):
        win = ttk.Toplevel(self.root); win.title(f"Editando Monitor: {monitor.nome}")
        frame = ttk.Frame(win, padding=(20,10)); frame.pack(fill='both', expand=True)
        dados_atuais = {"Nome": monitor.nome, "Valor da Bolsa (R$)": monitor.valor_bolsa, "Carga Horária (h)": monitor.carga_horaria}
        fields = ["Nome", "Valor da Bolsa (R$)", "Carga Horária (h)"]
        entries = self._criar_formulario(frame, fields, dados_atuais)
        def on_update():
            try:
                monitor.nome = entries["Nome"].get()
                # CORREÇÃO DE BUG: Faltava .get() aqui
                monitor.valor_bolsa = float(entries["Valor da Bolsa (R$)".get() or 0]) 
                monitor.carga_horaria = int(entries["Carga Horária (h)"].get() or 0)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info("Dados do monitor atualizados!", "Sucesso"); win.destroy()
            except (ErroMatricula, ValueError) as e: Messagebox.show_error(str(e), "Erro")
        ttk.Button(frame, text="Salvar Alterações", command=on_update, bootstyle="success").grid(row=len(fields), columnspan=2, pady=20)

    def _janela_remover(self):
        matricula = Querybox.get_string("Digite a matrícula a ser removida:", "Remover Pessoa")
        if not matricula: return
        try:
            pessoa = self.registro.buscar(matricula)
            if Messagebox.okcancel(f"Tem certeza que deseja remover {pessoa.nome} ({pessoa.get_tipo_entidade()})?", "Confirmar Remoção") == 'OK':
                self.registro.remover(matricula)
                self._salvar_dados(); self.listar_todos()
                Messagebox.show_info("Pessoa removida com sucesso.", "Sucesso")
        except MatriculaNaoEncontradaError as e: Messagebox.show_warning(str(e), "Não Encontrado")


    def _sair(self):
        if Messagebox.okcancel("Deseja salvar as alterações antes de sair?", "Sair") == 'OK':
            self._salvar_dados()
        self.root.quit()