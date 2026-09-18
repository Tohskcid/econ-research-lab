import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_proof_audit", ROOT / "scripts/check_proof_audit.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

audit_proof_content = MODULE.audit_proof_content


class ProofAuditTests(unittest.TestCase):
    def test_handwaving_detection(self):
        bad_text = r"""
        \begin{theorem}
        The equilibrium follows.
        \end{theorem}
        \begin{proof}
        Trivial algebra shows that \beta = 0. Clearly by inspection the result holds.
        \end{proof}
        """
        result = audit_proof_content(bad_text, "test_handwaving.tex")
        self.assertFalse(result["gate_passed"])
        self.assertEqual(result["checks"]["no_handwaving"]["status"], "fail")
        self.assertGreaterEqual(len(result["checks"]["no_handwaving"]["violations"]), 1)

    def test_missing_micro_macro_bridge(self):
        bad_text = r"""
        Suppose developer utility has Type I Extreme Value error:
        U_i = V_i + \xi_i, \quad \xi_i \sim \text{Gumbel}.
        The market choice probability is s_i = \exp(V_i) / \sum_k \exp(V_k).
        Aggregating gives the linear panel equation Y_{it} = \rho Y_{jt} + \beta T_{it} + \alpha_t + \varepsilon_{it}.
        """
        result = audit_proof_content(bad_text, "test_micro_macro.tex")
        self.assertFalse(result["gate_passed"])
        self.assertEqual(result["checks"]["micro_macro_bridge"]["status"], "fail")

    def test_missing_spatial_decay_rate(self):
        bad_text = r"""
        We consider the Spatial Durbin Model:
        Y = (I - \rho W)^{-1} [\beta T + \varepsilon].
        By the spatial central limit theorem of Jenish and Prucha (2012),
        the score converges to a normal distribution \mathcal{N}(0, \Omega).
        """
        result = audit_proof_content(bad_text, "test_spatial_decay.tex")
        self.assertFalse(result["gate_passed"])
        self.assertEqual(result["checks"]["spatial_decay_bound"]["status"], "fail")

    def test_missing_neyman_orthogonality_derivation(self):
        bad_text = r"""
        We apply Double Machine Learning with score \psi(W; \theta, \eta).
        The score is Neyman orthogonal, so the regularization bias is eliminated.
        """
        result = audit_proof_content(bad_text, "test_orthogonality.tex")
        self.assertFalse(result["gate_passed"])
        self.assertEqual(result["checks"]["neyman_orthogonality_derivation"]["status"], "fail")

    def test_fully_rigorous_proof_passes(self):
        good_text = r"""
        Under Type I Extreme Value Gumbel disturbances, choice probability is s_{it} = \frac{\exp(V_{it}/\sigma)}{\sum_k \exp(V_{kt}/\sigma)}.
        Following Berry (1994) log-odds normalization against reference county 0, the denominator partition function
        and inclusive value are strictly absorbed by time fixed effects \alpha_t.
        
        For the Spatial Durbin Model (I - \rho_0 W)^{-1}, the infinite Neumann expansion gives truncation error
        bounded by \|\psi - \mathbb{E}[\psi \mid \mathcal{F}_m]\| \le C |\rho_0|^m / (1 - |\rho_0|),
        establishing geometric decay of near-epoch dependence (NED).
        
        Evaluating the Gateaux directional derivative \left. \frac{d}{dr} \mathbb{E}[\psi(Z; \theta_0, \eta_0 + r(\eta - \eta_0))] \right|_{r=0},
        the law of iterated expectations yields zero identically.
        Therefore, by Jenish and Prucha (2012) spatial CLT, \sqrt{N}(\hat{\theta} - \theta_0) \xrightarrow{d} \mathcal{N}(0, J_0^{-1} \Omega_0 J_0^{-1}).
        """
        result = audit_proof_content(good_text, "good_proof.tex")
        self.assertTrue(result["gate_passed"])
        self.assertEqual(result["total_violations"], 0)


if __name__ == "__main__":
    unittest.main()
