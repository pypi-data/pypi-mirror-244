from faasmctl.util.backend import COMPOSE_BACKEND
from faasmctl.util.compose import run_compose_cmd
from faasmctl.util.config import (
    BACKEND_INI_STRING,
    get_faasm_ini_file,
    get_faasm_ini_value,
)
from invoke import task


@task(default=True, iterable=["s"])
def restart(ctx, s, ini_file=None):
    """
    Restart a running service in the cluster

    Parameters:
    - s (str, repeateble): service to get the logs from
    - ini_file (str): path to the cluster's INI file
    """
    if not ini_file:
        ini_file = get_faasm_ini_file()

    backend = get_faasm_ini_value(ini_file, "Faasm", BACKEND_INI_STRING)
    if backend != COMPOSE_BACKEND:
        raise RuntimeError(
            "Can only get a CLI shell for a cluster that is "
            "running on a '{}' backend".format(COMPOSE_BACKEND)
        )

    run_compose_cmd(ini_file, "restart {}".format(" ".join(s)))
