
# Funkdat
Funkdat is a Python script that finds a specified function within a repository and extracts the function along with all related code, such as classes and methods that are called within the target function. The extracted code is then merged into a single output file. This tool is useful for understanding and analyzing the functionality and dependencies of a specific function within a larger codebase, and can be particularly helpful to analyse code with OpenAI Chat.

## Requirements
- Python 3.7 or higher

## Usage
The script takes the following arguments:

`--repo`: The path to the repository containing the code.

`--function`: The name of the function you want to find.

`--filename` (*optional*): The filename in which to start the search for the function.

`--debug` (*optional*): Enable debug mode to show extra output.


To run the script, use the following command:
```bash
python3 funkdat.py --repo /path/to/repo --function function_name [--filename filename] [--debug]
```

Replace `/path/to/repo` with the path to the repository you want to search, function_name with the name of the function you want to find, and `filename` with the optional filename to start the search.

Por exemplo:
```bash
python3 funkdat.py --repo /Users/me/code/django-repo --function _generic_handler --filename apps/main/django/hooks/ExampleView.py
```

This command will search for the `_generic_handler` function in the `ExampleView.py` file within the `/Users/me/code/django-repo` repository.

The script will create an output file named `_generic_handler_output.py` containing the target function and all related code.

Enable the `--debug` flag to print additional information about the found nodes:


## Develop in a virtual environment

```bash
python3 -m venv funkdat
source funkdat/bin/activate
python funkdat.py --repo /path/to/repo --function function_name [--filename optional_filename.py]
```