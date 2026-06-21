# Plataforma de Ensino

<p align="center">
  <a href="README.pt-BR.md">
    <img alt="Leia em Portugues" src="https://img.shields.io/badge/README-Portugues-1f6feb?style=for-the-badge&labelColor=0d1117">
  </a>
  <a href="README.en.md">
    <img alt="Read in English" src="https://img.shields.io/badge/README-English-2ea043?style=for-the-badge&labelColor=0d1117">
  </a>
</p>

Sistema de gerenciamento de cursos e aprendizado online desenvolvido com Django. A plataforma permite criar e navegar por cursos, módulos e aulas, além de modelar matrículas, avaliações, solicitações acadêmicas, certificados e incidentes de integridade acadêmica.

## Tecnologias

- **Backend**: Django 6.0.3
- **Banco de dados**: SQLite
- **Frontend**: HTML5/CSS3 com templates Django
- **Idioma**: Português (Brasil)
- **Fuso horário**: America/Sao_Paulo

## Funcionalidades

### Implementadas

- Listagem de cursos na página inicial
- Navegação hierárquica: Curso -> Módulo -> Aula
- Sidebar com navegação por módulos e aulas
- Navegação entre aulas
- Criação e gerenciamento básico de cursos, módulos e aulas
- Registro, login e logout de estudantes
- Matrícula, listagem de matrículas e cancelamento de matrícula
- Painel administrativo via Django Admin

### Modeladas / em evolução

- **Avaliações**: provas objetivas, discursivas, projetos práticos e provas monitoradas
- **Alunos**: matrículas, aproveitamento de disciplinas, segunda chamada e revisão de notas
- **Certificações**: emissão, suspensão, revogação e renovação de certificados
- **Integridade acadêmica**: registro de incidentes acadêmicos

---

## Estrutura de Pastas

O projeto usa a própria pasta `plataforma_ensino/` como raiz do repositório e pacote Django. Por isso os arquivos de configuração (`settings.py`, `urls.py`, `asgi.py`, `wsgi.py`) ficam diretamente na raiz.

```text
plataforma_ensino/
|-- manage.py                 # CLI do Django
|-- settings.py               # Configurações globais do projeto
|-- urls.py                   # Roteamento raiz: admin, courses e students
|-- asgi.py                   # Entrada ASGI
|-- wsgi.py                   # Entrada WSGI
|-- requirements.txt          # Dependências Python
|-- README.md                 # Documentação principal
|-- README.pt-BR.md           # Documentação em português
|-- README.en.md              # Documentação em inglês
|-- ARCHITECTURE.md           # Resumo das camadas DDD adotadas
|-- diagrama.mmd              # Diagrama Mermaid
|-- .gitignore
|
|-- courses/                  # Contexto de cursos, módulos e aulas
|   |-- models.py             # Entidades ORM: Curso, Modulo, Aula, RegraCurso, PreRequisito
|   |-- urls.py               # Rotas públicas do contexto de cursos
|   |-- views.py              # Fachada de compatibilidade para presentation.views
|   |-- forms.py              # Fachada de compatibilidade para presentation.forms
|   |-- admin.py              # Registro dos modelos no Django Admin
|   |-- tests.py
|   |-- domain/
|   |   |-- repositories.py   # Contratos de repositório do domínio
|   |   `-- __init__.py
|   |-- application/
|   |   |-- selectors.py      # Consultas de leitura
|   |   |-- services.py       # Casos de uso que alteram estado
|   |   `-- __init__.py
|   |-- infrastructure/
|   |   |-- repositories.py   # Implementação com Django ORM
|   |   `-- __init__.py
|   |-- presentation/
|   |   |-- views.py          # Views HTTP do app de cursos
|   |   |-- forms.py          # Forms usados pela camada de apresentação
|   |   `-- __init__.py
|   `-- migrations/
|
|-- students/                 # Contexto de alunos e matrículas
|   |-- models.py             # Aluno, Matricula, Solicitacao e tipos derivados
|   |-- urls.py               # Rotas de autenticação, matrícula e área do estudante
|   |-- views.py              # Fachada de compatibilidade para presentation.views
|   |-- admin.py
|   |-- tests.py
|   |-- domain/
|   |   |-- exceptions.py
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- application/
|   |   |-- selectors.py
|   |   |-- services.py
|   |   `-- __init__.py
|   |-- infrastructure/
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- presentation/
|   |   |-- views.py
|   |   `-- __init__.py
|   `-- migrations/
|
|-- assessments/              # Contexto de avaliações e notas
|   |-- models.py             # Avaliacao e especializações
|   |-- views.py
|   |-- admin.py
|   |-- tests.py
|   |-- domain/
|   |   |-- policies.py       # Regras puras, como validação de nota
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- application/
|   |   |-- services.py
|   |   `-- __init__.py
|   |-- infrastructure/
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- presentation/
|   |   `-- __init__.py
|   `-- migrations/
|
|-- certifications/           # Contexto de certificados e integridade acadêmica
|   |-- models.py             # Certificado e IncidenteIntegridade
|   |-- views.py
|   |-- admin.py
|   |-- tests.py
|   |-- domain/
|   |   |-- policies.py
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- application/
|   |   |-- services.py
|   |   `-- __init__.py
|   |-- infrastructure/
|   |   |-- repositories.py
|   |   `-- __init__.py
|   |-- presentation/
|   |   `-- __init__.py
|   `-- migrations/
|
|-- templates/
|   |-- base.html
|   |-- courses/
|   |   |-- _sidebar.html
|   |   |-- home.html
|   |   |-- curso_detail.html
|   |   |-- modulo_detail.html
|   |   |-- aula_detail.html
|   |   |-- criar_curso.html
|   |   `-- gerenciar_curso.html
|   `-- students/
|       |-- login.html
|       |-- registro.html
|       `-- minhas_matriculas.html
|
|-- seed/
|   `-- seed.py               # Script de carga inicial de dados
|
`-- documents/
    |-- CRITICA_DDD.md
    |-- DOCUMENTACAO_NEGOCIO.md
    `-- Cases para Livro DDD - Eric Evans (1).pdf
