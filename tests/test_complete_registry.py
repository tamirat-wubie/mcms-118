from mcms.phase_registry import list_phases, get_phase
from mcms.module_registry import all_modules, modules_for_phase


def test_phase_registry_complete():
    phases = list_phases()
    assert len(phases) == 135
    assert get_phase(135)["phase"] == 135


def test_module_registry_generated():
    modules = all_modules()
    assert len(modules) >= 180
    assert modules_for_phase(135)
