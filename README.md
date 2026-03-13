# Construction Expense Manager

Aplicação web com Flask para registrar e gerenciar gastos de obras de construção.

## 🚀 Funcionalidades

- Gerenciamento de múltiplas casas/propriedades (nome, preço de venda, observações)
- CRUD completo de gastos com categorias e observações
- Categorias customizáveis com seed padrão
- Filtros de gastos por casa, categoria e período
- Formatação de valores em R$ (padrão brasileiro)
- Mensagens de feedback com animação fade-out
- Validação de dados no backend
- Confirmação antes de exclusões
- Interface responsiva com dark mode automático
- Persistência com SQLite

## 🛠️ Tecnologias

- Python 3.7+
- Flask
- SQLite
- Jinja2
- HTML5/CSS3

## 💻 Instalação

```bash
git clone git@github.com:vcrsantos/contruction_app.git
cd contruction_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Como Rodar

```bash
source venv/bin/activate
python app.py
```

Acesse: http://localhost:5000

## 📂 Estrutura

```
contruction_app/
├── app.py              # Aplicação Flask e rotas
├── database.py         # Configuração e inicialização do banco
├── backup.py           # Backup do banco de dados
├── wsgi.py             # Entry point para deploy (PythonAnywhere)
├── requirements.txt    # Dependências
├── templates/
│   ├── base.html           # Template base com navegação
│   ├── expenses.html       # Listagem e cadastro de gastos
│   ├── edit-expense.html   # Edição de gasto
│   ├── houses.html         # Listagem e cadastro de casas
│   ├── edit-house.html     # Edição de casa
│   ├── categories.html     # Listagem e cadastro de categorias
│   └── edit-category.html  # Edição de categoria
└── static/
    └── style.css           # Estilos com dark mode
```

## 🗂️ Banco de Dados

**houses**: id, name, selling_price, observations

**categories**: id, name (unique)

**expenses**: id, value, category, date, observations, house_id (FK → houses)

## 📊 Categorias Padrão

Aquisição e Regularização, Preparação do Terreno, Mão de Obra, Materiais de Construção, Projetos e Técnicos, Infraestrutura da Obra, Custos Administrativos

## 🌐 Deploy (PythonAnywhere)

1. Clone o repo no PythonAnywhere: `git clone ...`
2. Configure o Web App apontando o WSGI para `wsgi.py`
3. Adicione static files: URL `/static/` → diretório `static/`
4. Reload

## 👨‍💻 Autor

Victor Santos
