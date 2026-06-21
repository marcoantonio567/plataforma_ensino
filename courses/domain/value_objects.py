from dataclasses import dataclass


class InvalidCourseValue(ValueError):
    pass


@dataclass(frozen=True)
class CargaHoraria:
    valor: int

    def __post_init__(self):
        valor = int(self.valor)
        if valor <= 0:
            raise InvalidCourseValue("A carga horaria deve ser maior que zero.")
        object.__setattr__(self, "valor", valor)

    def __int__(self):
        return self.valor


@dataclass(frozen=True)
class CargaHorariaMinima:
    valor: int

    def __post_init__(self):
        valor = int(self.valor)
        if valor < 0:
            raise InvalidCourseValue("A carga horaria minima nao pode ser negativa.")
        object.__setattr__(self, "valor", valor)

    def __int__(self):
        return self.valor


@dataclass(frozen=True)
class DuracaoAula:
    valor: int

    def __post_init__(self):
        valor = int(self.valor)
        if valor <= 0:
            raise InvalidCourseValue("A duracao da aula deve ser maior que zero.")
        object.__setattr__(self, "valor", valor)

    def __int__(self):
        return self.valor


@dataclass(frozen=True)
class Ordem:
    valor: int

    def __post_init__(self):
        valor = int(self.valor)
        if valor < 1:
            raise InvalidCourseValue("A ordem deve ser maior que zero.")
        object.__setattr__(self, "valor", valor)

    def __int__(self):
        return self.valor


@dataclass(frozen=True)
class MediaMinima:
    valor: float

    def __post_init__(self):
        valor = float(self.valor)
        if not 0 <= valor <= 10:
            raise InvalidCourseValue("A media minima deve estar entre 0 e 10.")
        object.__setattr__(self, "valor", valor)

    def __float__(self):
        return self.valor
