import traceback


def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = f"py\n{traceback}{type(err).__name__}: {err}\n"

    return error if advance else f'{type(err).__name__}: {err}'
