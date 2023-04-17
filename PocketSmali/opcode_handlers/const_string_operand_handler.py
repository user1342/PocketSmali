def const_string_operand_handler(opcode, operands, runtime_env, emulator):
    # Extract the destination register from the operands list
    register = operands[0]

    # Extract the string value from the operands list
    string_value = " ".join(operands[1:])  # Extract string value and remove surrounding quotes
    string_value = string_value.strip('"')  # Remove surrounding double quotes from the string

    # Add the string value to the string pool and store the corresponding string index
    string_idx = runtime_env.add_to_string_pool(string_value)

    # Store the string index in the destination register using the runtime_env's set_register method
    runtime_env.set_register(register, string_idx)

    # The string value is now stored in the destination register as a string index,
    # effectively executing the instruction and storing the string value in the emulator's memory.