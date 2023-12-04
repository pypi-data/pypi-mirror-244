import os

if os.environ.get("USE_PRIVATE_API", "false") == "true":
    from yandex.cloud.priv.datasphere.v2.jobs import (
        jobs_pb2,
        jobs_pb2_grpc,
        project_job_service_pb2,
        project_job_service_pb2_grpc
    )

    from yandex.cloud.priv.datasphere.v1 import (
        operation_service_pb2,
        operation_service_pb2_grpc,
        project_pb2,
        project_service_pb2,
        project_service_pb2_grpc
    )

    from yandex.cloud.priv.operation import (
        operation_pb2
    )


else:
    from yandex.cloud.datasphere.v2.jobs import (
        jobs_pb2,
        jobs_pb2_grpc,
        project_job_service_pb2,
        project_job_service_pb2_grpc
    )

    from yandex.cloud.operation import (
        operation_service_pb2,
        operation_service_pb2_grpc
    )

    from yandex.cloud.datasphere.v2 import (
        project_pb2,
        project_service_pb2,
        project_service_pb2_grpc
    )

    from yandex.cloud.operation import (
        operation_pb2
    )
