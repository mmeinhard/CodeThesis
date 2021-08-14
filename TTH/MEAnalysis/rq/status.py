from rq import Queue, Worker
from rq.contrib.legacy import cleanup_ghosts
from redis import Redis
from collections import Counter
import socket
import sys
import subprocess
import logging

def get_workers_sge():
    ret = subprocess.check_output("qstat | grep rq_worker", shell=True)
    lines = ret.split("\n")
    ids = []
    for line in lines:
        if len(line)>0:
            spl = line.split()
            _id = int(spl[0])
            ids += [_id]
    return ids

if __name__ == "__main__":
    redis_conn = Redis(host=socket.gethostname(), port=6379)
    qmain = Queue("default", connection=redis_conn)

    workers = Worker.all(connection=redis_conn)
    jobs = qmain.get_jobs()

    if "--workers" in sys.argv:
        running_ids = get_workers_sge()
        
        states = []
        for worker in Worker.all(connection=redis_conn):
            ret = redis_conn.hgetall(worker.key)
            states += [ret["state"]]
            print worker.key, ret["state"], ret.get("current_job", None), redis_conn._ttl(worker.key)
            if not int(worker._name) in running_ids:
                logging.error("worker {0} has likely died!".format(worker._name))
        print "states " +" ".join(["{0}={1}".format(k, v) for k, v in dict(Counter(states)).items()])

    if "--jobs" in sys.argv:
        jobs = qmain.get_jobs()
        for job in jobs:
            print "job", job.key, job.status
    print "{0} workers, {1} jobs".format(len(workers), len(jobs))