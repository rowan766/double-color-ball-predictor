def walk_forward_windows(draws: list, initial_train_size: int):
    for target_index in range(initial_train_size, len(draws)):
        yield draws[:target_index], draws[target_index]
