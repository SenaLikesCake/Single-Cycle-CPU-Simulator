### Main Functions

def GetSpecificBits(num, start, span):
    temp = "0b0"
    temp += span * "1"
    temp = int(temp, 2)
    return bin((num >> start) & temp)

## TODO Test ALL Types when their functions are implemented
def ImmGen(instruction):
    # I-Type
    if GetSpecificBits(instruction, 0, 7) == '0b10011' or GetSpecificBits(instruction, 0, 7) == '0b11' or GetSpecificBits(instruction, 0, 7) == '0b1100111':
        return GetSpecificBits(instruction, 20, 12)
    # S-Type
    elif GetSpecificBits(instruction, 0, 7) == '0b100011':
        return GetSpecificBits(instruction, 7, 5) + GetSpecificBits(instruction, 25, 7)[2:]
    # B-Type
    elif GetSpecificBits(instruction, 0, 7) == '0b1100011':
        return GetSpecificBits(instruction, 7, 4) + GetSpecificBits(instruction, 25, 6)[2:] + GetSpecificBits(instruction, 11, 0)[2:] + GetSpecificBits(instruction, 31, 0)[2:]
    # U-Type
    elif GetSpecificBits(instruction, 0, 7) == '0b110111' or GetSpecificBits(instruction, 0, 7) == '0b10111':
        return GetSpecificBits(instruction, 12, 20) + 12 * "0"
    # J-Type
    elif GetSpecificBits(instruction, 0, 7) == '0b1101111':
        return GetSpecificBits(instruction, 31, 1) + GetSpecificBits(instruction, 12, 7)[2:] + GetSpecificBits(instruction, 20, 1)[2:] + GetSpecificBits(instruction, 21, 10)[2:]
    # R-Type / Fallback
    else:
        return None


def RegWrite(instruction):
    if (GetSpecificBits(instruction, 0, 7) == '0b110011' or
        GetSpecificBits(instruction, 0, 7) == '0b10011' or
        GetSpecificBits(instruction, 0, 7) == '0b11'):
        return True
    else:
        return False

def MemRead(instruction):
    if GetSpecificBits(instruction, 0, 7) == '0b11':
        return True
    else:
        return False

def MemWrite(instruction):
    if GetSpecificBits(instruction, 0, 7) == '0b100011':
        return True
    else:
        return False

def MemToReg(instruction):
    if GetSpecificBits(instruction, 0, 7) == '0b11':
        return True
    else:
        return False

def ALUSrc(instruction):
    if (GetSpecificBits(instruction, 0, 7) == '0b10011' or
        GetSpecificBits(instruction, 0, 7) == '0b11' or
        GetSpecificBits(instruction, 0, 7) == '0b1100111' or
        GetSpecificBits(instruction, 0, 7) == '0b100011' or
        GetSpecificBits(instruction, 0, 7) == '0b1100011' or
        GetSpecificBits(instruction, 0, 7) == '0b110111' or
        GetSpecificBits(instruction, 0, 7) == '0b10111' or
        GetSpecificBits(instruction, 0, 7) == '0b1101111'):
        return True
    else:
        return False

def ALU(num1, num2, aluControl = None):
    # num1 = int(registers[int(read1, 2)], 2)
    # num2 = int(registers[int(read2, 2)], 2)
    opcode = GetSpecificBits(instruction, 0, 7)
    # R-Type
    if opcode == '0b110011':
        if aluControl[1] == "0b0":
            # add
            if aluControl[0] == "0b0":
                return bin(num1 + num2)
            # sub
            else:
                return bin(num1 - num2)
        # xor
        elif aluControl[1] == "0b100":
            return bin(num1 ^ num2)
        # or
        elif aluControl[1] == "0b110":
            return bin(num1 | num2)
        # and
        elif aluControl[1] == "0b111":
            return bin(num1 & num2)
    # I-Type
    elif opcode == '0b10011':
        # addi
        if aluControl[1] == "0b0":
            return bin(num1 + num2)
        # xori
        elif aluControl[1] == "0b100":
            return bin(num1 ^ num2)
        # ori
        elif aluControl[1] == "0b110":
            return bin(num1 | num2)
        # andi
        elif aluControl[1] == "0b111":
            return bin(num1 & num2)
    # I-Type Load / S-Type
    elif opcode == "0b11" or opcode == "0b100011":
        return bin(num1 + num2)

### Initialization

## Initialize Program Counter
pc = 0b0

