# Teaching Platform

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
* Hierarchical navigation: Course → Module → Lesson
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
teaching_platform/                  # Project root
├── manage.py                       # Django CLI (runserver, migrate, etc.)
├── requirements.txt                # Python project dependencies
├── db.sqlite3                      # SQLite database
├── .gitignore                      # Git ignored files
├── README.md                       # Project documentation
│
├── teaching_platform/              # Django project configuration package
│   ├── __init__.py
│   ├── settings.py                 # Global settings (database, apps, language, etc.)
│   ├── urls.py                     # Root routing (admin + courses)
│   ├── wsgi.py                     # Entry point for WSGI servers (production)
│   └── asgi.py                     # Entry point for ASGI servers (async)
│
├── courses/                        # Courses app — only app with implemented views
│   ├── __init__.py
│   ├── apps.py                     # App configuration (CoursesConfig)
│   ├── models.py                   # Models: Course, Module, Lesson, CourseRule, Prerequisite
│   ├── views.py                    # Views: home, course_detail, module_detail, lesson_detail
│   ├── urls.py                     # Courses app routes
│   ├── admin.py                    # Model registration in admin panel
│   ├── tests.py                    # Tests (empty)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Creation of course tables
│
├── assessments/                    # Assessments app — models ready, views empty
│   ├── __init__.py
│   ├── apps.py                     # App configuration (AssessmentsConfig)
│   ├── models.py                   # Models: Assessment, ObjectiveAssessment, EssayAssessment,
│   │                               #          PracticalProject, ProctoredExam, CompletedAssessment
│   ├── views.py                    # Views (empty — in development)
│   ├── admin.py                    # Model registration in admin panel
│   ├── tests.py                    # Tests (empty)
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py         # Creation of base Assessment table
│       └── 0002_initial.py         # Creation of child types and CompletedAssessment
│
├── students/                       # Students app — models ready, views empty
│   ├── __init__.py
│   ├── apps.py                     # App configuration (StudentsConfig)
│   ├── models.py                   # Models: Student, Enrollment, Request, GradeReview,
│   │                               #          MakeupExam, CreditTransfer, Equivalence
│   ├── views.py                    # Views (empty — in development)
│   ├── admin.py                    # Model registration in admin panel
│   ├── tests.py                    # Tests (empty)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Creation of all student tables
│
├── certifications/                 # Certifications app — models ready, views empty
│   ├── __init__.py
│   ├── apps.py                     # App configuration (CertificationsConfig)
│   ├── models.py                   # Models: Certificate, IntegrityIncident
│   ├── views.py                    # Views (empty — in development)
│   ├── admin.py                    # Model registration in admin panel
│   ├── tests.py                    # Tests (empty)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py         # Creation of certification tables
│
└── templates/                      # Global HTML templates
    ├── base.html                   # Base template: layout with sidebar + content area
    └── courses/                    # Templates specific to the courses app
        ├── home.html               # Homepage — card grid with all courses
        ├── course_detail.html      # Course details with start button
        ├── module_detail.html      # Module details with lesson list
        ├── lesson_detail.html      # Lesson content with previous/next navigation
        └── _sidebar.html           # Reusable sidebar navigation component
