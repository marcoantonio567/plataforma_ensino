# Documentacao de Negocio - Plataforma de Ensino com Certificacao Profissional

Este documento descreve o que a plataforma faz, quais sao os principais conceitos do negocio e quais regras devem orientar o funcionamento do sistema.

O foco aqui nao e explicar tecnologia, arquitetura ou implementacao. O foco e deixar claro o comportamento esperado da plataforma.

## 1. Objetivo da plataforma

A plataforma e um sistema de ensino online voltado para cursos com certificacao profissional.

Ela permite:

- Criar e organizar cursos.
- Dividir cursos em modulos.
- Dividir modulos em aulas.
- Matricular alunos em cursos.
- Acompanhar progresso, carga horaria e desempenho.
- Aplicar diferentes tipos de avaliacoes.
- Registrar solicitacoes academicas.
- Controlar equivalencias para alunos vindos de outras instituicoes.
- Emitir, suspender, revogar e renovar certificados.
- Registrar incidentes de integridade academica.

## 2. Principais participantes

### Aluno

Pessoa cadastrada na plataforma que pode se matricular em cursos, assistir aulas, realizar avaliacoes, solicitar revisao de nota, pedir segunda chamada e solicitar aproveitamento de estudos anteriores.

### Administrador ou equipe academica

Responsavel por cadastrar cursos, modulos, aulas, regras de conclusao, avaliacoes, analisar solicitacoes, registrar incidentes e controlar certificados.

## 3. Estrutura academica

### Curso

Um curso representa uma formacao oferecida pela plataforma.

Cada curso pode ter:

- Nome.
- Carga horaria.
- Modulos.
- Aulas.
- Avaliacoes.
- Regras de conclusao.
- Pre-requisitos.

### Modulo

Um modulo e uma divisao interna do curso. Ele agrupa aulas relacionadas a um mesmo tema.

Regras esperadas:

- Um curso pode ter varios modulos.
- Os modulos devem possuir uma ordem dentro do curso.
- A ordem dos modulos deve ser respeitada na navegacao e exibicao.

### Aula

Uma aula e a menor unidade de conteudo do curso.

Regras esperadas:

- Uma aula pertence a um modulo.
- Uma aula deve ter titulo, conteudo e duracao.
- As aulas devem possuir uma ordem dentro do modulo.
- A duracao da aula contribui para o controle de carga horaria.

## 4. Matricula

A matricula representa o vinculo entre um aluno e um curso.

Uma matricula pode possuir os seguintes estados:

- Ativa.
- Trancada.
- Concluida.
- Cancelada.

Regras de negocio:

- Um aluno nao deve ter mais de uma matricula ativa para o mesmo curso.
- Uma matricula cancelada pode ser reativada, se a regra do negocio permitir.
- Uma matricula concluida nao deve ser alterada como se ainda estivesse em andamento.
- A matricula deve guardar a regra de curso vigente na data em que foi criada.
- Mudancas futuras nas regras do curso nao devem afetar matriculas antigas automaticamente.

## 5. Regra vigente na data da matricula

As regras de conclusao de um curso podem mudar ao longo do tempo.

Por exemplo:

- A media minima pode mudar.
- A carga horaria minima pode mudar.
- O projeto final pode passar a ser obrigatorio.
- Novos criterios de certificacao podem ser criados.

Regra principal:

```text
O aluno deve ser avaliado pela regra que estava vigente na data da sua matricula.
```

Isso significa que, ao criar uma matricula, a plataforma deve registrar qual regra do curso sera usada para aquele aluno.

Exemplo:

- Em 2026, o curso exige media minima 6.
- Em 2027, o mesmo curso passa a exigir media minima 7.
- Um aluno matriculado em 2026 deve continuar seguindo a regra de media minima 6.
- Um aluno matriculado em 2027 deve seguir a regra de media minima 7.

## 6. Avaliacoes

As avaliacoes medem o desempenho do aluno no curso ou em um modulo.

A plataforma suporta quatro tipos principais de avaliacao:

### Avaliacao objetiva

Avaliacao composta por questoes com respostas objetivas, como multipla escolha, verdadeiro ou falso ou alternativas fechadas.

Regras esperadas:

- Deve possuir questoes objetivas.
- Pode ser corrigida automaticamente.
- Gera uma nota para o aluno.

### Avaliacao discursiva

Avaliacao em que o aluno responde com texto livre.

Regras esperadas:

- Deve possuir um enunciado ou descricao.
- Normalmente exige correcao manual.
- Gera uma nota para o aluno.

### Projeto pratico

