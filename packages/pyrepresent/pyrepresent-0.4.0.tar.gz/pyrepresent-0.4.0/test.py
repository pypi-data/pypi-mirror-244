# test.py

import datetime as dt

import pandas as pd
import numpy as np

from represent import represent, indent, unwrap, colorize, to_string

@represent
class Model:

    def __init__(self) -> None:

        self.datetime = dt.datetime.now()
        self.date = self.datetime.date()
        self.time = self.datetime.time()

        self.self = self
        self.type = type(self)

        self.values = [1, 2, 3]

        self.objects = {
            'self': self.self,
            'type': self.type,
            self.self: self.self,
            self.type: self.type,
            (1, 2, 3): self.values
        }
        self.objects['data'] = self.objects

        self.zero = 0

        self.data = pd.DataFrame({1: [1, 2, 3]})
        self.array = np.array([[1, 2, 3], [4, 5, 6]])
    # end __init__
# Model

@represent
class Data:

    __slots__ = "x", "y"

    def __init__(self):

        self.x = 0
        self.y = 0
    # end __init__
# end Data

def main() -> None:
    """Tests the module."""

    print(Model())
    print(Data())
    print(colorize(indent(str(unwrap({Data(): 0, Data(): 1}, assign=True)))))
    print(to_string(unwrap(Data(), assign=False)))
    print(to_string(unwrap({Data(): 0, Data(): 1}, assign=False)))
# end main

if __name__ == "__main__":
    main()
# end if