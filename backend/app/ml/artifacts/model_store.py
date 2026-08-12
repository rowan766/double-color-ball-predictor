import pickle
from pathlib import Path


class ModelStore:
    def __init__(self, root: str | Path = "artifacts/models"):
        self.root = Path(root)

    def save(self, model, metadata: dict) -> str:
        self.root.mkdir(parents=True, exist_ok=True)
        filename = (
            f"{metadata.get('model_key', 'model')}-"
            f"{metadata.get('train_until_issue_no', 'unknown')}.pkl"
        )
        path = self.root / filename
        with path.open("wb") as file:
            pickle.dump({"model": model, "metadata": metadata}, file)
        return str(path)

    def load(self, artifact_path: str):
        with Path(artifact_path).open("rb") as file:
            payload = pickle.load(file)
        return payload["model"], payload.get("metadata", {})
