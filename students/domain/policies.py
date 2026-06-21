from enum import StrEnum


class EnrollmentStatus(StrEnum):
    ACTIVE = "ATIVA"
    LOCKED = "TRANCADA"
    COMPLETED = "CONCLUIDA"
    CANCELLED = "CANCELADA"


def reactivate_cancelled_enrollment(enrollment) -> bool:
    if enrollment.status != EnrollmentStatus.CANCELLED:
        return False

    enrollment.status = EnrollmentStatus.ACTIVE.value
    return True


def cancel_enrollment(enrollment):
    enrollment.status = EnrollmentStatus.CANCELLED.value
    return enrollment


def lock_enrollment(enrollment):
    enrollment.status = EnrollmentStatus.LOCKED.value
    return enrollment
