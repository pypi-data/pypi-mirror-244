import os
import json
import datetime
import sys
from platform import system
from typing import List

USER_HOME_PATH = os.path.expanduser("~")

if system() == "Windows":
    DATABASE_DIR = os.path.join(os.getenv("APPDATA"), "pydoli")
elif system() == "Linux":
    DATABASE_DIR = os.path.join(USER_HOME_PATH, ".local", "share", "pydoli")
JSON_PATH = os.path.join(DATABASE_DIR, "database.json")


def check_files():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w") as f:
            json.dump([], f, indent=4)


class Database:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        return data

    def save_with_existing_data(self, data):
        existing_data = self.load()
        existing_data.extend(data)
        with open(self.filename, "w") as f:
            json.dump(existing_data, f, indent=4)

    def save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def len(self):
        return len(self.load())


class Todo:
    VERSION = "0.1"
    NAME = "pydoli"

    def __init__(self, database):
        self.database = database

    def add(self, *args):
        """Pass the one or more tasks to add to the database"""

        if len(args) == 0:
            print("Please, insert a task")
            sys.exit(1)

        tasks = []

        len_database = self.database.len()

        for task in args:
            task = {
                "id": len_database + 1,
                "task": task,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "done": False,
            }
            len_database += 1
            tasks.append(task)
        self.database.save_with_existing_data(tasks)

    def remove(self, *args):
        """Pass the one or more ids tasks to remove from the database"""
        if len(args) == 0:
            print("Please, insert a id")
            sys.exit(1)
        
        if 'all' in args:
            self.database.save([])
            return
        
        for a in args:
            try:
                int(a)
            except ValueError:
                print(f"{a} not is an integer")
                sys.exit(1)
        
        database_data = self.database.load()
        new_data = list(filter(lambda x: str(x["id"]) not in args and x["id"] not in args, database_data))
        self.database.save(new_data)

    def list(self):
        database_data = self.database.load()
        CHECK = u'\u2713'
        CROSS = u'\u2717'
        for d in database_data:
            is_done = CHECK if d['done'] else CROSS
            print(f"{d['id']} [ {is_done} ] {d['task']} - {d['date']}")

    def edit(self, *args):
        """pass one ids and one task to edit"""
        if len(args) != 2:
            print("Please, pass one ids and the new task to edit")
            sys.exit(1)
        
        try:
            int(args[0])
        except ValueError:
            print(f"{args[0]} not is an integer")
            sys.exit(1)
        
        database_data = self.database.load()

        edited = False
        for d in database_data:
            if str(d["id"]) == args[0] or d["id"] == args[0]:
                d["task"] = args[1]
                edited = True
                break
        
        if not edited:
            print(f"{args[0]} not in database")
            sys.exit(1)
        
        self.database.save(database_data)

    def done(self, *args):
        if len(args) == 0:
            print("Please, insert a id")
            sys.exit(1)
        
        for a in args:
            try:
                int(a)
            except ValueError:
                print(f"{a} not is an integer")
                sys.exit(1)

        
        database_data = self.database.load()

        for d in database_data:
            if str(d["id"]) in args or d["id"] in args:
                d["done"] = True
        
        self.database.save(database_data)

    def help(self):
        print(
"""Usage: pydoli [PARAMETTER] [ARGS]
add [MULTIPLE TASKS]
remove [MULTIPLE IDS] or [all]
edit [ID] [NEW TASK]
done [MULTIPLE IDS]
list
help
version""")

    def version(self):
        print(self.VERSION, self.NAME)
        return

def main():
    PARAMETTERS = ["add", "remove", "list", "edit", "done", "help", "version"]
    args = sys.argv

    check_files()

    if len(args) == 1:
        pass
    elif args[1] in PARAMETTERS:
        database = Database(JSON_PATH)
        todo = Todo(database)
        if args[1] not in ["list", "help", "version"]:
            arguments = args[2::]
            getattr(todo, args[1])(*arguments)
            sys.exit()
        getattr(todo, args[1])()
    else:
        Todo(Database(JSON_PATH)).help()
        sys.exit()