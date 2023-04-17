def const_operand_handler(opcode, operands, runtime_env, emulator):
    # Extract the destination register from the operands list
    destination_reg = operands[0]

    # Extract the value from the operands list
    value = operands[1]

    # Store the value in the destination register using the runtime_env's set_register method
    runtime_env.set_register(destination_reg, value)

    # The value is now stored in the destination register, as specified by the instruction