Avaliacao baseada em entrega pratica, como projeto, repositorio, trabalho final ou solucao aplicada.

Regras esperadas:

- Pode exigir envio de link, arquivo ou repositorio.
- Pode ser obrigatoria para certificacao.
- Pode representar o projeto final do curso.
- Deve gerar uma nota ou aprovacao.

### Prova com monitoramento remoto

Avaliacao realizada com controle de integridade durante a prova.

Regras esperadas:

- Pode ter monitoramento ativo.
- Pode registrar eventos suspeitos.
- Pode gerar incidentes de integridade.
- Pode impactar a certificacao do aluno.

## 7. Notas e media

A plataforma deve registrar notas das avaliacoes realizadas pelos alunos.

Regras de negocio:

- A nota deve estar entre 0 e 10.
- A media final deve considerar as avaliacoes exigidas pelo curso.
- Avaliacoes podem ter pesos diferentes.
- O aluno precisa atingir a media minima definida pela regra vigente da sua matricula.

Exemplo:

```text
Se a regra vigente exige media minima 6.0,
o aluno so pode ser certificado se sua media final for maior ou igual a 6.0.
```

## 8. Carga horaria

Cada curso possui uma carga horaria definida.

A plataforma deve acompanhar a carga horaria cumprida pelo aluno.

Regras de negocio:

- O aluno precisa cumprir a carga horaria minima exigida.
- A carga horaria minima considerada deve ser a da regra vigente na data da matricula.
- Aulas, modulos ou atividades podem contribuir para essa carga horaria.
- O aluno nao deve receber certificacao se nao cumprir a carga horaria exigida.

## 9. Projeto final

Alguns cursos podem exigir projeto final para certificacao.

Regras de negocio:

- A obrigatoriedade do projeto final deve estar definida na regra do curso.
- Se o projeto final for obrigatorio, o aluno precisa conclui-lo.
- O projeto final pode ser representado como uma avaliacao do tipo projeto pratico.
- Um aluno sem projeto final concluido nao deve receber certificado quando a regra exigir esse criterio.

## 10. Certificacao profissional

A certificacao e o reconhecimento formal de que o aluno concluiu o curso conforme as regras exigidas.

Para receber certificacao, o aluno precisa:

- Atingir a media minima.
- Cumprir a carga horaria minima.
- Concluir o projeto final, quando obrigatorio.
- Nao possuir incidentes graves de integridade academica.
- Estar com a matricula concluida.

## 11. Estados do certificado

Um certificado pode ter os seguintes estados:

- Emitido.
- Suspenso.
- Revogado.

### Certificado emitido

Indica que o aluno cumpriu os requisitos e recebeu a certificacao.

### Certificado suspenso

Indica que o certificado esta temporariamente bloqueado.

Pode acontecer quando:

- Ha suspeita de irregularidade.
- Ha pendencia academica.
- Ha analise de incidente de integridade.
- Ha necessidade de revisao administrativa.

### Certificado revogado

Indica que o certificado perdeu validade de forma definitiva ou ate decisao formal.

Pode acontecer quando:

- Foi comprovada fraude.
- Foi identificado plagio grave.
- O aluno nao deveria ter sido certificado.
- Houve violacao grave das regras de integridade.

## 12. Validade e renovacao do certificado

A certificacao pode ter validade temporaria.

Regras de negocio:

- Um certificado pode ter data de validade.
- Se nao tiver data de validade, pode ser considerado vitalicio.
- Um certificado vencido pode exigir renovacao.
- A renovacao pode exigir nova avaliacao, novo projeto, atualizacao de conteudo ou analise academica.
- A renovacao deve respeitar as regras definidas para aquele tipo de certificacao.

Exemplo:

```text
Uma certificacao profissional pode valer por 2 anos.
Apos esse periodo, o aluno precisa renovar a certificacao para continuar valido.
```

## 13. Incidentes de integridade academica

Incidentes de integridade representam comportamentos que podem comprometer a confiabilidade da avaliacao ou da certificacao.

Exemplos de incidentes:

- Uso de material nao autorizado.
- Troca de aba durante prova monitorada.
- Uso de dispositivo secundario.
- Plagio.
- Fraude.
- Cola.

Regras de negocio:

- Incidentes devem ser vinculados a uma matricula, avaliacao ou aluno, conforme o caso.
- Incidentes graves podem impedir a certificacao.
- Incidentes graves podem suspender ou revogar um certificado.
- Nem todo incidente precisa ter o mesmo peso.
- A plataforma deve permitir analise academica antes de uma decisao definitiva.

## 14. Equivalencias

