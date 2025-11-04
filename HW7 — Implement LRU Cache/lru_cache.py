class LRUCache:
    def __init__(self, capacity: int):
        self.data = {}
        self.capacity = capacity

    def get(self, key: int) -> int:
        value = self.data.pop(key, None)  # Remove old value
        if value is None:
            return -1
        self.data[key] = value  # Insert it again to refresh the age
        return value

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data.pop(key)
        elif len(self.data) == self.capacity:
            self.data.pop(next(iter(self.data)))
        self.data[key] = value

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
