from enum import Enum


class CloudBaseImage(str, Enum):
    AWS = "benmotevalli/aws-jq-curl"
    GUTILS = "benmotevalli/gsutil-jq-curl"


class ModuleType(str, Enum):
    SYNC = "sync"  # Is run via a service call
    ASYNC = "async"  # Is executed via gitlab ci


class JobAction(str, Enum):
    PLAY = "play"
    RETRY = "retry"
    DELETE = "delete"
    CANCEL = "cancel"


class JobSecretTypes(str, Enum):
    ENV = "ENV"
    MOUNT = "MOUNT"


class JobStatus(str, Enum):
    NOT_SET = ""
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"  # argo, gitlab
    RUNNING = "RUNNING"  # argo, gitlab
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"  # argo, gitlab
    SUCCEEDED = "SUCCEEDED"  # argo


class ArgoWorkflowStoreType(str, Enum):
    LIVE = "live"
    ARCHIVE = "archive"
    DB = "db"
