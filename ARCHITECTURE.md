# Arquitetura DDD

O sistema esta dividido em quatro contextos delimitados:

- `courses`: catalogo, modulos, aulas e regras de curso.
- `students`: alunos, matriculas e solicitacoes academicas.
- `assessments`: avaliacoes e notas.
- `certifications`: certificados e integridade academica.

Cada contexto segue as mesmas camadas:

```text
context/
|-- domain/          # Politicas, excecoes e contratos sem dependencia da UI
|-- application/     # Casos de uso e consultas da aplicacao
|-- infrastructure/  # Repositorios e adaptadores do Django ORM
|-- presentation/    # Views e formularios HTTP
|-- models.py        # Modelos ORM e fachada estavel para o Django
|-- views.py         # Fachada de compatibilidade para URLs existentes
`-- admin.py
```

## Regra de dependencia

`presentation -> application -> domain`

A infraestrutura implementa os contratos do dominio e e injetada nos casos de
uso. Os servicos possuem implementacoes Django como padrao, mas aceitam
repositorios alternativos para testes ou outra persistencia.

## Convencoes

- Views tratam HTTP, autenticacao, mensagens e renderizacao.
- Services executam comandos que alteram estado e definem transacoes.
- Selectors concentram consultas de leitura.
- Repositories encapsulam detalhes do ORM.
- Policies guardam regras puras que podem ser testadas sem banco.
- Domain Services guardam operacoes de negocio que nao pertencem naturalmente a
  uma unica Entity ou Value Object.
- Imports publicos antigos sao mantidos para preservar URLs, admin e migrations.
