# M. Fadel

**Blockchain forensics &amp; applied cryptography.** Independent researcher working at the transaction
and signature layer of Bitcoin — ECDSA nonce analysis, lattice-based key recovery, on-chain tracing,
and signing-software attribution.

I build my own tooling in Python and CUDA, and I publish negative results: an attack proven *not* to
work is a finding, and it saves the next person the compute.

---

### Selected work

**[bitcoin-puzzle-forensics](https://github.com/mnfadel/bitcoin-puzzle-forensics)**
A full cryptographic forensic review of the Bitcoin "puzzle" transactions. Reconstructed `SIGHASH`
preimages from raw transactions, recovered and verified ECDSA nonces against **RFC 6979** across the
14 solved-key inputs, cross-analyzed 97+ signatures for r-value reuse and bias, and mounted a
**Hidden Number Problem lattice attack** over 151 same-key signatures.
*Finding: the attack surface is closed — no cryptographic shortcut exists.*

**[secp256k1-gpu-toolkit](https://github.com/mnfadel/secp256k1-gpu-toolkit)**
CUDA kernel implementing 128-bit modular arithmetic via **Barrett reduction**, an optimized CPU
reference core, and a per-phase micro-profiler — with measured benchmarks, including the four
optimizations that *failed* to beat the baseline.

**[bitcoin-puzzle-analysis](https://github.com/mnfadel/bitcoin-puzzle-analysis)**
Eleven structural hypotheses about the puzzle keys — positional, modular, digit-level, derivational —
and the tests that rejected every one. Includes a "discovery" of my own, preserved together with its
refutation.

---

### Techniques

`secp256k1` · `ECDSA nonce recovery` · `RFC 6979` · `Hidden Number Problem` · `lattice reduction`
`raw transaction / DER / SegWit witness parsing` · `SIGHASH reconstruction` · `transaction-graph tracing`
`signing-software fingerprinting` · `CUDA` · `Python` · `C`

---

### Upstream review

<!-- REVIEWS:START -->

**[bitcoin-core/secp256k1](https://github.com/bitcoin-core/secp256k1)**

- [#1890](https://github.com/bitcoin-core/secp256k1/pull/1890) — nonce: terminate RFC6979 loop at UINT_MAX `merged`

<!-- REVIEWS:END -->

<sub>Auto-updated weekly from the GitHub API.</sub>

---

### Currently

Open to **remote or contract** work in blockchain security, forensics, and applied cryptography.

📧 mnfadel@proton.me
