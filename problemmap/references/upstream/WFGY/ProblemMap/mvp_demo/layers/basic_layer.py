class BasicLayer:
    def __init__(self, name):
        self.name = name

    def process(self, data):
        print(f"[Layer: {self.name}] Processing data → {data}")
