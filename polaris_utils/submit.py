import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Any, Optional, Union

import jinja2
from pydantic import BaseModel, validator

PathLike = Union[Path, str]


class HPCSettings(BaseModel):
    allocation: str
    queue: str
    time: str
    nodes: int
    job_name: str
    filesystems: str
    workdir: Path
    command: str
    extras: Optional[str]
    binding_script: Optional[PathLike]
    nranks_per_node: int = 1
    ndepth: int = 64

    @validator("workdir")
    def workdir_exists(cls, v: Path) -> Path:
        v = v.resolve()
        v.mkdir(exist_ok=True, parents=True)
        return v

    # Commenting out for now to see if we can get this to work without it, Sams script say it is not needed
    def _nonfunc__init__(__pydantic_self__, **data: Any) -> None:
        nranks_per_node = data.get("nranks_per_node")
        if nranks_per_node == 1:
            binding_script = (
                Path(__file__).resolve().parent
                / "templates"
                / "run-polaris-node-level.sh"
            )
        elif nranks_per_node == 4:
            binding_script = (
                Path(__file__).resolve().parent
                / "templates"
                / "run-polaris-gpu-level.sh"
            )
        else:
            binding_script = ""
        super().__init__(binding_script=binding_script, **data)


def format_and_submit(template_name: str, settings: HPCSettings) -> None:
    """Add settings to a submit script and submit to HPC scheduler"""

    env = jinja2.Environment(
        loader=jinja2.PackageLoader("polaris_utils"),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )

    try:
        template = env.get_template(template_name + ".j2")
    except jinja2.exceptions.TemplateNotFound:
        raise ValueError(f"template {template_name} not found.")

    submit_script = template.render(settings.dict())

    launchers = {"polaris": "qsub"}
    suffixs = {"polaris": "pbs"}

    sbatch_script = settings.workdir / f"{settings.job_name}.{suffixs[template_name]}"
    with open(sbatch_script, "w") as f:
        f.write(submit_script)

    subprocess.run(f"{launchers[template_name]} {sbatch_script}".split())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-T", "--template", default="polaris")
    parser.add_argument("-a", "--allocation", default="RL-fold")
    parser.add_argument("-q", "--queue", default="debug")
    parser.add_argument("-t", "--time", default="01:00:00")
    parser.add_argument("-n", "--nodes", default=1, type=int)
    parser.add_argument("-j", "--job_name", default="polaris_submission")
    parser.add_argument("-w", "--workdir", default=Path("."), type=Path)
    parser.add_argument("-f", "--filesystems", default="home:eagle", type=str)
    parser.add_argument("--nranks_per_node", type=int, default=1)
    parser.add_argument("--ndepth", type=int, default=64)
    parser.add_argument("--binding_script", type=Path)
    parser.add_argument(
        "--command",
        type=str,
        required=True,
        help="Command to run, esape with quotes for commands with arguments",
    )
    parser.add_argument(
        "--extras",
        type=str,
        help="Extra configuration in pbs script. Could be loading conda env or other modules. Escape with quotes",
    )
    args = parser.parse_args()

    settings = HPCSettings(
        allocation=args.allocation,
        queue=args.queue,
        time=args.time,
        nodes=args.nodes,
        filesystems=args.filesystems,
        job_name=args.job_name,
        workdir=args.workdir,
        binding_script=args.binding_script,
        command=args.command,
        extras=args.extras,
        nranks_per_node=args.nranks_per_node,
        ndepth=args.ndepth,
    )

    # Log command for reproducibility
    with open("command.log", "w") as f:
        f.write(" ".join(sys.argv))

    format_and_submit(args.template, settings)
