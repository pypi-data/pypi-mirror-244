
from dataclasses import asdict, dataclass


@dataclass
class ComparerResult:
    true_positives: int
    false_positives: int
    false_negatives: int

    PPV: float = None
    sensitivity: float = None
    f1_score: float = None

    def __post_init__(self):
        self.PPV = self._get_PPV()
        self.sensitivity = self._get_sensitivity()
        self.f1_score = self._get_f1_score()

    def _get_PPV(self) -> float:
        if self.true_positives + self.false_positives == 0:
            return 0
        return round(self.true_positives / (self.true_positives + self.false_positives), 3)

    def _get_sensitivity(self) -> float:
        if self.true_positives + self.false_negatives == 0:
            return 0
        return round(self.true_positives / (self.true_positives + self.false_negatives), 3)

    def _get_f1_score(self) -> float:
        if self.sensitivity + self.PPV == 0:
            return 0
        return round(2 * self.PPV * self.sensitivity / (self.sensitivity + self.PPV), 3)

    def asdict(self):
        return asdict(self)

    def get_metric(self, metric: str, *args):
        if metric == 'PPV':
            return self.PPV
        elif metric == 'Sensitivity':
            return self.sensitivity
        elif metric == 'F1 Score':
            return self.f1_score
        else:
            raise Exception('Unknown metric')
