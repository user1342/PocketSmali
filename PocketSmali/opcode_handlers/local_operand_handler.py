def local_operand_handler(opcode, operands, runtime_env, emulator):
    # Extract the register, variable name, and type from the operands
    register = operands[0]
    variable_name, type = operands[1].split(":")
    type = type.strip("'").strip(";") # Remove quotes and semicolon from type
    variable_name = variable_name.strip('"') # Remove quotes from variable name

    # Set the register in the runtime environment with the extracted variable name and type
    runtime_env.set_register(register, value=None, name=variable_name, type=type)

    # Return from the function
    return