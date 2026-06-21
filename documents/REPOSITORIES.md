# Repositories

Os repositories do projeto representam abstracoes para recuperar e persistir
Aggregate Roots. As interfaces ficam na camada de dominio e as implementacoes
concretas com Django ORM ficam na camada de infraestrutura.

## Repositories definidos

| Agregado | Aggregate Root | Interface | Implementacao |
| --- | --- | --- | --- |
| Catalogo de curso | `Curso` | `courses.domain.repositories.CourseRepository` | `courses.infrastructure.repositories.DjangoCourseRepository` |
| Jornada academica | `Matricula` | `students.domain.repositories.EnrollmentRepository` | `students.infrastructure.repositories.DjangoEnrollmentRepository` |
| Avaliacao | `Avaliacao` | `assessments.domain.repositories.AssessmentRepository` | `assessments.infrastructure.repositories.DjangoAssessmentRepository` |
| Certificacao | `Certificado` | `certifications.domain.repositories.CertificateRepository` | `certifications.infrastructure.repositories.DjangoCertificateRepository` |

## Regras adotadas

- Interfaces de repository pertencem ao dominio e usam `Protocol`.
- Implementacoes concretas ficam em `infrastructure/repositories.py`.
- Nao ha repository para Value Objects.
- Nao ha repository para entidades internas como `Modulo`, `Aula`,
  `Solicitacao`, `Aproveitamento`, `SegundaChamada`, `RevisaoNota`,
  `Equivalencia` ou `AvaliacaoRealizada`.
- Quando uma entidade interna precisa ser persistida por causa do ORM, essa
  persistencia acontece dentro do repository da Aggregate Root correspondente.

## Exemplos

- Modulos e aulas sao manipulados por `CourseRepository`, porque pertencem ao
  agregado `Curso`.
- Solicitacoes e equivalencias sao manipuladas por metodos de `Matricula`, sem
  repository proprio.
- Resultado de avaliacao e salvo por `AssessmentRepository`, pois pertence ao
  contexto da root `Avaliacao`.
- `Certificado` tem repository proprio porque possui ciclo de vida independente:
  emissao, suspensao, renovacao e revogacao.
