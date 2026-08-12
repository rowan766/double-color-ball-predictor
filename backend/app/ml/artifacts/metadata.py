def build_artifact_metadata(model_key: str, train_until_issue_no: str, params: dict) -> dict:
    return {
        "model_key": model_key,
        "train_until_issue_no": train_until_issue_no,
        "params": params,
    }
