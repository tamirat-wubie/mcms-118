from __future__ import annotations

from dataclasses import dataclass

@dataclass
class AdapterSandboxPolicyResult:
    policy_key: str
    adapter_kind: str
    command_binary: str
    allowed_binaries: list[str]
    network_allowed: bool
    filesystem_mode: str
    environment_keys: list[str]
    allowed_environment_keys: list[str]
    timeout_seconds: float
    max_output_bytes: int
    sandbox_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def evaluate_adapter_sandbox_policy(policy_key: str, adapter_kind: str, command_binary: str, allowed_binaries: list[str], network_allowed: bool, filesystem_mode: str, environment_keys: list[str], allowed_environment_keys: list[str], timeout_seconds: float, max_output_bytes: int) -> AdapterSandboxPolicyResult:
    if not policy_key or not adapter_kind or not command_binary or filesystem_mode not in {"none", "readonly", "workspace_only", "write_temp_only"} or timeout_seconds <= 0 or max_output_bytes <= 0:
        status = "insufficient_data"; explanation = "Sandbox policy input is invalid."
    elif command_binary not in allowed_binaries:
        status = "command_denied"; explanation = "Command binary is not allowlisted."
    elif adapter_kind in {"opa", "cosign", "jsonschema"} and network_allowed:
        status = "network_denied"; explanation = "This adapter should not require network access."
    elif adapter_kind in {"github", "secret_manager"} and not network_allowed:
        status = "network_denied"; explanation = "This adapter requires network access but network is disabled."
    elif filesystem_mode not in {"readonly", "workspace_only", "write_temp_only"}:
        status = "filesystem_denied"; explanation = "Filesystem mode is too restrictive or invalid."
    elif any(key not in allowed_environment_keys for key in environment_keys):
        status = "environment_denied"; explanation = "Environment contains non-allowlisted keys."
    elif timeout_seconds > 300:
        status = "timeout_limit_exceeded"; explanation = "Timeout exceeds sandbox policy limit."
    elif max_output_bytes > 10_000_000:
        status = "output_limit_exceeded"; explanation = "Output limit exceeds sandbox policy limit."
    else:
        status = "sandbox_policy_ready"; explanation = "Adapter sandbox policy is ready."
    return AdapterSandboxPolicyResult(policy_key, adapter_kind, command_binary, allowed_binaries, network_allowed, filesystem_mode, environment_keys, allowed_environment_keys, timeout_seconds, max_output_bytes, status, explanation)
