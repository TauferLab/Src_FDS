from abstract_monitor import AbstractMonitor
import subprocess

class LSFMonitor(AbstractMonitor):

    def __init__(self, username: str, jobids: list, jobnames=[]):
        super(LSFMonitor, self).__init__(username, jobids, jobnames)
        self.status_cmd = "bjobs"

    def _get_current_job_list(self):
        if self.status_list is None:
            self.status_list = [self.status_cmd, "-u", self.username, "-o", "jobid"]
        proc = subprocess.Popen(self.status_list, stdout=subprocess.PIPE)
        out = proc.stdout.read().decode("utf-8")
        out_list = out.split("\n")
        out_list = list(filter(lambda a: a != "", out_list))
        out_list = list(filter(lambda a: a != "JOBID", out_list))
        return out_list

    def _get_job_query_cmd(self, jobid):
        return [self.status_cmd, jobid]

    def _get_user_query_cmd(self):
        return [self.status_cmd, "-u", self.username]