import unittest
from geometry import Vector, Segment, Line, Polygon, Circle


# https://onlinejudge.u-aizu.ac.jp/courses/library/4/CGL/all のサンプルケースのチェック.
# 5_A, 6_A, 7_G は未対応.
class TestBasicGeometry(unittest.TestCase):
    def test_1_A_Projection(self):
        l1 = Line(Vector(0, 0), Vector(3, 4))
        self.assertEqual(l1.projection(Vector(2, 5)), Vector(3.12, 4.16))
        l2 = Line(Vector(0, 0), Vector(2, 0))
        self.assertEqual(l2.projection(Vector(-1, 1)), Vector(-1, 0))
        self.assertEqual(l2.projection(Vector(0, 1)), Vector(0, 0))
        self.assertEqual(l2.projection(Vector(1, 1)), Vector(1, 0))

    def test_1_B_Reflection(self):
        l1 = Line(Vector(0, 0), Vector(3, 4))
        self.assertEqual(l1.reflection(Vector(2, 5)), Vector(4.24, 3.32))
        self.assertEqual(l1.reflection(Vector(1, 4)), Vector(3.56, 2.08))
        self.assertEqual(l1.reflection(Vector(0, 3)), Vector(2.88, 0.84))
        l2 = Line(Vector(0, 0), Vector(2, 0))
        self.assertEqual(l2.reflection(Vector(-1, 1)), Vector(-1, -1))
        self.assertEqual(l2.reflection(Vector(0, 1)), Vector(0, -1))
        self.assertEqual(l2.reflection(Vector(1, 1)), Vector(1, -1))

    def test_1_C_CounterClockWise(self):
        v1 = Vector(2, 0)
        self.assertEqual(v1.ccw(Vector(-1, 1)), 1)
        self.assertEqual(v1.ccw(Vector(-1, -1)), -1)
        self.assertEqual(v1.ccw(Vector(-1, 0)), 0)
        self.assertEqual(v1.ccw(Vector(0, 0)), 0)
        self.assertEqual(v1.ccw(Vector(3, 0)), 0)

    def test_2_A_Parallel_Orthogonal(self):
        l = Line(Vector(0, 0), Vector(3, 0))
        self.assertEqual(l.is_parallel(Line(Vector(0, 2), Vector(3, 2))), True)
        self.assertEqual(l.is_orthogonal(Line(Vector(1, 1), Vector(1, 4))), True)
        self.assertEqual(l.is_parallel(Line(Vector(1, 1), Vector(2, 2))), False)
        self.assertEqual(l.is_orthogonal(Line(Vector(1, 1), Vector(2, 2))), False)

    def test_2_B_intersection(self):
        s = Segment(Vector(0, 0), Vector(3, 0))
        self.assertEqual(s.is_crossing(Segment(Vector(1, 1), Vector(2, -1))), True)
        self.assertEqual(s.is_crossing(Segment(Vector(3, 1), Vector(3, -1))), True)
        self.assertEqual(s.is_crossing(Segment(Vector(3, -2), Vector(5, 0))), False)

    def test_2_C_CrossPoint(self):
        self.assertEqual(
            Segment(Vector(0, 0), Vector(2, 0)).crossing_point(
                Segment(Vector(1, 1), Vector(1, -1))
            ),
            Vector(1, 0),
        )
        self.assertEqual(
            Segment(Vector(0, 0), Vector(1, 1)).crossing_point(
                Segment(Vector(0, 1), Vector(1, 0))
            ),
            Vector(0.5, 0.5),
        )
        self.assertEqual(
            Segment(Vector(0, 0), Vector(1, 1)).crossing_point(
                Segment(Vector(1, 0), Vector(0, 1))
            ),
            Vector(0.5, 0.5),
        )

    def test_2_D_Distance(self):
        self.assertAlmostEqual(
            Segment(Vector(0, 0), Vector(1, 0)).distance_to_segment(
                Segment(Vector(0, 1), Vector(1, 1))
            ),
            1,
        )
        self.assertAlmostEqual(
            Segment(Vector(0, 0), Vector(1, 0)).distance_to_segment(
                Segment(Vector(2, 1), Vector(1, 2))
            ),
            1.4142135624,
        )
        self.assertAlmostEqual(
            Segment(Vector(-1, 0), Vector(1, 0)).distance_to_segment(
                Segment(Vector(0, 1), Vector(0, -1))
            ),
            0,
        )

    def test_3_A_Area(self):
        p1 = Polygon([Vector(0, 0), Vector(2, 2), Vector(-1, 1)])
        self.assertAlmostEqual(p1.area(), 2)
        p2 = Polygon([Vector(0, 0), Vector(1, 1), Vector(1, 2), Vector(0, 2)])
        self.assertAlmostEqual(p2.area(), 1.5)

    def test_3_B_Is_Convex(self):
        p1 = Polygon([Vector(0, 0), Vector(3, 1), Vector(2, 3), Vector(0, 3)])
        self.assertEqual(p1.is_convex(), True)
        p2 = Polygon(
            [Vector(0, 0), Vector(2, 0), Vector(1, 1), Vector(2, 2), Vector(0, 2)]
        )
        self.assertEqual(p2.is_convex(), False)

    def test_3_C_Polygon_Point_Containment(self):
        p1 = Polygon([Vector(0, 0), Vector(3, 1), Vector(2, 3), Vector(0, 3)])
        self.assertEqual(p1.side_of_point(Vector(2, 1)), 1)
        self.assertEqual(p1.side_of_point(Vector(0, 2)), 0)
        self.assertEqual(p1.side_of_point(Vector(3, 2)), -1)

    def test_4_A_Convex_Hull(self):
        p = Polygon(
            [
                Vector(2, 1),
                Vector(0, 0),
                Vector(1, 2),
                Vector(2, 2),
                Vector(4, 2),
                Vector(1, 3),
                Vector(3, 3),
            ]
        )
        ch = Polygon(
            [Vector(0, 0), Vector(2, 1), Vector(4, 2), Vector(3, 3), Vector(1, 3)]
        )
        self.assertListEqual(p.convex_hull().points, ch.points)

    def test_4_B_Diameter_of_a_Convex_Polygon(self):
        p1 = Polygon([Vector(0, 0), Vector(4, 0), Vector(2, 2)])
        self.assertAlmostEqual(p1.diameter(), 4)
        p2 = Polygon([Vector(0, 0), Vector(1, 0), Vector(1, 1), Vector(0, 1)])
        self.assertAlmostEqual(p2.diameter(), 1.414213562373)

    def test_4_C_Convex_Cut(self):
        p = Polygon([Vector(1, 1), Vector(4, 1), Vector(4, 3), Vector(1, 3)])
        l1 = Line(Vector(2, 0), Vector(2, 4))
        self.assertAlmostEqual(p.convex_cut_with_line(l1).area(), 2)
        l2 = Line(Vector(2, 4), Vector(2, 0))
        self.assertAlmostEqual(p.convex_cut_with_line(l2).area(), 4)

    def test_5_A_Closest_Pair(self):
        pass

    def test_6_A_Manhattan_Geometry(self):
        pass

    def test_7_A_Intersection(self):
        self.assertEqual(
            Circle(Vector(1, 1), 1).side_of_aparting_circle(Circle(Vector(6, 2), 2)),
            -1,
        )
        self.assertEqual(
            Circle(Vector(1, 1), 1).side_of_touching_circle(Circle(Vector(6, 2), 2)), 0
        )
        self.assertEqual(
            Circle(Vector(1, 2), 1).side_of_aparting_circle(Circle(Vector(4, 2), 2)), 0
        )
        self.assertEqual(
            Circle(Vector(1, 2), 1).side_of_touching_circle(Circle(Vector(4, 2), 2)), -1
        )
        self.assertEqual(
            Circle(Vector(1, 2), 1).side_of_aparting_circle(Circle(Vector(3, 2), 2)), 0
        )
        self.assertEqual(
            Circle(Vector(1, 2), 1).side_of_touching_circle(Circle(Vector(3, 2), 2)), 0
        )
        self.assertEqual(
            Circle(Vector(0, 0), 1).side_of_aparting_circle(Circle(Vector(1, 0), 2)), 0
        )
        self.assertEqual(
            Circle(Vector(0, 0), 1).side_of_touching_circle(Circle(Vector(1, 0), 2)), 1
        )
        self.assertEqual(
            Circle(Vector(0, 0), 1).side_of_aparting_circle(Circle(Vector(0, 0), 2)), 1
        )
        self.assertEqual(
            Circle(Vector(0, 0), 1).side_of_touching_circle(Circle(Vector(0, 0), 2)), 0
        )

    def test_7_B_Incircle_of_a_Triangle(self):
        p1 = Vector(1, -2)
        p2 = Vector(3, 2)
        p3 = Vector(-2, 0)
        l1 = Line(p1, p1 + ((p2 - p1).unit_vector() + (p3 - p1).unit_vector()) / 2)
        l2 = Line(p2, p2 + ((p1 - p2).unit_vector() + (p3 - p2).unit_vector()) / 2)
        center = l1.crossing_point(l2)
        self.assertEqual(
            center, Vector(0.53907943898209422325, -0.26437392711448356856)
        )
        self.assertAlmostEqual(
            Line(p1, p2).distance_to_point(center), 1.18845545916395465278
        )

        p1 = Vector(0, 3)
        p2 = Vector(4, 0)
        p3 = Vector(0, 0)
        l1 = Line(p1, p1 + ((p2 - p1).unit_vector() + (p3 - p1).unit_vector()) / 2)
        l2 = Line(p2, p2 + ((p1 - p2).unit_vector() + (p3 - p2).unit_vector()) / 2)
        center = l1.crossing_point(l2)
        self.assertEqual(center, Vector(1, 1))
        self.assertAlmostEqual(Line(p1, p2).distance_to_point(center), 1)

    def test_7_C_Circumcircle_of_a_Triangle(self):
        p1 = Vector(1, -2)
        p2 = Vector(3, 2)
        p3 = Vector(-2, 0)
        center = Segment(p1, p2).bisecter().crossing_point(Segment(p2, p3).bisecter())
        self.assertEqual(center, Vector(0.625, 0.6875))
        self.assertAlmostEqual(abs(center - p1), 2.71353666826155124291)

        p1 = Vector(0, 3)
        p2 = Vector(4, 0)
        p3 = Vector(0, 0)
        center = Segment(p1, p2).bisecter().crossing_point(Segment(p2, p3).bisecter())
        self.assertEqual(center, Vector(2, 1.5))
        self.assertAlmostEqual(abs(center - p1), 2.5)

    def test_7_D_CrossPoint_of_Cirle_and_Line(self):
        c = Circle(Vector(2, 1), 1)
        p1, p2 = c.crossing_points_with_line(Line(Vector(0, 1), Vector(4, 1)))
        self.assertTrue(
            (p1 == Vector(3, 1) and p2 == Vector(1, 1))
            or (p1 == Vector(1, 1) and p2 == Vector(3, 1))
        )
        p3 = c.crossing_points_with_line(Line(Vector(3, 0), Vector(3, 3)))[0]
        self.assertEqual(p3, Vector(3, 1))

    def test_7_E_CrossPoint_of_Circles(self):
        c = Circle(Vector(0, 0), 2)
        c1 = Circle(Vector(2, 0), 2)
        p1, p2 = c.crossing_points_with_circle(c1)
        self.assertTrue(
            (p1 == Vector(1, -1.73205080) and p2 == Vector(1, 1.73205080))
            or (p1 == Vector(1, 1.73205080) and p2 == Vector(1, -1.73205080))
        )
        c2 = Circle(Vector(0, 3), 1)
        p3 = c.crossing_points_with_circle(c2)[0]
        self.assertEqual(p3, Vector(0, 2))

    def test_7_F_Tangent_to_Circle(self):
        p = Vector(0, 0)
        c = Circle(Vector(2, 2), 2)
        p1, p2 = c.touching_points_with_tangent(p)
        self.assertTrue(
            (p1 == Vector(0, 2) and p2 == Vector(2, 0))
            or (p1 == Vector(2, 0) and p2 == Vector(0, 2))
        )

        p = Vector(-3, 0)
        c = Circle(Vector(2, 2), 2)
        p1, p2 = c.touching_points_with_tangent(p)
        self.assertTrue(
            (p1 == Vector(0.6206896552, 3.4482758621) and p2 == Vector(2, 0))
            or (p1 == Vector(2, 0) and p2 == Vector(0.6206896552, 3.4482758621))
        )

    def test_7_G_Common_Tangent(self):
        pass

    def test_7_H_Intersection_of_Circle_and_Polygon(self):
        c = Circle(Vector(0, 0), 5)
        p1 = Polygon([Vector(1, 1), Vector(4, 1), Vector(5, 5)])
        self.assertAlmostEqual(c.area_common_with_polygon(p1), 4.639858417607)
        self.assertAlmostEqual(p1.area_common_with_circle(c), 4.639858417607)
        p2 = Polygon([Vector(0, 0), Vector(-3, -6), Vector(1, -3), Vector(5, -4)])
        self.assertAlmostEqual(c.area_common_with_polygon(p2), 11.787686807576)
        self.assertAlmostEqual(p2.area_common_with_circle(c), 11.787686807576)

    def test_7_I_Intersection_of_Circles(self):
        c1 = Circle(Vector(0, 0), 1)
        c2 = Circle(Vector(2, 0), 2)
        self.assertAlmostEqual(c1.area_common_with_circle(c2), 1.40306643968573875104)
        self.assertAlmostEqual(c2.area_common_with_circle(c1), 1.40306643968573875104)

        c1 = Circle(Vector(1, 0), 1)
        c2 = Circle(Vector(0, 0), 3)
        self.assertAlmostEqual(c1.area_common_with_circle(c2), 3.14159265358979311600)
        self.assertAlmostEqual(c2.area_common_with_circle(c1), 3.14159265358979311600)


if __name__ == "__main__":
    unittest.main()
