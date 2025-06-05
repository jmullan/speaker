import math
from fractions import Fraction
from numbers import Number
from typing import Collection, Union


def nice(value: Number):
    decimal, whole = math.modf(value)
    whole = int(whole)
    if not decimal:
        return f'{whole:d}'
    fraction = Fraction(decimal).limit_denominator()
    if not whole:
        return f'{fraction}'
    return f'{whole:d} {fraction}'


class Reference:
    def __str__(self) -> str:
        return nice(self.value())

    def value(self) -> Number:
        raise NotImplementedError


Measurement = Union[Reference, Number]


class Inch(Reference):
    def __init__(self, measurement: Number):
        self.measurement = measurement

    def value(self) -> Number:
        measurement = self.measurement
        if isinstance(measurement, Reference):
            measurement = measurement.value()
        return measurement


class Add(Reference):
    def __init__(self, *args: Measurement):
        self.args = args  # type: Collection[Measurement]

    def value(self) -> Number:
        x = 0
        for y in self.args:
            if isinstance(y, Reference):
                x += y.value()
            else:
                x += y
        return x


class Subtract(Reference):
    def __init__(self, minuend: Measurement, subtrahend: Measurement):
        self.minuend = minuend
        self.subtrahend = subtrahend

    def value(self) -> Number:
        minuend = self.minuend
        if isinstance(minuend, Reference):
            minuend = minuend.value()
        subtrahend = self.subtrahend
        if isinstance(subtrahend, Reference):
            subtrahend = subtrahend.value()
        return minuend - subtrahend


class Piece:
    def __init__(self, name: str, quantity: int, thickness: Measurement, width: Measurement, length: Measurement):
        self.name = name
        self.thickness = Inch(thickness)
        self.length = length
        self.width = width
        self.quantity = quantity


def main():
    tq = Inch(23 / 32)
    half = Inch(15 / 32)
    depth = Inch(13)
    inside = Inch(12)
    width = Add(inside, half, half)

    A = Piece('A', 4, tq, 2.5, inside)
    H = Piece('H', 3, half, inside, depth)
    E = Piece('E', 1, tq, 3.5, inside)
    C = Piece('C', 2, tq, 2.5, Subtract(13, Add(A.thickness, A.thickness)))
    f_length = Subtract(13, Add(tq, H.thickness, H.thickness, A.width))
    F = Piece('F', 4, tq, 2.5, f_length)
    B = Piece('B', 2, tq, 2.5, Subtract(F.length, A.width))

    I = Piece('I', 1, half, 13, Add(H.length, E.thickness, F.width))
    D = Piece('D', 2, tq, 2.5, Subtract(I.length, Add(A.thickness, A.thickness)))

    height = Add(H.thickness, H.thickness, I.length)
    J = Piece('J', 2, half, depth, height)

    pieces = [A, B, C, D, E, F, H, I, J]

    for piece in pieces:
        print(f'{piece.name}: ({piece.quantity}) {piece.thickness}" X {piece.width}" X {piece.length}"')

    front = Add(C.length, E.thickness, F.width)
    print(f'{height}"H X {width}"W X {depth}"D')


if __name__ == "__main__":
    # execute only if run as a script
    main()
