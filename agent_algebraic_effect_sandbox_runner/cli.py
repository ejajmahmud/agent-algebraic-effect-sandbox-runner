"""CLI for Algebraic Effect Sandbox Runner."""
import argparse
from .core import AlgebraicEffectRunner, Effect

def sample_workflow():
    data = yield Effect("READ_FILE", {"path": "settings.txt"})
    result = yield Effect("TRANSFORM", {"data": data})
    return f"Completed: {result}"

def main():
    parser = argparse.ArgumentParser(description="Algebraic Effect Sandbox Runner CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate effect handling and resumption")
    args = parser.parse_args()

    runner = AlgebraicEffectRunner()
    runner.register_handler("READ_FILE", lambda p: "hello effect world")
    runner.register_handler("TRANSFORM", lambda p: p["data"].upper())

    outcome = runner.run(sample_workflow())
    print(f"Runner Outcome: {outcome}")
    print(f"Effects Logged: {[e.effect_type for e in runner.effect_log]}")

if __name__ == "__main__":
    main()
