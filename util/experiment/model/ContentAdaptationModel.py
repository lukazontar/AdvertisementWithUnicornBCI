class ContentAdaptationModel:
    def __init__(self, name: str = None):
        self.name = name

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError
