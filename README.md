# 🎓 SISGA - Sistema de Gestão Acadêmica

**Sistema Integrado de Gestão Acadêmica desenvolvido como projeto para a disciplina de Programação Orientada a Objetos (POO) na Universidade Federal de Sergipe (UFS).**

Este projeto demonstra a aplicação dos pilares da POO para criar um sistema robusto e flexível, com uma lógica de negócios bem definida e duas interfaces de usuário distintas: uma para terminal e uma aplicação web interativa.

---

## ✨ Funcionalidades Principais

* **Cadastro Multi-Perfil:** Permite o cadastro de Alunos, Professores e Monitores, cada um com seus atributos específicos.
* **Lógica de Negócio Clara:** Validações de dados (nomes, notas, valores numéricos) para garantir a integridade do sistema.
* **Persistência de Dados:** O estado da aplicação é salvo em um arquivo `registros.txt`, permitindo que os dados sejam mantidos entre as execuções.
* **Listagem e Filtragem:** Exibe a lista completa de pessoas cadastradas e permite a filtragem específica de alunos (Aprovados, Reprovados por Média, Reprovados por Falta).
* **Atualização e Remoção:** Permite a edição e exclusão de registros existentes através da matrícula.
* **Duas Interfaces:** O mesmo "cérebro" (lógica POO) é servido por duas "faces" diferentes:
    1.  Uma interface de terminal clássica.
    2.  Uma interface web moderna e reativa, publicada online.

---

## 🚀 Aplicação Online (Versão Web)

A interface web do projeto está publicada e pode ser acessada através do link abaixo:

**[https://sisga.onrender.com/](https://sisga.onrender.com/)**

---

## 🔧 Tecnologias e Conceitos Aplicados

* **Linguagem:** Python 3
* **Programação Orientada a Objetos (POO):**
    * **Abstração:** Uso de Classes Base Abstratas (`Matriculados`) para definir um "contrato" comum.
    * **Herança:** Classes `Aluno`, `Professor` e `Monitor` herdam atributos e métodos da classe base.
    * **Polimorfismo:** Métodos como `imprime()` e `getTipoEntidade()` que se comportam de maneira diferente dependendo do objeto.
    * **Encapsulamento:** Proteção de atributos e uso de getters/setters para controlar o acesso e validar os dados.
* **Tratamento de Exceções:** Criação de exceções customizadas para um controle de erros robusto.
* **Manipulação de Arquivos:** Leitura e escrita de arquivos de texto para persistência de dados.
* **Interface Web:**
    * **Streamlit:** Framework utilizado para construir a interface web interativa de forma rápida e eficiente.
    * **Pandas:** Usado para a exibição otimizada dos dados em tabelas na interface web.
* **Interface de Terminal:** Uso dos módulos padrão do Python (`os`) para uma experiência de usuário limpa no terminal.

---

## 📁 Estrutura do Projeto

A arquitetura do projeto foi pensada para separar a lógica de negócios da camada de apresentação, permitindo a fácil criação de múltiplas interfaces.
```bash
SISGA/
├── POO/                  # O "Cérebro": Contém toda a lógica orientada a objetos
│   ├── exceptions.py     # Exceções customizadas
│   ├── matriculados.py   # Classe base abstrata
│   ├── aluno.py          # Classe filha
│   ├── professor.py      # Classe filha
│   ├── monitor.py        # Classe filha
│   └── registro.py       # Classe que gerencia a coleção de objetos
│   ├── curso.py          # Classe de cursos
│   └── registro_curso.py # Classe gerenciadora de Cursos
│
├── main.py               # O "Rosto" 1: Interface de Terminal
├── interface_grafica.py  # O "Rosto" 2: Interface Web com Streamlit
├── requirements.txt      # Dependências para a versão Web
└── registros.txt         # Arquivo de dados para persistência
```

## 💻 Como Executar Localmente

### Pré-requisitos
* [Python 3.8+](https://www.python.org/downloads/)
* Git

### 1. Versão Web (Streamlit)

**Passo 1: Clone o repositório**
```bash
git clone https://github.com/RianPOliveira/SISGA.git
cd SISGA
```
**Passo 2: Crie e ative um ambiente virtual (Recomendado)**
```bash
# Para Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
```
**Passo 3: Instale as dependências**
```bash
pip install -r requirements.txt
```
**Passo 4: Execute a aplicação**
```bash
streamlit run interface_grafica.py
```

### 2. Versão via Terminal

**Passo 1 e 2: Siga os mesmos passos de clonar e ativar o ambiente virtual acima. Não é necessário instalar as dependências do requirements.txt para esta versão.**

**Passo 3: Execute a aplicação**
```bash
python main.py
```
