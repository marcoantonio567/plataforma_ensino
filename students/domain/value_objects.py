from dataclasses import dataclass
import re


class InvalidStudentValue(ValueError):
    pass


@dataclass(frozen=True)
class NumeroMatricula:
    valor: str

    _PATTERN = re.compile(r"^ALU[A-Z0-9]{4,12}$")

    def __post_init__(self):
        valor = str(self.valor).strip().upper()
        if not self._PATTERN.fullmatch(valor):
            raise InvalidStudentValue(
                "O numero de matricula deve seguir o formato ALU seguido de 4 a 12 letras ou numeros."
            )
        object.__setattr__(self, "valor", valor)

    def __str__(self):
        return self.valor


@dataclass(frozen=True)
class PercentualProgresso:
    valor: float

    def __post_init__(self):
        valor = float(self.valor)
        if not 0 <= valor <= 100:
            raise InvalidStudentValue("O progresso deve estar entre 0 e 100.")
        object.__setattr__(self, "valor", valor)

    def __float__(self):
        return self.valor


@dataclass(frozen=True)
class MediaFinal:
    valor: float

    def __post_init__(self):
        valor = float(self.valor)
        if not 0 <= valor <= 10:
            raise InvalidStudentValue("A media final deve estar entre 0 e 10.")
        object.__setattr__(self, "valor", valor)

    def __float__(self):
        return self.valor


@dataclass(frozen=True)
class CargaHorariaCumprida:
    valor: int

    def __post_init__(self):
        valor = int(self.valor)
        if valor < 0:
            raise InvalidStudentValue("A carga horaria cumprida nao pode ser negativa.")
        object.__setattr__(self, "valor", valor)

    def __int__(self):
        return self.valor
