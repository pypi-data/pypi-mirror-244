import unittest
from typeunions import typeunion


@typeunion
class MyUnion:
    RED:(str)
    GREEN:(str, int)
    BLUE:{'a': str, 'b': int}
    WHITE:()
    BLACK:{}

    def get_int(self) -> int:
        match self:
            case MyUnion.RED(_): return -1
            case MyUnion.GREEN(_, b): return b
            case MyUnion.BLUE(_, b): return b
            case MyUnion.WHITE: return -2
            case MyUnion.BLACK: return -3
            case _: raise TypeError(f"{self} does not exists")

class TestTypeUnion(unittest.TestCase):

    LIST_COLOR = [
        MyUnion.RED("Red"),
        MyUnion.GREEN("Green", 1),
        MyUnion.BLUE("Blue", 2),
        MyUnion.WHITE,
        MyUnion.BLACK
    ]

    def test_inheritance(self):
        for color in TestTypeUnion.LIST_COLOR:
            self.assertIsInstance(color, MyUnion)

    def test_equality(self):

        self.assertNotEqual(MyUnion.RED("Red"), MyUnion.GREEN("Green", 1))
        self.assertNotEqual(MyUnion.WHITE, MyUnion.BLACK)

        self.assertEqual(MyUnion.WHITE, MyUnion.WHITE)
        self.assertEqual(MyUnion.BLUE("Blue", 2), MyUnion.BLUE("Blue", 2))

    def test_match_case(self):

        def match_case(color: MyUnion):
            match color:
                case MyUnion.RED(a):
                    self.assertEqual(a, "Red")
                case MyUnion.GREEN(a, b):
                    self.assertEqual(a, "Green")
                    self.assertEqual(b, 1)
                case MyUnion.BLUE(a, b):
                    self.assertEqual(a, "Blue")
                    self.assertEqual(b, 2)
                case MyUnion.WHITE:
                    pass
                case MyUnion.BLACK:
                    pass
                case _:
                    raise self.failureException(f"{color} not found")


        for color in TestTypeUnion.LIST_COLOR:
            match_case(color)

    def test_match_case_2(self):
        expected = [ -1, 1, 2, -2, -3 ]
        actual = [color.get_int() for color in TestTypeUnion.LIST_COLOR]
        self.assertListEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
