from ..world_entities import WorldSignal

class SignalConfidenceEngine:
    def __init__(self):
        self.source_reliability = {
            "market_report": 0.9,
            "news": 0.7,
            "social": 0.3
        }

    def evaluate(self, signal: WorldSignal) -> float:
        base_confidence = self.source_reliability.get(signal.source, 0.5)
        # Boost confidence based on verification count
        boost = min(0.3, (signal.verification_count - 1) * 0.1)
        final_conf = min(1.0, base_confidence + boost)
        signal.confidence = final_conf
        return final_conf
