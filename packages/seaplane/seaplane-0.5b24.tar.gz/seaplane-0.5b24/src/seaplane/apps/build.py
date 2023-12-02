import json
import os
from typing import Any, Dict

import toml

from seaplane.config import config
from seaplane.errors import SeaplaneError
from seaplane.logs import log

from .decorators import context
from .executor import RealTaskExecutor, SchemaExecutor

PROJECT_TOML = "pyproject.toml"


def validate_project() -> None:
    """
    throws an error if the project directory isn't structured in ways
    we expect it to be.
    """
    if not os.path.exists(PROJECT_TOML):
        raise SeaplaneError(f"{PROJECT_TOML} file missing, seaplane init.")

    try:
        project = read_project_file()
        project_name = project["tool"]["poetry"]["name"]
        main = project["tool"]["seaplane"].get("main", None)

        if not os.path.exists(project_name):
            raise SeaplaneError(
                f"source file {project_name} directory missing, \
                    the source code has to live under {project_name} directory."
            )

        if not project_name or not main:
            raise SeaplaneError(f"{PROJECT_TOML} not valid.")
    except Exception as e:
        log.error_exception(e)
        raise SeaplaneError(f"Seaplane project {PROJECT_TOML} configuration is not valid.")


def read_project_file() -> Dict[str, Any]:
    file = open(PROJECT_TOML, "r")
    data = toml.loads(file.read())
    return data


def persist_schema(schema: Dict[str, Any]) -> None:
    if not os.path.exists("build"):
        os.makedirs("build")

    file_path = os.path.join("build", "schema.json")

    with open(file_path, "w") as file:
        json.dump(schema, file, indent=2)


def build() -> Dict[str, Any]:
    log.info("building...")

    validate_project()

    project_config = read_project_file()
    schema: Dict[str, Any] = {"apps": {}}

    context.set_executor(SchemaExecutor())

    for sm in context.apps:
        result = sm.func("entry_point")
        sm.return_source = result

    for sm in context.apps:
        app: Dict[str, Any] = {
            "id": sm.id,
            "entry_point": {"type": sm.type, "parameters": sm.parameters},
            "tasks": [],
            "io": {},
        }

        for c in sm.tasks:
            task = {"id": c.id, "name": c.name, "replicas": c.replicas}

            for source in c.sources:
                if not app["io"].get(source, None):
                    app["io"][source] = [c.id]
                else:
                    app["io"][source].append(c.id)

            app["tasks"].append(task)

        app["io"]["returns"] = sm.return_source
        schema["apps"][sm.id] = app

    schema["carrier_endpoint"] = config.carrier_endpoint
    schema["identity_endpoint"] = config.identify_endpoint

    persist_schema(schema)

    log.info("Apps build successfully!\n")

    context.set_executor(RealTaskExecutor(context.event_handler))

    return {"schema": schema, "config": project_config}
