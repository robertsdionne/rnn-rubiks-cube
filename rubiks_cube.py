import colorama
import enum

class Color(enum.Enum):
    white = 0
    red = 1
    blue = 2
    orange = 3
    green = 4
    yellow = 5

    def color(self):
        return COLORAMA_COLORS[self]

COLORAMA_COLORS = {
    Color.white: colorama.Fore.WHITE,
    Color.red: colorama.Fore.RED,
    Color.blue: colorama.Fore.BLUE,
    Color.orange: colorama.Fore.MAGENTA,
    Color.green: colorama.Fore.GREEN,
    Color.yellow: colorama.Fore.YELLOW,
}

#     012
#     345
#     678
#
#     UUU
#     UUU
#     UUU
# LLL FFF RRR BBB
# LLL FFF RRR BBB
# LLL FFF RRR BBB
#     DDD
#     DDD
#     DDD
class RubiksCube(object):

    def __init__(self, up=None, front=None, right=None, back=None, left=None, down=None):
        self.up = up if up else [[Color.white] * 3] * 3
        self.front = front if front else [[Color.red] * 3] * 3
        self.right = right if right else [[Color.blue] * 3] * 3
        self.back = back if back else [[Color.orange] * 3] * 3
        self.left = left if left else [[Color.green] * 3] * 3
        self.down = down if down else [[Color.yellow] * 3] * 3

    # X clockwise, x counterclockwise

    # 012    630
    # 345 -> 741
    # 678    852

    def U(self):
        return RubiksCube(
            up=self.__clockwise(self.up),
            front=[
                self.right[0],
                self.front[1],
                self.front[2],
            ],
            right=[
                self.back[0],
                self.right[1],
                self.right[2],
            ],
            back=[
                self.left[0],
                self.back[1],
                self.back[2],
            ],
            left=[
                self.front[0],
                self.left[1],
                self.left[2],
            ],
            down=self.down,
        )

    def u(self):
        return RubiksCube(
            up=self.__counterclockwise(self.up),
            front=[
                self.left[0],
                self.front[1],
                self.front[2],
            ],
            right=[
                self.front[0],
                self.right[1],
                self.right[2],
            ],
            back=[
                self.right[0],
                self.back[1],
                self.back[2],
            ],
            left=[
                self.back[0],
                self.left[1],
                self.left[2],
            ],
            down=self.down,
        )

    def F(self):
        return RubiksCube(
            up=[
                self.up[0],
                self.up[1],
                [self.left[2][2], self.left[1][2], self.left[0][2]],
            ],
            front=self.__clockwise(self.front),
            right=[
                [self.up[2][0], self.right[0][1], self.right[0][2]],
                [self.up[2][1], self.right[1][1], self.right[1][2]],
                [self.up[2][2], self.right[2][1], self.right[2][2]],
            ],
            back=self.back,
            left=[
                [self.left[0][0], self.left[0][1], self.down[0][0]],
                [self.left[1][0], self.left[1][1], self.down[0][1]],
                [self.left[2][0], self.left[2][1], self.down[0][2]],
            ],
            down=[
                [self.right[2][0], self.right[1][0], self.right[0][0]],
                self.down[1],
                self.down[2],
            ],
        )

    def f(self):
        return RubiksCube(
            up=[
                self.up[0],
                self.up[1],
                [self.right[0][0], self.right[1][0], self.right[2][0]],
            ],
            front=self.__counterclockwise(self.front),
            right=[
                [self.down[0][2], self.right[0][1], self.right[0][2]],
                [self.down[0][1], self.right[1][1], self.right[1][2]],
                [self.down[0][2], self.right[2][1], self.right[2][2]],
            ],
            back=self.back,
            left=[
                [self.left[0][0], self.left[0][1], self.up[2][2]],
                [self.left[1][0], self.left[1][1], self.up[2][1]],
                [self.left[2][0], self.left[2][1], self.up[2][0]],
            ],
            down=[
                [self.left[0][2], self.left[1][2], self.left[2][2]],
                self.down[1],
                self.down[2],
            ],
        )

    def R(self):
        return RubiksCube(
            up=[
                [self.up[0][0], self.up[0][1], self.front[0][2]],
                [self.up[1][0], self.up[1][1], self.front[1][2]],
                [self.up[2][0], self.up[2][1], self.front[2][2]],
            ],
            front=[
                [self.front[0][0], self.front[0][1], self.down[0][2]],
                [self.front[1][0], self.front[1][1], self.down[1][2]],
                [self.front[2][0], self.front[2][1], self.down[2][2]],
            ],
            right=self.__clockwise(self.right),
            back=[
                [self.up[2][2], self.back[0][1], self.back[0][2]],
                [self.up[1][2], self.back[1][1], self.back[1][2]],
                [self.up[0][2], self.back[2][1], self.back[2][2]],
            ],
            left=self.left,
            down=[
                [self.down[0][0], self.down[0][1], self.back[2][0]],
                [self.down[1][0], self.down[1][1], self.back[1][0]],
                [self.down[2][0], self.down[2][1], self.back[0][0]],
            ],
        )

    def r(self):
        return RubiksCube(
            up=[
                [self.up[0][0], self.up[0][1], self.back[2][0]],
                [self.up[1][0], self.up[1][1], self.back[1][0]],
                [self.up[2][0], self.up[2][1], self.back[0][0]],
            ],
            front=[
                [self.front[0][0], self.front[0][1], self.up[0][2]],
                [self.front[1][0], self.front[1][1], self.up[1][2]],
                [self.front[2][0], self.front[2][1], self.up[2][2]],
            ],
            right=self.__counterclockwise(self.right),
            back=[
                [self.down[2][2], self.back[0][1], self.back[0][2]],
                [self.down[1][2], self.back[1][1], self.back[1][2]],
                [self.down[0][2], self.back[2][1], self.back[2][2]],
            ],
            left=self.left,
            down=[
                [self.down[0][0], self.down[0][1], self.front[0][2]],
                [self.down[1][0], self.down[1][1], self.front[1][2]],
                [self.down[2][0], self.down[2][1], self.front[2][2]],
            ],
        )

    def B(self):
        return RubiksCube(
            up=[
                [self.right[0][2], self.right[1][2], self.right[2][2]],
                self.up[1],
                self.up[2],
            ],
            front=self.front,
            right=[
                [self.right[0][0], self.right[0][1], self.down[2][2]],
                [self.right[1][0], self.right[1][1], self.down[2][1]],
                [self.right[2][0], self.right[2][1], self.down[2][0]],
            ],
            back=self.__clockwise(self.back),
            left=[
                [self.up[0][2], self.left[0][1], self.left[0][2]],
                [self.up[0][1], self.left[1][1], self.left[1][2]],
                [self.up[0][0], self.left[2][1], self.left[2][2]],
            ],
            down=[
                self.down[0],
                self.down[1],
                [self.left[0][0], self.left[1][0], self.left[2][0]],
            ],
        )

    def b(self):
        return RubiksCube(
            up=[
                [self.left[2][0], self.left[1][0], self.left[0][0]],
                self.up[1],
                self.up[2],
            ],
            front=self.front,
            right=[
                [self.right[0][0], self.right[0][1], self.up[0][0]],
                [self.right[1][0], self.right[1][1], self.up[0][1]],
                [self.right[2][0], self.right[2][1], self.up[0][2]],
            ],
            back=self.__counterclockwise(self.back),
            left=[
                [self.down[2][0], self.left[0][1], self.left[0][2]],
                [self.down[2][1], self.left[1][1], self.left[1][2]],
                [self.down[2][2], self.left[2][1], self.left[2][2]],
            ],
            down=[
                self.down[0],
                self.down[1],
                [self.right[1][2], self.right[1][2], self.right[0][2]],
            ],
        )

    def L(self):
        return RubiksCube(
            up=[
                [self.back[2][2], self.up[0][1], self.up[0][2]],
                [self.back[1][2], self.up[1][1], self.up[1][2]],
                [self.back[0][2], self.up[2][1], self.up[2][2]],
            ],
            front=[
                [self.up[0][0], self.front[0][1], self.front[0][2]],
                [self.up[1][0], self.front[1][1], self.front[1][2]],
                [self.up[2][0], self.front[2][1], self.front[2][2]],
            ],
            right=self.right,
            back=[
                [self.back[0][0], self.back[0][1], self.down[2][0]],
                [self.back[1][0], self.back[1][1], self.down[1][0]],
                [self.back[2][0], self.back[2][1], self.down[0][0]],
            ],
            left=self.__clockwise(self.left),
            down=[
                [self.front[0][0], self.down[0][1], self.down[0][2]],
                [self.front[1][0], self.down[1][1], self.down[1][2]],
                [self.front[2][0], self.down[2][1], self.down[2][2]],
            ],
        )

    def l(self):
        return RubiksCube(
            up=[
                [self.front[0][0], self.up[0][1], self.up[0][2]],
                [self.front[1][0], self.up[1][1], self.up[1][2]],
                [self.front[2][0], self.up[2][1], self.up[2][2]],
            ],
            front=[
                [self.down[0][0], self.front[0][1], self.front[0][2]],
                [self.down[1][0], self.front[1][1], self.front[1][2]],
                [self.down[2][0], self.front[2][1], self.front[2][2]],
            ],
            right=self.right,
            back=[
                [self.back[0][0], self.back[0][1], self.up[2][0]],
                [self.back[1][0], self.back[1][1], self.up[1][0]],
                [self.back[2][0], self.back[2][1], self.up[0][0]],
            ],
            left=self.__counterclockwise(self.left),
            down=[
                [self.back[2][2], self.down[0][1], self.down[0][2]],
                [self.back[1][2], self.down[1][1], self.down[1][2]],
                [self.back[0][2], self.down[2][1], self.down[2][2]],
            ],
        )

    def D(self):
        return RubiksCube(
            up=self.up,
            front=[
                self.front[0],
                self.front[1],
                self.left[2],
            ],
            right=[
                self.right[0],
                self.right[1],
                self.front[2],
            ],
            back=[
                self.back[0],
                self.back[1],
                self.right[2],
            ],
            left=[
                self.left[0],
                self.left[1],
                self.back[2],
            ],
            down=self.__clockwise(self.down),
        )

    def d(self):
        return RubiksCube(
            up=self.up,
            front=[
                self.front[0],
                self.front[1],
                self.right[2],
            ],
            right=[
                self.right[0],
                self.right[1],
                self.back[2],
            ],
            back=[
                self.back[0],
                self.back[1],
                self.left[2],
            ],
            left=[
                self.left[0],
                self.left[1],
                self.front[2],
            ],
            down=self.__counterclockwise(self.down),
        )

    def __clockwise(self, face):
        return [
            [face[2][0], face[1][0], face[0][0]],
            [face[2][1], face[1][1], face[0][1]],
            [face[2][2], face[1][2], face[0][2]],
        ]

    def __counterclockwise(self, face):
        return [
            [face[0][2], face[1][2], face[2][2]],
            [face[0][1], face[1][1], face[2][1]],
            [face[0][0], face[1][0], face[2][0]],
        ]

    def __repr__(self):
        return 'RubiksCube(\n%s)' % '\n\n'.join(map(self.__repr_color, [self.up, self.front, self.right, self.back, self.left, self.down]))

    def __repr_color(self, face):
        return '\n'.join(map(lambda colors: ''.join(map(lambda color: color.color() + '\u25A0', colors)), face)) + colorama.Style.RESET_ALL
