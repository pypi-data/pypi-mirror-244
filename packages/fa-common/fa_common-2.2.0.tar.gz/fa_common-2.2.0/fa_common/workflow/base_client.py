from abc import ABC, abstractmethod
from typing import List, Optional, Union

from fa_common.storage import File

from .base_models import ArgoWorkflowId, ArgoWorkflowRun, ScidraModule, WorkflowProject, WorkflowRun


class WorkflowBaseClient(ABC):
    @abstractmethod
    async def run_job(
        self,
        project: WorkflowProject,
        description: str,
        module: ScidraModule,
        job_data: Union[dict, List[dict]],
        runner: str = "csiro-swarm",
        files: Union[List[File], List[List[File]]] = [],
        sync: bool = False,
        upload: bool = True,
        upload_runner: str | None = None,
    ) -> Union[WorkflowRun, ArgoWorkflowRun]:
        """
        The `run_job` function is an asynchronous function that runs a job in a workflow project using a
        specified module and job data, with options for runner, files, synchronization, and upload.


        :param files: The `files` parameter is a list of files that you want to include in the job. It
        can be either a list of `File` objects or a list of lists of `File` objects. If a single set of
        input file exists for the jobs, then use a list. If you wish to loop over a set of input files,
        then use of list of lists, where each inner list represent one set of input files.
        """

    @abstractmethod
    async def get_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[int, str, ArgoWorkflowId],
        output: bool = False,
        file_refs: bool = True,
        user_id: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> WorkflowRun:
        pass

    @abstractmethod
    async def delete_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[int, str, ArgoWorkflowId],
        user_id: Optional[str],
        namespace: Optional[str],
        force_data_delete: Optional[bool] = False,
    ):
        """
        :param force_data_delete: if True, if workflow does not exist in the records,
        it would yet continue with deletion of artifacts and output data.
        """

    @abstractmethod
    async def delete_workflow_artifacts(self, workflow_id: Union[int, str, ArgoWorkflowId]):
        pass

    @abstractmethod
    async def retry_workflow(self, workflow_id: Union[int, ArgoWorkflowId], user_id: Optional[str] = None):
        pass

    @abstractmethod
    async def get_workflow_log(
        self,
        workflow_id: Union[int, ArgoWorkflowId],
        bucket_id: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        pass

    @abstractmethod
    async def get_job_log(
        self, job_id: Union[int, str], workflow_id: Union[int, ArgoWorkflowId, None] = None, user_id: Optional[str] = None
    ):
        pass
