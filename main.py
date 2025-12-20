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
    # I-Type L
    elif opcode == '0b11':
        return bin(num1 + num2)

### Initialization

## Initialize Program Counter
pc = 0b0

## Initialize Program Memory
instructionMemory = []
for i in range (255):
    instructionMemory.append(0b0)

# TODO Read Files For Instructions 
instructionMemory[0] = 0b000000000100010000010000011

## Initialize Memory
memory = []
for i in range(2**6):
    memory.append(0)
memory[0] = bin(1)
memory[1] = bin(2)
memory[2] = bin(3)
memory[3] = bin(4)

## Initialize Registers
registers = []
for i in range(32):
    registers.append(0)
registers[4] = bin(0)

### Main Loop
# TODO Figure Out Exit Condition
while pc == 0:
    # Read Instruction
    instruction = instructionMemory[pc]
    
    # Registers Variables
    read1 = GetSpecificBits(instruction, 15, 5)
    read2 = GetSpecificBits(instruction, 20, 5)
    writeReg = GetSpecificBits(instruction, 7, 5)
    aluControl = [GetSpecificBits(instruction, 30, 1), GetSpecificBits(instruction, 12, 3)]
    if ALUSrc(instruction):
        imm = int(ImmGen(instruction), 2)
        aluResult = ALU(int(registers[int(read1, 2)], 2), imm, aluControl) 
    else:
        aluResult = ALU(int(registers[int(read1, 2)], 2), int(registers[int(read2, 2)], 2), aluControl)
    
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
    

print(f"read1: {read1} / {int(read1, 2)}")
print(f"read2: {read2} / {int(read2, 2)}")
print(f"writeReg: {writeReg} / {int(writeReg, 2)}")
print(f"writeData: {writeData} / {int(writeData, 2)}")
print(registers)
print(memory)
