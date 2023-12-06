import json
import os
from typing import List, Optional, Union

import yaml
from jinja2 import BaseLoader, Environment

from fa_common import CamelModel, get_settings
from fa_common.enums import WorkflowEnums
from fa_common.exceptions import UnImplementedError

from .base_enums import CloudBaseImage
from .base_models import JobTemplate


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
# to use with safe_dump:
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


dirname = os.path.dirname(__file__)


class ArgoTemplateConfig(CamelModel):
    # @REVIEW: We may want to move some of the below configs to ENV Vars.
    upload_strategy: WorkflowEnums.Upload.STRATEGY = WorkflowEnums.Upload.STRATEGY.EVERY
    upload_loc_name: WorkflowEnums.Upload.LOC_NAME = WorkflowEnums.Upload.LOC_NAME.POD_NAME
    run_strategy: WorkflowEnums.Run.STRATEGY = WorkflowEnums.Run.STRATEGY.GLOBAL
    save_run_logs: bool = True
    save_upload_logs: bool = True
    save_download_logs: bool = True
    continue_on_run_task_failure: bool = True
    logging_strategy: WorkflowEnums.Logging.STRATEGY = WorkflowEnums.Logging.STRATEGY.FROM_ARTIFACT
    file_access_method: WorkflowEnums.FileAccess.METHOD = WorkflowEnums.FileAccess.METHOD.DIRECT
    file_access_type: WorkflowEnums.FileAccess.ACCESS_TYPE = WorkflowEnums.FileAccess.ACCESS_TYPE.WITH_ROLE
    max_all_jobs_dependency: Optional[int] = 0
    app_input_path: str = "/app/input"
    app_output_path: str = "/app/module/output"

    def get(self):
        return self.model_dump()

    @property
    def has_secret(self) -> bool:
        return self.file_access_type == WorkflowEnums.FileAccess.ACCESS_TYPE.WITH_SECRET

    @property
    def logs_to_include(self) -> List:
        lst_logs = []
        if self.save_run_logs:
            lst_logs.append(WorkflowEnums.TEMPLATES.RUN)
        if self.save_download_logs:
            lst_logs.append(WorkflowEnums.TEMPLATES.DOWNLOAD)
        if self.save_upload_logs:
            lst_logs.append(WorkflowEnums.TEMPLATES.UPLOAD)

        return lst_logs

    @property
    def cloud_base_image(self) -> str:
        settings = get_settings()
        if settings.STORAGE_TYPE == WorkflowEnums.FileAccess.STORAGE.FIREBASE_STORAGE:
            return CloudBaseImage.GUTILS.value
        if settings.STORAGE_TYPE == WorkflowEnums.FileAccess.STORAGE.MINIO:
            return CloudBaseImage.AWS.value
        return None

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if key == "has_secret":
                raise AttributeError("has_secret is a computed property and cannot be set directly.")
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{key}'")

    def set_default(self):
        default_instance = ArgoTemplateConfig()
        for attr in vars(default_instance):
            setattr(self, attr, getattr(default_instance, attr))
        self.has_secret = self.file_access_type == WorkflowEnums.FileAccess.ACCESS_TYPE.WITH_SECRET


