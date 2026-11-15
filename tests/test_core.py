"""Automated test suite for Algebraic Effect Sandbox Runner."""
import unittest
from agent_algebraic_effect_sandbox_runner.core import AlgebraicEffectRunner, Effect

class TestAlgebraicEffectRunner(unittest.TestCase):
    def test_effect_handling_and_resumption(self):
        def flow():
            val = yield Effect("ADD_TEN", {"num": 5})
            return val * 2

        runner = AlgebraicEffectRunner()
        runner.register_handler("ADD_TEN", lambda p: p["num"] + 10)
        res = runner.run(flow())
        self.assertEqual(res, 30)
        self.assertEqual(len(runner.effect_log), 1)

    def test_unhandled_effect_raises(self):
        def flow():
            yield Effect("UNKNOWN", {})

        runner = AlgebraicEffectRunner()
        with self.assertRaises(RuntimeError):
            runner.run(flow())
