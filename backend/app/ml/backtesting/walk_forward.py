from app.ml.datasets.time_split import walk_forward_windows


class WalkForwardSplitter:
    def split(self, draws: list, initial_train_size: int):
        yield from walk_forward_windows(draws, initial_train_size)
