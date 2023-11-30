import time
from typing import Optional

from aocd import submit
from datetime import datetime


def submit_answer(answer, part="a", dt: Optional[datetime] = None):
    if not dt:
        today = datetime.today()
        day, year = today.day, today.year
    else:
        day, year = dt.day, dt.year

    submit(answer=answer, part=part, day=day, year=year)
