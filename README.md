# invoice-rounding-ledger

Compute exact rational line amounts, compare rounding scopes and allocate each equal-rate tax total by largest fractional remainder with stable id tie-breaks.

## User and task

Billing engineers reconciling line rounding against tax-group rounding, including credit lines. Individually rounded tax lines can disagree with a rounded group total; a correction should conserve the total and have deterministic tie-breaking.

## Install and first useful result

Python 3.10+ and pip. Git source install; no external-registry release is claimed.

```sh
git clone https://github.com/nripankadas07/invoice-rounding-ledger.git
cd invoice-rounding-ledger
python -m venv .venv
# POSIX: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install .
invoice-rounding-ledger example.json
```

Three 0.10 lines at rate 0.05 produce exact tax 0.5 minor units each. Group tax rounds to 2; ids A/B receive 1 each andC receives 0. Independently rounded tax lines total 3, so the scope difference is -1. The example is synthetic. JSON goes to stdout. Exit0 means analyzed with no review findings; exit 1 means review findings; exit 2 means malformed/unsupported input or an IO error. Differences explicitly labeled informational do not alone trigger exit 1. Help: `invoice-rounding-ledger --help`.

## Input contract

Required keys: currency (three uppercase letters used only as a label), digits (0..4) and lines. Each line requires unique id, quantity, unit_price, discount, tax_rate. Monetary/quantity/rate values are plain decimal strings, at most18 integer digits and12 fractional digits; exponent notation and floats are rejected. quantity may be negative for credits; unit_price>=0; discount and tax_rate in[0,1]. Net=quantity*unit_price*(1-discount). Tax=exact net*rate. Equal rational rates share a group. Round each group to nearest minor unit, ties away from zero, then distribute from mathematical floors by descending fractional remainder, ties by id. Output payable uses the sum of independently rounded line net amounts plus allocated group tax. Differences from invoice-net rounding are shown separately.

Every object rejects unknown keys. CLI input is UTF-8 JSON, read with a 2 MiB cap before parsing; duplicate keys/nonfinite values fail. Default arrays allow at most 512 entries, strings1..256 characters and nonnegative integers up to2^63-1 except where a tighter/different bound is documented. The example shows the complete input shape. JSON output includes the supplied identities; review it before sharing sensitive inputs.

## Validate

```sh
python -m unittest -v
python -m compileall -q invoice_rounding_ledger.py
python -m pip wheel --no-deps --wheel-dir dist .
python -m venv /tmp/invoice-rounding-ledger-installed
/tmp/invoice-rounding-ledger-installed/bin/python -m pip install --no-index --no-deps dist/*.whl
python test_installed_cli.py /tmp/invoice-rounding-ledger-installed/bin/python
```

The last commands show the Linux/POSIX path; use the equivalent Scripts/python.exe path on Windows. Remote configured CI uses Linux Python 3.10/3.12/3.14. [Validation](VALIDATION.md) records actual preparation checks and limits; a workflow configuration is not itself proof of a passing run.

## Scope and limitations

Arithmetic contract only. No jurisdiction-specific tax rules, currency exponent lookup, FX, inclusive taxes, compound taxes, shipping or invoice importers. Caller supplies rates and digits. Allocations can differ by a minor unit from individually rounded tax lines; this is explicit, not a legal/accounting correctness claim. No invoices or payments are sent.

No runtime third-party packages. Setuptools is a build dependency. Original implementation developed with AI assistance, MIT licensed; no competitor code, prose or branding copied. [Research](RESEARCH.md), [contribution](CONTRIBUTING.md), [support](SUPPORT.md) and [security](SECURITY.md) guidance are included.
