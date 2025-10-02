import re

from ci.praktika.info import Info

def get_ci_regression_jobs(pr_body):
    pattern = r"(#|- \[x\] +<!---ci_regression_)([|\w]+)"
    matches = []
    for match in re.findall(pattern, pr_body):
        matches.extend(match[-1].split("|"))
    return matches

if __name__ == "__main__":
    info = Info()

    info.store_kv_data("ci_regression_jobs", get_ci_regression_jobs(info.pr_body))
