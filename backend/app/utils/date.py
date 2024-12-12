from pendulum import now as _now
from pendulum import today as _today
from pendulum import yesterday as _yesterday
from pendulum.parser import parse  # noqa: F401


def tz(timezone: str = None) -> str:
    return timezone or "America/Sao_Paulo"


def today():
    return _today(tz())


def end_of_today():
    return today().end_of("day")


def start_of_yesterday():
    return _yesterday(tz()).start_of("day")


def now():
    return _now(tz())
