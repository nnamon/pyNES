# -*- coding: utf-8 -*-
import unittest
from pynes.asm import *
from pynes.lib import asm_def
from pynes.block import MemoryAddress


class StdLibTest(unittest.TestCase):

    def test_simple_function(self):
        @asm_def
        def simple():
            return (
                BIT + '$2002'
                )

        expression = simple.as_function()
        actual = str(expression)
        expected = '\n'.join([
            'simple:',
            'BIT $2002',
            'RTS'
            ]) + '\n'
        self.assertEquals(actual, expected)

    def test_reset(self):
        @asm_def
        def vblank():
            return (
                BIT + '$2002' +
                RTS
            )

        @asm_def
        def reset():
            return (
                SEI +
                vblank()
            )

        expression = reset()
        actual = str(expression)
        expected = '\n'.join([
            'reset:',
            'SEI',
            'vblank:',
            'BIT $2002',
            'RTS'
            ]) + '\n'
        self.assertEquals(actual, expected)

    def test_asm_function_with_single_instruction_proxy(self):
        @asm_def
        def single():
            return SEI

        single.calls = 2

        expression = single()
        actual = str(expression)
        expected = 'JSR single'
        self.assertEquals(actual, expected)

        actual_asm = str(single.asm())
        expected_asm = '\n'.join([
            'single:',
            'SEI',
            'RTS'
            ]) + '\n'

        self.assertEquals(actual_asm, expected_asm)

    def test_asm_function_with_single_instruction(self):
        @asm_def
        def single():
            return BIT + '$2002'

        single.calls = 2

        expression = single()
        actual = str(expression)
        expected = 'JSR single'
        self.assertEquals(actual, expected)

        actual_asm = str(single.asm())
        expected_asm = '\n'.join([
            'single:',
            'BIT $2002',
            'RTS'
            ]) + '\n'

        self.assertEquals(actual_asm, expected_asm)

    def test_vblank_with_more_than_one_call(self):
        @asm_def
        def vblank():
            return (
                BIT + '$2002'
            )

        vblank.calls = 2

        expression = vblank()
        actual = str(expression)
        expected = 'JSR vblank'
        self.assertEquals(actual, expected)

        actual_asm = str(vblank.asm())
        expected_asm = '\n'.join([
            'vblank:',
            'BIT $2002',
            'RTS'
            ]) + '\n'

        self.assertEquals(actual_asm, expected_asm)

    def test_vblank_with_recursive(self):
        @asm_def
        def vblank():
            return (
                BIT + '$2002' +
                BPL + vblank()
            )

        expression = vblank()
        actual = str(expression)

        expected = '\n'.join([
            'vblank:',
            'BIT $2002',
            'BPL vblank'
            ]) + '\n'
        self.assertEquals(actual, expected)

        expected_as_function = '\n'.join([
            'vblank:',
            'BIT $2002',
            'BPL vblank',
            'RTS'
            ]) + '\n'
        self.assertEquals(str(vblank.as_function()), expected_as_function)

    def test_vblank_with_recursive_called_more_than_once(self):
        @asm_def
        def vblank():
            return (
                BIT + '$2002' +
                BPL + vblank()
            )

        vblank.calls = 2

        expression = vblank()
        actual = str(expression)

        expected = 'JSR vblank'

        self.assertEquals(actual, expected)

        actual_asm = str(vblank.as_function())
        expected_asm = '\n'.join([
            'vblank:',
            'BIT $2002',
            'BPL vblank',
            'RTS'
            ]) + '\n'

        self.assertEquals(actual_asm, expected_asm)

