import unittest

from i2c_registers.i2c_register_section import I2cRegisterSection
from i2c_registers.i2c_register import I2cRegister, RegisterOperations


class I2cRegisterTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.section = I2cRegisterSection("test", 0, 7, [0] * 8)
        self.register = I2cRegister("test", 0x03,
                                    RegisterOperations.ReadWrite, False, {"test": self.section})

    def test_properties(self):
        self.assertEqual("TEST", self.register.name)
        self.assertEqual(3, self.register.reg_addr)
        self.assertEqual(RegisterOperations.ReadWrite, self.register.op_mode)
        self.assertEqual({"TEST": self.section}, self.register.sections)

    def test_get_section(self):
        seg = self.register.get_section("test")
        self.assertEqual("TEST", seg.name)
        self.assertEqual(0, seg.lsb)
        self.assertEqual(7, seg.msb)
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], seg.bits)

    def test_not_exist(self):
        with self.assertRaises(KeyError):
            self.register.get_section("DOES_NOT_EXIST")

    def test_len_bytes(self):
        result = self.register.len_bytes()
        self.assertEqual(1, result)

    def test_set_value_8bit(self):
        self.register.set_value(16)
        seg = self.register.get_section("test")
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0], seg.bits)


class I2cRegisterSetGetValueTestCase(unittest.TestCase):

    def test_set_value_16bit(self):
        register = I2cRegister("test", 0x03, RegisterOperations.ReadWrite, False, {})
        register.add_section("test_seg", 0, 15,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        register.set_value(31135)
        seg = register.get_section("test_seg")
        self.assertEqual([0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1], seg.bits)

    def test_get_value_8bit(self):
        register = I2cRegister("test", 0x03, RegisterOperations.ReadWrite, False, {})
        register.add_section("test_seg", 0, 7, [0, 0, 0, 1, 0, 0, 0, 0])

        reg_val = register.get_value()
        self.assertEqual(16, reg_val)

    def test_get_value_16bit(self):
        register = I2cRegister("test", 0x03, RegisterOperations.ReadWrite, False, {})
        register.add_section("test_seg", 0, 15,
                             [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1])
        # 799F
        # 31135
        # 0111 1001 1001 1111
        reg_val = register.get_value()
        self.assertEqual(31135, reg_val)

    def test_get_value_all_bits_8bit(self):
        register = I2cRegister("IODIR", 0x00, RegisterOperations.ReadWrite, False, {})
        register.add_section("IO7", 7, 7, [0])
        register.add_section("IO6", 6, 6, [0])
        register.add_section("IO5", 5, 5, [0])
        register.add_section("IO4", 4, 4, [1])
        register.add_section("IO3", 3, 3, [0])
        register.add_section("IO2", 2, 2, [0])
        register.add_section("IO1", 1, 1, [0])
        register.add_section("IO0", 0, 0, [0])

        reg_val = register.get_value()
        self.assertEqual(16, reg_val)

    def test_get_value_all_bits_16bit(self):
        register = I2cRegister("CONF", 0x00, RegisterOperations.ReadWrite, False, {})
        register.add_section("RST", 15, 15, [0])
        register.add_section("BRNG", 13, 14, [1, 1])
        register.add_section("PG", 11, 12, [1, 1])
        register.add_section("BADC", 7, 10, [0, 0, 1, 1])
        register.add_section("SADC", 3, 6, [0, 0, 1, 1])
        register.add_section("MODE", 0, 2, [1, 1, 1])

        # 799F
        # 31135
        # 0111 1001 1001 1111 -> 1111 1001 1001 1110

        reg_val = register.get_value()
        self.assertEqual(31135, reg_val)

    def test_get_value_duplicate_bits(self):
        register = I2cRegister("IODIR", 0x00, RegisterOperations.ReadWrite, False, {})
        register.add_section("IODIR", 0, 7, [0] * 8)
        register.add_section("IO7", 7, 7, [0])
        register.add_section("IO6", 6, 6, [0])
        register.add_section("IO5", 5, 5, [0])
        register.add_section("IO4", 4, 4, [0])
        register.add_section("IO3", 3, 3, [0])
        register.add_section("IO2", 2, 2, [0])
        register.add_section("IO1", 1, 1, [0])
        register.add_section("IO0", 0, 0, [0])

        with self.assertRaises(KeyError):
            register.get_value()

    def test_get_value_missing_bits(self):
        register = I2cRegister("IOCON", 0x00, RegisterOperations.ReadWrite, False, {})
        register.add_section("SREAD", 5, 5, [0])
        register.add_section("DISSLW", 4, 4, [0])
        register.add_section("ODR", 2, 2, [0])
        register.add_section("INTPOL", 1, 1, [0])

        with self.assertRaises(SyntaxError):
            register.get_value()

    def test_get_value_not_used_bits(self):
        register = I2cRegister("IOCON", 0x00, RegisterOperations.ReadWrite, False, {})
        register.add_not_used_section(6, 7)
        register.add_section("SREAD", 5, 5, [0])
        register.add_section("DISSLW", 4, 4, [1])
        register.add_not_used_section(3, 3)
        register.add_section("ODR", 2, 2, [0])
        register.add_section("INTPOL", 1, 1, [0])
        register.add_not_used_section(0, 0)

        reg_val = register.get_value()
        self.assertEqual(16, reg_val)


class I2cRegisterAddTestCase(unittest.TestCase):

    def test_perfect(self):
        register = I2cRegister("test", 0x03, RegisterOperations.ReadWrite, False, {})
        register.add_section("test_seg", 0, 2, [0] * 3)

        section = register.get_section("test_seg")
        self.assertEqual("TEST_SEG", section.name)
        self.assertEqual(0, section.lsb)
        self.assertEqual(2, section.msb)
        self.assertEqual([0, 0, 0], section.bits)


if __name__ == '__main__':
    unittest.main()
