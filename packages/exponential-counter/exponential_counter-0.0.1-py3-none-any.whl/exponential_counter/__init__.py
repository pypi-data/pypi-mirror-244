# SPDX-FileCopyrightText: 2023-present Xiang Wang <ramwin@qq.com>
#
# SPDX-License-Identifier: MIT


"""
counter that can be called multi times
"""


class LinearCounter:
    """basic Linear Counter"""

    def __init__(self, start=0, step=1, min_value=None, max_value=None):
        self.value = start
        self.step = step
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self):
        cur_value = self.value
        self.increment()
        if self.min_value is not None:
            self.value = max(self.value, self.min_value)
        if self.max_value is not None:
            self.value = min(self.value, self.max_value)
        return cur_value

    def increment(self):
        self.value += self.step


class ExponentialCounter(LinearCounter):
    """exponential incremental counter"""

    def __init__(self, start=0, step=2, min_value=None, max_value=None):
        super().__init__(start, step, min_value, max_value)

    def increment(self):
        self.value *= self.step
