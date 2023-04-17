def local_operand_handler(opcode, operands, runtime_env, emulator):
    register = operands[0]
    variable_name, type = operands[1].split(":")
    type = type.strip("'").strip(";")
    variable_name = variable_name.strip('"')
    runtime_env.set_register(register, value = None, name=variable_name, type=type)
    return