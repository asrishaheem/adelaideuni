def prepare_cudnn(deterministic: bool = None, benchmark: bool = None) -> None:
    """
    From: https://github.com/catalyst-team/catalyst/blob/master/catalyst/utils/torch.py

    Prepares CuDNN benchmark and sets CuDNN
    to be deterministic/non-deterministic mode
    Args:
        deterministic: deterministic mode if running in CuDNN backend.
        benchmark: If ``True`` use CuDNN heuristics to figure out
            which algorithm will be most performant
            for your model architecture and input.
            Setting it to ``False`` may slow down your training.
    """
    if torch.cuda.is_available():
        # CuDNN reproducibility
        # https://pytorch.org/docs/stable/notes/randomness.html#cudnn
        if deterministic is None:
            deterministic = (
                os.environ.get("CUDNN_DETERMINISTIC", "True") == "True"
            )
        cudnn.deterministic = deterministic

        # https://discuss.pytorch.org/t/how-should-i-disable-using-cudnn-in-my-code/38053/4
        if benchmark is None:
            benchmark = os.environ.get("CUDNN_BENCHMARK", "True") == "True"
        cudnn.benchmark = benchmark


__all__ = [
    "prepare_cudnn",
]
