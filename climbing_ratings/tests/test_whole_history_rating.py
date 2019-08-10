"""Tests for the whole_history_rating module"""

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

import unittest
import numpy as np
import climbing_ratings.whole_history_rating as whole_history_rating
from climbing_ratings.tests.assertions import assert_close


class TestWholeHistoryRatingFunctions(unittest.TestCase):
    """Tests for functions in the whole_history_rating module"""

    def test_expand_to_slices(self):
        """Test expand_to_slices()"""
        slices = [(0, 2), (2, 5)]
        values = np.array([1., 10.])
        expanded = whole_history_rating.expand_to_slices(values, slices)
        self.assertSequenceEqual([1., 1., 10., 10., 10.], expanded.tolist())
        
    def test_make_route_ascents(self):
        """Test make_route_ascents()"""
        ascents_clean = [0, 0, 0, 0, 0]
        ascents_page_slices = [(0, 5)]
        ascents_route = [0, 1, 0, 1, 0]
        
        ascents = whole_history_rating.make_route_ascents(
            ascents_clean, ascents_page_slices, ascents_route)
        self.assertSequenceEqual([3., 2.], ascents.wins.tolist())
        self.assertSequenceEqual([(0, 3), (3, 5)], ascents.slices)
        self.assertSequenceEqual([0, 0, 0, 0, 0], ascents.adversary.tolist())


class TestWholeHistoryRating(unittest.TestCase):
    """Tests for the WholeHistoryRating class"""
    
    def setUp(self):
        np.seterr(all='raise')
        self.assert_close = assert_close.__get__(self, self.__class__)
        # 1 climber, 1 page, 3 routes at grade "1", all with 1 clean and 1
        # non-clean ascent.
        ascents_route = [0, 0, 1, 1, 2, 2]
        ascents_clean = np.array([1., 0., 1., 0., 1., 0.])
        ascents_page_slices = [(0, 6)]
        pages_climber_slices = [(0, 1)]
        routes_grade = [1., 1., 1.]
        pages_gap = np.array([0.])
        self.whr = whole_history_rating.WholeHistoryRating(
            ascents_route, ascents_clean, ascents_page_slices,
            pages_climber_slices, routes_grade, pages_gap)

    def test_initialization(self):
        """Test WholeHistoryRating initialization"""
        route_ratings = self.whr.route_ratings
        self.assert_close([1., 1., 1.], route_ratings, 'route_ratings')

        page_ratings = self.whr.page_ratings
        self.assert_close([1.], page_ratings, 'page_ratings')

    def test_update_page_ratings(self):
        """Test WholeHistoryRating.update_page_ratings"""
        self.whr.update_page_ratings()
        self.assert_close(
            [1., 1.], self.whr.page_ratings, 'page_ratings')

    def test_update_route_ratings(self):
        """Test WholeHistoryRating.update_route_ratings"""
        self.whr.update_route_ratings()
        # Ratings should not change: both ascents had a 50% probability assuming
        # the initial ratings.
        self.assert_close(
            [1., 1., 1.], self.whr.route_ratings, 'route_ratings')