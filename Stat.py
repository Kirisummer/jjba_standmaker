import enum


class Stat(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

    @staticmethod
    def values():
        return Stat.A, Stat.B, Stat.C, Stat.D, Stat.E

    def __int__(self):
        return 5 - ord(self.name) + ord('A')
