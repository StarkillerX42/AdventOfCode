import sys
import pytest

import subprocess as sub

from pathlib import Path
from astropy.time import Time

@pytest.mark.all
def test_all_days():
    proj_dir = Path(__file__).absolute().parent.parent
    test_log = Path("./test_log.txt")
    with test_log.open('w') as log:
        log.write(proj_dir.as_posix() + '\n')
        for fil in sorted((proj_dir / "aoc").glob("day_*.py")):
            start = Time.now()
            p = sub.run(" ".join([sys.executable, fil.absolute().as_posix()]),
                        capture_output=True, shell=True)
            dt = Time.now() - start
            log.write(f"{p.returncode} {dt.sec:.3f}s {fil.as_posix()}\n")
            log.write(p.stdout.decode("utf-8"))
            p.check_returncode()


def test_all_days_verbose():
    proj_dir = Path(__file__).absolute().parent.parent
    for fil in sorted((proj_dir / "aoc").glob("day_*.py")):
        p = sub.run(" ".join(
            [sys.executable, fil.absolute().as_posix(), "-v"]
        ),
            capture_output=True, shell=True)
        p.check_returncode()
