import abc
import subprocess
from time import sleep

class AbstractMonitor(abc.ABC):

    def __init__(self, username: str, jobids: list, jobnames=[]):
        self.username = username
        self.jobids = jobids
        self.jobnames = jobnames
        self.status_cmd = None
        self.status_list = None

    def add_job(self, jobid, jobnames=None):
        if len(self.jobnames) != 0:
            if jobnames is None:
                self.jobnames.append("no_name")
            else:
                self.jobnames.append(jobnames)
        self.jobids.append(jobids)

    def add_jobs(self, jobids: list, jobnames=[]):
        if len(jobnames) != len(jobids):
            for i in jobids:
                self.add_job(i, None)
        else:
            for i, n in zip(jobids, jobnames):
                self.add_job(i, n)

    def update_jobs(self, jobids: list, jobnames=[]):
        self.jobids = jobids
        self.jobnames = jobnames

    def update(self, jobids: list, jobnames=[]):
        self.update_jobs(jobids, jobnames)

    @abc.abstractmethod
    def _get_current_job_list(self):
        pass

    def wait_on_job(self, jobid, sleep_secs=1):
        while True:
            job_list = self._get_current_job_list()
            if jobid not in job_list:
                break
            sleep(sleep_secs)

    def wait(self, sleep_secs=1):
        for j in self.jobids:
            self.wait_on_job(j, sleep_secs)

    @abc.abstractmethod
    def _get_job_query_cmd(self, jobid):
        pass

    def query_job_status(self, jobid):
        proc = subprocess.Popen(self._get_job_query_cmd(jobid), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stdout.read().decode("utf-8")
        err = proc.stderr.read().decode("utf-8")
        return (out, err)

    @abc.abstractmethod
    def _get_user_query_cmd(self):
        pass

    def query_user_jobs(self):
        proc = subprocess.Popen(self._get_user_query_cmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stdout.read().decode("utf-8")
        err = proc.stderr.read().decode("utf-8")
        return (out, err)