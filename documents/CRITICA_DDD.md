# Critica construtiva DDD - Plataforma de Ensino

Este documento avalia o projeto pela perspectiva de Domain-Driven Design (DDD), com foco nos pontos pedidos: linguagem ubiqua, entidades, value objects, agregados, aggregate roots, repositories, factories, domain services, modules, invariantes de dominio, protecao das regras de negocio, organizacao das camadas e principios de Supple Design.

## Visao geral

O projeto ja demonstra uma boa intencao arquitetural. Existem contextos separados por apps Django (`courses`, `students`, `assessments`, `certifications`) e cada app tenta organizar as responsabilidades em `domain`, `application`, `infrastructure` e `presentation`.

Esse e um bom primeiro passo. Porem, hoje o DDD ainda esta mais presente na organizacao das pastas do que no modelo de dominio em si. Boa parte das regras ainda fica espalhada entre models Django, services, forms, views e constraints simples de banco. Para evoluir, o principal objetivo deve ser tornar o dominio mais expressivo, mais protegido e menos dependente do framework.

## 1. Linguagem ubiqua

### O que esta bom

- O projeto usa termos do negocio em portugues: `Curso`, `Modulo`, `Aula`, `Aluno`, `Matricula`, `Avaliacao`, `Certificado`, `Solicitacao`, `SegundaChamada`, `RevisaoNota`.
- Os contextos principais sao faceis de entender.
- Os nomes das telas e models conversam bem com o dominio educacional.

### O que falta melhorar

- Ha mistura entre portugues e ingles em nomes importantes:
  - `create_module`, `create_lesson`, `record_grade`, `enroll_student`, `cancel_enrollment`.
  - Enquanto os models usam `Curso`, `Modulo`, `Aula`, `Matricula`.
- Isso enfraquece a linguagem ubiqua, porque o codigo muda de idioma entre dominio e aplicacao.
- Alguns conceitos ainda estao genericos demais:
  - `RegraCurso` poderia ser mais explicita, como `RegraConclusaoCurso`.
  - `Solicitacao` e ampla demais e nao deixa claro quais estados e regras valem para cada tipo de solicitacao.
  - `PreRequisito.referencia_id` usa um ID generico, o que esconde se o requisito e realmente um curso ou modulo valido.

### Sugestao pratica

Padronizar a linguagem do codigo em torno dos termos do dominio. Como o sistema esta em portugues, os casos de uso poderiam seguir o mesmo idioma:

- `matricular_aluno`
- `cancelar_matricula`
- `registrar_nota`
- `criar_modulo`
- `criar_aula`
- `emitir_certificado`
- `revogar_certificado`

Tambem vale criar um pequeno glossario no projeto, por exemplo:

```text
Aluno: pessoa cadastrada que pode se matricular em cursos.
Matricula: vinculo entre aluno e curso, com status, progresso e resultado.
Curso: trilha de aprendizado composta por modulos.
Modulo: agrupamento ordenado de aulas dentro de um curso.
Aula: unidade de conteudo dentro de um modulo.
Regra de conclusao: criterios minimos para concluir um curso.
Certificado: comprovante emitido para uma matricula concluida.
```

## 2. Entities

### O que esta bom

As principais entidades existem e possuem identidade propria:

- `Curso`
- `Modulo`
- `Aula`
- `Aluno`
- `Matricula`
- `Avaliacao`
- `AvaliacaoRealizada`
- `Certificado`
- `IncidenteIntegridade`

Essas classes fazem sentido como entidades porque possuem ciclo de vida, identidade e relacoes com outras partes do sistema.

### O que falta melhorar

- As entidades ainda estao muito anemicas em alguns pontos. Elas guardam dados, mas poucas protegem comportamento relevante.
- Algumas entidades possuem comportamento, mas esse comportamento acessa diretamente o ORM:
  - `Aluno.matricular()`
  - `Aluno.solicitar_aproveitamento()`
  - `Aluno.solicitar_segunda_chamada()`
  - `Aluno.solicitar_revisao_nota()`
  - `Certificado.revogar()`, `suspender()` e `renovar()`
- Isso mistura dominio com persistencia ou aplicacao.
- `Matricula`, que parece ser uma entidade central, quase nao possui comportamento proprio. Status como `ATIVA`, `TRANCADA`, `CONCLUIDA` e `CANCELADA` sao alterados diretamente fora dela.

### Sugestao pratica

