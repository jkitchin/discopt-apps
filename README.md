# discopt-apps

Nonconvex application builders for the
[discopt](https://github.com/jkitchin/discopt) modeling language. The
distribution ships **two** namespace subpackages — code written against
`from discopt.opf import ...` or `from discopt.pooling import ...` works
unchanged after installing this package.

Both builders emit a plain `discopt.modeling.core.Model`, so the same certified
global engine (McCormick relaxation + spatial branch-and-bound) solves them.

1. **AC optimal power flow** (`discopt.opf`) — the canonical hard QCQP of power
   systems. In rectangular voltage coordinates `V_i = e_i + j f_i` the power
   injections are quadratic in `(e, f)`, so the whole problem is a QCQP.
   `build_ac_opf_rectangular` turns a small network spec into a solvable model.

2. **The pooling problem** (`discopt.pooling`) — blend raw inputs of known
   quality through pools into spec-constrained products at maximum profit. The
   builder emits the tight pq-formulation (Tawarmalani & Sahinidis) whose RLT
   cuts make the root relaxation exact on classic instances (Haverly).

## Install

```bash
pip install discopt-apps
```

Requires `discopt>=0.6` (the first release with the public
`discopt.modeling.core` API).

## Quick start

AC-OPF on the built-in two-bus example:

```python
from discopt.opf import build_ac_opf_rectangular, two_bus_example

model = build_ac_opf_rectangular(two_bus_example())
result = model.solve()
print(result.status, float(result.objective))
```

The pooling problem on the canonical Haverly instance (optimum: profit 400):

```python
from discopt.pooling import build_pq_formulation, haverly_hpp1

model = build_pq_formulation(haverly_hpp1())
result = model.solve()
print(result.status, float(result.objective))
```

## Development

The project is uv-managed:

```bash
uv sync            # create .venv with discopt (pinned branch) + dev deps
uv run pytest      # fast test set (slow tests excluded by default)
uv run pytest -m ''    # everything, including the slow OPF reference solve
uv run ruff check .
uv run ruff format --check .
```

To develop against a local discopt checkout instead of the pinned branch, add
a `[tool.uv.sources]` override pointing `discopt` at your editable clone:

```toml
[tool.uv.sources]
discopt = { path = "../../projects/discopt", editable = true }
```

Docs are a Jupyter Book:

```bash
uv run jupyter-book build docs/
```

## Literature

The methods are referenced throughout the docs; the full bibliography is in
[docs/references.bib](docs/references.bib) (Carpentier / Frank–Steponavice /
Molzahn–Hiskens on AC-OPF; Haverly, McCormick, and Tawarmalani–Sahinidis on
pooling and its pq-formulation).
