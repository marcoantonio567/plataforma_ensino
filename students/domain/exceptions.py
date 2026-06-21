class EnrollmentAlreadyActive(Exception):
    """A matricula ja existe e nao precisa ser alterada."""


class InvalidEnrollmentTransition(ValueError):
    """A mudanca de estado solicitada nao e permitida para a matricula."""


class InvalidRequestTransition(ValueError):
    """A mudanca de estado solicitada nao e permitida para a solicitacao."""
