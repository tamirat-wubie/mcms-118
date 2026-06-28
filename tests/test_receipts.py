from mcms.core.receipts import Receipt, validate_hash_chain


def test_hash_chain_valid():
    r1 = Receipt("r1", "test", {"x": 1}, "")
    r2 = Receipt("r2", "test", {"y": 2}, r1.receipt_hash())
    assert validate_hash_chain([r1, r2]) is True


def test_hash_chain_invalid():
    r1 = Receipt("r1", "test", {"x": 1}, "")
    r2 = Receipt("r2", "test", {"y": 2}, "wrong")
    assert validate_hash_chain([r1, r2]) is False