Equivalencias permitem reconhecer estudos feitos pelo aluno em outras instituicoes.

Exemplo:

Um aluno cursou uma disciplina semelhante em outra instituicao e solicita que essa disciplina seja aproveitada na plataforma.

Regras de negocio:

- A equivalencia deve registrar a instituicao de origem.
- Deve registrar a disciplina ou conteudo de origem.
- Deve indicar qual disciplina, modulo ou conteudo sera aproveitado.
- Deve passar por analise academica.
- Pode ser aprovada ou rejeitada.
- Quando aprovada, pode contribuir para progresso, carga horaria ou dispensa de conteudo.

## 15. Solicitacoes academicas

A plataforma permite solicitacoes feitas pelo aluno.

Tipos principais:

- Aproveitamento de estudos.
- Segunda chamada.
- Revisao de nota.

### Aproveitamento de estudos

Pedido para reconhecer conteudo cursado anteriormente.

### Segunda chamada

Pedido para realizar uma avaliacao em nova data ou nova oportunidade.

### Revisao de nota

Pedido para revisar a nota atribuida a uma avaliacao.

Estados esperados de uma solicitacao:

- Pendente.
- Em analise.
- Aprovada.
- Rejeitada.

Regras de negocio:

- Toda solicitacao deve possuir justificativa.
- Toda solicitacao deve estar vinculada a uma matricula.
- Solicitacoes devem ser analisadas antes de aprovacao ou rejeicao.
- A aprovacao de uma solicitacao pode alterar a situacao academica do aluno.

## 16. Pre-requisitos

Cursos ou modulos podem exigir pre-requisitos.

Regras de negocio:

- Um pre-requisito pode ser outro curso.
- Um pre-requisito pode ser um modulo.
- O aluno deve cumprir os pre-requisitos antes de avancar ou se matricular, conforme a regra definida.
- A plataforma deve validar se o pre-requisito apontado realmente existe.

## 17. Fluxo resumido do aluno

Um fluxo esperado do aluno na plataforma:

1. O aluno cria sua conta.
2. O aluno escolhe um curso.
3. A plataforma cria uma matricula para o aluno.
4. A matricula registra a regra vigente do curso naquela data.
5. O aluno acessa modulos e aulas.
6. O aluno realiza avaliacoes.
7. A plataforma registra notas, progresso e carga horaria.
8. O aluno pode solicitar equivalencia, segunda chamada ou revisao de nota.
9. A plataforma verifica se todos os criterios de conclusao foram cumpridos.
10. Se aprovado, o aluno recebe certificado.
11. O certificado pode ser valido por tempo indeterminado ou ter validade temporaria.
12. O certificado pode ser suspenso, revogado ou renovado conforme as regras.

## 18. Regras essenciais do negocio

As regras mais importantes da plataforma sao:

- A certificacao depende da media minima.
- A certificacao depende da carga horaria cumprida.
- A certificacao depende da conclusao do projeto final quando ele for obrigatorio.
- A certificacao depende da ausencia de incidentes graves de integridade.
- As regras do curso podem mudar com o tempo.
- Cada matricula deve respeitar a regra vigente na data em que foi criada.
- Avaliacoes podem ser objetivas, discursivas, projetos praticos ou provas monitoradas.
- Certificados podem ter validade temporaria.
- Certificados podem ser suspensos.
- Certificados podem ser revogados.
- Certificados podem exigir renovacao.
- Alunos vindos de outras instituicoes podem solicitar equivalencias.
- Incidentes de integridade devem ser considerados na decisao de certificacao.

## 19. Glossario do negocio

| Termo | Significado |
| --- | --- |
| Aluno | Pessoa que realiza cursos na plataforma. |
| Curso | Formacao oferecida pela plataforma. |
| Modulo | Parte organizada de um curso. |
| Aula | Unidade de conteudo dentro de um modulo. |
| Matricula | Vinculo entre aluno e curso. |
| Avaliacao | Instrumento usado para medir desempenho do aluno. |
| Projeto pratico | Avaliacao baseada em entrega aplicada. |
| Prova monitorada | Avaliacao acompanhada por mecanismo de integridade. |
| Media minima | Nota minima exigida para conclusao ou certificacao. |
| Carga horaria | Tempo exigido ou cumprido no curso. |
| Certificado | Documento que comprova a conclusao do curso. |
| Certificacao | Processo de reconhecimento profissional do aluno. |
| Incidente de integridade | Evento que compromete a confianca academica. |
| Equivalencia | Reconhecimento de estudos feitos em outra instituicao. |
| Regra vigente | Regra valida em uma data especifica. |

