# functiongroup
FunctionGroup is a Python utility designed to simplify the implementation of protocols using pure functions. If you've ever found yourself creating classes solely to group related functions when implementing protocols, this package offers an elegant solution.

## Example

Let's consider a scenario where you have a protocol for saving and loading dictionaries, like the `DictIO` example below:

```python
from typing import Protocol


class DictIO(Protocol):
    def save_dict(self, dict_: dict[str, str], file_name: str) -> None:
        ...

    def load_dict(self, file_name: str) -> dict[str, str]:
        ...
```

Traditionally, you'd implement this protocol by creating a class:

```python
import json


class JsonDictIO(DictIO):
    def save_dict(self, dict_: dict[str, str], file_name: str) -> None:
        with open(file_name, "w") as f:
            json.dump(dict_, f)

    def load_dict(self, file_name: str) -> dict[str, str]:
        with open(file_name) as f:
            return json.load(f)

dict_io = JsonDictIO()
```

However, you may wonder why you need a class when you're not modifying its state or using any dunder methods. You're essentially using the class to group related functions, so why not use a `FunctionGroup` instead?

```python
from functiongroup import FunctionGroup


json_dict_io = FunctionGroup()

@json_dict_io.register
def save_dict(dict_: dict[str, str], file_name: str) -> None:
    with open(file_name, "w") as f:
        json.dump(dict_, f)


@json_dict_io.register
def load_dict(file_name: str) -> dict[str, str]:
    with open(file_name) as f:
        return json.load(f)

dict_io = json_dict_io()
```

This approach encourages a more functional code style and provides all the advantages of pure functions.
