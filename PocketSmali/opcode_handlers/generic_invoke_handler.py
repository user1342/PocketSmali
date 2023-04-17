import re


def generic_invoke_handler(opcode, operands, runtime_env, emulator):
    pattern = r'L(.*?);->(\w+)\((.*?)\)'

    # Extract class path and method name using regular expression
    code = operands[len(operands) - 1]
    params = operands[:len(operands)-1]
    formatted_params = []
    for param in params:
        param = param.strip("{").strip("}").strip("'").strip(",").strip("},'")
        formatted_params.append(param)


    match = re.match(pattern, code)
    if match:
        class_path = match.group(1)
        method_name = match.group(2)

        emulator._call_method(method_name, class_path, formatted_params)
    else:
        if emulator.is_enforcing:
            raise Exception("Invalid invoke call: {} - {}".format(opcode, operands))
        else:
            print("Invalid invoke call: {} - {}".format(opcode, operands))
