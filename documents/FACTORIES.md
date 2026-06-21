# Factories

Factories sao usadas apenas quando a criacao de uma Entity ou Aggregate exige
mais do que preencher campos diretamente.

## Factories implementadas

### `AlunoFactory`

Responsavel por criar `Aluno` para um `User`.

Motivos:

- gera o numero de matricula;
- aplica o Value Object `NumeroMatricula`;
- define a data de ingresso padrao;
- exige um usuario valido.

### `MatriculaFactory`

Responsavel por criar `Matricula`.

Motivos:

- combina os objetos `Aluno`, `Curso` e `RegraCurso`;
- busca a regra vigente quando ela nao e informada;
- impede matricula sem regra vigente;
- impede o uso de regra pertencente a outro curso;
- inicializa a matricula com status ativo.

## Onde factories nao foram criadas

`Curso`, `Modulo`, `Aula`, `Solicitacao`, `AvaliacaoRealizada` e `Certificado`
continuam sendo criados por construtores simples, metodos da Aggregate Root ou
services de dominio ja existentes.

Esses casos nao receberam factories porque a criacao atual ja expressa a regra
de negocio sem adicionar uma camada artificial apenas para aumentar a quantidade
de padroes.
