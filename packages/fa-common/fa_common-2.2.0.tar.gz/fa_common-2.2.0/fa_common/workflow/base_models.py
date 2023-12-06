"""
base_models.py
"""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import pytz
from dateutil import parser
from pydantic import ConfigDict, field_validator

from fa_common import CamelModel
from fa_common.storage import File

from .base_enums import ModuleType

"""
  #####  ### ####### #          #    ######     #       #######  #####     #     #####  #     #
 #     #  #     #    #         # #   #     #    #       #       #     #   # #   #     #  #   #
 #        #     #    #        #   #  #     #    #       #       #        #   #  #         # #
 #  ####  #     #    #       #     # ######     #       #####   #  #### #     # #          #
 #     #  #     #    #       ####### #     #    #       #       #     # ####### #          #
 #     #  #     #    #       #     # #     #    #       #       #     # #     # #     #    #
  #####  ###    #    ####### #     # ######     ####### #######  #####  #     #  #####     #

"""


class JobRun(CamelModel):
    id: int
    workflow_id: int
    status: str = ""
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[float] = None
    name: str = ""
    stage: Optional[str] = None
    output: Optional[Union[List, dict]] = None
    files: Optional[List[File]] = None
    log: Optional[bytes] = None
    model_config = ConfigDict(use_enum_values=True)

    def get_compare_time(self) -> datetime:
        if self.started_at is None:
            if self.status not in ["failed", "canceled", "skipped"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


class WorkflowRun(CamelModel):
    """Equivilant to  gitlab pipeline"""

    id: int
    gitlab_project_id: int
    gitlab_project_branch: str
    commit_id: str
    status: str = ""
    jobs: List[JobRun] = []
    hidden_jobs: Optional[List[JobRun]] = []
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[int] = None


class FileFieldDescription(CamelModel):
    name: str
    description: str
    valid_extensions: List[str]
    max_size: Optional[int] = None
    mandatory: bool = False


class ScidraModule(CamelModel):
    version: str = "1.0.0"
    name: str
    description: str = ""
    module_type: ModuleType = ModuleType.ASYNC
    docker_image: str
    input_schema: str = ""
    output_schema: str = ""
    input_files: List[FileFieldDescription] = []
    cpu_limit: Union[str, int, float] = "4000m"
    cpu_request: Union[str, int, float] = "1000m"
    memory_limit_gb: Union[str, int] = 8
    memory_request_gb: Union[str, int] = 2


class WorkflowProject(CamelModel):
    name: str
    user_id: str
    bucket_id: str
    gitlab_project_id: Optional[int] = None
    created: Optional[str] = None
    timezone: str = "UTC"

    @field_validator("timezone")
    @classmethod
    def must_be_valid_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError(f"{v} is not a valid timezone")
        return v


"""
 ######
 #     # ######  ####  #    # # #####  ###### #####     ######  ####  #####     ##### ###### #    # #####  #        ##   ##### # #    #  ####
 #     # #      #    # #    # # #    # #      #    #    #      #    # #    #      #   #      ##  ## #    # #       #  #    #   # ##   # #    #
 ######  #####  #    # #    # # #    # #####  #    #    #####  #    # #    #      #   #####  # ## # #    # #      #    #   #   # # #  # #
 #   #   #      #  # # #    # # #####  #      #    #    #      #    # #####       #   #      #    # #####  #      ######   #   # #  # # #  ###
 #    #  #      #   #  #    # # #   #  #      #    #    #      #    # #   #       #   #      #    # #      #      #    #   #   # #   ## #    #
 #     # ######  ### #  ####  # #    # ###### #####     #       ####  #    #      #   ###### #    # #      ###### #    #   #   # #    #  ####

"""


class InputJobTemplate(CamelModel):
    files: Optional[List[File]] = []
    parameters: str = '"{"message": "no inputs!"}"'


class JobSecrets(CamelModel):
    name: Optional[str] = None
    mount_path: Optional[str] = None


class JobTemplate(CamelModel):
    custom_id: Union[int, str] = None  # `custom_id` for reference purposes, e.g. inside the workflow or to correlate inputs/outputs
    custom_name: Optional[str] = None  # `custom_name` for reference purposes, e.g. inside the workflow or to correlate inputs/outputs
    module_name: Optional[str] = None  # `module_name`: the name of the analysis module. At present, it is used as metadata
    inputs: InputJobTemplate = None
    dependency: Optional[List[str]] = []  # dependency: List of `custom_id` which current job depends on
    folder_path_upload: Optional[str] = None  # folder_path_upload: the full folder path to upload output files to.
    image: str = None  # image: container image address
    commands_main: str = None  # `main`: main run command. Command should be provided fully.
    commands_pre: Optional[str] = "echo empty pre-command"  # `pre`: list of commands to be run prior to the main block (not implemented)
    commands_post: Optional[str] = "echo empty post-command"  # `post`: list of commands to be run after the main block (not implemented)
    resource_cpu: Union[float, str] = 0.2
    resource_memory: str = "128Mi"
    env_secrets: List[JobSecrets] = []
    mount_secrets: List[JobSecrets] = []


"""
 ######                                                                            #
 #     # ######  ####  #    # # #####  ###### #####     ######  ####  #####       # #   #####   ####   ####
 #     # #      #    # #    # # #    # #      #    #    #      #    # #    #     #   #  #    # #    # #    #
 ######  #####  #    # #    # # #    # #####  #    #    #####  #    # #    #    #     # #    # #      #    #
 #   #   #      #  # # #    # # #####  #      #    #    #      #    # #####     ####### #####  #  ### #    #
 #    #  #      #   #  #    # # #   #  #      #    #    #      #    # #   #     #     # #   #  #    # #    #
 #     # ######  ### #  ####  # #    # ###### #####     #       ####  #    #    #     # #    #  ####   ####

"""


class NodeResourceDuration(CamelModel):
    cpu: Optional[int] = None
    memory: Optional[int] = None


class Parameters(CamelModel):
    name: Optional[str] = None
    value: Optional[Union[str, int]] = None


class ArgoArtifactRepoS3(CamelModel):
    key: str


class ArgoArtifacts(CamelModel):
    name: Optional[str] = None
    path: Optional[str] = None
    s3: Optional[ArgoArtifactRepoS3] = None


class ArgoNodeInOut(CamelModel):
    parameters: Optional[List[Parameters]] = None
    artifacts: Optional[List[ArgoArtifacts]] = None


class ArgoWorkflowId(CamelModel):
    uid: Optional[str] = None
    name: Optional[str] = None


class ArgoNode(CamelModel):
    id: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    type: Optional[str] = None
    template_name: Optional[str] = None
    template_scope: Optional[str] = None
    phase: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    progress: Optional[str] = None
    resources_duration: Optional[NodeResourceDuration] = None
    children: Optional[List[str]] = None
    outbound_nodes: Optional[List[str]] = None
    inputs: Optional[ArgoNodeInOut] = None
    outputs: Optional[ArgoNodeInOut] = None

    # Extra Amendments
    pod_name: Optional[str] = None
    task_name: Optional[str] = None  # This is the task name initially defined in the manifest
    output_json: Optional[Union[List, dict]] = None
    files: Optional[List[File]] = None
    log: Optional[bytes] = None
    model_config = ConfigDict(use_enum_values=True)

    def set_pod_task_names(self):
        if self.id is not None and self.name is not None:
            # Set pod-name
            match = re.match(r"^(.*?)-(\d+)$", self.id if self.id is not None else "")
            if match:
                prefix, id_number = match.groups()
                self.pod_name = f"{prefix}-{self.template_name}-{id_number}"

            # Set task-name
            parts = self.name.split(".")
            self.task_name = parts[-1] if len(parts) > 1 else ""
        # FIXME else case

    def get_compare_time(self) -> datetime:
        if self.started_at is None:
            if self.status not in ["Failed"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


class ArgoWorkflowMetadata(CamelModel):
    name: Optional[str] = None
    generate_name: Optional[str] = None
    namespace: Optional[str] = None
    uid: Optional[str] = None
    creation_timestamp: Optional[str] = None


class ArgoWorkflowStatus(CamelModel):
    phase: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    progress: Optional[str] = None
    nodes: Optional[List[ArgoNode]] = []


T = TypeVar("T", bound="ArgoWorkflowRun")


class ArgoWorkflowRun(CamelModel):
    metadata: Optional[ArgoWorkflowMetadata] = None
    status: Optional[ArgoWorkflowStatus] = None
    spec: Optional[dict] = {}
    jobs: Optional[List[JobRun]] = []

    @classmethod
    def populate_from_res(cls: Type[T], res, fields) -> T:
        try:
            res_dict = res if isinstance(res, dict) else res.to_dict()

            init_args: Dict[str, Any] = {}
            if "metadata" in fields:
                init_args["metadata"] = ArgoWorkflowMetadata(**res_dict.get("metadata", {}))
            if "status" in fields:
                status = res_dict.get("status", {})
                if "nodes" in status:
                    nodes = []
                    for _, v in status["nodes"].items():
                        nodes.append(v)
                    status["nodes"] = nodes
                init_args["status"] = ArgoWorkflowStatus(**status)
            if "spec" in fields:
                init_args["spec"] = res_dict.get("spec", {})

            return cls(**init_args)
        except Exception as e:
            raise ValueError("Could not parse response") from e
