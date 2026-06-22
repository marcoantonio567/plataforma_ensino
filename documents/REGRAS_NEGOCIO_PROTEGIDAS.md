# Regras de negocio protegidas

Este documento demonstra onde as principais regras de negocio ficam protegidas
no codigo. A regra geral do projeto e manter a protecao perto do objeto que
possui o estado critico, usando Value Objects, metodos de dominio, Domain
Services e constraints do banco como camadas complementares.

## Matriz de regras

| Regra de negocio | Classe onde foi implementada | Objeto que protege | Como impede estado invalido | Invariante mantida |
| --- | --- | --- | --- | --- |
| Curso deve ter carga horaria positiva | `Curso`, `CargaHoraria` | Aggregate Root `Curso` | `Curso.save()` e `Curso.clean()` aplicam o Value Object `CargaHoraria` | Nao existe curso com carga horaria menor ou igual a zero |
| Regra de curso deve ter media minima valida | `RegraCurso`, `MediaMinima` | Entidade `RegraCurso` dentro do agregado `Curso` | `RegraCurso.save()` e `RegraCurso.clean()` aplicam `MediaMinima` | Media minima fica entre 0 e 10 |
| Regra de curso nao pode terminar antes de iniciar | `RegraCurso` | Entidade `RegraCurso` | `validar_periodo()` e chamado no `save()` e no `clean()` | Periodo de vigencia da regra e cronologicamente valido |
| Modulos e aulas devem ter ordem positiva | `Modulo`, `Aula`, `Ordem` | Aggregate Root `Curso` e entidades internas | `save()`, `clean()` e metodos de criacao aplicam `Ordem` | Ordem sempre e maior que zero |
| Aula deve pertencer ao curso quando criada pela raiz | `Curso.adicionar_aula()` | Aggregate Root `Curso` | `_ensure_modulo_belongs_to_course()` rejeita modulo de outro curso | O agregado `Curso` nao manipula aulas de outro curso |
| Duracao da aula deve ser positiva | `Aula`, `DuracaoAula` | Entidade `Aula` | `Aula.save()`, `Aula.clean()` e `Modulo._adicionar_aula()` aplicam `DuracaoAula` | Nenhuma aula tem duracao menor ou igual a zero |
| Matricula deve registrar regra do curso | `Matricula`, `MatriculaFactory` | Aggregate Root `Matricula` | Factory exige regra vigente e `Matricula.save()` rejeita ausencia de regra | Toda matricula conhece a regra usada para avaliar conclusao |
| Regra da matricula deve pertencer ao mesmo curso | `Matricula`, `MatriculaFactory` | Aggregate Root `Matricula` | Factory e `_validate_course_rule()` rejeitam regra de outro curso | Matricula nao pode ser avaliada por regra de curso diferente |
| Aluno nao pode ter duas matriculas no mesmo curso | `Matricula` | Banco e Aggregate Root `Matricula` | `unique_together = ("aluno", "curso")` | Existe no maximo uma matricula por aluno e curso |
| Transicoes de status de matricula seguem fluxo permitido | `Matricula` | Aggregate Root `Matricula` | Metodos `cancelar`, `trancar`, `reativar`, `concluir` e `_validate_status_transition()` bloqueiam transicoes invalidas no `save()` | Matricula concluida nao volta para ativa, e estados so mudam por fluxo permitido |
| Progresso deve ficar entre 0 e 100 | `Matricula`, `PercentualProgresso` | Aggregate Root `Matricula` | `atualizar_progresso()`, `save()` e `clean()` aplicam Value Object | Progresso nunca fica abaixo de 0 nem acima de 100 |
| Media final deve ficar entre 0 e 10 | `Matricula`, `MediaFinal` | Aggregate Root `Matricula` | `concluir()`, `save()` e `clean()` aplicam Value Object | Media final sempre fica na escala academica valida |
| Carga horaria cumprida nao pode ser negativa | `Matricula`, `CargaHorariaCumprida` | Aggregate Root `Matricula` | `atualizar_progresso()`, `concluir()`, `save()` e `clean()` aplicam Value Object | Carga horaria cumprida nunca e negativa |
| Solicitacoes so podem ser abertas para itens do mesmo curso | `Matricula` | Aggregate Root `Matricula` | `_ensure_modulo_belongs_to_course()` e `_ensure_avaliacao_belongs_to_course()` rejeitam modulo ou avaliacao externos | Solicitacoes pertencem a jornada academica da propria matricula |
| Solicitacao deve seguir fluxo de analise | `Solicitacao` | Entidade interna do agregado `Matricula` | `iniciar_analise()`, `aprovar()` e `rejeitar()` validam status atual | Solicitacao finalizada nao volta para analise nem muda livremente |
| Nota deve ficar entre 0 e 10 | `AvaliacaoRealizada`, `Nota` | Aggregate Root `Avaliacao` e entidade interna | `registrar_nota()`, `save()` e `clean()` aplicam `validate_grade()` | Toda nota registrada fica na escala valida |
| Peso da avaliacao deve ser positivo | `Avaliacao` | Aggregate Root `Avaliacao` | `alterar_peso()`, `save()` e `clean()` rejeitam peso menor ou igual a zero | Avaliacao nunca pondera nota com peso invalido |
| Aluno nao pode registrar duas realizacoes da mesma avaliacao | `AvaliacaoRealizada` | Banco e agregado `Avaliacao` | `unique_together = ("aluno", "avaliacao")` | Existe no maximo um resultado por aluno e avaliacao |
| Certificado so pode ser emitido para matricula elegivel | `AvaliadorElegibilidadeCertificado`, `Certificado` | Domain Service e Aggregate Root `Certificado` | `Certificado.save()` valida status emitido com o Domain Service | Certificado emitido sempre corresponde a matricula concluida e elegivel |
| Emissao exige media minima e carga horaria minima da regra da matricula | `AvaliadorElegibilidadeCertificado` | Domain Service de certificacao | `validar_emissao()` compara dados da matricula com `RegraCurso` | Certificacao respeita a regra congelada na matricula |
| Emissao pode exigir projeto final concluido | `AvaliadorElegibilidadeCertificado`, `Certificado` | Domain Service e Aggregate Root `Certificado` | `Certificado.save()` consulta projeto pratico aprovado quando a regra exige | Certificado nao e emitido sem projeto final obrigatorio |
| Incidente grave bloqueia emissao de certificado | `AvaliadorElegibilidadeCertificado`, `Certificado` | Domain Service e Aggregate Root `Certificado` | `Certificado.save()` consulta incidentes graves antes de emitir | Matricula com violacao grave nao recebe certificado emitido |
| Certificado possui ciclo de vida protegido | `Certificado` | Aggregate Root `Certificado` | `emitir()`, `suspender()`, `revogar()`, `renovar()` e `_validate_status_transition()` rejeitam transicoes invalidas | Certificado revogado nao volta a emitido, suspenso ou renovado |
| Existe apenas um certificado por matricula | `Certificado` | Banco e Aggregate Root `Certificado` | `OneToOneField` entre certificado e matricula | Matricula nao recebe certificados duplicados |

