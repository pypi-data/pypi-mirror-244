import os

from hypothesis import HealthCheck, settings
from hypothesis.strategies import just, one_of

from cattrs import UnstructureStrategy

settings.register_profile(
    "CI", settings(suppress_health_check=[HealthCheck.too_slow]), deadline=None
)

if "CI" in os.environ:
    settings.load_profile("CI")

unstructure_strats = one_of(just(s) for s in UnstructureStrategy)