```

> Observação: pela configuração atual de `settings.py`, o SQLite (`db.sqlite3`) é gerado um nível acima da pasta do projeto.

---

## Decisão Arquitetural: Estrutura DDD por App

### Contexto

Em projetos Django com vários domínios, como cursos, alunos, avaliações e certificações, existem duas formas comuns de aplicar DDD. A estrutura centralizada agrupa todas as camadas em pastas globais (`domain/`, `application/`, `infrastructure/`, `interfaces/`). A estrutura descentralizada organiza essas camadas dentro de cada app Django.

### Decisão

Este projeto adota DDD por app. Cada bounded context mantém suas próprias regras de negócio, casos de uso, adaptadores e interfaces de apresentação:

```text
courses/
  domain/
  application/
  infrastructure/
  presentation/

students/
  domain/
  application/
  infrastructure/
  presentation/
```

### Justificativa

A escolha favorece modularidade e baixo acoplamento. Como cada app representa uma área funcional do negócio, manter as camadas dentro dele facilita evoluir, testar e compreender o contexto sem navegar por diretórios globais muito amplos. Também preserva a forma natural de organização do Django, onde apps são unidades de responsabilidade, roteamento, admin, migrations e configuração.

Exemplo prático:

```python
# students/application/services.py
def enroll_student(student, course, repository=None):
    repository = repository or DjangoStudentRepository()
    enrollment = repository.find_enrollment(student, course)

    if enrollment is None:
        return EnrollmentResult(
            enrollment=repository.enroll(student, course),
            created=True,
        )

    return EnrollmentResult(enrollment=enrollment)
