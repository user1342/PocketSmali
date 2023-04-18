import os
import re
import warnings

from PocketSmali.RuntimeEnviroment import RuntimeEnviroment
from PocketSmali.opcode_handlers.const_string_operand_handler import const_string_operand_handler
from PocketSmali.opcode_handlers.const_operand_handler import const_operand_handler
from PocketSmali.opcode_handlers.generic_invoke_handler import generic_invoke_handler
from PocketSmali.opcode_handlers.generic_move_handler import generic_move_handler
from PocketSmali.opcode_handlers.local_operand_handler import local_operand_handler

# Define Emulator class
class Emulator():

    # Dictionary to map opcode handlers to their respective opcodes
    dict_of_opcode_handlers ={
        "const-string": const_string_operand_handler,
        "const":const_operand_handler,
        ".local": local_operand_handler,
        "invoke": generic_invoke_handler,
        "move-result": generic_move_handler
    }

    stubs = {}  # Dictionary to store stubs

    is_verbose = False
    is_enforcing = False
    runtime_env = None
    smali_files_root_dir = None

    def __str__(self):
        # To String method
        return  "Runtime enviroment - registers '{}', string pool '{}'".format(self.runtime_env.registers, self.runtime_env.string_pool)


    # Constructor
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

    # Method to add a stub to the stubs dictionary
    def add_stub(self, path, function=None):
        self.stubs[path] = function

    # Method to emulate a single Smali instruction
    def emulate_smali_instruction(self, instruction):
        self._parse_line_of_smali_code(instruction)

    # Method to emulate a Smali method
    def emulate_smali_method(self, smali_file_path,  method_name, arguments = None):
        smali_method = self._get_method_from_smali_file(smali_file_path,  method_name)
        return self._emulate(smali_method, arguments)

    # Method to explain a Smali method
    def explain_smali_method(self, smali_file_path,  method_name, arguments = None):
        smali_method = self._get_method_from_smali_file(smali_file_path,  method_name)
        raise Exception("Not implemented")
        #TODO

    # Method to emulate a block of Smali code
    def emulate_smali_code(self, smali_code, arguments = None):
        return self._emulate(smali_code, arguments)

    # Method to explain a block of Smali code
    def explain_smali_code(self, smali_code, arguments = None):
        raise Exception("Not implemented")
        #TODO

    def _get_method_from_smali_file(self, path_to_smali_file, method_name):
        # Check if the path to the smali file is in the stubs dictionary
        if path_to_smali_file in self.stubs:
            # If it is, check if the stub function is not None, and if so, call it
            if self.stubs[path_to_smali_file] != None:
                self.stubs[path_to_smali_file]()
            return "None"  # Return "None" indicating that the method was not found

        method_contents = ''  # Initialize an empty string to store the method contents
        with open(path_to_smali_file, 'r') as f:  # Open the smali file for reading
            lines = f.readlines()  # Read all lines in the file
            is_method = False  # Initialize a boolean flag to track if we're inside a method or not
            for line in lines:
                if line.strip().startswith('.method'):  # If the line starts with '.method'
                    pattern = r'^\.method.*{}\(.*\).*'.format(
                        re.escape(method_name))  # Define a regex pattern to match the method name
                    if re.match(pattern, line):  # If the line matches the method name pattern
                        is_method = True  # Set the flag indicating we're inside a method
                        method_contents += line  # Add the line to the method contents
                elif is_method:  # If we're inside a method
                    method_contents += line  # Add the line to the method contents
                    if line.strip().startswith(
                            '.end method'):  # If the line starts with '.end method', indicating the end of the method
                        is_method = False  # Reset the flag indicating we're no longer inside a method

        if method_contents == '':
            # If the method contents are still empty, indicating that the method was not found in the current smali file
            with open(path_to_smali_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith(".super"):  # If the line starts with '.super'
                        instruction, super_path = line.split(" ")  # Split the line by space to get the superclass path
                        super_path = super_path.strip("L").replace(";", "").strip("\n")  # Clean up the superclass path

                        if super_path in self.stubs:
                            # If the superclass path is in the stubs dictionary, check if the stub function is not None, and if so, call it
                            if self.stubs[super_path] != None:
                                self.stubs[super_path]()
                            return "None"  # Return "None" indicating that the method was not found

                        super_location = self._find_directory_from_partial_path(
                            super_path)  # Call a helper function to find the directory for the superclass

                        if super_location == None:  # If the superclass directory was not found
                            return "None"  # Return "None" indicating that the method was not found

                        method_contents = self._get_method_from_smali_file(super_location,
                                                                           method_name)  # Recursively call this function with the superclass directory to search for the method

                        if method_contents == "":
                            raise Exception("No method of name '{}' found at path '{}'".format(method_name,
                                                                                               path_to_smali_file))  # If the method contents are still empty after searching the superclass, raise an exception indicating that the method was not found
                        break

        return method_contents  # Return the method contents if found, otherwise an empty string

    def _find_directory_from_partial_path(self, partial_path, root_directory=None):
        # Check if root_directory is None, if so, use default value
        if root_directory == None:
            root_directory = self.smali_files_root_dir

        # Extract the filename from partial_path
        filename = os.path.basename(partial_path)
        # Split the filename into name and extension
        filename, _ = os.path.splitext(filename)
        directory = None
        full_path = None
        # Replace dots with platform-specific separator in the parent directory
        parent_directory = os.path.dirname(partial_path).replace('.', os.sep)
        # Iterate through all directories and subdirectories under root_directory
        for root, dirnames, filenames in os.walk(root_directory):
            # Construct the full path of the parent directory
            parent_dir = os.path.normpath(os.path.join(root, parent_directory))
            # Check if the parent directory exists
            if os.path.isdir(parent_dir):
                # Set directory as the parent directory
                directory = parent_dir
                # Construct the full path of the smali file by appending filename with .smali extension
                full_path = os.path.join(directory, "{}.smali".format(filename))
                # Check if the constructed file path exists
                if os.path.isfile(full_path):
                    # If yes, break out of the loop
                    break
                else:
                    # If no, set full_path to None
                    full_path = None
        # Check if directory is None
        if directory == None:
            # If yes, raise an exception or print an error message based on self.is_enforcing flag
            if self.is_enforcing:
                raise Exception("Couldn't find directory for {}".format(partial_path))
            else:
                print("Couldn't find directory for {}".format(partial_path))
        # Return the full path of the smali file, which may be None if not found
        return full_path

    def _parse_line_of_smali_code(self, line):
        # Check for various conditions where the line can be skipped or ignored
        if not line or line.startswith("#") or line.isspace() or line.startswith("None"):
            # Skip empty lines, comments, and lines starting with "None"
            return
        elif line.startswith(".locals") or line.startswith(".param"):
            # Skip lines starting with ".locals" or ".param"
            return
        elif line.startswith(".line"):
            # Handle lines starting with ".line" if self.is_verbose flag is True
            if self.is_verbose:
                print("Emulating line '{}'".format(line.split(".line")[1]))
                return
        elif line.startswith(".end method"):
            # Skip lines starting with ".end method"
            return

        # Handle return instructions
        elif line.startswith("return"):
            # Extract return parameters from the line
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
                # Call the handler function for the opcode
                self.dict_of_opcode_handlers[instruction](opcode, operands, self.runtime_env, self)
                # Break out of the loop after finding a matching opcode handler
                break
        else:
            # If no handler is found for the opcode
            if self.is_enforcing:
                # Raise an exception if self.is_enforcing flag is True
                raise Exception("No handler for opcode '{}' found".format(opcode))
            elif self.is_verbose:
                # Print a warning message if self.is_verbose flag is True
                print("No handler for opcode '{}' found. Skipping.".format(opcode))

        if self.is_verbose:
            # Print the runtime environment information if self.is_verbose flag is True
            print("Runtime environment - registers '{}', string pool '{}'".format(self.runtime_env.registers,
                                                                                  self.runtime_env.string_pool))

    def _parse_paramiter(self, line, paramiter):
        # Split the line into tokens
        tokens = line.split()

        # Extract the opcode and operands
        opcode = tokens[0]
        register, name, filler, type = tokens[1:]

        # Remove any commas, double quotes, and semicolons from the extracted values
        register = register.replace(",", "")
        name = name.replace('"', "")
        type = type.replace(";", "")

        # Call a method to set the register value in the runtime environment
        self.runtime_env.set_register(register, paramiter, name, type)

    def _call_method(self, method_name, method_location, param_registers=None):
        # Save a copy of registers
        cached_registers = self.runtime_env.registers

        # Clear registers in the runtime environment
        self.runtime_env.registers = {}

        # Set appropriate arguments (not implemented in the code)
        if param_registers:
            pass

        # Find the directory from the partial path of the method location
        method_location = self._find_directory_from_partial_path(method_location)

        if method_location is None:
            # Restore registers
            self.runtime_env.registers = cached_registers
            return "None"

        # Call a method to emulate the Smali method with given parameters
        return_registers = self.emulate_smali_method(method_location, method_name, param_registers)

        if return_registers is not None:
            # Save the return registers in the runtime environment
            self.runtime_env.save_return_registers(return_registers)

        # Restore registers
        self.runtime_env.registers = cached_registers

    def _emulate(self, smali_code, argument_values):
        if type(smali_code) != list:
            # If smali_code is not a list, convert it to a list of lines
            smali_code = smali_code.splitlines()

        # Get parameter declaration lines
        paramiter_declaration_lines = []
        for line in smali_code:
            line = line.strip()
            if line.startswith(".param"):
                # If line starts with '.param', add it to the list of parameter declaration lines
                paramiter_declaration_lines.append(line)

        # Set 'a' args (registers for arguments)
        if argument_values is not None:
            for i in range(len(argument_values)):
                # Set the register for each argument value using 'a' register naming convention (e.g., a0, a1, a2, etc.)
                self.runtime_env.set_register(f'a{i}', argument_values[i])

        # Set parameter registers
        if paramiter_declaration_lines:
            for i in range(len(paramiter_declaration_lines)):
                if argument_values is None:
                    # If argument_values is None, call _parse_paramiter with None for argument value
                    self._parse_paramiter(paramiter_declaration_lines[i], None)
                else:
                    # Otherwise, call _parse_paramiter with corresponding argument value
                    self._parse_paramiter(paramiter_declaration_lines[i], argument_values[i])

        # Emulate Smali
        for line in smali_code:
            line = line.strip()
            return_value = self._parse_line_of_smali_code(line)
            if return_value is not None:
                # If a SMALI return-* instruction has been executed, the function should end
                return return_value
