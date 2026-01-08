from collections import deque

class SessionMonitor:
    """
    Maintains a sliding window of confidence scores
    to enable continuous behavioral authentication.
    """

    def __init__(self, window_size=5):
        self.confidences = deque(maxlen=window_size)

    def update(self, confidence):
        self.confidences.append(confidence)

    def assess(self):
        avg = sum(self.confidences) / len(self.confidences)

        if len(self.confidences) < self.confidences.maxlen:
            return "LEARNING", avg
        elif avg <= 0.25:
            return "STABLE", avg
        elif avg <= 0.45:
            return "DRIFTING", avg
        else:
            return "COMPROMISED", avg

    def history(self):
        """
        Returns confidence timeline for explainability.
        """
        return list(self.confidences)
