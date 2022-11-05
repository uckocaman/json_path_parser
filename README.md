# json_path_parser
Script that gives the path of the keys in the json file.

## Purpose

To write a json file to a sql based table, it must define the path of the keys. In large documents, this is difficult. At the same time, the probability of making mistakes is high.

## How it works?

This can be automated with the main.py script. You can convert it by entering the path of the json file as in the example below.

```
python main.py 'example_data/example_data.json'
```

## Example Output

<img width="308" alt="example_output" src="https://user-images.githubusercontent.com/33186542/198098799-62224315-58b4-4486-89b9-2f9db0f1f9bd.png">
