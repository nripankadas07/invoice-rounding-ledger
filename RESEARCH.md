# Candidate brief and comparison — 15 October 2026

**User:** Billing engineers reconciling line rounding against tax-group rounding, including credit lines.

**Pain and smallest capability:** Individually rounded tax lines can disagree with a rounded group total; a correction should conserve the total and have deterministic tie-breaking. Compute exact rational line amounts, compare rounding scopes and allocate each equal-rate tax total by largest fractional remainder with stable id tie-breaks.

**Acceptance criteria:** Allocated tax sums to each rounded group for positive, negative and mixed-sign inputs; permutation does not change id-based allocation; equivalent decimal rates coalesce; discount/quantity math is exact; duplicate ids and float/exponent values fail.

**Demand evidence:** Inferred operator/developer need, not a verified customer request. Current upstream READMEs, relevant docs/code and accessible issues were inspected. Issue titles below provide context about maintenance and operational work; they are not presented as requests for this tool. No claimed competitor absence is inferred from a successful example here.

**Discovery path:** Accurate repository description/topics, a runnable captured-input example and this evidence file; discoverable by `invoice; invoice rounding` and the task-specific terms. No unsolicited outreach or activity manipulation.

## Relevant established alternatives found

Live GitHub searches used Most stars ordering; exact queries/URLs/observations are in research-provenance.json. Highest-star relevant comparable found for this bounded workflow: `midday-ai/midday`. Broader collections, tutorials, proxies or unrelated applications in broad results were excluded by relevance; this is not an exhaustive global ranking. Focused invoice-rounding and matrix queries were sparse and broader established tools were retained transparently.

| Comparable | Stars observed | Latest push observed | Archived | API license classification |
| --- | ---: | --- | --- | --- |
| [midday-ai/midday](https://github.com/midday-ai/midday) | 15072 | 2026-06-13T13:40:35Z | False | AGPL-3.0 |
| [invoiceninja/invoiceninja](https://github.com/invoiceninja/invoiceninja) | 10277 | 2026-10-13T21:03:09Z | False | NOASSERTION |
| [crater-invoice-inc/crater](https://github.com/crater-invoice-inc/crater) | 8353 | 2024-08-10T09:32:07Z | False | AGPL-3.0 |

Observations are dated in research-provenance.json, including README blob hashes and accessible issue links. NOASSERTION means the API did not classify the license; upstream terms must be read before reuse. No upstream source was incorporated.

Midday describes an integrated business workflow, Invoice Ninja an invoicing platform with hosted/self-hosted paths, and Crater a web/mobile invoicing application. This isolated arithmetic witness is smaller in scope; it is not a replacement or a proven missing feature in those products. Midday current README calls invoicing upcoming; Crater last push observed2024-08-10, so stars do not establish active support.

Installation and first-use paths were inspected in current documentation, not benchmarked. These alternatives provide broader workflows, operational reliability features, docs/examples and support communities. This tool offers a bounded file/JSON contract, explicit failure modes and runnable fixtures but lacks their broader product capabilities, adoption evidence and maintenance history. Our build/install example measures only our behavior. Competitor installs, time-to-first-result, reliability and technical performance were not measured; no superiority claim or numerical performance comparison is made. Stars inform discovery, not quality or speed.

## Portfolio and candidate distinctness

Distinct from table-reconcile (keyed CSV value comparison), decimal-ts (decimal utility) and value-density-lab (product scoring): this creates a conserved per-line tax allocation with explicit rounding-scope differences.

All 178 owned repository identities/descriptions and the current project index were compared. Related release-asset-matrix, table-reconcile, sqlite-rehearsal and traceweave READMEs were inspected. The five candidates have separate users/contracts: backup dependency preservation, Kafka recovery positions, tax allocation arithmetic, span ancestry/interval coverage and CI matrix inclusion provenance. They are independent tools, not renamed/forked/subdivided versions of one product. Shared JSON CLI and packaging scaffolding does not substitute for their distinct algorithms and tests.
