from enum import StrEnum


class EnrollmentStatus(StrEnum):
    ACTIVE = "ATIVA"
    LOCKED = "TRANCADA"
    COMPLETED = "CONCLUIDA"
    CANCELLED = "CANCELADA"


def reactivate_cancelled_enrollment(enrollment) -> bool:
    if enrollment.status != EnrollmentStatus.CANCELLED:
        return False

    enrollment.reativar()
    return True


def cancel_enrollment(enrollment):
    return enrollment.cancelar()


def lock_enrollment(enrollment):
    return enrollment.trancar()
