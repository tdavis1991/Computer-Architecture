"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.reg = {}
    
        for i in range(8):
            self.reg[i] = 0

        self.PC = 0

        self.SP = 7

        self.IR = "00000000"

        self.FL = 0b00000000

        self.CMD = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = [
            0b10000010, # LDI R0,10
            0b00000000,
            0b00001010,
            0b10000010,# LDI R1,20
            0b00000001,
            0b00010100,
            0b10000010, # LDI R2,TEST1
            0b00000010,
            0b00010011,
            0b10100111, # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010101, # JEQ R2
            0b00000010,
            0b10000010, # LDI R3,1
            0b00000011,
            0b00000001,
            0b01000111, # PRN R3
            0b00000011,
            # TEST1 (address 19):
            0b10000010, # LDI R2,TEST2
            0b00000010,
            0b00100000,
            0b10100111, # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010110, # JNE R2
            0b00000010,
            0b10000010, # LDI R3,2
            0b00000011,
            0b00000010,
            0b01000111, # PRN R3
            0b00000011,
            # TEST2 (address 32):
            0b10000010, # LDI R1,10
            0b00000001,
            0b00001010,
            0b10000010, # LDI R2,TEST3
            0b00000010,
            0b00110000,
            0b10100111, # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010101, # JEQ R2
            0b00000010,
            0b10000010, # LDI R3,3
            0b00000011,
            0b00000011,
            0b01000111, # PRN R3
            0b00000011,
            # TEST3 (address 48):
            0b10000010, # LDI R2,TEST4
            0b00000010,
            0b00111101,
            0b10100111, # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010110, # JNE R2
            0b00000010,
            0b10000010, # LDI R3,4
            0b00000011,
            0b00000100,
            0b01000111, # PRN R3
            0b00000011,
            # TEST4 (address 61):
            0b10000010, # LDI R3,5
            0b00000011,
            0b00000101,
            0b01000111, # PRN R3
            0b00000011,
            0b10000010, # LDI R2,TEST5
            0b00000010,
            0b01001001,
            0b01010100, # JMP R2
            0b00000010,
            0b01000111, # PRN R3
            0b00000011,
            # TEST5 (address 73):
            0b00000001 # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
    
    def HLT(self):
        self.PC += 1
        sys.exit()

    def PRN(self):
        print(self.reg[self.ram_read(self.PC+1)])
        self.PC += 2

    def LDI(self):
        register = self.ram_read(self.PC+1)
        self.reg[register] = self.ram_read(self.PC+2)
        self.PC += 3

    def CMP(self):
        reg_a = self.ram_read(self.PC+1)
        reg_b = self.ram_read(self.PC+2)

        # 00000LGE
        #Set self.FL to 0b00000001(equal) if both registers are equal
        if self.reg[reg_a] == self.reg[reg_b]:
            self.FL = 0b00000001
        #Set self.FL to 0b00000100(less than) if register a is less than register b
        elif self.reg[reg_a] < self.reg[reg_b]:
            self.FL = 0b00000100
        #Set self.FL to 0b00000010(greater than) if register a is greater than register b
        elif self.reg[reg_a] > self.reg[reg_b]:
            self.FL = 0b00000010

        self.PC += 3
    
    def JMP(self):
        reg = self.ram_read(self.PC+1)
        self.PC = self.reg[reg]
    
    def JEQ(self):
        reg = self.ram_read(self.PC+1)

        if self.FL == 0b00000001:
            self.PC = self.reg[reg]

        else:
            self.PC += 2
    
    def JNE(self):
        reg = self.ram_read(self.PC+1)
        move = self.FL & 0b00000001
        
        if move == 1:
            self.PC = self.reg[reg]
        else:
            self.PC += 2

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.PC = 0
        self.reg[self.SP] = -1

        while True:
            self.IR = self.ram_read(self.PC)

            if self.IR in self.CMD.keys():
                self.CMD[self.IR]()


new_cpu = CPU()
new_cpu.load()
new_cpu.run()