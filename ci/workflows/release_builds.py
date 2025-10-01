from praktika import Workflow

from ci.defs.defs import DOCKERS, SECRETS, ArtifactConfigs
from ci.defs.job_configs import JobConfigs
from ci.jobs.scripts.workflow_hooks.filter_job import should_skip_job

builds_for_release_branch = [
    job.unset_provides("unittest")
    for job in JobConfigs.build_jobs
    if "coverage" not in job.name
]

PRIORITY_BUILD_JOBS = [
    job.name
    for job in JobConfigs.build_jobs
    if any(
        substr in job.name
        for substr in (
            "binary",
            "release",
        )
    )
]

workflow = Workflow.Config(
    name="Release Builds",
    event=Workflow.Event.DISPATCH,
    jobs=[
        *[
            job.set_dependency(
                PRIORITY_BUILD_JOBS if job.name not in PRIORITY_BUILD_JOBS else []
            )
            for job in builds_for_release_branch
        ],
        JobConfigs.docker_sever,
        JobConfigs.docker_keeper,
        *JobConfigs.install_check_master_jobs,
        *[
            job
            for job in JobConfigs.functional_tests_jobs
            if any(t in job.name for t in ("release", "binary"))
        ],
    ],
    additional_jobs=["GrypeScan", "SignRelease", "CIReport"],
    artifacts=[
        *ArtifactConfigs.clickhouse_binaries,
        *ArtifactConfigs.clickhouse_stripped_binaries,
        *ArtifactConfigs.clickhouse_debians,
        *ArtifactConfigs.clickhouse_rpms,
        *ArtifactConfigs.clickhouse_tgzs,
    ],
    dockers=DOCKERS,
    secrets=SECRETS,
    enable_job_filtering_by_changes=False,
    enable_cache=False,
    enable_report=True,
    enable_cidb=True,
    enable_commit_status_on_failure=True,
    pre_hooks=[
        # "python3 ./ci/jobs/scripts/workflow_hooks/store_data.py",
        # "python3 ./ci/jobs/scripts/workflow_hooks/version_log.py",
    ],
    workflow_filter_hooks=[should_skip_job],
    post_hooks=[],
)

WORKFLOWS = [
    workflow,
]
