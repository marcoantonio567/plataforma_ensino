# Domain Services

Domain Services sao usados apenas quando uma operacao importante do dominio nao
pertence naturalmente a uma unica Entity ou Value Object.

Eles devem representar uma operacao real da linguagem do negocio. Classes
genericas como `AlunoService`, `CursoService` ou `CertificadoService` nao sao
consideradas Domain Services apenas pelo nome.

## Domain Service implementado

### `AvaliadorElegibilidadeCertificado`

Local: `certifications/domain/services.py`

Operacao de negocio: validar se uma matricula esta elegivel para emissao de
certificado.

Por que e Domain Service:

- a decisao envolve `Matricula`;
- depende da `RegraCurso` registrada na matricula;
- depende de resultados de projeto pratico;
- depende de incidentes de integridade academica;
- nao pertence naturalmente apenas a `Certificado`, porque o certificado ainda
  nem precisa existir quando a elegibilidade e avaliada.

## O que nao foi tratado como Domain Service

Os arquivos `application/services.py` continuam sendo Application Services.
Eles coordenam transacoes, repositories e casos de uso da aplicacao.

Exemplos:

- `students.application.services.enroll_student`;
- `courses.application.services.create_module`;
- `assessments.application.services.record_grade`;
- `certifications.application.services.issue`.

Esses casos nao foram renomeados para Domain Services porque eles coordenam fluxo
da aplicacao, persistencia e retorno para a interface.

Regras que pertencem naturalmente a uma Entity ou Value Object continuam onde
estao. Exemplos:

- transicoes de `Matricula`;
- ciclo de vida de `Certificado`;
- validacao de nota;
- regra vigente de `Curso`.