```

---

## App Descriptions

### `teaching_platform/` — Project Configuration

Core Django package containing global settings and root routing.

| File                  | Purpose                                                                      |
| --------------------- | ---------------------------------------------------------------------------- |
| `settings.py`         | Defines database, installed apps, language, timezone, and template directory |
| `urls.py`             | Maps `/admin/` to the Django admin panel and `/` to the `courses` app URLs   |
| `wsgi.py` / `asgi.py` | Entry points for deployment on production servers                            |

---

### `courses/` — Course Management

The only app with implemented views and templates. Responsible for all content navigation.

**Models:**

| Model          | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `Course`       | Course with name, workload, and timestamps                                 |
| `Module`       | Ordered module within a course                                             |
| `Lesson`       | Lesson with title, content, duration, and order within the module          |
| `CourseRule`   | Completion rules: minimum grade, minimum workload, mandatory final project |
| `Prerequisite` | Course or module prerequisite for enrollment                               |

**Views:**

| View            | Route                                                 | Description                             |
| --------------- | ----------------------------------------------------- | --------------------------------------- |
| `home`          | `/`                                                   | Lists all available courses             |
| `course_detail` | `/<course_id>/`                                       | Displays course details and start link  |
| `module_detail` | `/<course_id>/module/<module_id>/`                    | Lists module lessons                    |
| `lesson_detail` | `/<course_id>/module/<module_id>/lesson/<lesson_id>/` | Displays lesson content with navigation |

---

### `assessments/` — Assessments

Models prepared for multiple assessment types using multi-table inheritance.

**Models:**

| Model                 | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `Assessment`          | Base assessment linked to a module (type + weight)      |
| `ObjectiveAssessment` | Multiple-choice exam with questions stored in JSONField |
| `EssayAssessment`     | Essay exam with text description                        |
| `PracticalProject`    | Project with optional repository link                   |
| `ProctoredExam`       | Exam with active remote monitoring                      |
| `CompletedAssessment` | Record of a student’s grade in an assessment            |

---

### `students/` — Students and Enrollments

Models to manage the student academic lifecycle, from enrollment to administrative requests.

**Models:**

| Model            | Description                                                           |
| ---------------- | --------------------------------------------------------------------- |
| `Student`        | Student profile linked to Django `User` (student ID, admission date)  |
| `Enrollment`     | Course enrollment (status, final grade, progress, completed workload) |
| `CreditTransfer` | Request for previously completed subject credit transfer              |
| `MakeupExam`     | Makeup exam request                                                   |
| `GradeReview`    | Grade review request                                                  |
| `Equivalence`    | Record of subject equivalence from another institution                |

The `Student` model includes methods to perform all requests directly: `enroll()`, `suspend_enrollment()`, `request_credit_transfer()`, `request_makeup_exam()`, and `request_grade_review()`.

---

### `certifications/` — Certifications and Academic Integrity

Models for certificate issuance and academic integrity incident tracking.

**Models:**

| Model               | Description                                                                      |
| ------------------- | -------------------------------------------------------------------------------- |
| `Certificate`       | Course completion certificate linked to an enrollment (with validity and status) |
| `IntegrityIncident` | Record of academic incidents (cheating, plagiarism, fraud, others)               |

The `Certificate` model includes the methods `revoke()`, `suspend()`, and `renew()` for lifecycle management.

---

### `templates/` — HTML Templates

| Template                     | Description                                                                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `base.html`                  | Base layout with dark sidebar (280px), breadcrumb bar, and content area. Blocks: `title`, `sidebar`, `breadcrumb`, `content` |
| `courses/home.html`          | Standalone homepage with a course card grid (does not inherit from `base.html`)                                              |
| `courses/course_detail.html` | Course details; inherits from `base.html`                                                                                    |
| `courses/module_detail.html` | Module lesson list; inherits from `base.html`                                                                                |
| `courses/lesson_detail.html` | Lesson content with previous/next buttons; inherits from `base.html`                                                         |
| `courses/_sidebar.html`      | Sidebar navigation component with expandable modules and lessons (prefixed with `_` because it is a partial template)        |

---

## Model Relationships

```text
Course ──< Module ──< Lesson
  │           │
  │           └──< Assessment (objective / essay / project / proctored)
  │                    │
  │                    └──< CompletedAssessment >── Student
  │
  └──< Prerequisite
  └── CourseRule

Student ──< Enrollment >── Course
              │
              ├──< CreditTransfer >── Module
              ├──< MakeupExam >── Assessment
              ├──< GradeReview >── Assessment
              ├──< Equivalence
              ├── Certificate
              └──< IntegrityIncident
```

---

## Installation

**Requirements:** Python 3.12+

```bash
# Clone the repository
git clone <repository-url>
cd teaching_platform

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
| `/<course_id>/`                                       | `course_detail` | Course details            |
| `/<course_id>/module/<module_id>/`                    | `module_detail` | Module details            |
| `/<course_id>/module/<module_id>/lesson/<lesson_id>/` | `lesson_detail` | Lesson content            |
| `/admin/`                                             | —               | Django admin panel        |

---

## Dependencies

```text
Django==6.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```

