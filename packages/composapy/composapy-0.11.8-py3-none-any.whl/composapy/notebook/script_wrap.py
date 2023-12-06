import sys
from pathlib import Path

from System import Object
from CompAnalytics.Core import ContractSerializer
from System.Collections.Generic import List, KeyValuePair
from composapy.notebook import inject
from composapy.notebook.nbr_globals import RETURN_VALUES_KEYWORD, EXECUTION_HANDLE_VAR



EXECUTION_HANDLE_VAR = "_execution_handle"
RETURN_VALUES_KEYWORD = "return_values"


def execute_script(input_script_path: str, serialized_params_path: str) -> None:
    run_directory = Path(serialized_params_path).parent
    serialized_return_values_path = Path(run_directory, "outputs.serialized")
    output_locals = {}

    with open(serialized_params_path, "r") as _file:
        serialized_json = _file.read()

    deserialized_list = ContractSerializer.Deserialize(
        serialized_json, List[KeyValuePair[str, Object]]
    )

    variables_dict = {}
    for parameter in deserialized_list:
        variables_dict[parameter.Key] = parameter.Value

    with open(input_script_path, "rb") as source_file:
        code = compile(source_file.read(), input_script_path, "exec")
    
    exec(code, variables_dict, output_locals)
    
    return_values = output_locals[RETURN_VALUES_KEYWORD]

    inject.serialize_return_values(
        variables_dict[EXECUTION_HANDLE_VAR], return_values, serialized_return_values_path.as_posix()
    )


if __name__ == "__main__":
    args = sys.argv
    input_nb_path = args[1]
    serialized_params_path = args[2]

    execute_script(input_nb_path, serialized_params_path)