Colocar comportamentos importantes dentro das entidades ou em domain services, mas sem deixar que qualquer camada altere estados livremente.

Exemplo conceitual:

```python
matricula.cancelar()
matricula.reativar()
matricula.concluir(media_final, carga_horaria_cumprida)
matricula.trancar()
```

Dentro desses metodos devem ficar as regras:

- Nao cancelar matricula ja concluida.
- Nao concluir matricula sem cumprir carga horaria minima.
- Nao concluir matricula com media abaixo da minima.
- Nao reativar matricula concluida.

## 3. Value Objects

### O que esta bom

O projeto ja possui alguns valores que poderiam virar Value Objects:

- Nota
- Carga horaria
- Duracao da aula
- Numero de matricula
- Periodo de validade do certificado
- Ordem de modulo/aula
- Media minima
- Progresso da matricula

### O que falta melhorar

Hoje esses conceitos aparecem como tipos primitivos:

- `FloatField` para nota, media, progresso.
- `PositiveIntegerField` para carga horaria e duracao.
- `CharField` para numero de matricula.
- `DateField` para validade.

Isso cria "obsessao por primitivos". O problema nao e usar campos simples no banco, mas deixar regras importantes soltas.

Exemplos:

- Nota deve estar entre 0 e 10.
- Progresso deve estar entre 0 e 100.
- Duracao da aula deve ser maior que zero.
- Carga horaria do curso deve ser maior que zero.
- Numero de matricula deve seguir um formato unico.

### Sugestao pratica

Criar objetos pequenos para validar e nomear conceitos do dominio.

Exemplos:

```python
Nota(8.5)
PercentualProgresso(70)
CargaHoraria(40)
DuracaoAula(30)
NumeroMatricula("ALU12345678")
```

Mesmo que o Django salve isso em campos simples, a aplicacao pode construir esses objetos antes de mudar o estado do dominio. Isso melhora legibilidade e reduz validacoes duplicadas.

## 4. Aggregates

### O que esta bom

O projeto ja sugere agregados naturais:

- Curso com modulos, aulas, regras e pre-requisitos.
- Aluno com matriculas e solicitacoes.
- Matricula com avaliacoes realizadas, certificado e incidentes.
- Avaliacao com realizacoes.

### O que falta melhorar

Os limites dos agregados ainda nao estao claros. Hoje qualquer parte do sistema consegue acessar models relacionados diretamente pelo ORM e alterar dados sem passar por uma raiz.

Exemplos:

- `Modulo` pode ser criado diretamente por `course.modulos.create`.
- `Aula` pode ser criada diretamente por `module.aulas.create`.
- `Matricula.status` pode ser alterado diretamente.
- `Certificado.status` pode ser alterado diretamente.

Isso enfraquece o controle das invariantes.

### Sugestao pratica

Definir explicitamente quais objetos pertencem a cada agregado e como eles podem ser modificados.

Uma proposta inicial:

| Agregado | Aggregate Root | Entidades internas |
| --- | --- | --- |
| Catalogo de curso | `Curso` | `Modulo`, `Aula`, `PreRequisito`, `RegraCurso` |
| Jornada academica | `Matricula` | `Solicitacao`, `Equivalencia`, possivelmente `AvaliacaoRealizada` |
| Avaliacao | `Avaliacao` | Questoes, criterios, realizacoes dependendo da regra |
| Certificacao | `Certificado` ou `Matricula` | Certificado, incidentes de integridade |

Depois disso, evitar que entidades internas sejam manipuladas diretamente de fora do agregado.

## 5. Aggregate Roots

### O que esta bom

Algumas roots aparecem naturalmente:

- `Curso` para organizar conteudo.
- `Matricula` para controlar a relacao aluno-curso.
- `Avaliacao` para controlar provas e notas.
- `Certificado` para ciclo de vida da certificacao.

### O que falta melhorar

- `Matricula` deveria ser uma das roots mais importantes, mas hoje e tratada quase como registro de banco.
- Muitas regras passam por `Aluno`, mas o estado critico esta em `Matricula`.
- `Curso` nao controla diretamente a criacao de modulo/aula. A criacao fica em service e usa relacoes ORM.
- `Certificado` chama service de aplicacao dentro do model, criando dependencia circular conceitual: o dominio depende da camada de aplicacao.

### Sugestao pratica

Dar autoridade clara para as roots:

