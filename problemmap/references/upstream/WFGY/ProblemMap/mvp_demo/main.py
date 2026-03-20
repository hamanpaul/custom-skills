from layers.basic_layer import BasicLayer
from operators.math_operator import add, multiply
from instruments.timer_tool import Timer
from patterns.simple_pattern import run_pattern
from jump_table.simple_jump import jump_example

if __name__ == "__main__":
    print("=== WFGY MVP Demo ===")

    # Layer demo
    layer = BasicLayer("ExampleLayer")
    layer.process("Hello WFGY")

    # Operators demo
    print("Add 2 + 3 =", add(2, 3))
    print("Multiply 4 * 5 =", multiply(4, 5))

    # Instruments demo
    t = Timer()
    t.start()
    _ = sum(range(1000))
    t.stop()

    # Patterns demo
    run_pattern()

    # Jump table demo
    jump_example("B")
