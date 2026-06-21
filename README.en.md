# Teaching Platform

<p align="center">
  <a href="README.md">
    <img alt="Leia em Portugues" src="https://img.shields.io/badge/README-Portugues-1f6feb?style=for-the-badge&labelColor=0d1117">
  </a>
  <a href="README.en.md">
    <img alt="Read in English" src="https://img.shields.io/badge/README-English-2ea043?style=for-the-badge&labelColor=0d1117">
  </a>
</p>

An online course management and e-learning system built with Django. The platform provides a complete structure for course creation and navigation, with support for assessments, student management, and certificate issuance. 

## Technologies

* **Backend**: Django 6.0.3
* **Database**: SQLite
* **Frontend**: HTML5/CSS3 (Django templates)
* **Language**: Portuguese (Brazil)
* **Timezone**: America/Sao_Paulo

## Features

### Implemented

* Course listing on the homepage
* Hierarchical navigation: Course -> Module -> Lesson
* Sidebar navigation for modules and lessons
* Navigation between lessons (previous/next)
* Full administrative panel via Django Admin

### Modeled (In Development)

* **Assessments**: multiple-choice exams, essay exams, practical projects, and proctored exams
* **Students**: enrollments, subject credit transfers, makeup exams, grade review requests
* **Certifications**: digital certificate issuance with UUID verification and validity control
* **Academic Integrity**: incident tracking and management

---

## Project Structure

```text
plataforma_ensino/                  # Project root
|-- manage.py                       # Django CLI (runserver, migrate, etc.)
|-- requirements.txt                # Python project dependencies
|-- db.sqlite3                      # SQLite database
|-- .gitignore                      # Git ignored files
|-- README.md                       # Project documentation
|
|-- plataforma_ensino/              # Django project configuration package
|   |-- __init__.py
|   |-- settings.py                 # Global settings (database, apps, language, etc.)
|   |-- urls.py                     # Root routing (admin + courses)
|   |-- wsgi.py                     # Entry point for WSGI servers (production)
|   +-- asgi.py                     # Entry point for ASGI servers (async)
|
|-- courses/                        # Courses app - only app with implemented views
|   |-- __init__.py
|   |-- apps.py                     # App configuration (CoursesConfig)
|   |-- models.py                   # Models: Curso, Modulo, Aula, RegraCurso, PreRequisito
|   |-- views.py                    # Views: home, curso_detail, modulo_detail, aula_detail
|   |-- urls.py                     # Courses app routes
|   |-- admin.py                    # Model registration in admin panel
|   |-- tests.py                    # Tests (empty)
|   +-- migrations/
|       |-- __init__.py
|       +-- 0001_initial.py         # Creation of course tables
|
|-- assessments/                    # Assessments app - models ready, views empty
|   |-- __init__.py
|   |-- apps.py                     # App configuration (AssessmentsConfig)
|   |-- models.py                   # Models: Avaliacao, AvaliacaoObjetiva, AvaliacaoDiscursiva,
|   |                               #         ProjetoPratico, ProvaMonitorada, AvaliacaoRealizada
|   |-- views.py                    # Views (empty - in development)
|   |-- admin.py                    # Model registration in admin panel
|   |-- tests.py                    # Tests (empty)
|   +-- migrations/
|       |-- __init__.py
|       |-- 0001_initial.py         # Creation of base Avaliacao table
|       +-- 0002_initial.py         # Creation of child types and AvaliacaoRealizada
|
|-- students/                       # Students app - models ready, views empty
|   |-- __init__.py
|   |-- apps.py                     # App configuration (StudentsConfig)
|   |-- models.py                   # Models: Aluno, Matricula, Request, RevisaoNota,
|   |                               #         SegundaChamada, Aproveitamento, Equivalencia
|   |-- views.py                    # Views (empty - in development)
|   |-- admin.py                    # Model registration in admin panel
|   |-- tests.py                    # Tests (empty)
|   +-- migrations/
|       |-- __init__.py
|       +-- 0001_initial.py         # Creation of all student tables
|
|-- certifications/                 # Certifications app - models ready, views empty
|   |-- __init__.py
|   |-- apps.py                     # App configuration (CertificationsConfig)
|   |-- models.py                   # Models: Certificado, IncidenteIntegridade
|   |-- views.py                    # Views (empty - in development)
|   |-- admin.py                    # Model registration in admin panel
|   |-- tests.py                    # Tests (empty)
|   +-- migrations/
|       |-- __init__.py
|       +-- 0001_initial.py         # Creation of certification tables
|
+-- templates/                      # Global HTML templates
    |-- base.html                   # Base template: layout with sidebar + content area
    +-- courses/                    # Templates specific to the courses app
        |-- home.html               # Homepage - card grid with all courses
        |-- curso_detail.html       # Course details with start button
        |-- modulo_detail.html      # Module details with lesson list
        |-- aula_detail.html        # Lesson content with previous/next navigation
        +-- _sidebar.html           # Reusable sidebar navigation component
```

---

## App Descriptions

### `plataforma_ensino/` - Project Configuration

Core Django package containing global settings and root routing.

| File                  | Purpose                                                                      |
| --------------------- | ---------------------------------------------------------------------------- |
| `settings.py`         | Defines database, installed apps, language, timezone, and template directory |
| `urls.py`             | Maps `/admin/` to the Django admin panel and `/` to the `courses` app URLs   |
| `wsgi.py` / `asgi.py` | Entry points for deployment on production servers                            |

