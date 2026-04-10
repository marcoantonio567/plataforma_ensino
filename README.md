# Plataforma de Ensino

Sistema de gerenciamento de cursos e aprendizado online desenvolvido com Django. A plataforma oferece uma estrutura completa para criação e navegação de cursos, com suporte a avaliações, gestão de alunos e emissão de certificados.

## Tecnologias

- **Backend**: Django 6.0.3
- **Banco de dados**: SQLite
- **Frontend**: HTML5/CSS3 (templates Django)
- **Idioma**: Português (Brasil)
- **Fuso horário**: America/Sao_Paulo

## Funcionalidades

### Implementadas
- Listagem de cursos na página inicial
- Navegação hierárquica: Curso → Módulo → Aula
- Sidebar com navegação por módulos e aulas
- Navegação entre aulas (anterior/próxima)
- Painel administrativo completo via Django Admin

### Modeladas (em desenvolvimento)
- **Avaliações**: provas objetivas, discursivas, projetos práticos e provas monitoradas
- **Alunos**: matrículas, aproveitamento de disciplinas, segunda chamada, revisão de notas
- **Certificações**: emissão de certificados digitais com UUID de verificação e controle de validade
- **Integridade acadêmica**: registro e gestão de incidentes

---

## Estrutura de Pastas

```
plataforma_ensino/                  # Raiz do projeto
├── manage.py                       # CLI do Django (runserver, migrate, etc.)
├── requirements.txt                # Dependências Python do projeto
├── db.sqlite3                      # Banco de dados SQLite
├── .gitignore                      # Arquivos ignorados pelo Git
├── README.md                       # Documentação do projeto
│
├── plataforma_ensino/              # Pacote de configuração do projeto Django
│   ├── __init__.py
│   ├── settings.py                 # Configurações globais (banco, apps, idioma, etc.)
│   ├── urls.py                     # Roteamento raiz (admin + courses)
│   ├── wsgi.py                     # Ponto de entrada para servidores WSGI (produção)
│   └── asgi.py                     # Ponto de entrada para servidores ASGI (async)
│
├── courses/                        # App de cursos — única com views implementadas
│   ├── __init__.py
│   ├── apps.py                     # Configuração do app (CoursesConfig)
│   ├── models.py                   # Modelos: Curso, Modulo, Aula, RegraCurso, PreRequisito
│   ├── views.py                    # Views: home, curso_detail, modulo_detail, aula_detail
│   ├── urls.py                     # Rotas do app de cursos
│   ├── admin.py                    # Registro dos modelos no painel admin
│   ├── tests.py                    # Testes (vazio)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Criação das tabelas de cursos
│
├── assessments/                    # App de avaliações — modelos prontos, views vazias
│   ├── __init__.py
│   ├── apps.py                     # Configuração do app (AssessmentsConfig)
│   ├── models.py                   # Modelos: Avaliacao, AvaliacaoObjetiva, AvaliacaoDiscursiva,
│   │                               #          ProjetoPratico, ProvaMonitorada, AvaliacaoRealizada
│   ├── views.py                    # Views (vazio — em desenvolvimento)
│   ├── admin.py                    # Registro dos modelos no painel admin
│   ├── tests.py                    # Testes (vazio)
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py         # Criação da tabela base Avaliacao
│       └── 0002_initial.py         # Criação dos tipos filhos e AvaliacaoRealizada
│
├── students/                       # App de alunos — modelos prontos, views vazias
│   ├── __init__.py
│   ├── apps.py                     # Configuração do app (StudentsConfig)
│   ├── models.py                   # Modelos: Aluno, Matricula, Solicitacao, RevisaoNota,
│   │                               #          SegundaChamada, Aproveitamento, Equivalencia
│   ├── views.py                    # Views (vazio — em desenvolvimento)
│   ├── admin.py                    # Registro dos modelos no painel admin
│   ├── tests.py                    # Testes (vazio)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Criação de todas as tabelas de alunos
│
├── certifications/                 # App de certificações — modelos prontos, views vazias
│   ├── __init__.py
│   ├── apps.py                     # Configuração do app (CertificationsConfig)
│   ├── models.py                   # Modelos: Certificado, IncidenteIntegridade
│   ├── views.py                    # Views (vazio — em desenvolvimento)
│   ├── admin.py                    # Registro dos modelos no painel admin
│   ├── tests.py                    # Testes (vazio)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Criação das tabelas de certificações
│
└── templates/                      # Templates HTML globais do projeto
    ├── base.html                   # Template base: layout com sidebar + área de conteúdo
    └── courses/                    # Templates específicos do app de cursos
        ├── home.html               # Página inicial — grade de cards com todos os cursos
        ├── curso_detail.html       # Detalhes de um curso com botão para iniciar
        ├── modulo_detail.html      # Detalhes de um módulo com lista de aulas
        ├── aula_detail.html        # Conteúdo de uma aula com navegação anterior/próxima
        └── _sidebar.html           # Componente reutilizável de navegação lateral
```

---

## Descrição dos Apps

### `plataforma_ensino/` — Configuração do Projeto

Pacote central do Django. Contém as configurações globais e o roteamento raiz.

| Arquivo | Função |
|---------|--------|
| `settings.py` | Define banco de dados, apps instalados, idioma, fuso horário e diretório de templates |
| `urls.py` | Mapeia `/admin/` para o painel Django e `/` para as URLs do app `courses` |
| `wsgi.py` / `asgi.py` | Pontos de entrada para deploy em servidores de produção |

