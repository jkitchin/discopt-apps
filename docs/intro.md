# discopt-apps

**discopt-apps** bundles two nonconvex application builders for the
[discopt](https://github.com/jkitchin/discopt) modeling language. Each installs
as a `discopt` namespace subpackage, so `from discopt.opf import ...` and
`from discopt.pooling import ...` work exactly as they did when the modules
lived in the base package.

Both builders emit a plain `discopt.modeling.core.Model`; the global machinery
(McCormick relaxation + spatial branch-and-bound) is reused unchanged, so each
application is solved by the same certified engine as any other model.

1. **AC optimal power flow** (`discopt.opf`) — the canonical hard QCQP of power
   systems {cite:p}`Carpentier1962,FrankSteponavice2012`. In **rectangular**
   voltage coordinates $V_i = e_i + j f_i$ the power injections are quadratic in
   $(e, f)$, so the whole problem is a QCQP {cite:p}`Jabr2006,Molzahn2019` —
   exactly the structure the PSD/SOC moment cuts target.
   `build_ac_opf_rectangular` turns a small network spec into a solvable model.

2. **The pooling problem** (`discopt.pooling`) — route raw inputs of known
   quality through blending pools to spec-constrained products at maximum
   profit {cite:p}`Haverly1978`. The blended quality is a *bilinear* function of
   inflows, so the problem is a nonconvex NLP whose naive McCormick relaxation
   {cite:p}`McCormick1976` is weak. `build_pq_formulation` builds the
   pq-formulation of {cite:t}`Tawarmalani2002`, whose RLT cuts make the root
   relaxation provably tighter, so classic instances (Haverly) close in a
   handful of branch-and-bound nodes.

## Install

```bash
pip install discopt-apps
```

Requires `discopt>=0.6` (the first release with the public
`discopt.modeling.core` API).

## Where to start

- Power systems / QCQP: see the {doc}`AC-OPF notebook <notebooks/ac_opf>`.
- Blending / bilinear NLP: see the
  {doc}`pooling notebook <notebooks/pooling_pq>`.
