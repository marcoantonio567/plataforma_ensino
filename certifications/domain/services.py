class CertificationDenied(ValueError):
    pass


class AvaliadorElegibilidadeCertificado:
    @staticmethod
    def validar_emissao(
        matricula,
        *,
        concluiu_projeto_obrigatorio: bool,
        possui_incidente_grave: bool,
    ) -> None:
        regra = matricula.regra_curso

        if regra is None:
            raise CertificationDenied(
                "A matricula nao possui regra de curso vigente registrada."
            )

        if matricula.status != "CONCLUIDA":
            raise CertificationDenied(
                "A matricula precisa estar concluida para emitir certificado."
            )

        if matricula.media_final is None:
            raise CertificationDenied("A matricula nao possui media final registrada.")

        if matricula.media_final < regra.media_minima:
            raise CertificationDenied("A media final esta abaixo da media minima exigida.")

        if matricula.carga_horaria_cumprida < regra.carga_horaria_minima:
            raise CertificationDenied(
                "A carga horaria cumprida esta abaixo do minimo exigido."
            )

        if regra.exige_projeto_final and not concluiu_projeto_obrigatorio:
            raise CertificationDenied(
                "O projeto final obrigatorio ainda nao foi concluido."
            )

        if possui_incidente_grave:
            raise CertificationDenied(
                "A matricula possui incidente grave de integridade academica."
            )


def validar_emissao_certificado(
    matricula,
    *,
    concluiu_projeto_obrigatorio: bool,
    possui_incidente_grave: bool,
) -> None:
    return AvaliadorElegibilidadeCertificado.validar_emissao(
        matricula,
        concluiu_projeto_obrigatorio=concluiu_projeto_obrigatorio,
        possui_incidente_grave=possui_incidente_grave,
    )
