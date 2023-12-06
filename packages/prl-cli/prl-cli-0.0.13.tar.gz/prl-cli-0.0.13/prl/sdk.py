import io
import json
import os
from abc import ABC, abstractmethod
from typing import Callable

import attrs
import click
from openai import OpenAI
from tqdm import tqdm

from .run import _run
from .suite import _update, pull_


@attrs.define()
class RunEvaluationResults:
    results_link: str


def parse_test_suite_id_from_url(test_suite_url: str) -> str:
    start_index = test_suite_url.find("test_suite_id=") + len("test_suite_id=")
    return test_suite_url[start_index:]


def run_evaluations(
    test_suite_url: str,
    generate_fn: Callable[[str], str],
    description="Ran automatically using the PRL SDK",
    maximum_threads=1,
    verbosity=1,
):
    test_suite_id = parse_test_suite_id_from_url(test_suite_url)
    in_mem_file = io.StringIO()

    pull_(in_mem_file, test_suite_id)

    in_mem_file.seek(0)
    suite_data = json.load(in_mem_file)

    if verbosity == 0:
        for test in suite_data["tests"]:
            test["fixed_output"] = generate_fn(test["input_under_test"])
    else:
        for test in tqdm(suite_data["tests"]):
            test["fixed_output"] = generate_fn(test["input_under_test"])

    # TODO: Going back and forth between files, strings, json etc. too much right now
    _update(test_suite_id, False, io.StringIO(json.dumps(suite_data)), True)
    run_url = _run(
        {
            "use_fixed_output": True,
            "description": description,
            "maximum_threads": maximum_threads,
        },
        test_suite_id,
    )

    if verbosity >= 1:
        click.secho(
            "Successfully updated test suite with new fixed outputs and started a new run.",
            fg="green",
        )
        click.secho(run_url, bold=True)

    return run_url
