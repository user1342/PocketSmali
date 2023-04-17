def generic_move_handler(opcode, operands, runtime_env, emulator):
    # Get the return registers from the emulator's runtime environment
    return_registers = emulator.runtime_env.return_registers

    # If there are no return registers, return early
    if return_registers is None:
        return

    # Get the keys of the return_registers dictionary as a list
    return_registers_keys = list(return_registers.keys())

    # Initialize an iterator for accessing return registers
    iterator = 0

    # Loop through the operands (registers to be moved)
    for register in operands:
        # Set the value of the current return register in the emulator's runtime environment
        # to the corresponding register in the operands list
        emulator.runtime_env.set_register(register, return_registers[return_registers_keys[iterator]])

        # Increment the iterator
        iterator = iterator + 1