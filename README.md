
# Funkdat

Funkdat is a Python script that finds a specified function within a repository and extracts the function along with all related code, such as classes and methods that are called within the target function. The extracted code is then merged into a single output file. This tool is useful for understanding and analyzing the functionality and dependencies of a specific function within a larger codebase.  For open source projects, this can be particularly helpful to analyse code with OpenAI Chat.

**Features:**

- Locate specific functions in a code repository
- Find related functions, classes, and methods
- Control the level of recursion to explore related code
- Optional filename to start the search
- Debug mode for displaying extra output
- Output the results in a separate Python file

## Requirements
- Python 3.7 or higher

## Usage
```bash
python code_explorer.py --repo <repository_path> --function <function_name> [--filename <file_name>] [--debug] [--recursion-level <recursion_level>]
```

**Arguments:**

`--repo`: The path to the repository containing the code.

`--function`: The name of the function you want to find.

`--filename` (*optional*): The filename in which to start the search for the function.

`--debug` (*optional*): Enable debug mode to show extra output.

`--recursion-level` (*optional*): Level of recursion for finding related code (default: -1, unlimited recursion)


To run the script, use the following command:
```bash
python3 funkdat.py --repo /path/to/repo --function function_name [--filename filename] [--debug]
```

Replace `/path/to/repo` with the path to the repository you want to search, function_name with the name of the function you want to find, and `filename` with the optional filename to start the search.

Por exemplo:
```bash
python3 funkdat.py --repo /Users/me/code/django-repo --function _generic_handler --filename apps/main/django/hooks/ExampleView.py --recursion-level 2
```

This command will search for the `_generic_handler` function in the `ExampleView.py` file within the `/Users/me/code/django-repo` repository and explore related code up to 2 levels deep.

The script will create an output file named `_generic_handler_output.py` containing the target function and all related code.

Enable the `--debug` flag to print additional information about the found nodes:


## Develop in a virtual environment

```bash
python3 -m venv funkdat
source funkdat/bin/activate
python funkdat.py --repo /path/to/repo --function function_name [--filename optional_filename.py]
```