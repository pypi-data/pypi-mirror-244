import re

from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List
from .assets import trim_path_string
from colorama import just_fix_windows_console
just_fix_windows_console()


class Configure:
    def __init__(
        self,
        config_settings: Dict,
        path_config_file: str | Path,
        numeric_vars: List[str] = None,
        int_vars: List[str] = None,
        comma_sep_vars: List[str] = None,
        mandatory_vars: List[str] = None
    ) -> None:
        """
        Structure of the config file:\n
        [header] \n
        param1 = \n
        param2 = \n

        @config_settings: 
        Dictionary of which the keys are the headers and associated values are the parameters: List | Tuple

        @path_config_file:
        Pathname of the config file

        @numeric_vars
        List of the variables that are supposed to be numeric

        @mandatory_vars
        Variables whose existence in the config file are mandatory. Default all variables are mandatory
        """
        self.config_settings = config_settings
        self.path_config_file = path_config_file
        self.numeric_vars = numeric_vars
        self.int_vars = int_vars
        self.comma_sep_vars = comma_sep_vars
        self.mandatory_vars = mandatory_vars

    def prepare_input_params(self) -> Dict:
        try:
            parameters = {}
            config = ConfigParser()
            config.read(self.path_config_file)

            for header, variables_names in self.config_settings.items():
                for variable_name in variables_names:
                    variable = config.get(header, variable_name)
                    if self.mandatory_vars is None:
                        if not variable:
                            raise Exception(
                                f"Please provide information for {variable_name}\n")

                    else:
                        if variable_name in self.mandatory_vars and not variable:
                            raise Exception(
                                f"Please provide information for {variable_name}\n")

                    variable = trim_path_string(variable)
                    parameters[variable_name] = variable

            return parameters

        except Exception as e:
            raise Exception(
                f"Failed to extract input parameters\n", e)

    def handle_numerics(self, parameters: Dict):
        for key, value in parameters.items():
            if key in self.numeric_vars:
                try:
                    parameters[key] = float(value)

                except ValueError as ve:
                    raise ValueError(
                        f"Failed to convert {key} to float\n", ve)

                except Exception as e:
                    raise Exception(
                        "Unexpected error in converting str to float", e)
        return parameters

    def handle_ints(self, parameters: Dict):
        for key, value in parameters.items():
            if key in self.int_vars:
                try:
                    parameters[key] = int(value)

                except ValueError as ve:
                    raise ValueError(
                        f"Failed to convert {key} to int\n", ve)

                except Exception as e:
                    raise Exception(
                        "Unexpected error in converting str to int", e)
        return parameters

    def handle_comma_sep(self, parameters: Dict):
        for key, value in parameters.items():
            if key in self.comma_sep_vars:
                try:
                    parameters[key] = value.split(",")

                except Exception as e:
                    raise Exception(
                        "Unexpected error in converting str to int", e)
        return parameters
    

    def get_params(self) -> Dict:
        parameters = self.prepare_input_params()
        if self.numeric_vars is not None:
            parameters = self.handle_numerics(parameters)

        if self.int_vars is not None:
            parameters = self.handle_ints(parameters)

        if self.comma_sep_vars is not None:
            parameters = self.handle_comma_sep(parameters)
            
        return parameters


class ConfigureText():
    def __init__(
        self,
        path_config_file: str | Path,
        mandatory_vars: List[str],
        numeric_vars: List[str] = None,
        boolean_vars: List[str] = None,
    ) -> None:
        """
        This class is to prepare the inputs without the conventional .cfg file (no headers)
        The parameters and the value should be separated by "="
        "#" counts as comments in the text file and will NOT be processed
        """
        self.path_config_file = path_config_file
        self.mandatory_vars = mandatory_vars
        self.numeric_vars = numeric_vars
        self.boolean_vars = boolean_vars

    def prepare_input_params(self) -> Dict:
        try:
            constants = {}
            with open(self.path_config_file, "r") as f:
                for line in f:
                    if not re.search(r"^#", line) and line.strip():
                        key, var = line.strip().replace('"', '').replace("'", "").split("=")
                        key = key.strip()
                        var = var.strip()

                        if key in self.mandatory_vars and not var:
                            raise Exception(
                                "Make sure you provide information for the mandatory input params")

                        elif key in self.numeric_vars:
                            try:
                                constants[key] = float(var)
                            except Exception as e:
                                raise Exception(
                                    f"Provide a number {self.numeric_vars}", e)

                        elif key in self.boolean_vars:
                            try:
                                constants[key] = eval(var.capitalize())
                            except Exception as e:
                                raise Exception(
                                    f"Provide a boolean for {self.boolean_vars}", e)

                        else:
                            constants[key] = var

            if not constants:
                raise Exception(
                    "Please provide all the required information\n")
            return constants

        except Exception as e:
            raise Exception("Failed to extract input parameters", e)
