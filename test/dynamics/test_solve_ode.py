# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# pylint: disable=invalid-name,broad-except

"""Tests for solve_ode."""

import numpy as np
from scipy.linalg import expm

from qiskit import QiskitError
from qiskit_dynamics import solve_ode
from qiskit_dynamics.models import GeneratorModel
from qiskit_dynamics.signals import Signal
from qiskit_dynamics.dispatch import Array

from .common import QiskitDynamicsTestCase, TestJaxBase


class Testsolve_ode_exceptions(QiskitDynamicsTestCase):
    """Test exceptions of solve_ode."""

    def test_method_does_not_exist(self):
        """Test method does not exist exception."""

        try:
            solve_ode(lambda t, y: y, t_span=[0.0, 1.0], y0=np.array([1.0]), method="notamethod")
        except QiskitError as qe:
            self.assertTrue("not a supported ODE method" in str(qe))


# pylint: disable=too-many-instance-attributes
class Testsolve_ode_Base(QiskitDynamicsTestCase):
    """Some reusable routines for testing basic solving functionality."""

    def setUp(self):
        self.t_span = [0.0, 1.0]
        self.y0 = Array(np.eye(2, dtype=complex))

        self.X = Array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        self.Y = Array([[0.0, -1j], [1j, 0.0]], dtype=complex)
        self.Z = Array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

        # simple generator and rhs
        # pylint: disable=unused-argument
        def generator(t):
            return -1j * 2 * np.pi * self.X / 2

        def rhs(t, y):
            return generator(t) @ y

        self.basic_generator = generator
        self.basic_rhs = rhs

        # define simple model
        self.w = 2.0
        self.r = 0.1
        signals = [self.w, Signal(lambda t: 1.0, self.w)]
        operators = [-1j * 2 * np.pi * self.Z / 2, -1j * 2 * np.pi * self.r * self.X / 2]
        self.basic_model = GeneratorModel(operators=operators, signals=signals)

    def test_solve_ode_w_GeneratorModel(self):
        """Test solve on a GeneratorModel."""

        results = solve_ode(
            self.basic_model,
            y0=Array([0.0, 1.0], dtype=complex),
            t_span=[0, 1 / self.r],
            rtol=1e-9,
            atol=1e-9,
        )
        yf = results.y[-1]

        self.assertTrue(np.abs(yf[0]) ** 2 > 0.999)

    def _variable_step_method_standard_tests(self, method):
        """tests to run on a variable step solver."""

        results = solve_ode(
            self.basic_rhs, t_span=self.t_span, y0=self.y0, method=method, atol=1e-10, rtol=1e-10
        )

        expected = expm(-1j * np.pi * self.X.data)

        self.assertAllClose(results.y[-1], expected)

        # pylint: disable=unused-argument
        def quad_rhs(t, y):
            return Array([t ** 2], dtype=float)

        results = solve_ode(
            quad_rhs, t_span=[0.0, 1.0], y0=Array([0.0]), method=method, atol=1e-10, rtol=1e-10
        )
        expected = Array([1.0 / 3])
        self.assertAllClose(results.y[-1], expected)


class Testsolve_ode_numpy(Testsolve_ode_Base):
    """Basic tests for `numpy`-based ODE solver methods."""

    def test_standard_problems_solve_ivp(self):
        """Run standard tests for variable step methods in `solve_ivp`."""

        self._variable_step_method_standard_tests("RK45")
        self._variable_step_method_standard_tests("RK23")
        self._variable_step_method_standard_tests("BDF")
        self._variable_step_method_standard_tests("DOP853")


class Testsolve_ode_jax(Testsolve_ode_Base, TestJaxBase):
    """Basic tests for jax ODE solvers."""

    def test_standard_problems_jax(self):
        """Run standard tests for variable step `jax` methods."""
        self._variable_step_method_standard_tests("jax_odeint")
