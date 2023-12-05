# pydoli
A simple todo list cli

## Installation

with pip:

```
pip install pydoli
```

or arch btw:
```
in comming...
```

## Terminal Usage

```
in comming...
```

## Module Usage

Adding tasks:

```python
from pydoli import add

add("New task")
add("Second task", "Excersice", "Code")
```

Remove and done tasks:

```python
from pydoli import remove, done

remove(1, "3")
done(2, "4")
remove("all")
```

Edit task:

```python
from pydoli import edit

edit(1, "Other task")
edit("3", "Other other task")
```

List tasks:

```python
from pydoli import list_tasks

list_tasks()
```

The format of tasks:

```
<ID> [ ✓ ] <TASK> - <CREATED DATE>
<ID> [ ✗ ] <TASK> - <CREATED DATE>
```

Help and version (this is more for terminal usage):

```python
from pydoli import pydoli_help, version

pydoli_help()
version()
```

```
Usage: pydoli [PARAMETTER] [ARGS]
add [MULTIPLE TASKS]
remove [MULTIPLE IDS] or [all]
edit [ID] [NEW TASK]
done [MULTIPLE IDS]
list
help
version
```