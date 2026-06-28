from mcms.core.maturity import CapabilityMaturity


def test_maturity_valid():
    item = CapabilityMaturity("webauthn", "M1")
    assert item.validate() is True
    assert item.to_dict()["meaning"] == "symbolic model implemented"
