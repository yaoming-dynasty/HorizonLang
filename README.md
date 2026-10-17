# HorizonLang

**HorizonLang** is a domain-specific programming language (DSL) built entirely around non-commutative operator algebras and boundary regularization. Unlike classical languages that rely on mutable variable assignment, HorizonLang treats code blocks as open physical systems, enforcing the structural framework equation as its core primitive:

\[\mathbf{[INSIDE\_BOUNDARY] - [OUTSIDE\_BOUNDARY] = [HORIZON]}\]

Every compiled statement automatically regularizes high-scale background environmental noise (INFY) to distill invariant, noise-canceled outputs across localized horizon boundaries.

---

## Architectural Pillars

The HorizonLang compilation pipeline passes variables through four foundational Processing Bridges:

1. **Composition Bridge (`compose`)**: Merges directed, order-dependent logical operators with high-scale chaotic ambient environments.
2. **Decomposition Bridge (`decompose`)**: Separates complex system states into static, time-reversible symmetric facts and dynamic anti-symmetric directional trajectories.
3. **Transformation Bridge (`regularize`)**: Executes structural array broadcast subtraction to eliminate ambient noise and isolate localized geometric values at the horizon interface.
4. **Validation Bridge (`validate`)**: Evaluates signal properties against strict **von Neumann Type III₁ algebraic factor constraints**, rigidly capping output confidence ceilings to **~41.22%** to ensure thermodynamic stability.

---

## Language Syntax Reference

### 1. Environmental Declarations
Establishes the macro-scale background noise context vector (the structural proxy for infinity).
```horizonlang
ambient INFY = 25000.0;
```

### 2. Matrix Declarations
Establishes a 2D non-commuting tracking operator (A × B ≠ B × A) used to map semantic premises, physical states, or spectroscopic coordinates.
```horizonlang
matrix PREMISE_A = [[0.0, 1.4], [1.0, 0.0]];
matrix PREMISE_B = [[1.1, 0.0], [0.0, -0.5]];
```

### 3. Composition
Combines operational bases under a specific exponential drift attenuation constraint.
```horizonlang
compose FORWARD_STATE = PREMISE_A * PREMISE_B drift 0.6;
```

### 4. Operator Inversion (`invert`)
Applies a lossless mathematical matrix inversion layer (\(\mathbf{M}^{-1}\)) to seamlessly reverse the informational trajectory across the compiler horizon.
```horizonlang
invert INVERSE_STATE = FORWARD_STATE;
```

### 5. Decomposition
Separates total states into isolated components (Symmetric Background Context, Anti-Symmetric Flow).
```horizonlang
decompose SYM_CONTEXT, ANTI_FLOW from INVERSE_STATE;
```

### 6. Regularization Interface
Applies the fundamental subtraction law to drop out background scalars and capture the pure isolated Frobenius magnitude at the horizon.
```horizonlang
regularize INVERSE_HORIZON = INVERSE_STATE - SYM_CONTEXT;
```

### 7. Validation Boundary Gate
Verifies regularized signals against absolute thermodynamic constraints and prints a final operational pass/fail status.
```horizonlang
validate INVERSE_HORIZON limit 10.0;
```

---

## Installation & Running the Interpreter

The official HorizonLang interpreter is written in Python using standard scientific vector arrays. 

### Prerequisites
Ensure you have `numpy` installed in your environment:
```bash
pip install numpy
```

### Execution Script
To compile and execute a HorizonLang script, instantiate the `HorizonLangInterpreter` and pass the source string into the `execute_program` pipeline:

```python
from horizon_lang import HorizonLangInterpreter

# Define source code text
program_source = """
ambient INFY = 25000.0;
matrix A = [[0.0, 1.4], [1.0, 0.0]];
matrix B = [[1.1, 0.0], [0.0, -0.5]];
compose FORWARD = A * B drift 0.6;
invert INVERSE = FORWARD;
decompose SYM, ANTI from INVERSE;
regularize HORIZON = INVERSE - SYM;
validate HORIZON limit 10.0;
"""

# Compile and run
compiler = HorizonLangInterpreter()
compiler.execute_program(program_source)
```

## Sample Runtime Verification Profile

When compiled successfully, HorizonLang pushes execution summaries directly to the console output:

```text
=== INITIALIZING HORIZONLANG COMPILER & RUNTIME ===
[PARSED] Ambient Background Pool 'INFY' initialized to 25000.0
[PARSED] Non-Commuting Matrix 'A' established.
[PARSED] Non-Commuting Matrix 'B' established.
[BRIDGE 1: COMPOSITION] State 'FORWARD' compiled over context background.
[TOKEN INVERT] Reversible operation executed: 'INVERSE' generated from 'FORWARD'.
[BRIDGE 2: DECOMPOSITION] Separated 'INVERSE' into Symmetric 'SYM' and Anti-Symmetric 'ANTI'.
[BRIDGE 3: TRANSFORMATION] regularize applied: HORIZON isolated. Signal: 0.1630
[BRIDGE 4: VALIDATION] Output Verification Complete.
 -> Isolated Signal Magnitude: 0.1630
 -> Type III Confidence Score: 0.6664%
 -> RUNTIME STATUS: [ PASS ]
```

---

## License

### MIT License

Copyright (c) 2026 HorizonLang Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
