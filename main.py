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
    if GetSpecificBits(instruction, 0, 7) == '0b110011':
        return True
    else:
        return False

def ALU(read1, read2, aluControl = None):
    num1 = int(registers[int(read1, 2)], 2)
    num2 = int(registers[int(read2, 2)], 2)

    ## R-Type
    def Add(num1, num2):
        return bin(num1 + num2)
    def Sub(num1, num2):
        return bin(num1 - num2)
    
    
    if aluControl[1] == "0b0":
        if aluControl[0] == "0b0":
            return Add(num1, num2)
        else:
            return Sub(num1, num2)

    

### Initialization

## Initialize Program Counter
pc = 0b0

## Initialize Program Memory
instructionMemory = []
for i in range (255):
    instructionMemory.append(0b0)

# TODO Read Files For Instructions 
instructionMemory[0] = 0b01000000001100100000001000110011

## Initialize Registers
registers = []
for i in range(32):
    registers.append(0)
registers[4] = bin(4)
registers[3] = bin(1)

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
    writeData = (ALU(read1, read2, aluControl))
    

    ### End of Cycle
    # Update Registers if RegWrite
    if RegWrite(instruction):
        registers[int(f"{writeReg}", 2)] = writeData
    # Update Program Counter (End Of Cycle)
    pc += 4
    

print(f"read1: {read1}")
print(f"read2: {read2}")
print(f"writeReg: {writeReg}")
print(f"writeData: {writeData}")
print(registers)
