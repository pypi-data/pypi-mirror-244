from ..pydoli import add, remove, done, edit, list_tasks, pydoli_help, version

print("Pydoli version:", version())
input("Press enter to continue...")

input("Add a task...")
add("Buy milk")
add("Buy eggs", "Buy milk and eggs")
add("Buy eggs 2", "Buy milk and eggs 2")


list_tasks()

print("\n"*100)
input("Mark task as done...")
done(1)
done(2, "3")

list_tasks()

print("\n"*100)
input("Remove task...")
remove(1)
remove(2, "3")

list_tasks()

print("\n"*100)
input("Remove all tasks...")
remove("all")

list_tasks()

print("\n"*100)
input("Edit a task...")
add("Buy milk")
add("Buy eggs")

edit(1, "Buy eggs")
edit(2, "Buy milk")

list_tasks()

print("\n"*100)

pydoli_help()