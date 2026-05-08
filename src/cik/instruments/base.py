from __future__ import annotations

class Instrument:
    name = "base"
    version = "v0.1"

    def anchor(self, context): raise NotImplementedError
    def shape(self, anchored): raise NotImplementedError
    def measure(self, shaped): raise NotImplementedError
    def weight(self, measured): raise NotImplementedError
    def stress(self, weighted): return weighted
    def classify(self, stressed): raise NotImplementedError
    def fossilize(self, classified): raise NotImplementedError
    def verify(self, artifacts): return artifacts
    def index(self, verified): return verified
    def interpret(self, indexed): return indexed