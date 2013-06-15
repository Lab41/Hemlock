import hemlock

class TestClass:
    def func(self, x):
        return x + 1

    def test_one(self):
        assert self.func(3) == 5

    def test_two(self):
        assert self.func(3) == 4