- `Curso.adicionar_modulo(nome)`
- `Modulo.adicionar_aula(titulo, duracao, conteudo)`
- `Matricula.cancelar()`
- `Matricula.reativar()`
- `Matricula.registrar_progresso(percentual)`
- `Matricula.concluir()`
- `Certificado.suspender()`
- `Certificado.revogar()`
- `Certificado.renovar(validade)`

A camada de aplicacao deve coordenar o caso de uso e salvar, mas nao deveria ser o unico lugar onde as regras vivem.

## 6. Repositories

### O que esta bom

O projeto ja possui interfaces com `Protocol` em `domain/repositories.py` e implementacoes Django em `infrastructure/repositories.py`.

Isso e positivo porque:

- Reduz acoplamento direto com o ORM.
- Facilita testes.
- Indica uma direcao correta de arquitetura.

### O que falta melhorar

- Os repositories ainda sao muito finos e tecnicos.
- Alguns metodos representam operacoes de banco, nao operacoes do dominio:
  - `next_module_order`
  - `next_lesson_order`
  - `save_enrollment`
  - `delete_lesson`
- Selectors ainda acessam ORM diretamente, o que pode ser aceitavel para leitura, mas precisa ser uma decisao consciente.
- Views ainda usam `get_object_or_404` com models diretamente em varios pontos.

### Sugestao pratica

Fazer repositories mais orientados a agregados:

```python
CourseRepository.get(course_id)
CourseRepository.save(course)
EnrollmentRepository.get_by_student_and_course(student_id, course_id)
EnrollmentRepository.save(matricula)
CertificateRepository.get_by_enrollment(enrollment_id)
CertificateRepository.save(certificado)
```

Para consultas de tela, `selectors` podem continuar existindo, mas devem ser tratados como leitura otimizada, nao como local para regra de negocio.

## 7. Factories

### O que esta bom

Existem criacoes centralizadas em services/repositories:

- Criacao de aluno com numero de matricula.
- Criacao de matricula.
- Criacao de modulo e aula com ordem sequencial.

### O que falta melhorar

Nao existem factories explicitas para criacoes com regra.

Casos que merecem factory:

- Criar `Aluno` com numero de matricula valido e unico.
- Criar `Matricula` com regra vigente do curso.
- Criar `Certificado` apenas quando a matricula estiver concluida.
- Criar `AvaliacaoRealizada` com nota valida.
- Criar `Modulo` e `Aula` respeitando ordem e duplicidade.

### Sugestao pratica

Criar factories quando a construcao tiver regra, nao apenas quando for `objects.create`.

Exemplos:

```python
AlunoFactory.criar_para_usuario(user)
MatriculaFactory.criar(aluno, curso, regra_vigente)
CertificadoFactory.emitir_para(matricula)
AvaliacaoRealizadaFactory.registrar(aluno, avaliacao, nota, data)
```

Factories ajudam a impedir que objetos nascam em estado invalido.

## 8. Domain Services

### O que esta bom

O projeto possui policies puras:

- `validate_grade`
- `renewed_expiration`

Tambem possui services de aplicacao com transacoes:

- Matricula.
- Cursos.
- Certificados.
- Avaliacoes.

### O que falta melhorar

- Alguns services atuais parecem ser application services, nao domain services.
- Domain services deveriam representar regras de dominio que nao pertencem naturalmente a uma unica entidade.
- Hoje regras importantes ainda nao existem ou estao simplificadas demais.

Exemplos de regras que poderiam virar domain services:

- Verificar se aluno pode se matricular em um curso considerando pre-requisitos.
- Calcular media final ponderada.
- Verificar se matricula pode receber certificado.
- Avaliar se incidente de integridade bloqueia certificacao.
- Determinar regra de curso vigente por data.

### Sugestao pratica

Separar melhor:

- Application Service: coordena caso de uso, transacao, repositorios e retorno para a UI.
- Domain Service: executa regra pura do negocio.

Exemplo:

```python
PodeMatricularAluno.verificar(aluno, curso, historico)
CalculadoraMediaFinal.calcular(avaliacoes_realizadas)
PoliticaCertificacao.pode_emitir(matricula, incidentes)
```

## 9. Modules

### O que esta bom

Os apps representam bons candidatos a bounded contexts:

- `courses`
- `students`
- `assessments`
- `certifications`

A separacao por camadas dentro de cada app tambem ajuda.

### O que falta melhorar

