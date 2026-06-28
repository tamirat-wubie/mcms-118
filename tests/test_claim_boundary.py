from mcms.core.boundaries import compile_claim_boundary


def test_blocks_customer_ready_claim():
    result = compile_claim_boundary("ready for customers", "production_customer_ready_claim", 1.0)
    assert result.allowed is False
    assert result.status == "blocked_claim"


def test_allows_source_backed_claim_with_evidence():
    result = compile_claim_boundary("NaCl is a compound", "source_backed_claim", 0.8)
    assert result.allowed is True
