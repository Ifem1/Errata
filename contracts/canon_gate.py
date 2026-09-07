# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
from dataclasses import dataclass


@gl.contract_interface
class IErrata:
    class View:
        def is_claim_current(self, claim_id: u256, expected_claim_hash: str) -> bool: ...

    class Write:
        pass


@allow_storage
@dataclass
class ExecutionReceipt:
    caller: Address
    claim_id: u256
    claim_hash: str
    action_hash: str


class CanonGate(gl.Contract):
    errata_address: Address
    executions: TreeMap[str, ExecutionReceipt]
    execution_count: u256

    def __init__(self, errata_address: Address):
        self.errata_address = errata_address
        self.execution_count = u256(0)

    @gl.public.write
    def execute_if_current(
        self,
        claim_id: u256,
        expected_claim_hash: str,
        action_hash: str,
    ) -> None:
        action = str(action_hash).strip().lower()
        if len(action) != 64:
            raise gl.vm.UserError("EXPECTED: action_hash must be a 32-byte hex digest without 0x")
        for char in action:
            if char not in "0123456789abcdef":
                raise gl.vm.UserError("EXPECTED: action_hash must be lowercase hex")
        if self.executions.get(action) is not None:
            raise gl.vm.UserError("EXPECTED: action already executed")

        errata = IErrata(self.errata_address)
        if not errata.view().is_claim_current(claim_id, expected_claim_hash):
            raise gl.vm.UserError("EXPECTED: Errata claim is not current")

        self.executions[action] = ExecutionReceipt(
            caller=gl.message.sender_address,
            claim_id=claim_id,
            claim_hash=str(expected_claim_hash),
            action_hash=action,
        )
        self.execution_count = u256(int(self.execution_count) + 1)

    @gl.public.view
    def was_executed(self, action_hash: str) -> bool:
        return self.executions.get(str(action_hash).strip().lower()) is not None

    @gl.public.view
    def get_execution(self, action_hash: str) -> dict:
        item = self.executions.get(str(action_hash).strip().lower())
        if item is None:
            return {}
        return {
            "caller": str(item.caller),
            "claim_id": int(item.claim_id),
            "claim_hash": str(item.claim_hash),
            "action_hash": str(item.action_hash),
        }
