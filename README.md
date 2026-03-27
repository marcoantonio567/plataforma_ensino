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
- **Certificações**: emissão de certificados digitais com código de verificação e controle de validade
- **Integridade acadêmica**: registro e gestão de incidentes

## Estrutura do Projeto

```
plataforma_ensino/
├── plataforma_ensino/      # Configurações do projeto Django
├── courses/                # App de cursos (views implementadas)
├── assessments/            # App de avaliações (modelos prontos)
├── students/               # App de alunos (modelos prontos)
├── certifications/         # App de certificações (modelos prontos)
├── templates/              # Templates HTML
│   ├── base.html
│   └── courses/
└── manage.py
```

## Modelos

### Courses
| Modelo | Descrição |
|--------|-----------|
| `Curso` | Curso com título, descrição, carga horária, nota mínima e pré-requisitos |
| `Modulo` | Módulos ordenados dentro de um curso |
| `Aula` | Aulas com conteúdo, duração e ordem dentro de um módulo |

### Assessments
| Modelo | Descrição |
|--------|-----------|
| `Avaliacao` | Avaliação vinculada a um módulo (objetiva, discursiva, projeto, prova) |
| `TrabalhoPratico` | Trabalho prático com prazo vinculado a um curso |

### Students
| Modelo | Descrição |
|--------|-----------|
| `Aluno` | Perfil do aluno com CPF e data de nascimento |
| `Matricula` | Matrícula do aluno em um curso |
| `Aproveitamento` | Solicitação de aproveitamento de disciplina |
| `SegundaChamada` | Solicitação de segunda chamada em avaliação |
| `RevisaoNota` | Recurso de revisão de nota |

### Certifications
| Modelo | Descrição |
|--------|-----------|
| `Certificado` | Certificado de conclusão com UUID de verificação e validade |
| `IncidenteIntegridade` | Registro de incidente de integridade acadêmica |

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

## URLs

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial com lista de cursos |
| `/<curso_id>/` | Detalhes do curso |
| `/<curso_id>/modulo/<modulo_id>/` | Detalhes do módulo |
| `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | Conteúdo da aula |
| `/admin/` | Painel administrativo |

## Dependências

```
Django==6.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```
