def jump_example(option):
    table = {
        "A": lambda: print("Jumped to branch A"),
        "B": lambda: print("Jumped to branch B"),
        "C": lambda: print("Jumped to branch C"),
    }
    action = table.get(option, lambda: print("Invalid option"))
    action()
