import uuid

from django.utils import timezone

from students.domain.value_objects import NumeroMatricula
from students.models import Aluno, Matricula


class AlunoFactory:
    @staticmethod
    def criar_para_usuario(user, *, numero_matricula=None, data_ingresso=None):
        if user is None:
            raise ValueError("O usuario e obrigatorio para criar um aluno.")

        numero = numero_matricula or f"ALU{uuid.uuid4().hex[:8].upper()}"
        return Aluno(
            usuario=user,
            numero_matricula=str(NumeroMatricula(numero)),
            data_ingresso=data_ingresso or timezone.localdate(),
        )


class MatriculaFactory:
    @staticmethod
    def criar(aluno, curso, *, regra_curso=None):
        if aluno is None:
            raise ValueError("O aluno e obrigatorio para criar uma matricula.")
        if curso is None:
            raise ValueError("O curso e obrigatorio para criar uma matricula.")

        regra = regra_curso if regra_curso is not None else curso.regra_vigente()
        if regra is None:
            raise ValueError("Nao existe regra vigente para o curso informado.")
        if not MatriculaFactory._regra_pertence_ao_curso(regra, curso):
            raise ValueError("A regra informada nao pertence ao curso da matricula.")

        return Matricula(
            aluno=aluno,
            curso=curso,
            regra_curso=regra,
            status=Matricula.Status.ATIVA,
        )

    @staticmethod
    def _regra_pertence_ao_curso(regra, curso):
        if regra.curso_id is not None and curso.pk is not None:
            return regra.curso_id == curso.pk
        return regra.curso == curso
