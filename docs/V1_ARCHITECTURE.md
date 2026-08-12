# V1 Architecture

This repository is a monorepo with a separated FastAPI backend and React frontend.

The V1 priority is a correct experiment loop:

1. Store historical draw data.
2. Compute features without future leakage.
3. Train models through a shared interface.
4. Produce red and blue ball probabilities.
5. Generate candidate tickets from probabilities.
6. Run walk-forward backtests.
7. Compare every model with the random baseline.

Deep learning models are intentionally out of scope for V1.
