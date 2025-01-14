from typing import Union
from collections import deque
from math import atan2, cos, pi, sin

EPS = 1e-8  # 許容誤差
DIGITS = 10  # 出力で表示する桁数


def equal(a, b):
    return abs(a - b) < EPS


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> "Point":
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other) -> "Point":
        assert other != 0, "division by zero"
        return Point(self.x / other, self.y / other)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other: "Point") -> bool:
        return equal(self.x, other.x) and equal(self.y, other.y)

    def __ne__(self, other: "Point") -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return f"{self.x:.{DIGITS}f} {self.y:.{DIGITS}f}"

    def format(self) -> str:
        return f"({self.x:.{DIGITS}f}, {self.y:.{DIGITS}f})"

    def dot(self, other: "Point") -> float:
        """内積

        Args:
            other (Point): 演算対象

        Returns:
            float: 計算結果
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Point") -> float:
        """外積

        Args:
            other (Point): 演算対象

        Returns:
            float: 計算結果
        """
        return self.x * other.y - self.y * other.x

    def move(self, dx, dy) -> "Point":
        """平行移動

        Args:
            dx (float): x軸方向の移動量
            dy (float): y軸方向の移動量

        Returns:
            Point: 移動後の座標
        """
        return Point(self.x + dx, self.y + dy)

    def rotate(self, theta, origin: "Point" = None) -> "Point":
        """回転移動

        Args:
            theta (float): 回転する角度（ラジアン）
            origin (Point, optional): 原点. Defaults to (0, 0).

        Returns:
            Point: 移動後の座標
        """
        if origin is None:
            origin = Point(0, 0)
        relative = self - origin
        return origin + Point(
            relative.x * cos(theta) - relative.y * sin(theta),
            relative.x * sin(theta) + relative.y * cos(theta),
        )

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def ccw(self, other: "Point") -> int:
        """回転方向を判定

        Args:
            other (Point): もう片方の点

        Returns:
            int: (self から見て other が) 1: 反時計回り, -1: 時計回り, 0: 直線上
        """
        if equal(self.cross(other), 0):
            return 0
        elif self.cross(other) < 0:
            return -1
        else:
            return 1

    def unit_vector(self) -> "Point":
        """単位ベクトルを取得

        Returns:
            Point: 同じ方向の単位ベクトル
        """
        if equal(abs(self), 0):
            return Point(0, 0)
        return self / abs(self)


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        assert p1 != p2, "p1 and p2 must be different"
        self.p1 = p1.copy()
        self.p2 = p2.copy()

    def __str__(self) -> str:
        return f"{self.p1} {self.p2}"

    def format(self) -> str:
        return f"{self.p1.format()} -- {self.p2.format()}"

    def slope(self) -> float:
        """傾き

        Returns:
            float: 直線の傾き, y軸に平行な場合は inf
        """
        if equal(self.p1.x, self.p2.x):
            return float("inf")
        else:
            return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    def projection(self, p: Point) -> Point:
        """射影

        Args:
            p (Point): もとの座標

        Returns:
            Point: 移動後の座標
        """
        base = self.p2 - self.p1
        return self.p1 + base * (p - self.p1).dot(base) / abs(base) ** 2

    def reflection(self, p: Point) -> Point:
        """反射

        Args:
            p (Point): もとの座標

        Returns:
            Point: 反射後の座標
        """
        return p + (self.projection(p) - p) * 2

    def is_parallel(self, other: "Line") -> bool:
        """平行かどうか判定

        Args:
            other (Line): 比較対象の直線

        Returns:
            bool: True: 平行, False: 平行でない
        """
        return equal((self.p2 - self.p1).cross(other.p2 - other.p1), 0)

    def is_orthogonal(self, other: "Line") -> bool:
        """垂直かどうか判定

        Args:
            other (Line): 比較対象の直線

        Returns:
            bool: True: 垂直, False: 垂直でない
        """
        return equal((self.p2 - self.p1).dot(other.p2 - other.p1), 0)

    def is_including_point(self, p: Point) -> bool:
        """直線上に点 p が存在するかどうか

        Args:
            p (Point): 判定対象の点

        Returns:
            bool: True: 直線上に存在, False: 直線上に存在しない
        """
        if self.p1 == p or self.p2 == p:
            return True
        return (self.p2 - self.p1).ccw(p - self.p1) == 0

    def is_crossing(self, other: Union["Line", "Segment"]) -> bool:
        """直線の交差判定

        Args:
            other (Line | Segment): 判定対象の直線または線分

        Returns:
            bool: True: 交差, False: 交差しない
        """
        if type(other) == Line:
            return self._is_crossing_line(other)
        if type(other) == Segment:
            return self._is_crossing_segment(other)
        raise ValueError("invalid type")

    def _is_crossing_line(self, other: "Line") -> bool:
        if self.is_including_point(other.p1):
            return True
        return not self.is_parallel(other)

    def _is_crossing_segment(self, other: "Segment") -> bool:
        if self.is_including_point(other.p1) or self.is_including_point(other.p2):
            return True
        ccw1 = (self.p2 - self.p1).ccw(other.p1 - self.p1)
        ccw2 = (self.p2 - self.p1).ccw(other.p2 - self.p1)
        return ccw1 * ccw2 < 0

    def crossing_point(self, other: Union["Line", "Segment"]) -> Union[Point, None]:
        """他の直線との交点

        Args:
            other (Line | Segment): 対象の直線または線分

        Returns:
            Point | None: 交点の座標. 交差しない場合は None. 平行な場合も None
        """
        if self.is_parallel(other) or not self.is_crossing(other):
            return None
        d1 = (self.p2 - self.p1).cross(other.p2 - other.p1)
        d2 = (self.p2 - self.p1).cross(self.p2 - other.p1)
        if equal(d1, 0) and equal(d2, 0):
            return other.p1
        return other.p1 + (other.p2 - other.p1) * (d2 / d1)

    def distance_to_point(self, p: Point) -> float:
        """直線と点の距離

        Args:
            p (Point): 対象の点

        Returns:
            float: 距離
        """
        projection = self.projection(p)
        return abs(p - projection)


class Segment(Line):
    def __init__(self, p1: Point, p2: Point) -> None:
        super().__init__(p1, p2)

    def __abs__(self) -> float:
        return abs(self.p2 - self.p1)

    def bisecter(self) -> "Line":
        """垂直二等分線

        Returns:
            Line: 計算結果の直線
        """
        center = (self.p1 + self.p2) / 2
        p1 = self.p1.rotate(pi / 2, center)
        p2 = self.p2.rotate(pi / 2, center)
        return Line(p1, p2)

    def is_including_point(self, p: Point) -> bool:
        """線分上に点 p が存在するかどうか

        Args:
            p (Point): 判定対象の点

        Returns:
            bool: True: 線分上に存在, False: 線分上に存在しない
        """
        ref = (self.p2 - self.p1).dot(p - self.p1) / abs(self)
        between = equal(ref, 0) or equal(ref, abs(self)) or 0 < ref < abs(self)
        return super().is_including_point(p) and between

    def is_crossing(self, other: Union["Line", "Segment"]) -> bool:
        """線分の交差判定

        Args:
            other (Line | Segment): 判定対象の直線または線分

        Returns:
            bool: True: 交差, False: 交差しない
        """
        if type(other) == Line:
            return self._is_crossing_line(other)
        if type(other) == Segment:
            return self._is_crossing_segment(other)
        raise ValueError("invalid type")

    def _is_crossing_line(self, other: "Line") -> bool:
        return other._is_crossing_line(self)

    def _is_crossing_segment(self, other: "Segment") -> bool:
        if (
            self.is_including_point(other.p1)
            or self.is_including_point(other.p2)
            or other.is_including_point(self.p1)
            or other.is_including_point(self.p2)
        ):
            return True

        ccw1 = (self.p2 - self.p1).ccw(other.p1 - self.p1)
        ccw2 = (self.p2 - self.p1).ccw(other.p2 - self.p1)
        ccw3 = (other.p2 - other.p1).ccw(self.p1 - other.p1)
        ccw4 = (other.p2 - other.p1).ccw(self.p2 - other.p1)
        return ccw1 != ccw2 and ccw3 != ccw4

    def distance_to_point(self, p: Point) -> float:
        """線分と点の距離

        Args:
            p (Point): 対象の点

        Returns:
            float: 距離
        """
        projection = self.projection(p)
        if self.is_including_point(projection):
            return abs(p - projection)
        return min(abs(self.p1 - p), abs(self.p2 - p))

    def distance_to_segment(self, other: "Segment") -> float:
        """線分と線分の距離

        Args:
            other (Segment): 対象の線分

        Returns:
            float: 最も近い2点の距離
        """
        if self.is_crossing(other):
            return 0
        return min(
            self.distance_to_point(other.p1),
            self.distance_to_point(other.p2),
            other.distance_to_point(self.p1),
            other.distance_to_point(self.p2),
        )


class Polygon:
    def __init__(self, points: list[Point]) -> None:
        """自己交差を含まない多角形

        Args:
            points (list[Point]): 頂点を反時計回りに追加したリスト
        """
        self.points = [points[0].copy()]
        for p in points[1:]:
            if self.points[-1] != p:
                self.points.append(p.copy())
        self.n = len(self.points)

    def __str__(self) -> str:
        return "\n".join([str(p) for p in self.points])

    def format(self) -> str:
        return " -> ".join([p.format() for p in self.points])

    def area(self) -> float:
        """多角形内部の面積. O(self.n)

        Returns:
            float: 面積
        """
        area = 0
        for i in range(self.n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % self.n]
            area += p1.cross(p2) / 2
        return abs(area)

    def is_convex(self) -> bool:
        """凸多角形かどうか判定. O(self.n)

        Returns:
            bool: True: 凸多角形, False: 凹多角形. 3点が一直線上にある場合も True
        """
        top = 0
        bottom = 0
        for i in range(self.n):
            a = self.points[i]
            b = self.points[(i + 1) % self.n]
            c = self.points[(i + 2) % self.n]
            top = max(top, (b - a).ccw(c - b))
            bottom = min(bottom, (b - a).ccw(c - b))
        return not (top == 1 and bottom == -1)

    def side_of_point(self, p: Point) -> int:
        """多角形と点の位置関係を判定. O(self.n)

        Args:
            p (Point): 判定対象の点

        Returns:
            int: 1: 内部, 0: 線上, -1: 外部
        """

        theta = 0  # p の周りを何度周回するか
        for i in range(self.n):
            a = self.points[i]
            b = self.points[(i + 1) % self.n]
            if Segment(a, b).is_including_point(p):
                return 0
            theta += atan2((a - p).cross(b - p), (a - p).dot(b - p))
        return -1 if -pi < theta < pi else 1

    def convex_hull(self) -> "Polygon":
        """現在 self に含まれている点から構成される凸包を返す. O(self.n)

        Returns:
            Polygon: 生成された凸包
        """
        points = self.points
        points.sort(key=lambda p: (p.y, p.x))

        if self.n <= 2:
            return Polygon(points)
        elif self.n == 3:
            if (points[1] - points[0]).ccw(points[2] - points[0]) < 0:
                points = [points[0], points[2], points[1]]
            return Polygon(points)

        right = deque([points[0].copy(), points[1].copy()])
        for i in range(2, self.n):
            next = points[i].copy()
            curr = right.pop()
            prev = right.pop()
            while True:
                if (curr - prev).ccw(next - curr) >= 0:
                    right.append(prev)
                    right.append(curr)
                    break
                if len(right) == 0:
                    right.append(prev)
                    break
                curr = prev.copy()
                prev = right.pop()

            right.append(next)

        left = deque([points[self.n - 1].copy(), points[self.n - 2].copy()])
        for i in range(self.n - 2)[::-1]:
            next = points[i].copy()
            curr = left.pop()
            prev = left.pop()
            while True:
                if (curr - prev).ccw(next - curr) >= 0:
                    left.append(prev)
                    left.append(curr)
                    break
                if len(left) == 0:
                    left.append(prev)
                    break
                curr = prev.copy()
                prev = left.pop()

            left.append(next)

        right.pop()
        left.pop()
        return Polygon(list(right) + list(left))

    def diameter(self) -> float:
        """多角形の直径（最遠点対）. O(self.n)

        Returns:
            float: 直径
        """
        ch = self.convex_hull()
        if ch.n == 2:
            return abs(ch.points[0] - ch.points[1])
        i = j = 0
        for k in range(ch.n):
            if ch.points[k].x < ch.points[i].x:
                i = k
            if ch.points[k].x > ch.points[j].x:
                j = k
        res = 0
        si, sj = i, j
        while i != sj or j != si:
            res = max(res, abs(ch.points[i] - ch.points[j]))
            vi = ch.points[(i + 1) % ch.n] - ch.points[i]
            vj = ch.points[(j + 1) % ch.n] - ch.points[j]
            if vi.cross(vj) < 0:
                i = (i + 1) % ch.n
            else:
                j = (j + 1) % ch.n

        return res

    def convex_common(self, other: "Polygon") -> "Polygon":
        """凸多角形同士の共通部分. O(self.n * other.n)

        Args:
            other (Polygon): もう片方の凸多角形
        """
        ch_self = self.convex_hull()
        ch_other = other.convex_hull()

        points = []

        for p in ch_self.points:
            if ch_other.side_of_point(p) == 1:
                points.append(p)

        for p in ch_other.points:
            if ch_self.side_of_point(p) == 1:
                points.append(p)

        for i in range(ch_self.n):
            seg1 = Segment(ch_self.points[i], ch_self.points[(i + 1) % ch_self.n])
            for j in range(ch_other.n):
                seg2 = Segment(
                    ch_other.points[j], ch_other.points[(j + 1) % ch_other.n]
                )
                if seg1.is_crossing(seg2):
                    points.append(seg1.crossing_point(seg2))

        polygon = Polygon(points)
        return polygon.convex_hull()

    def convex_cut_with_line(self, other: Line) -> "Polygon":
        """凸多角形を直線で切断. O(self.n)

        Args:
            other (Line): 切断する直線

        Returns:
            Polygon: 切断後の反時計周り側の凸多角形
        """
        points = []
        for i in range(self.n):
            if (other.p2 - other.p1).ccw(self.points[i] - other.p1) != -1:
                points.append(self.points[i])
            seg = Segment(self.points[i], self.points[(i + 1) % self.n])
            if (self.points[i] - other.p1).ccw(other.p2 - other.p1) * (
                self.points[(i + 1) % self.n] - other.p1
            ).ccw(other.p2 - other.p1) < 0:
                points.append(seg.crossing_point(other))
        return Polygon(points).convex_hull()

    def area_common_with_circle(self, other: "Circle") -> float:
        """円と多角形の共通部分の面積

        Args:
            other (Circle): 対象の円

        Returns:
            float: 共通部分の面積
        """
        area = 0
        points = []
        for i in range(self.n):
            points.append(self.points[i])
            seg = Segment(self.points[i], self.points[(i + 1) % self.n])
            for p in other.crossing_points_with_line(seg):
                if seg.is_including_point(p) and p != seg.p1 and p != seg.p2:
                    points.append(p)
        for i in range(len(points)):
            seg = Segment(points[i], points[(i + 1) % len(points)])
            dot = (seg.p1 - other.center).dot(seg.p2 - other.center)
            cross = (seg.p1 - other.center).cross(seg.p2 - other.center)
            if other.side_of_point(seg.p1) == -1 or other.side_of_point(seg.p2) == -1:
                theta = atan2(cross, dot)
                area += other.radius**2 * theta / 2
            else:
                area += cross / 2
        return abs(area)


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        assert radius > 0, "radius must be positive"
        self.center = center.copy()
        self.radius = radius

    def __str__(self) -> str:
        return f"{self.center} {self.radius}"

    def format(self) -> str:
        return f"o: {self.center.format()}, r: {self.radius:.{DIGITS}f}"

    def area(self) -> float:
        """円の面積

        Returns:
            float: 面積
        """
        return pi * self.radius**2

    def side_of_point(self, p: Point) -> int:
        """円と点の位置関係を判定.

        Args:
            p (Point): 判定対象の点

        Returns:
            int: 1: 内部, 0: 線上, -1: 外部
        """
        dist = abs(self.center - p)
        if equal(dist, self.radius):
            return 0
        return 1 if dist < self.radius else -1

    def side_of_touching_circle(self, other: "Circle") -> int:
        """円が接している側を判定

        Args:
            other (Circle): もう片方の円

        Returns:
            int: 1: 内接, 0: 接しない, -1: 外接
        """
        if equal(abs(self.center - other.center), abs(self.radius - other.radius)):
            return 1
        elif equal(abs(self.center - other.center), self.radius + other.radius):
            return -1
        else:
            return 0

    def side_of_aparting_circle(self, other: "Circle") -> int:
        """円同士の関係を判定

        Args:
            other (Circle): もう片方の円

        Returns:
            int: 1: 内部, 0: 交点を1つ以上持つ, -1: 外部
        """
        if self.side_of_touching_circle(other):
            return 0
        elif abs(self.center - other.center) < abs(self.radius - other.radius):
            return 1
        elif self.radius + other.radius < abs(self.center - other.center):
            return -1
        else:
            return 0

    def crossing_points_with_circle(self, other: "Circle") -> list[Point]:
        """円と円の交点

        Args:
            other (Circle): 対象の円

        Returns:
            list[Point]: 0~2個の交点を含むリスト
        """
        if self.side_of_touching_circle(other) == 1:
            unit = (other.center - self.center).unit_vector()
            if self.radius > other.radius:
                return [self.center + unit * self.radius]
            else:
                return [other.center - unit * other.radius]
        elif self.side_of_touching_circle(other) == -1:
            unit = (other.center - self.center).unit_vector()
            return [self.center + unit * self.radius]
        elif self.side_of_aparting_circle(other) == 0:
            dist = abs(self.center - other.center)
            cosine = (self.radius**2 - other.radius**2 + dist**2) / (2 * dist)
            h = (self.radius**2 - cosine**2) ** 0.5
            unit = (other.center - self.center).unit_vector()
            p = self.center + unit * cosine
            return [p + unit.rotate(pi / 2) * h, p - unit.rotate(pi / 2) * h]
        else:
            return []

    def is_touching_line(self, other: Line) -> bool:
        """直線と円が接しているかどうかを判定

        Args:
            other (Line): 対象の直線

        Returns:
            bool: True: 接している, False: 接していない
        """
        return equal(other.distance_to_point(self.center), self.radius)

    def is_crossing_line(self, other: Line) -> bool:
        """直線と円が交わるかどうかを判定

        Args:
            other (Segment): 対象の直線

        Returns:
            bool: True: 1点以上で交わる, False: 交わらない
        """
        if self.is_touching_line(other):
            return True
        return other.distance_to_point(self.center) < self.radius

    def crossing_points_with_line(self, other: Line) -> list[Point]:
        """直線と円の交点

        Args:
            other (Segment): 対象の直線

        Returns:
            list[Point]: 0~2個の交点を含むリスト
        """
        if not self.is_touching_line(other) and not self.is_crossing_line(other):
            return []
        projection = other.projection(self.center)
        if self.is_touching_line(other):
            return [projection]
        dist = abs(projection - self.center)
        unit = (other.p2 - other.p1).unit_vector()
        d = (self.radius**2 - dist**2) ** 0.5
        return [projection - unit * d, projection + unit * d]

    def area_common_with_polygon(self, other: Polygon) -> float:
        """多角形との共通部分の面積

        Args:
            other (Polygon): 対象の多角形

        Returns:
            float: 共通部分の面積
        """
        return other.area_common_with_circle(self)

    def area_common_with_circle(self, other: "Circle") -> float:
        """円と円の共通部分の面積

        Args:
            other (Circle): 対象の円

        Returns:
            float: 共通部分の面積
        """
        if (
            self.side_of_aparting_circle(other) == 1
            or self.side_of_touching_circle(other) == 1
        ):
            return min(self.area(), other.area())
        elif (
            self.side_of_aparting_circle(other) == -1
            or self.side_of_touching_circle(other) == -1
        ):
            return 0
        else:
            p1, p2 = self.crossing_points_with_circle(other)
            theta1 = atan2(
                (p1 - self.center).cross(other.center - self.center),
                (p1 - self.center).dot(other.center - self.center),
            )
            theta2 = atan2(
                (p1 - other.center).cross(self.center - other.center),
                (p1 - other.center).dot(self.center - other.center),
            )
            arc1 = abs(self.radius**2 * theta1)
            arc2 = abs(other.radius**2 * theta2)
            tri1 = (p1 - self.center).cross(p2 - self.center) / 2
            tri2 = (p2 - other.center).cross(p1 - other.center) / 2
            return arc1 + arc2 + tri1 + tri2

    def touching_points_with_tangent(self, other: Point) -> list[Point]:
        """other を通る接線の接点

        Args:
            other (Point): 対象の点

        Returns:
            list[Point]: 接点のリスト
        """
        if self.side_of_point(other) == 1:
            return []
        elif self.side_of_point(other) == 0:
            return [other.copy()]
        else:
            radius = (abs(other - self.center) ** 2 - self.radius**2) ** 0.5
            return self.crossing_points_with_circle(Circle(other, radius))


class PillowManager:
    SIZE = 1000
    OFFSET = 0

    def __init__(self, bottom=0, top=500, axis=True, grid: int = None) -> None:
        """可視化用クラス

        Args:
            bottom (int, optional): 座標の最小値. 2軸で共通 Defaults to 0.
            top (int, optional): 座標の最大値. 2軸で共通. Defaults to 500.
            axis (bool, optional): x=0, y=0 を強調するかどうか. Defaults to True.
            grid (int, optional): 補助線の間隔. None なら表示なし. Defaults to None.
        """

        # コメントアウトのみで提出可能にするため，pillow は初期化時に import
        from PIL import Image, ImageDraw

        self.im = Image.new(
            "RGB",
            (self.SIZE + self.OFFSET * 2, self.SIZE + self.OFFSET * 2),
            (255, 255, 255),
        )
        self.draw = ImageDraw.Draw(self.im)
        self.bottom = bottom
        self.top = top
        axis and self._add_axis()
        (grid is not None) and self._add_grid(grid)

    def _check_point(self, p: Point) -> None:
        assert self.bottom <= p.x <= self.top, f"{p.x=} is out of range"
        assert self.bottom <= p.y <= self.top, f"{p.y=} is out of range"

    def _convert(self, p: Point) -> Point:
        magn = self.SIZE / (self.top - self.bottom)
        x = (p.x - self.bottom) * magn + self.OFFSET
        y = (p.y - self.bottom) * magn + self.OFFSET
        return Point(x, y)

    def _add_axis(self) -> None:
        axis_x = Segment(Point(self.bottom, 0), Point(self.top, 0))
        axis_y = Segment(Point(0, self.bottom), Point(0, self.top))
        self.draw_segment(axis_x, width=3, color=(200, 200, 200))
        self.draw_segment(axis_y, width=3, color=(200, 200, 200))

    def _add_grid(self, grid: int) -> None:
        for i in range(0, self.top + 1, grid):
            parallel_x = Segment(Point(i, self.bottom), Point(i, self.top))
            parallel_y = Segment(Point(self.bottom, i), Point(self.top, i))
            self.draw_segment(parallel_x, color=(200, 200, 200))
            self.draw_segment(parallel_y, color=(200, 200, 200))
        for i in range(0, self.bottom - 1, -grid):
            parallel_x = Segment(Point(i, self.bottom), Point(i, self.top))
            parallel_y = Segment(Point(self.bottom, i), Point(self.top, i))
            self.draw_segment(parallel_x, color=(200, 200, 200))
            self.draw_segment(parallel_y, color=(200, 200, 200))

    def draw_point(self, p: Point, size=None, color=(0, 0, 0)) -> None:
        if size is None:
            size = self.SIZE / 150
        center = self._convert(p)
        self.draw.ellipse(
            (center.x - size, center.y - size, center.x + size, center.y + size),
            fill=color,
        )

    def draw_line(self, line: Line, width=1, color=(0, 0, 0)) -> None:
        lb = Point(self.bottom, self.bottom)
        lt = Point(self.bottom, self.top)
        rb = Point(self.top, self.bottom)
        rt = Point(self.top, self.top)
        if -1 < line.slope() < 1:
            p1 = Line(lb, lt).crossing_point(line)
            p2 = Line(rt, rb).crossing_point(line)
        else:
            p1 = Line(lb, rb).crossing_point(line)
            p2 = Line(rt, lt).crossing_point(line)
        self.draw_segment(Segment(p1, p2), width, color)

    def draw_segment(self, segment: Segment, width=1, color=(0, 0, 0)) -> None:
        p1 = self._convert(segment.p1)
        p2 = self._convert(segment.p2)
        self.draw.line((p1.x, p1.y, p2.x, p2.y), fill=color, width=width)

    def draw_polygon(self, polygon: Polygon, width=1, color=(0, 0, 0)) -> None:
        for i in range(polygon.n):
            p1 = polygon.points[i]
            p2 = polygon.points[(i + 1) % polygon.n]
            self.draw_segment(Segment(p1, p2), width, color)

    def draw_circle(self, circle: Circle, color=(0, 0, 0)) -> None:
        lb = self._convert(circle.center - Point(circle.radius, circle.radius))
        rt = self._convert(circle.center + Point(circle.radius, circle.radius))
        self.draw.ellipse(
            (lb.x, lb.y, rt.x, rt.y),
            outline=color,
        )

    def save(self, path: str = "./pillow_image.jpg") -> None:
        from PIL import ImageOps

        ImageOps.flip(self.im).save(path, quality=95)
