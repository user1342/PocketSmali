def const_string_operand_handler(opcode, operands, runtime_env, emulator):
    # Extract the register and string value from the operand
    register = operands[0]
    string_value = " ".join(operands[1:])  # Extract string value and remove surrounding quotes
    string_value = string_value.strip('"')
    # Add the string value to the string pool and store the corresponding string index
    string_idx = runtime_env.add_to_string_pool(string_value)

    # Store the string index in the register
    runtime_env.set_register(register,string_idx)