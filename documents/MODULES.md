# Modules

Modules organizam o sistema por conceitos do dominio, nao apenas por criterios
tecnicos. Neste projeto, os apps Django representam modulos de negocio e cada
um agrupa entidades, regras, repositories, factories, services de aplicacao e
interfaces relacionadas ao mesmo conceito.

As pastas `domain`, `application`, `infrastructure` e `presentation` sao camadas
internas de cada modulo. Elas nao substituem o modulo de negocio; apenas
organizam responsabilidades dentro dele.

## Modulos de negocio

| Pacote Django | Nome no dominio | Conceito agrupado |
| --- | --- | --- |
| `courses` | Catalogo de Cursos | Cursos, modulos, aulas, pre-requisitos e regras de curso |
| `students` | Jornada Academica | Alunos, matriculas, progresso, solicitacoes e equivalencias |
| `assessments` | Avaliacoes | Avaliacoes, tipos de prova, projetos praticos e notas |
| `certifications` | Certificacao e Integridade Academica | Certificados, emissao, renovacao, revogacao e incidentes |

## Criterios usados

- O nome do modulo precisa apontar para uma area reconhecivel do negocio.
- Os elementos internos devem mudar por motivos relacionados ao mesmo conceito.
- Regras de negocio ficam no modulo que possui o conceito principal.
- Camadas tecnicas nao devem virar a principal forma de navegacao do dominio.

## Decisoes

Os pacotes continuam em ingles para preservar compatibilidade com imports,
migrations, URLs e configuracao Django ja existentes.

Para refletir a linguagem do negocio na aplicacao, cada `AppConfig` recebeu um
`verbose_name` em portugues:

- `Catalogo de Cursos`;
- `Jornada Academica`;
- `Avaliacoes`;
- `Certificacao e Integridade Academica`.

Essa decisao evita uma renomeacao arriscada dos pacotes e, ao mesmo tempo,
deixa explicito que os apps sao modulos de dominio, nao apenas divisorias
tecnicas.

## O que nao deve virar modulo separado

Pastas como `repositories`, `selectors`, `services`, `forms` ou `views` nao sao
modulos de dominio por si so. Elas sao responsabilidades tecnicas dentro de um
modulo de negocio.

Tambem nao foram criados modulos genericos como `core`, `utils` ou `shared`
porque isso tenderia a agrupar codigo por conveniencia tecnica, nao por conceito
do dominio.
