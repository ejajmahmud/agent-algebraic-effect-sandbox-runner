"""Core algebraic effect sandbox runner."""
from typing import Dict, Any, Callable, Generator

class Effect:
    def __init__(self, effect_type: str, payload: Dict[str, Any]):
        self.effect_type = effect_type
        self.payload = payload

class AlgebraicEffectRunner:
    def __init__(self):
        self.handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self.effect_log = []

    def register_handler(self, effect_type: str, handler: Callable[[Dict[str, Any]], Any]):
        self.handlers[effect_type] = handler

    def run(self, generator: Generator[Effect, Any, Any]) -> Any:
        resumption_val = None
        while True:
            try:
                effect = generator.send(resumption_val)
                self.effect_log.append(effect)
                if effect.effect_type not in self.handlers:
                    raise RuntimeError(f"Unhandled algebraic effect: {effect.effect_type}")
                resumption_val = self.handlers[effect.effect_type](effect.payload)
            except StopIteration as e:
                return e.value