```

### Alternativas consideradas

A estrutura centralizada pode ser útil em sistemas menores ou em equipes que preferem visualizar todas as entidades de domínio juntas. Porém, em projetos com múltiplos apps, ela tende a misturar contextos e aumentar o custo de navegação.

### Consequências

Positivamente, a arquitetura por app melhora coesão, isolamento e escalabilidade organizacional. Negativamente, pode gerar repetição de pastas e exige disciplina para evitar duplicação de conceitos compartilhados. Quando houver regras transversais, elas devem ser extraídas com critério para módulos compartilhados bem definidos.

---

## Descrição das Camadas

Cada contexto segue a mesma organização:

| Camada | Responsabilidade |
|--------|------------------|
| `domain/` | Políticas, exceções e contratos sem dependência de HTTP ou ORM concreto |
| `application/` | Casos de uso, serviços transacionais e selectors de leitura |
| `infrastructure/` | Implementações concretas, principalmente repositórios baseados no Django ORM |
| `presentation/` | Views e forms ligados à camada HTTP |
| `models.py` | Modelos ORM e fachada estável para o Django |
| `views.py` / `forms.py` | Fachadas de compatibilidade para imports antigos, URLs e admin |

Regra de dependência esperada:

```text
presentation -> application -> domain
```

A infraestrutura implementa os contratos do domínio e é usada pelos serviços de aplicação.

---

## Descrição dos Apps

### `courses/` - Cursos

Responsável pelo catálogo de cursos, módulos, aulas e regras de conclusão.

**Modelos principais:**

| Modelo | Descrição |
|--------|-----------|
| `Curso` | Curso com nome, carga horária e timestamps |
| `Modulo` | Módulo ordenado dentro de um curso |
| `Aula` | Aula com título, conteúdo, duração e ordem |
| `RegraCurso` | Regras de conclusão, média mínima, carga horária mínima e projeto final |
| `PreRequisito` | Pré-requisito de curso ou módulo |

**Views/rotas principais:**

| Rota | View | Descrição |
|------|------|-----------|
| `/` | `home` | Lista os cursos |
| `/novo/` | `criar_curso` | Cria um curso |
| `/<curso_id>/` | `curso_detail` | Exibe detalhes do curso |
| `/<curso_id>/gerenciar/` | `gerenciar_curso` | Gerencia curso, módulos e aulas |
| `/<curso_id>/modulo/<modulo_id>/` | `modulo_detail` | Exibe um módulo |
| `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | `aula_detail` | Exibe uma aula |

### `students/` - Alunos e Matrículas

Responsável por autenticação simples de estudante, matrícula em curso e solicitações acadêmicas.

**Modelos principais:**

| Modelo | Descrição |
|--------|-----------|
| `Aluno` | Perfil vinculado ao `User` do Django |
| `Matricula` | Matrícula de um aluno em um curso |
| `Solicitacao` | Base para solicitações acadêmicas |
| `Aproveitamento` | Solicitação de aproveitamento de disciplina |
| `SegundaChamada` | Solicitação de segunda chamada |
| `RevisaoNota` | Solicitação de revisão de nota |
| `Equivalencia` | Registro de equivalência entre disciplinas |

**Rotas:**

| Rota | Descrição |
|------|-----------|
| `/estudante/login/` | Login |
| `/estudante/logout/` | Logout |
| `/estudante/registro/` | Registro de usuário |
| `/estudante/minhas-matriculas/` | Área de matrículas do estudante |
| `/estudante/matricular/<curso_id>/` | Matrícula em curso |
| `/estudante/cancelar/<matricula_id>/` | Cancelamento de matrícula |

### `assessments/` - Avaliações

Modela avaliações e notas usando herança de tabelas do Django.

| Modelo | Descrição |
|--------|-----------|
| `Avaliacao` | Avaliação base vinculada a um módulo |
| `AvaliacaoObjetiva` | Avaliação com questões em `JSONField` |
| `AvaliacaoDiscursiva` | Avaliação discursiva com descrição textual |
| `ProjetoPratico` | Projeto com repositório opcional |
| `ProvaMonitorada` | Prova com monitoramento remoto |
| `AvaliacaoRealizada` | Nota de um aluno em uma avaliação |

### `certifications/` - Certificações e Integridade

Modela certificados e incidentes acadêmicos.

| Modelo | Descrição |
|--------|-----------|
| `Certificado` | Certificado vinculado a uma matrícula |
| `IncidenteIntegridade` | Registro de incidente acadêmico |

O `Certificado` expõe métodos de ciclo de vida como `revogar()`, `suspender()` e `renovar()`, delegando a lógica para a camada de aplicação.

---

## Relações entre os Modelos

```text
Curso --< Modulo --< Aula
  |           |
  |           `--< Avaliacao (objetiva / discursiva / projeto / monitorada)
  |                    |
  |                    `--< AvaliacaoRealizada >-- Aluno
  |
  |--< PreRequisito
  `-- RegraCurso

Aluno --< Matricula >-- Curso
              |
              |--< Aproveitamento >-- Modulo
              |--< SegundaChamada >-- Avaliacao
              |--< RevisaoNota    >-- Avaliacao
              |--< Equivalencia
              |-- Certificado
              `--< IncidenteIntegridade
```

---

## Instalação

**Pré-requisitos:** Python 3.12+

```bash
git clone <url-do-repositorio>
cd plataforma_ensino

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:

- Aplicação: [http://localhost:8000](http://localhost:8000)
- Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Dependências

```text
Django==6.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```
