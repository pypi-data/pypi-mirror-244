"""
@SUGGESTION:
 - Keeping enums separate from models. enums are constants and they do not have any dependencies.
 - Noticed that sometimes keeping them together could cause circular dependencies.
 - If agreed, we can start refactoring this.
"""


from enum import Enum


class StorageType(str, Enum):
    MINIO = "MINIO"
    GCP_STORAGE = "GCP_STORAGE"
    FIREBASE_STORAGE = "FIREBASE_STORAGE"
    NONE = "NONE"


class WorkflowEnums:
    class TYPE(str, Enum):
        GITLAB = "GITLAB"
        ARGO = "ARGO"
        NONE = "NONE"

    class TEMPLATES(str, Enum):
        UPLOAD = "upload-template"
        DOWNLOAD = "download-template"
        RUN = "run-template"
        ARCHIVE = "archive-workflow-template"

    class TEMPLATE_FORMATS(str, Enum):  # noqa: N801
        TEXT = "text"
        YAML = "yaml"
        JSON = "json"

    class FileAccess:
        STORAGE = StorageType

        class METHOD(str, Enum):
            DIRECT = "direct"
            SIGNED_URL = "signed-url"

        # class STORAGE(str, Enum):
        #     GCS = "gcs"
        #     S3 = "S3"

        class ACCESS_TYPE(str, Enum):  # noqa: N801
            WITH_ROLE = "WITH_ROLE"
            WITH_SECRET = "WITH_SECRET"

    class Upload:
        class STRATEGY(str, Enum):
            ONE_GO = "one-go"  # This option uploads outputs of all jobs once all jobs are completed successfully.
            EVERY = "every"  # This option uploads outputs of each job the moment it is done successfully.

        class LOC_NAME(str, Enum):  # noqa: N801
            TASK_NAME = "task-name"
            POD_NAME = "pod-name"

    class Run:
        class STRATEGY(str, Enum):
            NODAL = "nodal"
            GLOBAL = "global"

    class Logging:
        class STRATEGY(str, Enum):
            FROM_ARTIFACT = "from-artifact"  # This option outputs the log as an artifact and passes it to the upload task.
            FROM_POD = "from-pod"  # This option directly refers to the argo log location within the pod.
