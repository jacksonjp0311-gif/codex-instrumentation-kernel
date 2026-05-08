from __future__ import annotations


class InstrumentationLoop:
    def run(self, instrument, context: dict):
        anchored = instrument.anchor(context)
        shaped = instrument.shape(anchored)
        measured = instrument.measure(shaped)
        weighted = instrument.weight(measured)
        stressed = instrument.stress(weighted)
        classified = instrument.classify(stressed)
        artifacts = instrument.fossilize(classified)
        verified = instrument.verify(artifacts)
        indexed = instrument.index(verified)
        semantic = instrument.interpret(indexed)
        return semantic