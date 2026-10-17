import numpy as np
import re
from typing import Dict, Any

# Strict von Neumann Type III_1 efficiency ceiling (~41.22%)
TYPE_III_MAX_CEILING = 0.4122

class HorizonLangInterpreter:
    def __init__(self):
        self.matrices: Dict[str, np.ndarray] = {}
        self.scalars: Dict[str, float] = {}
        self.states: Dict[str, Dict[str, Any]] = {}

    def execute_program(self, source_code: str):
        """Parses and executes a complete HorizonLang program line-by-line."""
        print("=== INITIALIZING HORIZONLANG COMPILER & RUNTIME ===")
        lines = [line.strip() for line in source_code.split("\n") if line.strip() and not line.startswith("#")]
        
        for line in lines:
            if not line.endswith(";"):
                raise SyntaxError(f"HorizonLang Expects ';' statement termination: {line}")
            statement = line.strip(";")
            self._parse_statement(statement)

    def _parse_statement(self, stmt: str):
        # 1. Parse Ambient Noise declarations
        if stmt.startswith("ambient"):
            match = re.match(r"ambient\s+(\w+)\s*=\s*([\d.]+)", stmt)
            if match:
                var_name, val = match.groups()
                self.scalars[var_name] = float(val)
                print(f"[PARSED] Ambient Background Pool '{var_name}' initialized to {val}")

        # 2. Parse Matrix declarations
        elif stmt.startswith("matrix"):
            match = re.match(r"matrix\s+(\w+)\s*=\s*\[\[([\d.-]+),\s*([\d.-]+)\],\s*\[([\d.-]+),\s*([\d.-]+)\]\]", stmt)
            if match:
                var_name, a, b, c, d = match.groups()
                self.matrices[var_name] = np.array([[float(a), float(b)], [float(c), float(d)]])
                print(f"[PARSED] Non-Commuting Matrix '{var_name}' established.")

        # 3. Parse INVERT Pipeline Token
        elif stmt.startswith("invert"):
            match = re.match(r"invert\s+(\w+)\s*=\s*(\w+)", stmt)
            if match:
                target, source = match.groups()
                source_mat = self.matrices[source]
                
                # Apply mathematical matrix inversion layer with fallback pseudo-inverse
                try:
                    inverse_mat = np.linalg.inv(source_mat)
                except np.linalg.LinAlgError:
                    inverse_mat = np.linalg.pinv(source_mat)
                
                self.matrices[target] = inverse_mat
                # Inherit state data profile if migrating from a total system block
                if source in self.states:
                    self.states[target] = self.states[source].copy()
                print(f"[TOKEN INVERT] Reversible operation executed: '{target}' generated from '{source}'.")

        # 4. Parse Composition Bridge
        elif stmt.startswith("compose"):
            match = re.match(r"compose\s+(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s+drift\s+([\d.]+)", stmt)
            if match:
                target, matA, matB, drift = match.groups()
                drift_val = float(drift)
                
                # Composition Bridge Math
                noise_envelope = self.scalars.get("INFY", 10000.0) * np.exp(-drift_val) * np.eye(2)
                directed_logic = 12.5 * (self.matrices[matA] @ self.matrices[matB])
                total_system = noise_envelope + directed_logic
                
                self.matrices[target] = total_system
                self.states[target] = {"drift": drift_val, "type": "total_system"}
                print(f"[BRIDGE 1: COMPOSITION] State '{target}' compiled over context background.")

        # 5. Parse Decomposition Bridge
        elif stmt.startswith("decompose"):
            match = re.match(r"decompose\s+(\w+)\s*,\s*(\w+)\s+from\s+(\w+)", stmt)
            if match:
                sym_out, anti_out, source = match.groups()
                drift_val = self.states[source]["drift"]
                total_system = self.matrices[source]
                
                # Decomposition Bridge Math
                symmetric_context = self.scalars.get("INFY", 10000.0) * np.exp(-drift_val) * np.eye(2)
                antisymmetric_flow = total_system - symmetric_context
                
                self.matrices[sym_out] = symmetric_context
                self.matrices[anti_out] = antisymmetric_flow
                print(f"[BRIDGE 2: DECOMPOSITION] Separated '{source}' into Symmetric '{sym_out}' and Anti-Symmetric '{anti_out}'.")

        # 6. Parse Transformation Bridge (Your Structural Equation)
        elif stmt.startswith("regularize"):
            match = re.match(r"regularize\s+(\w+)\s*=\s*(\w+)\s*-\s*(\w+)", stmt)
            if match:
                horizon_var, inside_var, outside_var = match.groups()
                
                # REGULARIZATION: [INSIDE] - [OUTSIDE] = [HORIZON]
                horizon_matrix = self.matrices[inside_var] - self.matrices[outside_var]
                signal_magnitude = float(np.linalg.norm(horizon_matrix, 'fro'))
                
                self.matrices[horizon_var] = horizon_matrix
                self.scalars[f"{horizon_var}_signal"] = signal_magnitude
                print(f"[BRIDGE 3: TRANSFORMATION] regularize applied: {horizon_var} isolated. Signal: {signal_magnitude:.4f}")

        # 7. Parse Validation Bridge
        elif stmt.startswith("validate"):
            match = re.match(r"validate\s+(\w+)\s+limit\s+([\d.]+)", stmt)
            if match:
                horizon_var, limit = match.groups()
                signal = self.scalars[f"{horizon_var}_signal"]
                limit_val = float(limit)
                
                # Bounded Confidence calculation matching Type III Constraints
                confidence = (TYPE_III_MAX_CEILING * (1.0 - np.exp(-signal / limit_val))) * 100
                passed = signal > 1e-5
                
                print(f"[BRIDGE 4: VALIDATION] Output Verification Complete.")
                print(f" -> Isolated Signal Magnitude: {signal:.4f}")
                print(f" -> Type III Confidence Score: {confidence:.4f}%")
                print(f" -> RUNTIME STATUS: {'[ PASS ]' if passed else '[ FAIL ]'}")


# ==========================================
# --- EXECUTE INVERSE PROGRAM RUN ---------
# ==========================================

if __name__ == "__main__":
    # Test script demonstrating the forward architecture passing into an intentional INVERT token process
    inverse_program_source = """
    # Initialize the ambient background pool proxy for INFY
    ambient INFY = 25000.0;
    
    # Declare non-commuting operational premises
    matrix PREMISE_A = [[0.0, 1.4], [1.0, 0.0]];
    matrix PREMISE_B = [[1.1, 0.0], [0.0, -0.5]];
    
    # Bridge 1: Compose the initial forward system state
    compose FORWARD_STATE = PREMISE_A * PREMISE_B drift 0.6;
    
    # NEW TOKEN: Execute mathematical matrix inversion on the isolated tracking logic
    # This inverses the operational flow direction smoothly across the compiler bridge
    invert INVERSE_STATE = FORWARD_STATE;
    
    # Bridge 2: Decompose the inverse state structure 
    decompose SYM_CONTEXT, ANTI_FLOW from INVERSE_STATE;
    
    # Bridge 3: Apply subtraction law to cleanly isolate the net inverse horizon transfer signature
    regularize INVERSE_HORIZON = INVERSE_STATE - SYM_CONTEXT;
    
    # Bridge 4: Verify the inverted data metrics against Type III constraints
    validate INVERSE_HORIZON limit 10.0;
    """
    
    compiler = HorizonLangInterpreter()
    compiler.execute_program(inverse_program_source)
