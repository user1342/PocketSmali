def const_operand_handler(opcode, operands, runtime_env, emulator):
    destination_reg = operands[0]
    value = operands[1]
    runtime_env.set_register(destination_reg, value)  # Store the value in the destination register