class ArgoTemplateGenerator:

    """
     #####  ####### #     # ####### ###  #####
    #     # #     # ##    # #        #  #     #
    #       #     # # #   # #        #  #
    #       #     # #  #  # #####    #  #  ####
    #       #     # #   # # #        #  #     #
    #     # #     # #    ## #        #  #     #
     #####  ####### #     # #       ###  #####

    """

    config: ArgoTemplateConfig = ArgoTemplateConfig()
    jinja_env: Environment = Environment(
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        loader=BaseLoader(),
    )

    """
      #####  ######  #######    #    ####### #######
     #     # #     # #         # #      #    #
     #       #     # #        #   #     #    #
     #       ######  #####   #     #    #    #####
     #       #   #   #       #######    #    #
     #     # #    #  #       #     #    #    #
      #####  #     # ####### #     #    #    #######

    """

    @classmethod
    def create(
        cls,
        workflow_name: str,
        jobs: List[JobTemplate],
        job_base: JobTemplate,
        # image_url: Optional[str] = None,
        # run_command: Optional[str] = None,
        # pre_commands: Optional[List[str]] = None,
        # post_commands: Optional[List[str]] = None,
        # cpu: Optional[Union[str,int]]=None,
        # memory: Optional[str]=None,
        has_upload: Optional[bool] = True,
    ):
        """
        @AddMe: Handle None checks.
        """
        base_template = cls.gen_base_block(workflow_name)
        download_template = cls.gen_download_template()
        # run_template      = cls.gen_run_template(image_url, pre_commands, run_command, post_commands, cpu=cpu, memory=memory, max_dependency=max_dependency)
        run_template = cls.gen_run_template(job_base)
        main_template = cls.gen_tasks_main_template(jobs, has_upload)
        arch_template = cls.get_archive_template(job_base)

        base_template["spec"]["templates"] = [main_template, download_template, run_template, arch_template]

        if has_upload:
            upload_template = cls.gen_upload_template(jobs)
            base_template["spec"]["templates"].append(upload_template)

        return base_template

    """
     ####### ####### ######     ####### ####### #     # ######  #          #    ####### #######
        #    #     # #     #       #    #       ##   ## #     # #         # #      #    #
        #    #     # #     #       #    #       # # # # #     # #        #   #     #    #
        #    #     # ######        #    #####   #  #  # ######  #       #     #    #    #####
        #    #     # #             #    #       #     # #       #       #######    #    #
        #    #     # #             #    #       #     # #       #       #     #    #    #
        #    ####### #             #    ####### #     # #       ####### #     #    #    #######

    """

    @classmethod
    def gen_base_block(cls, workflow_name: str):
        """
        This function creates the base-top block of the manifest.
        Most contents in this block are common.
        """
        # FIXME: Check with Sam. This might overlap with MINIO secrets.
        # @REVIEW

        settings = get_settings()
        params = {
            "NAME": f"{workflow_name}-",
            "SECRET_NAME": settings.STORAGE_SECRET_NAME,
            "HAS_SECRET": cls.config.has_secret,
            "ARCHIVE_TEMP_NAME": WorkflowEnums.TEMPLATES.ARCHIVE.value,
        }

        return cls._populate_template_block("template_base.yaml", params)

    @classmethod
    def get_archive_template(cls, job_base: JobTemplate):
        settings = get_settings()
        params = {
            "ARCHIVE_TEMP_NAME": WorkflowEnums.TEMPLATES.ARCHIVE.value,
            "SECRET_NAME": settings.STORAGE_SECRET_NAME,
            "SECRET_KEY": settings.STORAGE_SECRET_KEY,
            "HAS_SECRET": cls.config.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "CLOUD_BASE_IMAGE": cls.config.cloud_base_image,
            "UPLOAD_BASE_PATH": job_base.folder_path_upload,
            "ARGO_BASE_URL": settings.ARGO_URL,
            "NAMESPACE": settings.ARGO_NAMESPACE,
        }

        return cls._populate_template_block("template_archive_workflow.yaml", params)

    """
     ######  ####### #     # #     # #       #######    #    ######     #     # ####### ######  #######    ####### ####### #     # ######  #          #    ####### #######
     #     # #     # #  #  # ##    # #       #     #   # #   #     #    ##    # #     # #     # #             #    #       ##   ## #     # #         # #      #    #
     #     # #     # #  #  # # #   # #       #     #  #   #  #     #    # #   # #     # #     # #             #    #       # # # # #     # #        #   #     #    #
     #     # #     # #  #  # #  #  # #       #     # #     # #     #    #  #  # #     # #     # #####         #    #####   #  #  # ######  #       #     #    #    #####
     #     # #     # #  #  # #   # # #       #     # ####### #     #    #   # # #     # #     # #             #    #       #     # #       #       #######    #    #
     #     # #     # #  #  # #    ## #       #     # #     # #     #    #    ## #     # #     # #             #    #       #     # #       #       #     #    #    #
     ######  #######  ## ##  #     # ####### ####### #     # ######     #     # ####### ######  #######       #    ####### #     # #       ####### #     #    #    #######

    """

    @classmethod
    def gen_download_template(cls):
        if cls.config.file_access_method == WorkflowEnums.FileAccess.METHOD.SIGNED_URL:
            raise UnImplementedError("Signed url for downloading files is not yet implemented.")

        if cls.config.file_access_method is None:
            raise ValueError(
                "Download access method and storage type should be defined."
                + "Make sure config parameters (file_access_method, file_cloud_storage) are set."
            )

        settings = get_settings()

        params = {
            "TEMPLATE_NAME": WorkflowEnums.TEMPLATES.DOWNLOAD.value,
            "SECRET_NAME": settings.STORAGE_SECRET_NAME,
            "SECRET_KEY": settings.STORAGE_SECRET_KEY,
            "HAS_SECRET": cls.config.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "DOWNLOAD_LOGGING": cls.config.save_download_logs,
            "CLOUD_BASE_IMAGE": cls.config.cloud_base_image,
        }

        return cls._populate_template_block("template_download.yaml", params)

    """
     ######  #     # #     #    #     # ####### ######  #######    ####### ####### #     # ######  #          #    ####### #######
     #     # #     # ##    #    ##    # #     # #     # #             #    #       ##   ## #     # #         # #      #    #
     #     # #     # # #   #    # #   # #     # #     # #             #    #       # # # # #     # #        #   #     #    #
     ######  #     # #  #  #    #  #  # #     # #     # #####         #    #####   #  #  # ######  #       #     #    #    #####
     #   #   #     # #   # #    #   # # #     # #     # #             #    #       #     # #       #       #######    #    #
     #    #  #     # #    ##    #    ## #     # #     # #             #    #       #     # #       #       #     #    #    #
     #     #  #####  #     #    #     # ####### ######  #######       #    ####### #     # #       ####### #     #    #    #######

    """

    @classmethod
    def gen_run_template(
        cls,
        job_base: JobTemplate,
        # image_url: Optional[str] = None,
        # run_command: Optional[str] = None,
        # cpu: Optional[Union[int,str]] = None,
        # memory: Optional[str] = None,
        # max_dependency: Optional[int] = 0
    ):
        if cls.config.run_strategy is None:
            raise ValueError("Running strategy is not set!")

        settings = get_settings()  # noqa: F841

        if cls.config.run_strategy == WorkflowEnums.Run.STRATEGY.GLOBAL:
            params = {
                "APP_INPUT_PATH": cls.config.app_input_path,
                "APP_PRE_COMMAND": job_base.commands_pre,
                "APP_MAIN_COMMAND": job_base.commands_main,
                "APP_POST_COMMAND": job_base.commands_post,
                "APP_OUTPUT_PATH": cls.config.app_output_path,
                "MEMORY": job_base.resource_memory,
                "HAS_ENV_SECRETS": len(job_base.env_secrets) > 0,
                "ENV_SECRETS": job_base.env_secrets,
                "CPU": job_base.resource_cpu,
                "IMAGE_URL": job_base.image,
                "MAX_NUM": cls.config.max_all_jobs_dependency,
            }

            return cls._populate_template_block("template_run_global.yaml", params)

        if cls.config.run_strategy == WorkflowEnums.Run.STRATEGY.NODAL:
            params = {
                "HAS_ENV_SECRETS": len(job_base.env_secrets) > 0,
                "ENV_SECRETS": job_base.env_secrets,
                "APP_INPUT_PATH": cls.config.app_input_path,
                "APP_OUTPUT_PATH": cls.config.app_output_path,
                "MAX_NUM": cls.config.max_all_jobs_dependency,
            }

            return cls._populate_template_block("template_run_nodal.yaml", params)

        raise ValueError("Running strategy is unknown in the workflow!")

    """
     #     # ######  #       #######    #    ######     #     # ####### ######  #######    ####### ####### #     # ######  #          #    ####### #######
     #     # #     # #       #     #   # #   #     #    ##    # #     # #     # #             #    #       ##   ## #     # #         # #      #    #
     #     # #     # #       #     #  #   #  #     #    # #   # #     # #     # #             #    #       # # # # #     # #        #   #     #    #
     #     # ######  #       #     # #     # #     #    #  #  # #     # #     # #####         #    #####   #  #  # ######  #       #     #    #    #####
     #     # #       #       #     # ####### #     #    #   # # #     # #     # #             #    #       #     # #       #       #######    #    #
     #     # #       #       #     # #     # #     #    #    ## #     # #     # #             #    #       #     # #       #       #     #    #    #
      #####  #       ####### ####### #     # ######     #     # ####### ######  #######       #    ####### #     # #       ####### #     #    #    #######

    """

    @classmethod
    def gen_upload_template(cls, jobs: List[JobTemplate]):
        if cls.config.upload_strategy is None:
            raise ValueError(
                "Upload strategy and storage type should be defined."
                + "Make sure config parameters (upload_strategy, file_cloud_storage) are set."
            )

        settings = get_settings()

        params = {
            "TEMPLATE_NAME": WorkflowEnums.TEMPLATES.UPLOAD.value,
            "SECRET_NAME": settings.STORAGE_SECRET_NAME,
            "SECRET_KEY": settings.STORAGE_SECRET_KEY,
            "HAS_SECRET": cls.config.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "UPLOAD_LOGGING": cls.config.save_upload_logs,
            "RUN_LOGGING": cls.config.save_run_logs,
            "CLOUD_BASE_IMAGE": cls.config.cloud_base_image,
        }

        if cls.config.upload_strategy == WorkflowEnums.Upload.STRATEGY.EVERY:
            return cls._populate_template_block("template_upload_every.yaml", params)

        if cls.config.upload_strategy == WorkflowEnums.Upload.STRATEGY.ONE_GO:
            job_params = []
            for _, job in enumerate(jobs):
                job_custom_id = job.custom_id
                job_name = cls._gen_internal_job_name(job_custom_id)
                tar_path = job_name
                if cls.config.upload_loc_name == WorkflowEnums.Upload.LOC_NAME.POD_NAME:
                    tar_path = f"{cls.config.upload_loc_name.value}-{job_custom_id}"

                job_params.append(
                    {
                        "NAME": job_name,
                        "ID": job_custom_id,
                        "TAR_PATH": tar_path,
                        "UPLOAD_BASE_PATH": job.folder_path_upload,
                    }
                )

            params["JOBS"] = job_params
            return cls._populate_template_block("template_upload_one_go.yaml", params)

    """
     #     #                    #######                                                             #######
     ##   ##   ##   # #    #       #    ###### #    # #####  #        ##   ##### ######                #      ##    ####  #    #  ####
     # # # #  #  #  # ##   #       #    #      ##  ## #    # #       #  #    #   #                     #     #  #  #      #   #  #
     #  #  # #    # # # #  #       #    #####  # ## # #    # #      #    #   #   #####     #####       #    #    #  ####  ####    ####
     #     # ###### # #  # #       #    #      #    # #####  #      ######   #   #                     #    ######      # #  #        #
     #     # #    # # #   ##       #    #      #    # #      #      #    #   #   #                     #    #    # #    # #   #  #    #
     #     # #    # # #    #       #    ###### #    # #      ###### #    #   #   ######                #    #    #  ####  #    #  ####

    """

    @classmethod
    def gen_tasks_main_template(cls, jobs: List[JobTemplate], has_upload: Optional[bool] = True):
        is_nodal = cls.config.run_strategy == WorkflowEnums.Run.STRATEGY.NODAL

        TASKS_TEMP = []
        TASKS = []
        for i, job in enumerate(jobs):
            job_name = cls._gen_internal_job_name(job.custom_id)

            TASK = {
                "INDEX": i,
                "DOWNLOAD_TASK_NAME": f"download-files-{job.custom_id}",
                "DOWNLOAD_TEMPLATE_NAME": WorkflowEnums.TEMPLATES.DOWNLOAD.value,
                "DOWNLOAD_FILES": json.dumps(json.dumps([file_ref.model_dump() for file_ref in job.inputs.files])),
                "DOWNLOAD_REQUIRED": len(job.inputs.files) > 0,
                "RUN_TASK_NAME": job_name,
                "RUN_TASK_CUSTOM_ID": job.custom_id,
                "RUN_TEMPLATE_NAME": WorkflowEnums.TEMPLATES.RUN.value,
                "RUN_INPUT_PARAMS": job.inputs.parameters,
                "RUN_HAS_DEPENDENCY": len(job.dependency) > 0,
                "RUN_CONTINUE_ON": cls.config.continue_on_run_task_failure,
                "RUN_LIST_DEPENDENCY": [
                    {
                        "INDEX": ii,
                        "PAR_JOB_NAME": cls._gen_internal_job_name(par_custom_id),
                        "PAR_JOB": cls._get_job(jobs, par_custom_id),
                        "ART_NAME": cls._get_dependency_artifact_name(ii)[1],
                        "LOC_NAME": cls._get_dependency_artifact_name(ii)[0],
                    }
                    for ii, par_custom_id in enumerate(job.dependency)
                ],
                "RUN_NODAL_PARAMS": [
                    {"NAME": "IMAGE", "VALUE": job.image},
                    {"NAME": "MEMORY", "VALUE": job.resource_memory},
                    {"NAME": "CPU", "VALUE": job.resource_cpu},
                    {"NAME": "COMMAND", "VALUE": job.commands_main},
                    {"NAME": "PRE_COMMAND", "VALUE": job.commands_pre},
                    {"NAME": "POST_COMMAND", "VALUE": job.commands_post},
                ]
                if is_nodal
                else [],
                "UPLOAD_TASK_NAME": f"upload-{job.custom_id}",
                "UPLOAD_TEMPLATE_NAME": WorkflowEnums.TEMPLATES.UPLOAD.value,
                "UPLOAD_BASE_PATH": job.folder_path_upload,
            }

            if has_upload and cls.config.upload_strategy == WorkflowEnums.Upload.STRATEGY.EVERY:
                TASKS_TEMP.append(cls._populate_template_block("task_upload_every.yaml", {"TASK": TASK}))

            if TASK["DOWNLOAD_REQUIRED"]:
                TASKS_TEMP.append(cls._populate_template_block("task_download.yaml", {"TASK": TASK}))

            if TASK["RUN_HAS_DEPENDENCY"]:
                TASKS_TEMP.append(cls._populate_template_block("task_run_chained.yaml", {"TASK": TASK}))
            else:
                TASKS_TEMP.append(cls._populate_template_block("task_run_single.yaml", {"TASK": TASK}))

            TASKS.append(TASK)

        if has_upload and cls.config.upload_strategy == WorkflowEnums.Upload.STRATEGY.ONE_GO:
            TASKS_TEMP.append(cls._populate_template_block("task_upload_one_go.yaml", {"TASKS": TASKS}))

        # return TASKS
        return {"name": "main", "dag": {"tasks": TASKS_TEMP}}

    """
     ######                                       #######
     #     # ###### #      ###### ##### ######       #    ###### #    # #####  #        ##   ##### ######
     #     # #      #      #        #   #            #    #      ##  ## #    # #       #  #    #   #
     #     # #####  #      #####    #   #####        #    #####  # ## # #    # #      #    #   #   #####
     #     # #      #      #        #   #            #    #      #    # #####  #      ######   #   #
     #     # #      #      #        #   #            #    #      #    # #      #      #    #   #   #
     ######  ###### ###### ######   #   ######       #    ###### #    # #      ###### #    #   #   ######

    """

    @classmethod
    def delete_workflow_artifacts(cls, workflow_uname: str):
        manifest = cls._get_template_block("workflow_delete_artifacts.yaml", format=WorkflowEnums.TEMPLATE_FORMATS.YAML)
        manifest["spec"]["arguments"]["parameters"][0]["value"] = workflow_uname
        manifest["spec"]["templates"][0]["image"] = CloudBaseImage.AWS
        return manifest

    """
     #     #
     #     # ###### #      #####  ###### #####   ####
     #     # #      #      #    # #      #    # #
     ####### #####  #      #    # #####  #    #  ####
     #     # #      #      #####  #      #####       #
     #     # #      #      #      #      #   #  #    #
     #     # ###### ###### #      ###### #    #  ####

    """

    @classmethod
    def _gen_internal_job_name(cls, custom_id: Union[str, int]):
        return f"task-{custom_id}"

    @classmethod
    def _get_job(cls, jobs: List[JobTemplate], custom_id: Union[str, int]):
        job = list(filter(lambda job: job.custom_id == custom_id, jobs))

        if len(job) == 1:
            return job[0]
        raise ValueError(f"Cannot get a unique job with provided id: {custom_id}")

    @classmethod
    def _get_dependency_artifact_name(cls, index: int):
        loc_name = f"dep-art-loc-{index + 1}"
        art_name = f"dep-art-{index + 1}"
        return loc_name, art_name

    @classmethod
    def manifest_to_yaml(cls, template, filename=None):
        if filename is None:
            filename = f"{template['metadata']['generateName']}.yaml"

        with open(filename, "w") as outfile:
            yaml.dump(template, outfile)

    @classmethod
    def yaml_to_manifest(cls, yaml_path):
        with open(yaml_path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    def _get_template_block(cls, name: str, format: WorkflowEnums.TEMPLATE_FORMATS = WorkflowEnums.TEMPLATE_FORMATS.TEXT):  # noqa: A002
        """
        Gets yaml template from `argo-templates` folder and returns it in different formats.
        """
        if format == WorkflowEnums.TEMPLATE_FORMATS.YAML:
            return ArgoTemplateGenerator.yaml_to_manifest(os.path.join(dirname, f"argo-templates/{name}"))

        if format == WorkflowEnums.TEMPLATE_FORMATS.TEXT:
            with open(os.path.join(dirname, f"argo-templates/{name}"), "r") as f:
                return f.read()

    @classmethod
    def _populate_template_block(cls, name: str, parameters: dict):
        """
        Pass the name of template and its parameters and get back the populated template.
        """
        template_txt = cls._get_template_block(name, format=WorkflowEnums.TEMPLATE_FORMATS.TEXT)
        template_jin = cls.jinja_env.from_string(template_txt)
        return yaml.safe_load(template_jin.render(parameters))
