import os
import re
import warnings

from PocketSmali.RuntimeEnviroment import RuntimeEnviroment
from PocketSmali.opcode_handlers.const_string_operand_handler import const_string_operand_handler
from PocketSmali.opcode_handlers.const_operand_handler import const_operand_handler
from PocketSmali.opcode_handlers.generic_invoke_handler import generic_invoke_handler
from PocketSmali.opcode_handlers.generic_move_handler import generic_move_handler
from PocketSmali.opcode_handlers.local_operand_handler import local_operand_handler


class Emulator():

    # In Smali, the period (.) before the keyword local indicates that it is a directive rather than a regular
    # instruction. Smali uses directives to provide additional information to the assembler during the build process,
    # such as defining local variables, setting labels, specifying method signatures, and more. Directives are used
    # to guide the assembler and are not part of the Dalvik bytecode that is executed at runtime.
    dict_of_opcode_handlers ={
        "const-string": const_string_operand_handler,
        "const":const_operand_handler,
        ".local": local_operand_handler,
        "invoke": generic_invoke_handler,
        "move-result": generic_move_handler
    }

    stubs = {}

    is_verbose = False
    is_enforcing = False
    runtime_env = None
    smali_files_root_dir = None

    def __str__(self):
        return "Runtime environment - registers '{}', string pool '{}'".format(self.runtime_env.registers, self.runtime_env.string_pool)

    def __init__(self, smali_files_root_dir = None, is_verbose = False, is_enforcing = False):
        self.is_enforcing = is_enforcing
        self.is_verbose = is_verbose
        self.runtime_env = RuntimeEnviroment()
        self.smali_files_root_dir = smali_files_root_dir
        if smali_files_root_dir == None:
            self.smali_files_root_dir = os.getcwd()
            warnings.warn("No 'smali_files_root_dir' set, defaulting to CWD. This may have unintended behaviour. This "
                          "should be set to the root dir of your apps SMALI code.")
        else:
            self.smali_files_root_dir = smali_files_root_dir

    def add_stub(self, path, function=None):
        self.stubs[path] = function

    def emulate_smali_instruction(self, instruction):
        self._parse_line_of_smali_code(instruction)

    def emulate_smali_method(self, smali_file_path,  method_name, arguments = None):
        smali_method = self._get_method_from_smali_file(smali_file_path,  method_name)
        return self._emulate(smali_method, arguments)

    def explain_smali_method(self, smali_file_path,  method_name, arguments = None):
        smali_method = self._get_method_from_smali_file(smali_file_path,  method_name)


    def emulate_smali_code(self, smali_code, arguments = None):
        return self._emulate(smali_code, arguments)

    def explain_smali_code(self, smali_code, arguments = None):
        pass

    def _get_method_from_smali_file(self, path_to_smali_file, method_name):

        if path_to_smali_file in self.stubs:
            if self.stubs[path_to_smali_file] != None:
                self.stubs[path_to_smali_file]()
            return "None"

        method_contents = ''
        with open(path_to_smali_file, 'r') as f:
            lines = f.readlines()
            is_method = False
            for line in lines:
                if line.strip().startswith('.method'):
                    pattern = r'^\.method.*{}\(.*\).*'.format(re.escape(method_name))
                    if re.match(pattern, line):
                        is_method = True
                        method_contents += line
                elif is_method:
                    method_contents += line
                    if line.strip().startswith('.end method'):
                        is_method = False

        if method_contents == '':

            with open(path_to_smali_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith(".super"):
                        instruction, super_path = line.split(" ")
                        super_path = super_path.strip("L").replace(";","").strip("\n")

                        if super_path in self.stubs:
                            if self.stubs[super_path] != None:
                                self.stubs[super_path]()
                            return "None"

                        super_location = self._find_directory_from_partial_path(super_path)

                        if super_location == None:
                            return "None"

                        method_contents = self._get_method_from_smali_file(super_location, method_name)

                        if method_contents == "":

                            raise Exception("No method of name '{}' found at path '{}'".format(method_name, path_to_smali_file))
                        break

        return method_contents

    def _find_directory_from_partial_path(self, partial_path, root_directory = None):

        if root_directory == None:
            root_directory = self.smali_files_root_dir

        filename = os.path.basename(partial_path)
        filename, _ = os.path.splitext(filename)
        directory= None
        full_path = None
        parent_directory = os.path.dirname(partial_path).replace('.', os.sep)
        for root, dirnames, filenames in os.walk(root_directory):
            parent_dir = os.path.normpath(os.path.join(root, parent_directory))
            if os.path.isdir(parent_dir):

                directory = parent_dir
                full_path = os.path.join(directory,"{}.smali".format(filename))

                if os.path.isfile(full_path):
                    break
                else:
                    full_path = None
        if directory == None:
            if self.is_enforcing:
                raise Exception("Couldn't find directory for {}".format(partial_path))
            else:
                print("Couldn't find directory for {}".format(partial_path))

        return full_path

    def _parse_line_of_smali_code(self, line):

        if not line or line.startswith("#") or line.isspace() or line.startswith("None"):
            return
        elif line.startswith(".locals") or line.startswith(".param"):
            return
        elif line.startswith(".line"):
            if self.is_verbose:
                #print("Emulating line '{}'".format(line.split(".line")[1]))
                return
        elif line.startswith(".end method"):
            return

        # Handle return instructions
        elif line.startswith("return"):
            tokens = line.split(" ")
            return_params = tokens[1:]
            return return_params

        # Split the line into tokens
        tokens = line.split()

        # Extract the opcode and operands
        opcode = tokens[0]
        operands = tokens[1:]

        opcode = opcode.split("/")[0]

        # Run the handler for the given opcode
        for instruction in self.dict_of_opcode_handlers:
            instruction = instruction.strip()
            if opcode.startswith(instruction):
                self.dict_of_opcode_handlers[instruction](opcode, operands, self.runtime_env, self)
                break
        else:
            if self.is_enforcing:
                raise Exception("No handler for opcode '{}' found".format(opcode))
            elif self.is_verbose:
                    print("No handler for opcode '{}' found. Skipping.".format(opcode))


        if self.is_verbose:
            print("Runtime environment - registers '{}', string pool '{}'".format(self.runtime_env.registers, self.runtime_env.string_pool))

    def _parse_paramiter(self, line, paramiter):

        # Split the line into tokens
        tokens = line.split()

        # Extract the opcode and operands
        opcode = tokens[0]
        register, name, filler, type = tokens[1:]

        register = register.replace(",","")
        name = name.replace('"',"")
        type = type.replace(";","")

        self.runtime_env.set_register(register,paramiter,name,type)

    def _call_method(self, method_name, method_location, param_registers = None):

        # Save a copy of registers
        cached_registers = self.runtime_env.registers

        self.runtime_env.registers = {}

        # Set appropriate arguments
        if param_registers:
            pass

        # Call method
        method_location = self._find_directory_from_partial_path(method_location)

        if method_location == None:
            # Restore registers
            self.runtime_env.registers = cached_registers
            return "None"

        return_registers = self.emulate_smali_method(method_location, method_name, param_registers)

        if return_registers != None:
            self.runtime_env.save_return_registers(return_registers)

        # Restore registers
        self.runtime_env.registers = cached_registers

    def _emulate(self, smali_code, argument_values):

        if type(smali_code) != list:
            smali_code = smali_code.splitlines()

        # Get params if any
        paramiter_declaration_lines = []
        for line in smali_code:
            line = line.strip()
            if line.startswith(".param"):
                paramiter_declaration_lines.append(line)

        # Set 'a' args
        if argument_values is not None:
            for i in range(len(argument_values)):
                self.runtime_env.set_register(f'a{i}',argument_values[i])

        # Set .param
        if paramiter_declaration_lines != []:
            for i in range(len(paramiter_declaration_lines)):
                if argument_values == None:
                    self._parse_paramiter(paramiter_declaration_lines[i], None)
                else:
                    self._parse_paramiter(paramiter_declaration_lines[i], argument_values[i])

        # Emulate Smali
        for line in smali_code:
            line = line.strip()
            return_value = self._parse_line_of_smali_code(line)
            if return_value != None:
                # If return value is not None then a SMALI return-* instruction has been executed and the function should end
                return return_value