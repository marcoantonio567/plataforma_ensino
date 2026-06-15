class DjangoCertificateRepository:
    def save(self, certificate, *, fields: list[str]) -> None:
        certificate.save(update_fields=fields)
