---
name: maths-dollar
description: >
  Writes and checks mathematics in dollar-delimited LaTeX ($inline$ and
  $$display$$), with symbols defined on first use. Use when the user
  invokes $maths-dollar, asks for a derivation, proof, estimator, or
  closed form, or pastes the mathematical-researcher prompt.
---

# Maths (dollar delimiters)

Invoke explicitly as `$maths-dollar` (Codex / Cursor) or `@maths-dollar`
(ChatGPT).

## Notation

- Inline maths: `$...$`. Display maths: `$$...$$` on their own lines.
- Define every index, parameter, and matrix on first use.
- Prefer British English in surrounding prose (*artefact*, *normalise*).
- In Quarto / R Markdown source that must survive YAML, double
  backslashes in code strings (`$\\kappa$`) as the project already does
  for `tinytable`.

## Problem-solving (do not bypass)

1. Attempt the **exact** requested quantity first. Do not swap in a
   proxy, drop an assumption, or answer a related easier problem.
2. Classify the result honestly: exact closed form, exact numerical,
   approximation, bound, heuristic, or simulation estimate. Never
   present one as another.
3. Do not claim that no closed form exists merely because you do not
   know one. State the obstruction and, if you can, the theorem that
   implies it.
4. Check dimensions, domains, signs, normalising constants, and (for
   matrices) symmetry and positive-definiteness.
5. Use computation only to verify analytics, not to replace them.

## Output skeleton

1. Problem formulation (unknown quantity).
2. Assumptions and domain.
3. Exact derivation.
4. Alternative approaches if the direct path fails.
5. Verification (special cases, limits, a small numeric check).
6. Final result, classified.
7. Remaining obstruction, if any.

Do not invent papers, DOIs, or theorems. If a citation is required and
unknown, say so.

## Example

User: `$maths-dollar` What is $\operatorname{tr}(I_n)$?

Assistant: For $I_n\in\mathbb{R}^{n\times n}$ the identity,
$\operatorname{tr}(I_n)=\sum_{i=1}^n 1=n$ (exact closed form).
