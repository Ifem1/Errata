# Errata

**Correction-aware public fact infrastructure for GenLayer.**

Errata is a standalone reusable Intelligent Contract primitive. It tracks a public record across later confirmations, amendments, corrections, retractions, and superseding publications without rewriting history.

There is intentionally **no frontend**. Builders consume Errata through typed Intelligent Contract interfaces.

## The problem

Most oracle-style systems can answer a question from a source at one moment. They are much weaker at a different problem:

> What should happen when a previously relied-upon public record is later corrected or retracted?

Deleting or overwriting the old fact destroys auditability. Ignoring the correction leaves downstream contracts operating on stale evidence.

Errata preserves both:

1. immutable historical revision lineage; and
2. deterministic invalidation of claims that pin an obsolete canonical revision.

## Core protocol

A record starts in `DRAFT`.

The creator freezes:

- a subject;
- a bounded semantic record definition; and
- up to six HTTPS authority hosts that form the declared evidence surface.

Publishing the initial record seals that surface.

Later callers may propose publications only from the sealed host set (or its subdomains). GenLayer validators independently fetch and classify the publication relative to the current canonical statement:

- `CONFIRMS`
- `AMENDS`
- `CORRECTS`
- `RETRACTS`
- `SUPERSEDES`
- `UNRELATED`
- `AMBIGUOUS`

`AMENDS`, `CORRECTS`, `RETRACTS`, and `SUPERSEDES` are material relations. They advance the canonical revision. `CONFIRMS`, `UNRELATED`, and `AMBIGUOUS` remain auditable revision receipts but do not move canonical state.

## Consensus design

Errata uses `gl.vm.run_nondet_unsafe`.

The leader:

1. independently renders the public source;
2. classifies the revision relationship;
3. returns a bounded canonical statement, rationale, and short verbatim evidence excerpt.

A validator independently re-fetches the same source and re-runs the semantic task.

The validator rejects a proposal unless:

- the relation class matches its independent result;
- material evidence is grounded in the validator's own fetched source;
- replacement statements are semantically equivalent to the validator's independently derived statement; and
- a `CONFIRMS` result remains semantically equivalent to the prior canonical statement.

Storage mutation occurs only after consensus.

## Persistent state

Every material revision creates a new immutable lineage node with:

- source URL;
- prior revision id;
- semantic relation;
- statement;
- grounded evidence;
- evidence hash;
- revision hash; and
- lineage hash.

The record exposes:

- `definition_hash` — binds subject, definition, and sealed evidence surface;
- `canon_hash` — binds the currently operative revision and lineage;
- `canon_version` — increments only on material canonical changes.

## Dependency invalidation

Builders can create immutable dependent claims pinned to the current canonical revision.

Claims may also depend on earlier claims, creating a bounded acyclic dependency DAG.

When a material correction changes the canonical revision, Errata deterministically marks claims pinned to the old revision `STALE` and cascades staleness to descendants.

The LLM never decides which dependent claims become stale. Once consensus establishes a material canonical change, invalidation is deterministic.

## Real cross-contract consumer

`contracts/canon_gate.py` is a separate Intelligent Contract.

It executes an action only when:

```python
errata.view().is_claim_current(claim_id, expected_claim_hash)
```

returns `True`.

It also stores executed action hashes to prevent replay.

This is included so reuse is not merely documentary: the intended StudioNet proof is to deploy **both** contracts, execute successfully while the claim is current, register a correction, and then show the same consumer refusing a new action because the Errata claim became stale.

## Trust boundary

Errata does **not** claim:

- that a configured authority host is objectively authoritative;
- that every real-world correction will be discovered;
- that an off-surface publication is invalid in the real world; or
- that a stored statement is legal advice.

It proves a narrower property:

> Within a creator-sealed public HTTPS evidence surface, GenLayer validators agreed on the semantic relationship between a later publication and the current canonical record, and deterministic contract logic updated lineage and dependency freshness accordingly.

This keeps the primitive honest and composable.

## Repository layout

```text
contracts/
  errata.py                 main primitive
  canon_gate.py     cross-contract reuse proof

tests/
  direct/                   GenLayer Direct Mode adversarial/lifecycle tests
  unit/                     static structural checks

scripts/
  preflight.py
  test_all.sh
  deploy_errata.sh
  deploy_canon_gate.sh
```

No frontend, wallet UI, database, backend, API key, or private service is required.

## Test

Static checks:

```bash
python scripts/preflight.py
python -m pytest tests/unit -q
```

Direct Mode:

```bash
python -m pip install -r requirements-test.txt
gltest tests/direct -v -s
```

## Deploy

Deploy Errata:

```bash
./scripts/deploy_errata.sh
```

Then deploy the consumer with the finalized Errata address:

```bash
./scripts/deploy_canon_gate.sh 0xYOUR_ERRATA_ADDRESS
```

Do not claim network verification until both deployments and the cross-contract stale-claim lifecycle have finalized successfully.

## Verified StudioNet deployments

The contracts were deployed to GenLayer StudioNet (chain ID `61999`) and their receipts were polled to `FINALIZED` with `SUCCESS` execution and majority agreement:

| Contract | Address | Deployment transaction |
| --- | --- | --- |
| Errata | `0x245A87125Af6Ab2DF7E3e70e3797820C0b01F70A` | `0x4a1af301a473316f8f144a19aeec39421c3b4f69e36ca8fbe7e6786096c97203` |
| CanonGate | `0x27b49ed5675278188CB637e560F282636Df53aF3` | `0x72a79eaff4c1292f4b6f38bb4721fee98bbbb06fb37ed346c409bc300fbd8320` |

Reproduce the local checks with:

```bash
python scripts/preflight.py
python -m pytest tests/unit -q
python -m pip install -r requirements-test.txt
gltest tests/direct -v -s
```

The intended reviewer lifecycle is: create and publish an initial record, create a claim pinned to it, execute through CanonGate while current, submit a confirming publication that leaves canon and the claim current, submit a consensus-backed correction or supersession that advances canon and deterministically stales the claim, observe CanonGate reject the stale claim, then create a claim pinned to the corrected revision and execute successfully again. The repository contains no frontend, wallet UI, backend, database, or unrelated product layer.
