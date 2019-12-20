"""Tests for the log_normal_distribution module"""

# Copyright 2019 Dean Scarff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import unittest
from ..log_normal_distribution import LogNormalDistribution
from .assertions import assert_close


class TestLogNormalDistribution(unittest.TestCase):
    """Tests for the LogNormalDistribution class"""

    def setUp(self):
        np.seterr(all="raise")
        self.assert_close = assert_close.__get__(self, self.__class__)

    def test_get_derivatives_var_1(self):
        """Test LogNormalDistribution(mu, 1).get_derivatives()"""
        mu = np.array([0.0, 1.0, 2.0])
        x = np.array([1.0, 1.0, 1.0])
        dist = LogNormalDistribution(mu, 1.0)
        d1, d2 = dist.get_derivatives(x)
        self.assert_close([0.0, 1.0, 2.0], d1, "d1")
        self.assert_close([-1.0, -1.0, -1.0], d2, "d2")

    def test_get_derivatives_var_2(self):
        """Test LogNormalDistribution(0, 2).get_derivatives()"""
        x = np.exp([0.0, 1.0, 2.0])
        dist = LogNormalDistribution(0.0, 2.0)
        d1, d2 = dist.get_derivatives(x)
        self.assert_close([0.0, -0.5, -1.0], d1, "d1")
        self.assert_close([-0.5, -0.5, -0.5], d2, "d2")
