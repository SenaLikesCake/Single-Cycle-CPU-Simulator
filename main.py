### Main Functions

def GetSpecificBits(num, start, span):
    temp = "0b0"
    temp += span * "1"
    temp = int(temp, 2) 
    return bin((num >> start) & temp)

def RegWrite(instruction):
    if GetSpecificBits(instruction, 0, 7) == '0b110011':
        return True
    else:
        return False

# TODO Add ALU Control
def ALU(read1, read2, aluControl = None):
    read1 = int(read1, 2)
    read2 = int(read2, 2)
    ## R-Type
    def Add(num1, num2):
        return bin(num1 + num2)
    def Sub(num1, num2):
        return bin(num1 - num2)
    return Add(read1, read2)

### Initialization

## Initialize Program Counter
pc = 0b0

## Initialize Program Memory
instructionMemory = []
for i in range (255):
    instructionMemory.append(0b0)

# TODO Read Files For Instructions 
instructionMemory[0] = 0b00000000010000100000001000110011

## Initialize Registers
registers = []
for i in range(32):
    registers.append(0)
registers[4] = bin(4)

### Main Loop
# TODO Figure Out Exit Condition
while pc == 0:
    # Read Instruction
    instruction = instructionMemory[pc]
    
    # Registers Variables
    read1 = GetSpecificBits(instruction, 15, 5)
    read2 = GetSpecificBits(instruction, 20, 5)
    writeReg = GetSpecificBits(instruction, 7, 5)
    writeData = (ALU(read1, read2))

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
