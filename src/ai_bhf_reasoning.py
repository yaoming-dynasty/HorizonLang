import numpy as np

class AIBHFReasoningEngine:
    def __init__(self, total_latent_capacity: float, max_context_tokens: float):
        self.omega_out_latent = total_latent_capacity  # Maximal knowledge space
        self.max_context = max_context_tokens          # Hard context window limit
        
    def compute_cognitive_horizon(self, attention_focus_factor: float, token_consumption_fraction: float) -> dict:
        """
        Computes the AI's active reasoning horizon as context fills up and 
        attention constraints (prompt filtering) narrow the focus.
        """
        # 1. Attention & Prompt Filtering: Narrowing focus from total latent knowledge
        active_latent_domain = min(self.omega_out_latent, self.omega_out_latent * attention_focus_factor)
        latent_horizon_delta = self.omega_out_latent - active_latent_domain

        # 2. Context Window Exhaustion: Tracking consumed tokens vs. remaining capacity
        consumed_tokens = self.max_context * token_consumption_fraction
        if not (0.0 <= token_consumption_fraction <= 1.0):
            raise ValueError("Token consumption fraction must be between 0.0 and 1.0.")
            
        remaining_context_capacity = self.max_context - consumed_tokens

        # Total cognitive finitude: balancing latent creativity against context limits
        total_cognitive_finitude = latent_horizon_delta + remaining_context_capacity

        return {
            "latent_reasoning_frontier": latent_horizon_delta,
            "remaining_context_capacity": remaining_context_capacity,
            "total_cognitive_finitude": total_cognitive_finitude
        }

# Example Execution: Simulating an AI running a long multi-turn reasoning task
if __name__ == "__main__":
    ai_engine = AIBHFReasoningEngine(total_latent_capacity=5000.0, max_context_tokens=128.00)
    
    print("Attention Focus | Token Usage | Latent Frontier (H) | Context Buffer | Total Finitude")
    print("-" * 80)
    
    # Simulate tightening attention and filling up the context window over time
    for focus, usage in zip([0.9, 0.5, 0.2], [0.1, 0.5, 0.9]):
        result = ai_engine.compute_cognitive_horizon(focus, usage)
        frontier = result["latent_reasoning_frontier"]
        buffer = result["remaining_context_capacity"]
        finitude = result["total_cognitive_finitude"]
        print(f"{focus:15.1f} | {usage:11.1f} | {frontier:19.2f} | {buffer:14.2f} | {finitude:14.2f}")
