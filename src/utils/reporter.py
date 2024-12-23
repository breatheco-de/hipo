class Reporter:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def get_results(self):
        return self.results