---

### `courses/` — Gerenciamento de Cursos

Único app com views e templates implementados. Responsável por toda a navegação de conteúdo.

**Modelos:**

| Modelo | Descrição |
|--------|-----------|
| `Curso` | Curso com nome, carga horária e timestamps |
| `Modulo` | Módulo ordenado dentro de um curso |
| `Aula` | Aula com título, conteúdo, duração e ordem dentro do módulo |
| `RegraCurso` | Regras de conclusão: média mínima, carga horária mínima, projeto final obrigatório |
| `PreRequisito` | Pré-requisito de curso ou módulo para matrícula |

**Views:**

| View | Rota | Descrição |
|------|------|-----------|
| `home` | `/` | Lista todos os cursos disponíveis |
| `curso_detail` | `/<curso_id>/` | Exibe detalhes do curso e link para iniciar |
| `modulo_detail` | `/<curso_id>/modulo/<modulo_id>/` | Lista aulas do módulo |
| `aula_detail` | `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | Exibe conteúdo da aula com navegação |

---

### `assessments/` — Avaliações

Modelos prontos para múltiplos tipos de avaliação usando herança de tabelas (multi-table inheritance).

**Modelos:**

| Modelo | Descrição |
|--------|-----------|
| `Avaliacao` | Avaliação base vinculada a um módulo (tipo + peso) |
| `AvaliacaoObjetiva` | Prova de múltipla escolha com questões em JSONField |
| `AvaliacaoDiscursiva` | Prova dissertativa com descrição em texto |
| `ProjetoPratico` | Projeto com link de repositório opcional |
| `ProvaMonitorada` | Prova com monitoramento remoto ativo |
| `AvaliacaoRealizada` | Registro de nota de um aluno em uma avaliação |

---

### `students/` — Alunos e Matrículas

Modelos para gerenciar o ciclo de vida acadêmico do aluno, desde a matrícula até solicitações administrativas.

**Modelos:**

| Modelo | Descrição |
|--------|-----------|
| `Aluno` | Perfil do aluno vinculado ao `User` do Django (número de matrícula, data de ingresso) |
| `Matricula` | Matrícula em um curso (status, média final, progresso, carga horária cumprida) |
| `Aproveitamento` | Solicitação de aproveitamento de disciplina cursada anteriormente |
| `SegundaChamada` | Solicitação de segunda chamada em uma avaliação |
| `RevisaoNota` | Recurso de revisão de nota de uma avaliação |
| `Equivalencia` | Registro de equivalência de disciplina de outra instituição |

O modelo `Aluno` possui métodos para realizar todas as solicitações diretamente: `matricular()`, `trancar_matricula()`, `solicitar_aproveitamento()`, `solicitar_segunda_chamada()` e `solicitar_revisao_nota()`.

---

### `certifications/` — Certificações e Integridade Acadêmica

Modelos para emissão de certificados e registro de incidentes de integridade.

**Modelos:**

| Modelo | Descrição |
|--------|-----------|
| `Certificado` | Certificado de conclusão de curso vinculado a uma matrícula (com validade e status) |
| `IncidenteIntegridade` | Registro de incidente acadêmico (cola, plágio, fraude, outros) |

O `Certificado` possui os métodos `revogar()`, `suspender()` e `renovar()` para controle do ciclo de vida.

---

### `templates/` — Templates HTML

| Template | Descrição |
|----------|-----------|
| `base.html` | Layout base com sidebar escura (280px), barra de breadcrumb e área de conteúdo. Blocos: `title`, `sidebar`, `breadcrumb`, `content` |
| `courses/home.html` | Página standalone com grid de cards dos cursos (não herda de `base.html`) |
| `courses/curso_detail.html` | Detalhes do curso; herda de `base.html` |
| `courses/modulo_detail.html` | Lista de aulas do módulo; herda de `base.html` |
| `courses/aula_detail.html` | Conteúdo da aula com botões anterior/próxima; herda de `base.html` |
| `courses/_sidebar.html` | Componente de navegação lateral com módulos e aulas expansíveis (prefixado com `_` por ser parcial) |

---

## Relações entre os Modelos

```
Curso ──< Modulo ──< Aula
  │           │
  │           └──< Avaliacao (objetiva / discursiva / projeto / monitorada)
  │                    │
  │                    └──< AvaliacaoRealizada >── Aluno
  │
  └──< PreRequisito
  └── RegraCurso

Aluno ──< Matricula >── Curso
              │
              ├──< Aproveitamento >── Modulo
              ├──< SegundaChamada >── Avaliacao
              ├──< RevisaoNota    >── Avaliacao
              ├──< Equivalencia
              ├── Certificado
              └──< IncidenteIntegridade
```

---

## Instalação

**Pré-requisitos:** Python 3.12+

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd plataforma_ensino

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse em [http://localhost:8000](http://localhost:8000)

O painel administrativo está disponível em [http://localhost:8000/admin](http://localhost:8000/admin)

---

## URLs

| Rota | View | Descrição |
|------|------|-----------|
| `/` | `home` | Página inicial com lista de cursos |
| `/<curso_id>/` | `curso_detail` | Detalhes do curso |
| `/<curso_id>/modulo/<modulo_id>/` | `modulo_detail` | Detalhes do módulo |
| `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | `aula_detail` | Conteúdo da aula |
| `/admin/` | — | Painel administrativo Django |

---

## Dependências

```
Django==6.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```
