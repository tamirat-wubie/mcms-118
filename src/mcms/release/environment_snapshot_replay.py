from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass
class EnvironmentSnapshotReplayResult:
    snapshot_key: str
    release_key: str
    original_snapshot_hash: str
    replay_snapshot_hash: str
    original_environment: dict
    replay_environment: dict
    replay_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def hash_environment_snapshot(environment_snapshot: dict) -> str:
    return sha256(json.dumps(environment_snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def replay_environment_snapshot(snapshot_key: str, release_key: str, original_environment: dict, replay_environment: dict) -> EnvironmentSnapshotReplayResult:
    if not snapshot_key or not release_key or not original_environment:
        return EnvironmentSnapshotReplayResult(snapshot_key, release_key, "", "", original_environment, replay_environment, "insufficient_data", "Environment snapshot replay input is invalid.")
    original_hash = hash_environment_snapshot(original_environment)
    replay_hash = hash_environment_snapshot(replay_environment)
    if not replay_environment:
        status="environment_snapshot_missing"; explanation="Replay environment snapshot is missing."
    elif original_hash != replay_hash:
        status="environment_snapshot_replay_drift"; explanation="Replay environment snapshot differs from original."
    else:
        status="environment_snapshot_replay_matched"; explanation="Replay environment snapshot matches original."
    return EnvironmentSnapshotReplayResult(snapshot_key, release_key, original_hash, replay_hash, original_environment, replay_environment, status, explanation)
