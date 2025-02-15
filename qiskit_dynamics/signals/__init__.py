# -*- coding: utf-8 -*-

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

"""
========================================
Signals (:mod:`qiskit_dynamics.signals`)
========================================

.. currentmodule:: qiskit_dynamics.signals

Tools for constructing time-dependent signals in RHS :mod:`qiskit_dynamics.models`.

Signal Classes
==============

.. autosummary::
   :toctree: ../stubs/

   Signal
   DiscreteSignal
   SignalSum
   DiscreteSignalSum
   SignalList

Transfer Functions
==================

.. autosummary::
   :toctree: ../stubs/

   Convolution
"""

from .signals import Signal, DiscreteSignal, SignalSum, DiscreteSignalSum, SignalList
from .transfer_functions import Convolution, Sampler, IQMixer
