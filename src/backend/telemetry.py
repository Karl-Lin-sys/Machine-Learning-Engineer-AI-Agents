import time
import uuid
from typing import Dict, Any

class TelemetryLogger:
    """
    A simple mockup telemetry service to track token usage, cost, and latency.
    This fulfills the 'cost-efficiency' and 'reliability' job requirements.
    """
    def __init__(self):
        self.logs = []
        
    def start_trace(self) -> str:
        return str(uuid.uuid4())
        
    def log_interaction(self, trace_id: str, prompt_tokens: int, completion_tokens: int, latency_ms: float):
        # Using typical OpenAI model approximations for cost tracking:
        cost_per_1k_prompt = 0.00015
        cost_per_1k_completion = 0.0006
        
        total_cost = (prompt_tokens / 1000.0) * cost_per_1k_prompt + \
                     (completion_tokens / 1000.0) * cost_per_1k_completion
                     
        log_entry = {
            "trace_id": trace_id,
            "latency_ms": latency_ms,
            "cost_usd": total_cost,
            "timestamp": time.time()
        }
        
        self.logs.append(log_entry)
        print(f"[TELEMETRY] Trace {trace_id} completed in {latency_ms:.2f}ms. Estimated cost: ${total_cost:.5f}")
        return log_entry
        
telemetry = TelemetryLogger()
