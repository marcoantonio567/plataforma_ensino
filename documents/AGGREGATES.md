# Aggregates e Aggregate Roots

Este documento explicita as fronteiras de consistencia dos principais agregados do
projeto. A regra geral e que codigo de aplicacao deve solicitar mudancas por meio
da Aggregate Root, deixando entidades internas protegidas por metodos de dominio.

## Catalogo de Curso

- Aggregate Root: `Curso`
- Entidades internas: `RegraCurso`, `Modulo`, `Aula`, `PreRequisito`
- Fronteira: estrutura academica e regras de oferta de um curso
- Justificativa: modulo, aula, ordem, carga horaria e regra vigente so fazem
  sentido dentro de um curso especifico.

Operacoes externas esperadas:

- `Curso.adicionar_modulo(...)`
- `Curso.adicionar_aula(modulo, ...)`
- `Curso.remover_modulo(modulo)`
- `Curso.remover_aula(aula)`
- `Curso.regra_vigente(...)`

Invariantes protegidas:

- A carga horaria do curso deve ser maior que zero.
- A ordem de modulo/aula deve ser maior que zero.
- A duracao da aula deve ser maior que zero.
- Uma aula so pode ser adicionada a modulo pertencente ao curso.
- Uma remocao de modulo/aula precisa respeitar a fronteira do curso.

## Jornada Academica

- Aggregate Root: `Matricula`
- Entidades internas: `Solicitacao`, `Aproveitamento`, `SegundaChamada`,
  `RevisaoNota`, `Equivalencia`
- Fronteira: ciclo de vida do aluno dentro de um curso especifico
- Justificativa: progresso, status, solicitacoes e equivalencias dependem da
  relacao aluno-curso representada pela matricula.

Operacoes externas esperadas:

- `Matricula.cancelar()`
- `Matricula.trancar()`
- `Matricula.reativar()`
- `Matricula.concluir(...)`
- `Matricula.atualizar_progresso(...)`
- `Matricula.solicitar_aproveitamento(...)`
- `Matricula.solicitar_segunda_chamada(...)`
- `Matricula.solicitar_revisao_nota(...)`
- `Matricula.registrar_equivalencia(...)`

Invariantes protegidas:

- Transicoes de status passam por metodos da matricula.
- Progresso deve ficar entre 0 e 100.
- Media final deve ficar entre 0 e 10.
- Carga horaria cumprida nao pode ser negativa.
- Solicitacoes so podem ser abertas para itens do mesmo curso da matricula.

## Avaliacao

- Aggregate Root: `Avaliacao`
- Entidades internas: `AvaliacaoRealizada`
- Fronteira: definicao da avaliacao e registro de resultado para aluno
- Justificativa: nota, peso e resultado avaliado pertencem ao processo de
  avaliacao.

Operacoes externas esperadas:

- `Avaliacao.nota_ponderada(...)`
- `Avaliacao.alterar_peso(...)`
- `AvaliacaoRealizada.registrar_nota(...)`

Invariantes protegidas:

- Nota deve ficar entre 0 e 10.
- Peso da avaliacao deve ser maior que zero.

## Certificacao

- Aggregate Root: `Certificado`
- Entidades internas: ciclo de status do certificado
- Entidade relacionada pela jornada academica: `IncidenteIntegridade`
- Fronteira: emissao, suspensao, renovacao e revogacao do certificado
- Justificativa: o certificado possui ciclo de vida proprio apos a matricula
  estar apta para certificacao.

Operacoes externas esperadas:

- `Certificado.emitir(...)`
- `Certificado.suspender()`
- `Certificado.revogar()`
- `Certificado.renovar(...)`

Invariantes protegidas:

- Certificado revogado nao pode ser emitido, suspenso ou renovado.
- Certificado suspenso nao pode ser suspenso novamente.
- A emissao inicial e validada pelo domain service de certificacao antes de
  modificar o certificado.