- Os limites entre contextos ainda estao vazando por imports diretos de models.
- `students` conhece `courses.Curso` e `courses.RegraCurso`.
- `assessments` conhece `courses.Modulo` e `students.Aluno`.
- `certifications` conhece `students.Matricula`.

Em Django isso e comum, mas em DDD vale deixar claro se esses sao contextos realmente separados ou apenas modulos internos do mesmo monolito.

### Sugestao pratica

Como o projeto parece ser um monolito modular, uma abordagem realista e:

- Manter os apps separados.
- Evitar que regras de um app sejam alteradas diretamente por outro.
- Usar application services ou interfaces para comunicacao entre contextos.
- Documentar os limites:
  - `courses` define estrutura do curso.
  - `students` gerencia a jornada do aluno.
  - `assessments` gerencia notas e avaliacoes.
  - `certifications` decide emissao, suspensao e revogacao de certificados.

## 10. Invariantes de dominio

### O que esta bom

Algumas invariantes ja aparecem:

- Nota entre 0 e 10 em `validate_grade`.
- Uma matricula por aluno e curso via `unique_together`.
- Uma realizacao por aluno e avaliacao via `unique_together`.
- Ordem unica de modulo por curso.
- Ordem unica de aula por modulo.
- Certificado unico por matricula via `OneToOneField`.

### O que falta melhorar

Muitas invariantes importantes ainda nao estao protegidas:

- Curso deveria ter carga horaria maior que zero.
- Aula deveria ter duracao maior que zero.
- Progresso da matricula deveria ficar entre 0 e 100.
- Media final deveria ficar entre 0 e 10.
- Matricula concluida deveria exigir media minima e carga horaria minima.
- Certificado deveria ser emitido apenas para matricula concluida.
- Certificado talvez nao devesse ser renovado se estiver revogado.
- Aluno nao deveria se matricular sem cumprir pre-requisitos.
- Pre-requisito deveria apontar para um curso ou modulo existente.
- Pesos de avaliacao talvez devam ser positivos.
- Status de solicitacao deveria seguir fluxo permitido, por exemplo: `PENDENTE -> EM_ANALISE -> APROVADA/REJEITADA`.

### Sugestao pratica

Criar uma lista oficial de invariantes por agregado e cobrir cada uma com teste.

Exemplo:

```text
Matricula:
- Nao pode ser concluida se estiver cancelada.
- Nao pode ser concluida sem media minima.
- Nao pode ser reativada se estiver concluida.
- Progresso deve ficar entre 0 e 100.

Certificado:
- So pode ser emitido para matricula concluida.
- Nao pode renovar certificado revogado sem processo explicito.
- Certificado suspenso nao deve ser considerado valido.
```

## 11. Protecao das regras de negocio

### O que esta bom

- Algumas operacoes passam por services.
- Ha uso de `transaction.atomic`.
- Alguns testes verificam comportamento basico.
- Repositories ajudam a reduzir acesso direto ao ORM em alguns fluxos.

### O que falta melhorar

- Ainda e possivel alterar campos criticos diretamente:
  - `matricula.status = ...`
  - `certificado.status = ...`
  - `avaliacao_realizada.nota = ...`
- Forms podem salvar models diretamente, como `CursoForm.save()`.
- Views ainda buscam e manipulam models diretamente.
- O Admin do Django provavelmente permite alterar estados sem passar pelas regras de dominio.

### Sugestao pratica

Proteger regras em varias camadas, sem depender de uma so:

- Entidades e domain services validam regras principais.
- Application services coordenam casos de uso.
- Banco protege unicidade e integridade basica.
- Forms validam entrada do usuario.
- Admin deve chamar services ou ter validacoes equivalentes para campos sensiveis.
- Testes garantem que fluxos invalidos falham.

O ideal e que o caminho mais facil para alterar o sistema tambem seja o caminho correto.

## 12. Organizacao das responsabilidades entre camadas

### O que esta bom

A intencao esta bem descrita em `ARCHITECTURE.md`:

```text
presentation -> application -> domain
infrastructure implementa contratos do dominio
```

Isso e uma boa base.

### O que falta melhorar

Na pratica, algumas responsabilidades se misturam:

- `models.py` e ao mesmo tempo ORM, entidade e fachada Django.
- `Certificado` chama services da camada de aplicacao.
- `Aluno` cria registros diretamente com ORM.
- Views ainda usam models e queries diretamente.
- Forms salvam entidades diretamente.
- Selectors fazem consultas diretas, inclusive cruzando contextos.

