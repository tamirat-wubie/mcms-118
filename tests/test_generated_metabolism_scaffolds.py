import importlib

from mcms.module_registry import modules_for_phase


def test_phase_135_scaffolds_import_and_evaluate():
    for row in modules_for_phase(135):
        module_name = row["module"].removesuffix(".py")
        mod = importlib.import_module(f"mcms.metabolism.{module_name}")
        result = mod.evaluate(mod.CapabilityInput(subject_key="release/1", evidence_strength=0.9))
        assert result.status in {"supported", "evidence_required", "safety_boundary"}
        assert "production_customer_ready_claim" in result.blocked_claims
