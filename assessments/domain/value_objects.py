from dataclasses import dataclass


class InvalidGrade(ValueError):
    pass


@dataclass(frozen=True)
class Nota:
    valor: float

    def __post_init__(self):
        valor = float(self.valor)
        if not 0 <= valor <= 10:
            raise InvalidGrade("A nota deve estar entre 0 e 10.")
        object.__setattr__(self, "valor", valor)

    def __float__(self):
        return self.valor

    def __str__(self):
        return f"{self.valor:g}"
