from __future__ import annotations

from cik.instruments.rcc_drift.instrument import RCCDriftInstrument


REGISTRY = {
    "rcc-drift": RCCDriftInstrument,
}


def list_instruments() -> list[str]:
    return sorted(REGISTRY.keys())


def get_instrument(name: str):
    if name not in REGISTRY:
        raise KeyError(f"Unknown instrument: {name}")
    return REGISTRY[name]()