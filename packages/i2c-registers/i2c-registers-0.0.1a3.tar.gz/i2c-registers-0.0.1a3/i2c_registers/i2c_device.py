#!/usr/bin/python3

from i2c_registers.i2c_register_section import I2cRegisterSection
from i2c_registers.i2c_register import I2cRegister, RegisterOperations


class I2cDevice:

    def __init__(self,
                 dev_addr: int,
                 byteorder: str,
                 i2c,
                 registers: dict[str, I2cRegister]):

        self.dev_addr = dev_addr
        self.byte_order = byteorder
        self.i2c = i2c
        self.registers = {k.upper(): v for k, v in registers.items()}

        return

    def __str__(self):
        out = "I2cDevice<device_address={}, registers={{\n".format(self.dev_addr)

        for k in self.registers:
            v = self.registers[k]
            # Indent output from Register.str
            v = str(v)
            v = v.split("\n")

            new_v = ""
            for i in range(0, len(v)):
                # Don't indent first line
                if i != 0:
                    new_v += "    "

                new_v += v[i]

                # No newline on last line
                if i != len(v) - 1:
                    new_v += "\n"

            out += "    {}={}\n".format(k, new_v)

        out += "}>"
        return out

    def add(self, name: str, address: int, op_mode: RegisterOperations, signed: bool,
            sections: dict[str, I2cRegisterSection]):
        key = name.upper()
        if key in self.registers:
            raise KeyError("I2cRegister with name already exists. name: {}".format(name))

        register = I2cRegister(name.upper(), address, op_mode, signed, sections)
        register.set_parent(self)

        self.registers[key] = register

        return self.registers[key]

    def get(self, name: str, read_first: bool = False) -> I2cRegister:
        key = name.upper()
        if key not in self.registers:
            raise KeyError("Register with name \"{}\" not found".format(name))

        # Read first if asked
        if read_first:
            self.read(key)

        return self.registers[key]

    def read(self, name: str):
        return self.get(name).read()

    def write(self, name: str):
        return self.get(name).write()