---

### `courses/` - Course Management

The only app with implemented views and templates. Responsible for all content navigation.

**Models:**

| Model          | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `Curso`       | Course with name, workload, and timestamps                                 |
| `Modulo`       | Ordered module within a course                                             |
| `Aula`       | Lesson with title, content, duration, and order within the module          |
| `RegraCurso`   | Completion rules: minimum grade, minimum workload, mandatory final project |
| `PreRequisito` | Course or module prerequisite for enrollment                               |

**Views:**

| View            | Route                                                 | Description                             |
| --------------- | ----------------------------------------------------- | --------------------------------------- |
| `home`          | `/`                                                   | Lists all available courses             |
| `curso_detail` | `/<curso_id>/`                                       | Displays course details and start link  |
| `modulo_detail` | `/<curso_id>/modulo/<modulo_id>/`                    | Lists module lessons                    |
| `aula_detail` | `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | Displays lesson content with navigation |

---

### `assessments/` - Assessments

Models prepared for multiple assessment types using multi-table inheritance.

**Models:**

| Model                 | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `Avaliacao`          | Base assessment linked to a module (type + weight)      |
| `AvaliacaoObjetiva` | Multiple-choice exam with questions stored in JSONField |
| `AvaliacaoDiscursiva`     | Essay exam with text description                        |
| `ProjetoPratico`    | Project with optional repository link                   |
| `ProvaMonitorada`       | Exam with active remote monitoring                      |
| `AvaliacaoRealizada` | Record of a student's grade in an assessment            |

---

### `students/` - Students and Enrollments

Models to manage the student academic lifecycle, from enrollment to administrative requests.

**Models:**

| Model            | Description                                                           |
| ---------------- | --------------------------------------------------------------------- |
| `Aluno`        | Student profile linked to Django `User` (student ID, admission date)  |
| `Matricula`     | Course enrollment (status, final grade, progress, completed workload) |
| `Aproveitamento` | Request for previously completed subject credit transfer              |
| `SegundaChamada`     | Makeup exam request                                                   |
| `RevisaoNota`    | Grade review request                                                  |
| `Equivalencia`    | Record of subject equivalence from another institution                |

The `Aluno` model includes methods to perform all requests directly: `matricular()`, `trancar_matricula()`, `solicitar_aproveitamento()`, `solicitar_segunda_chamada()`, and `solicitar_revisao_nota()`.

---

### `certifications/` - Certifications and Academic Integrity

Models for certificate issuance and academic integrity incident tracking.

**Models:**

| Model               | Description                                                                      |
| ------------------- | -------------------------------------------------------------------------------- |
| `Certificado`       | Course completion certificate linked to an enrollment (with validity and status) |
| `IncidenteIntegridade` | Record of academic incidents (cheating, plagiarism, fraud, others)               |

The `Certificado` model includes the methods `revogar()`, `suspender()`, and `renovar()` for lifecycle management.

---

### `templates/` - HTML Templates

| Template                     | Description                                                                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `base.html`                  | Base layout with dark sidebar (280px), breadcrumb bar, and content area. Blocks: `title`, `sidebar`, `breadcrumb`, `content` |
| `courses/home.html`          | Standalone homepage with a course card grid (does not inherit from `base.html`)                                              |
| `courses/curso_detail.html` | Course details; inherits from `base.html`                                                                                    |
| `courses/modulo_detail.html` | Module lesson list; inherits from `base.html`                                                                                |
| `courses/aula_detail.html` | Lesson content with previous/next buttons; inherits from `base.html`                                                         |
| `courses/_sidebar.html`      | Sidebar navigation component with expandable modules and lessons (prefixed with `_` because it is a partial template)        |

---

## Model Relationships

```text
Curso --< Modulo --< Aula
  |           |
  |           +--< Avaliacao (objective / essay / project / proctored)
  |                    |
  |                    +--< AvaliacaoRealizada >-- Aluno
  |
  +--< PreRequisito
  +-- RegraCurso

Aluno --< Matricula >-- Curso
              |
              |--< Aproveitamento >-- Modulo
              |--< SegundaChamada >-- Avaliacao
              |--< RevisaoNota >-- Avaliacao
              |--< Equivalencia
              |-- Certificado
              +--< IncidenteIntegridade
```

---

## Installation

**Requirements:** Python 3.12+

```bash
# Clone the repository
git clone <repository-url>
cd plataforma_ensino

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Access the application at:

```text
http://localhost:8000
```

The admin panel is available at:

```text
http://localhost:8000/admin
```

---

## URLs

| Route                                                 | View            | Description               |
| ----------------------------------------------------- | --------------- | ------------------------- |
| `/`                                                   | `home`          | Homepage with course list |
| `/<curso_id>/`                                       | `curso_detail` | Course details            |
| `/<curso_id>/modulo/<modulo_id>/`                    | `modulo_detail` | Module details            |
| `/<curso_id>/modulo/<modulo_id>/aula/<aula_id>/` | `aula_detail` | Lesson content            |
| `/admin/`                                             | -               | Django admin panel        |

---

## Dependencies

```text
Django==6.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3 
```




