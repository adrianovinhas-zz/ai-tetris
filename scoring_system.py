class ScoringSystem(type):
    _instance = None
    points = 0

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ScoringSystem, cls).__call__(*args, **kwargs)
        return cls._instance

    @abstractmethod
    def score_lines(cls):

    @abstractmethod
    def score_drop(cls):

class DefaultScoringSystem(ScoringSystem):
    __metaclass__ = ScoringSystem
