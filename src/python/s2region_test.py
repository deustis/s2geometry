"""Tests for S2Region base class pybind11 bindings."""

import math
import unittest
import s2geometry_pybind as s2


class TestS2RegionInheritance(unittest.TestCase):

    # --- isinstance checks ---

    def test_s2cap_is_s2region(self):
        cap = s2.S2Cap.from_point(s2.S2Point(1.0, 0.0, 0.0))
        self.assertIsInstance(cap, s2.S2Region)

    def test_s2cell_is_s2region(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        self.assertIsInstance(cell, s2.S2Region)

    def test_s2latlng_rect_is_s2region(self):
        rect = s2.S2LatLngRect.full()
        self.assertIsInstance(rect, s2.S2Region)


class TestS2RegionCapBound(unittest.TestCase):

    def test_cap_bound_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(10.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        bound = region.cap_bound()
        self.assertIsInstance(bound, s2.S2Cap)
        self.assertTrue(bound.contains_point(center))

    def test_cap_bound_from_cell(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        region: s2.S2Region = cell
        bound = region.cap_bound()
        self.assertIsInstance(bound, s2.S2Cap)
        self.assertTrue(bound.contains_point(cell.center()))

    def test_cap_bound_from_rect(self):
        rect = s2.S2LatLngRect.from_point(
            s2.S2LatLng.from_degrees(0.0, 0.0))
        region: s2.S2Region = rect
        bound = region.cap_bound()
        self.assertIsInstance(bound, s2.S2Cap)


class TestS2RegionRectBound(unittest.TestCase):

    def test_rect_bound_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(10.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        bound = region.rect_bound()
        self.assertIsInstance(bound, s2.S2LatLngRect)
        self.assertFalse(bound.is_empty())

    def test_rect_bound_from_cell(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        region: s2.S2Region = cell
        bound = region.rect_bound()
        self.assertIsInstance(bound, s2.S2LatLngRect)
        self.assertTrue(bound.contains_point(cell.center()))

    def test_rect_bound_from_rect(self):
        rect = s2.S2LatLngRect.full()
        region: s2.S2Region = rect
        bound = region.rect_bound()
        self.assertIsInstance(bound, s2.S2LatLngRect)
        self.assertTrue(bound.is_full())


class TestS2RegionCellUnionBound(unittest.TestCase):

    def test_cell_union_bound_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(1.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        cell_ids = region.cell_union_bound()
        self.assertIsInstance(cell_ids, list)
        self.assertGreater(len(cell_ids), 0)
        for cid in cell_ids:
            self.assertIsInstance(cid, s2.S2CellId)

    def test_cell_union_bound_from_cell(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        region: s2.S2Region = cell
        cell_ids = region.cell_union_bound()
        self.assertIsInstance(cell_ids, list)
        self.assertGreater(len(cell_ids), 0)

    def test_cell_union_bound_from_rect(self):
        rect = s2.S2LatLngRect.from_point(
            s2.S2LatLng.from_degrees(45.0, 45.0))
        region: s2.S2Region = rect
        cell_ids = region.cell_union_bound()
        self.assertIsInstance(cell_ids, list)
        self.assertGreater(len(cell_ids), 0)


class TestS2RegionContainsCell(unittest.TestCase):

    def test_contains_cell_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(90.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        leaf_cell = s2.S2Cell(s2.S2CellId.from_face(0).child(0).child(0).child(0))
        self.assertTrue(region.contains_cell(leaf_cell))

    def test_contains_cell_from_rect(self):
        rect = s2.S2LatLngRect.full()
        region: s2.S2Region = rect
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        self.assertTrue(region.contains_cell(cell))

    def test_not_contains_cell_from_empty_cap(self):
        cap = s2.S2Cap()
        region: s2.S2Region = cap
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        self.assertFalse(region.contains_cell(cell))


class TestS2RegionMayIntersect(unittest.TestCase):

    def test_may_intersect_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(10.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        nearby_cell = s2.S2Cell(s2.S2CellId.from_face(0))
        self.assertTrue(region.may_intersect(nearby_cell))

    def test_may_intersect_from_cell(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        region: s2.S2Region = cell
        self.assertTrue(region.may_intersect(cell))

    def test_may_intersect_from_rect(self):
        rect = s2.S2LatLngRect.full()
        region: s2.S2Region = rect
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        self.assertTrue(region.may_intersect(cell))


class TestS2RegionContainsPoint(unittest.TestCase):

    def test_contains_point_from_cap(self):
        center = s2.S2Point(1.0, 0.0, 0.0)
        radius = s2.S1Angle.from_degrees(10.0)
        cap = s2.S2Cap(center, radius)
        region: s2.S2Region = cap
        self.assertTrue(region.contains_point(center))

    def test_contains_point_from_cell(self):
        cell = s2.S2Cell(s2.S2CellId.from_face(0))
        region: s2.S2Region = cell
        self.assertTrue(region.contains_point(cell.center()))

    def test_contains_point_from_rect(self):
        rect = s2.S2LatLngRect.full()
        region: s2.S2Region = rect
        p = s2.S2Point(1.0, 0.0, 0.0)
        self.assertTrue(region.contains_point(p))


if __name__ == "__main__":
    unittest.main()