## Initialize Program Memory
# instructionMemory = []
# for i in range (255):
    # instructionMemory.append(0b0)

inputfile = "test.txt"
file = open(inputfile, "r")
content = file.read()
instructionarr = content.split("\n")

instructionMemory = []
for i in range(255):
    if i % 4 == 0 and i // 4 < len(instructionarr):
        instructionMemory.append(instructionarr[i // 4])
    else:
        instructionMemory.append(None)

# instructionMemory[0] = 0b00000000010000000010000000100011

## Initialize Memory
memory = []
for i in range(2**6):
    memory.append(0)


## Initialize Registers
registers = []
for i in range(32):
    registers.append(0)
# registers[2] = bin(1)
# registers[3] = bin(2)

### Main Loop
# TODO Figure Out Exit Condition
while instructionMemory[pc] != None:
    # Read Instruction
    instruction = int(instructionMemory[pc], 2)

    # Decode Instruction
    readReg1 = GetSpecificBits(instruction, 15, 5)
    readReg2 = GetSpecificBits(instruction, 20, 5)
    writeReg = GetSpecificBits(instruction, 7, 5)
    aluControl = [GetSpecificBits(instruction, 30, 1), GetSpecificBits(instruction, 12, 3)]
    imm = int(ImmGen(instruction), 2)

    # Read Registers
    readData1 = registers[int(readReg1, 2)]
    readData2 = registers[int(readReg2, 2)]

    # Convert readData To Binary
    if type(readData1) == int:
        readData1 = bin(readData1)
    if type(readData2) == int:
        readData2 = bin(readData2)

    # MUX To Choose Between Read Data 2 Or Imm
    if ALUSrc(instruction):
        # TODO Get imm On Decode Step
        aluResult = ALU(int(readData1, 2), imm, aluControl)
    else:
        aluResult = ALU(int(readData1, 2), int(readData2, 2), aluControl)

    # Read Memory
    if MemRead(instruction):
        # lb
        if GetSpecificBits(instruction, 12, 3) == '0b0':
            readData = memory[int(aluResult, 2)]
        # lh
        elif GetSpecificBits(instruction, 12, 3) == '0b1':
            readData = memory[int(aluResult, 2)] + memory[int(aluResult, 2) + 1][2:]
        # lw
        elif GetSpecificBits(instruction, 12, 3) == '0b10':
            readData = memory[int(aluResult, 2)] + memory[int(aluResult, 2) + 1][2:] + memory[int(aluResult, 2) + 2][2:] + memory[int(aluResult, 2) + 3][2:]

    # Write Memory
    if MemWrite(instruction):
        writeData = readData2
        writeData = '0b' + "0" * (34 - len(writeData)) + writeData[2:]
        #sb
        if GetSpecificBits(instruction, 12, 3) == '0b0':
            mem1 = bin(int('0b' + writeData[-8:], 2))
            memory[int(aluResult, 2)] = mem1
        #sh
        elif GetSpecificBits(instruction, 12, 3) == '0b1':
            mem2 = bin(int('0b' + writeData[-16:-8], 2))
            mem1 = bin(int('0b' + writeData[-8:], 2))
            memory[int(aluResult, 2)] = mem2
            memory[int(aluResult, 2) + 1] = mem1
        #sw
        elif GetSpecificBits(instruction, 12, 3) == '0b10':
            mem4 = bin(int(writeData[:11], 2))
            mem3 = bin(int('0b' + writeData[11:19], 2))
            mem2 = bin(int('0b' + writeData[-16:-8], 2))
            mem1 = bin(int('0b' + writeData[-8:], 2))
            memory[int(aluResult, 2)] = mem4
            memory[int(aluResult, 2) + 1] = mem3
            memory[int(aluResult, 2) + 2] = mem2
            memory[int(aluResult, 2) + 3] = mem1

    # MUX To Choose Write Data To Be Read Data Or ALU Result
    if MemToReg(instruction):
        writeData = readData
    else:
        writeData = aluResult

    ### End of Cycle
    # Update Registers if RegWrite
    if RegWrite(instruction):
        registers[int(f"{writeReg}", 2)] = writeData

    # Update Program Counter (End Of Cycle)
    pc += 4


# print(f"read1: {read1} / {int(read1, 2)}")
# print(f"read2: {read2} / {int(read2, 2)}")
# print(f"mem1: {mem1} / {int(mem1, 2)}")
print(f"writeData: {writeData} / {int(writeData, 2)}")
print(registers)
print(memory)