## Aggregates e invariantes principais

### Catalogo de Curso

Aggregate Root: `Curso`.

Invariantes mantidas:

- Curso tem carga horaria positiva.
- Modulos e aulas tem ordem positiva.
- Aulas tem duracao positiva.
- Modulos e aulas manipulados pela raiz pertencem ao mesmo curso.
- Regras de curso possuem periodo valido e media minima dentro da escala.

### Jornada Academica

Aggregate Root: `Matricula`.

Invariantes mantidas:

- Toda matricula possui uma regra de curso associada.
- A regra associada pertence ao curso da matricula.
- Existe apenas uma matricula por aluno e curso.
- Status de matricula muda apenas por transicoes permitidas.
- Progresso, media final e carga horaria cumprida permanecem em faixas validas.
- Solicitacoes e equivalencias pertencem a propria jornada aluno-curso.

### Avaliacao

Aggregate Root: `Avaliacao`.

Invariantes mantidas:

- Peso da avaliacao e positivo.
- Nota registrada fica entre 0 e 10.
- Existe apenas uma realizacao por aluno e avaliacao.

### Certificacao

Aggregate Root: `Certificado`.

Invariantes mantidas:

- Certificado emitido exige matricula concluida.
- Certificado emitido respeita media minima, carga horaria minima, projeto final
  obrigatorio e ausencia de incidente grave.
- Certificado revogado nao pode voltar a emitido, suspenso ou renovado.
- Existe apenas um certificado por matricula.

## Evidencias em testes

As regras acima sao cobertas por testes nos arquivos:

- `courses/tests.py`
- `students/tests.py`
- `assessments/tests.py`
- `certifications/tests.py`

Os testes verificam Value Objects, transicoes de status, factories, services de
aplicacao, Domain Service de certificacao e bloqueios contra alteracoes diretas
por `save()`.
