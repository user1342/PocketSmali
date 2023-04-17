import re


def generic_invoke_handler(opcode, operands, runtime_env, emulator):
    # Define the regular expression pattern to match class path, method name, and parameters
    pattern = r'L(.*?);->(\w+)\((.*?)\)'

    # Extract the code (method invocation) and parameters from the operands list
    code = operands[len(operands) - 1]
    params = operands[:len(operands) - 1]

    # Format the parameters by removing unnecessary characters
    formatted_params = []
    for param in params:
        param = param.strip("{").strip("}").strip("'").strip(",").strip("},'")
        formatted_params.append(param)

    # Attempt to match the code (method invocation) against the regular expression pattern
    match = re.match(pattern, code)
    if match:
        # If the match is successful, extract the class path and method name
        class_path = match.group(1)
        method_name = match.group(2)

        # Call the _call_method() method of the emulator object with the extracted method name, class path,
        # and formatted parameters to invoke the method
        emulator._call_method(method_name, class_path, formatted_params)
    else:
        if emulator.is_enforcing:
            # If the match is unsuccessful and the emulator is in enforcing mode, raise an exception
            raise Exception("Invalid invoke call: {} - {}".format(opcode, operands))
        else:
            # If the match is unsuccessful and the emulator is not in enforcing mode, print a warning message
            print("Invalid invoke call: {} - {}".format(opcode, operands))