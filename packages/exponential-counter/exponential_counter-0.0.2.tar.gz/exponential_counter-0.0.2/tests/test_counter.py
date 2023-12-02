#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from unittest import TestCase

from exponential_counter import LinearCounter, ExponentialCounter


class Test(TestCase):

    def test_base(self):
        counter = LinearCounter(max_value=4)
        values = [counter() for i in range(8)]
        self.assertEqual(
            values,
            [0, 1, 2, 3, 4, 4, 4, 4]
        )

    def test_exponential(self):
        counter = ExponentialCounter(start=2, max_value=32)
        values = [counter() for i in range(6)]
        self.assertEqual(
            values,
            [2, 4, 8, 16, 32, 32]
        )

        counter = ExponentialCounter(start=4, step=3, max_value=32)
        values = [counter() for i in range(6)]
        self.assertEqual(
            values,
            [4, 12, 32, 32, 32, 32]
        )
