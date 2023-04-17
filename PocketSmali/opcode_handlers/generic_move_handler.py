def generic_move_handler(opcode, operands, runtime_env, emulator):
    return_registers = emulator.runtime_env.return_registers

    if return_registers == None:
        return

    return_registers_keys = list(return_registers.keys())
    iterator = 0
    for register in operands:
        emulator.runtime_env.set_register(register,return_registers[return_registers_keys[iterator]])
        iterator = iterator+1