### Sugestao pratica

Uma divisao mais limpa seria:

| Camada | Responsabilidade |
| --- | --- |
| Presentation | HTTP, forms, templates, mensagens, redirecionamento |
| Application | Casos de uso, transacoes, orquestracao, chamada de repositorios |
| Domain | Entidades, value objects, invariantes, policies, domain services |
| Infrastructure | ORM, banco, adaptadores, integracoes externas |

Regra simples para guiar o projeto:

```text
Views nao decidem regra de negocio.
Forms nao salvam mudancas criticas sozinhos.
Services de aplicacao nao devem conter toda a inteligencia do dominio.
Models nao devem chamar application services.
Repositories nao devem virar lugar de regra de negocio.
```

## 13. Supple Design

Supple Design significa deixar o modelo mais expressivo, flexivel e facil de usar corretamente. Nem todo projeto precisa aplicar todos os padroes, mas alguns seriam uteis aqui.

### Pontos aplicaveis ao projeto

#### Intention-Revealing Interfaces

Os metodos devem revelar intencao de negocio, nao detalhes tecnicos.

Melhor:

```python
matricula.concluir()
certificado.revogar()
curso.adicionar_modulo(nome)
```

Menos expressivo:

```python
matricula.status = "CONCLUIDA"
certificate.status = CertificateStatus.REVOKED
course.modulos.create(...)
```

#### Side-Effect-Free Functions

Regras de calculo devem ser puras quando possivel.

Bons candidatos:

- Calcular media final.
- Validar nota.
- Verificar carga horaria minima.
- Verificar se certificado esta valido.
- Determinar se uma matricula pode ser concluida.

#### Assertions

As entidades devem deixar claro o que nunca pode acontecer.

Exemplo:

```text
Uma nota nunca pode ser menor que 0 ou maior que 10.
Uma matricula cancelada nao pode ser concluida.
Um certificado revogado nao deve voltar a emitido sem regra explicita.
```

#### Conceptual Contours

Separar conceitos que mudam por motivos diferentes:

- Regras de conclusao do curso.
- Regras de matricula.
- Regras de avaliacao.
- Regras de certificacao.
- Regras de integridade academica.

Hoje alguns desses conceitos existem, mas ainda nao estao fortes como unidades de dominio.

## Prioridades recomendadas

### Prioridade 1 - Proteger `Matricula`

`Matricula` parece ser o centro da jornada academica. Ela deveria concentrar regras sobre status, progresso, media, conclusao e cancelamento.

Criar metodos como:

- `cancelar()`
- `reativar()`
- `trancar()`
- `concluir()`
- `atualizar_progresso()`

E impedir transicoes invalidas.

### Prioridade 2 - Criar Value Objects simples

Comecar pelos mais importantes:

- `Nota`
- `PercentualProgresso`
- `CargaHoraria`
- `DuracaoAula`
- `NumeroMatricula`

Isso reduz erro e melhora leitura.

### Prioridade 3 - Formalizar regras de conclusao e certificacao

Criar regras claras para:

- Quando uma matricula pode ser concluida.
- Quando um certificado pode ser emitido.
- Quando um certificado pode ser suspenso, renovado ou revogado.
- Como incidentes de integridade afetam certificacao.

### Prioridade 4 - Melhorar repositories por agregado

Evitar repositories muito pequenos e tecnicos. Eles devem carregar e salvar agregados relevantes.

### Prioridade 5 - Reduzir vazamento do ORM nas regras

O Django ORM pode continuar sendo usado, mas as regras de negocio nao deveriam depender diretamente de `objects.create`, `save()` e alteracao livre de campos em qualquer lugar.

## Conclusao

O projeto esta no caminho certo estruturalmente: tem contextos, camadas, repositories, services e policies. O principal ponto de melhoria e transformar essa estrutura em um dominio mais rico e protegido.

Hoje a arquitetura comunica "quero seguir DDD". O proximo passo e fazer o codigo comunicar "as regras do negocio moram no dominio e sao dificeis de burlar".

Se a evolucao for incremental, a melhor ordem seria:

1. Fortalecer `Matricula` como aggregate root.
2. Criar value objects para nota, progresso e carga horaria.
3. Extrair regras de conclusao/certificacao para domain services ou policies.
4. Ajustar application services para orquestrar, nao concentrar toda a regra.
5. Cobrir invariantes com testes de dominio.

