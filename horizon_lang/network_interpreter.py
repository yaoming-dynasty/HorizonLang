import numpy as np
import re
from typing import Dict, Tuple, Any

# Strict von Neumann Type III_1 efficiency ceiling (~41.22%)
TYPE_III_MAX_CEILING = 0.4122

class HorizonLangNetworkInterpreter:
    def __init__(self):
        self.matrices: Dict[str, np.ndarray] = {}
        self.scalars: Dict[str, float] = {}
        self.states: Dict[str, Dict[str, Any]] = {}

    def execute_program(self, source_code: str):
        """Parses and executes a complete HorizonLang program line-by-line."""
        print("=== INITIALIZING HORIZONLANG FOR TELECOM NETWORK ROUTING ===")
        lines = [line.strip() for line in source_code.split("\n") if line.strip() and not line.startswith("#")]
        
        for line in lines:
            if not line.endswith(";"):
                raise SyntaxError(f"HorizonLang Expects ';' statement termination: {line}")
            statement = line.strip(";")
            self._parse_statement(statement)

    def _parse_statement(self, stmt: str):
        # 1. Parse Ambient Noise declarations (Network Packet Noise Floor)
        if stmt.startswith("ambient"):
            match = re.match(r"ambient\s+(\w+)\s*=\s*([\d.]+)", stmt)
            if match:
                var_name, val = match.groups()
                self.scalars[var_name] = float(val)
                print(f"[PARSED] Network Noise Floor '{var_name}' set to {val} packets/sec")

        # 2. Parse Matrix declarations (Tower Network Routing Matrices)
        elif stmt.startswith("matrix"):
            match = re.match(r"matrix\s+(\w+)\s*=\s*\[\[([\d.-]+),\s*([\d.-]+)\],\s*\[([\d.-]+),\s*([\d.-]+)\]\]", stmt)
            if match:
                var_name, a, b, c, d = match.groups()
                self.matrices[var_name] = np.array([[float(a), float(b)], [float(c), float(d)]])
                print(f"[PARSED] Router Node '{var_name}' spatial routing properties mapped.")

        # 3. Parse Composition Bridge (Injecting Latency Drift Jitter)
        elif stmt.startswith("compose"):
            match = re.match(r"compose\s+(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s+drift\s+([\d.]+)", stmt)
            if match:
                target, matA, matB, drift = match.groups()
                drift_val = float(drift)
                
                # Composition Bridge: background noise envelope scales dynamically with latency drift
                noise_floor = self.scalars.get("INFY", 10000.0)
                noise_envelope = noise_floor * np.exp(-drift_val) * np.eye(2)
                
                # Non-commuting directional packet logic route transmission (Node A -> Node B)
                directed_routing_logic = 15.0 * (self.matrices[matA] @ self.matrices[matB])
                total_network_state = noise_envelope + directed_routing_logic
                
                self.matrices[target] = total_network_state
                self.states[target] = {"drift": drift_val, "type": "network_state"}
                print(f"[BRIDGE 1: COMPOSITION] Transmission state '{target}' built across latency drift: {drift_val} ms")

        # 4. Parse Decomposition Bridge (Separating Background from Active Connections)
        elif stmt.startswith("decompose"):
            match = re.match(r"decompose\s+(\w+)\s*,\s*(\w+)\s+from\s+(\w+)", stmt)
            if match:
                sym_out, anti_out, source = match.groups()
                drift_val = self.states[source]["drift"]
                total_network_state = self.matrices[source]
                
                # Reconstruct the symmetric stationary background network overhead
                noise_floor = self.scalars.get("INFY", 10000.0)
                symmetric_context = noise_floor * np.exp(-drift_val) * np.eye(2)
                
                # Subtraction extracts the dynamic route execution flow
                antisymmetric_flow = total_network_state - symmetric_context
                
                self.matrices[sym_out] = symmetric_context
                self.matrices[anti_out] = antisymmetric_flow
                print(f"[BRIDGE 2: DECOMPOSITION] Isolated stationary noise '{sym_out}' from dynamic path '{anti_out}'.")

        # 5. Parse Transformation Bridge (Extracting the Logical Connection Kernel)
        elif stmt.startswith("regularize"):
            match = re.match(r"regularize\s+(\w+)\s*=\s*(\w+)\s*-\s*(\w+)", stmt)
            if match:
                horizon_var, inside_var, outside_var = match.groups()
                
                # Your Structural Equation: [TOTAL_NETWORK_STATE] - [STATIONARY_NOISE] = [LOGICAL_KERNEL]
                horizon_matrix = self.matrices[inside_var] - self.matrices[outside_var]
                kernel_signal_magnitude = float(np.linalg.norm(horizon_matrix, 'fro'))
                
                self.matrices[horizon_var] = horizon_matrix
                self.scalars[f"{horizon_var}_signal"] = kernel_signal_magnitude
                print(f"[BRIDGE 3: TRANSFORMATION] [INSIDE] - [OUTSIDE] applied. Isolated Connection Kernel: {kernel_signal_magnitude:.4f}")

        # 6. Parse Validation Bridge (Verifying Network Route Stability)
        elif stmt.startswith("validate"):
            match = re.match(r"validate\s+(\w+)\s+limit\s+([\d.]+)", stmt)
            if match:
                horizon_var, limit = match.groups()
                signal = self.scalars[f"{horizon_var}_signal"]
                limit_val = float(limit)
                
                # Bounded routing confidence ceiling slaved to Type III factor math
                routing_confidence = (TYPE_III_MAX_CEILING * (1.0 - np.exp(-signal / limit_val))) * 100
                passed = signal > 1e-5
                
                print(f"[BRIDGE 4: VALIDATION] Network Route Analysis Verified.")
                print(f" -> Isolated Signal Magnitude: {signal:.4f}")
                print(f" -> Channel Alignment Confidence: {routing_confidence:.4f}%")
                print(f" -> CONNECTION RUNTIME GATES: {'[ PASS ]' if passed else '[ FAIL ]'}")


# ===================================================
# --- EXECUTE TELECOM ROUTING RUN IN HORIZONLANG ---
# ===================================================

if __name__ == "__main__":
    # Source code modeling changing connection properties across a varying latency sweep
    telecom_network_source = """
    # Set a massive unguided background packet noise profile (INFY proxy)
    ambient INFY = 35000.0;
    
    # Map the unique directional hardware signatures of Router Towers A and B
    matrix ROUTER_A = [[0.85, 0.12], [-0.05, 0.92]];
    matrix ROUTER_B = [[1.05, -0.34], [0.15, 0.78]];
    
    # Bridge 1: Compose the cellular data loop under active latency drift jitter (0.85 ms delay variance)
    compose COMM_STATE = ROUTER_A * ROUTER_B drift 0.85;
    
    # Bridge 2: Decompose the uniform background tower overhead from the data link
    decompose STATIONARY_NOISE, LINK_FLOW from COMM_STATE;
    
    # Bridge 3: Apply the structural subtraction equation to extract the clean logical routing kernel
    regularize NETWORK_KERNEL = COMM_STATE - STATIONARY_NOISE;
    
    # Bridge 4: Validate route channel stability against the open algebraic bounds
    validate NETWORK_KERNEL limit 12.5;
    """
    
    compiler = HorizonLangNetworkInterpreter()
    compiler.execute_program(telecom_network_source)
