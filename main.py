### Main Functions

def GetSpecificBits(num, start, span):
    temp = "0b0"
    temp += span * "1"
    temp = int(temp, 2) 
    return bin((num >> start) & temp)

def Registers(read1, read2, writeReg, writeData = None):

    return ALU(read1, read2)

def RegWrite(instruction):

    return None

def ALU(read1, read2, aluControl):
    def ADD(num1, num2):
        return num1 + num2
    return None

### Initialization

## Initialize Program Counter
pc = 0b0

## Initialize Program Memory
instructionMemory = []
for i in range (255):
    instructionMemory.append(0b0)

# TODO Read Files For Instructions 
instructionMemory[0] = 0b00000000100010000001000110011

## Initialize Registers
registers = []
for i in range(32):
    registers.append(0)

### Main Loop
# TODO Figure Out Exit Condition
while pc == 0:
    # Read Instruction
    instruction = instructionMemory[pc]

    Registers(GetSpecificBits(instruction, 15, 5), GetSpecificBits(instruction, 20, 5), GetSpecificBits(instruction, 7, 5))


    # Update Program Counter (End Of Cycle)
    pc += 4
    


