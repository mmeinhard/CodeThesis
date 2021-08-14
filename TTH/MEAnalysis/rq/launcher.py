import logging

from redis import Redis
import rq
from rq import Queue
from rq import push_connection, get_failed_queue, Worker
from job import count, sparse, plot, makecategory, makelimits, mergeFiles, validateFiles
import socket

import time, os, sys
from collections import Counter
import uuid
import cPickle as pickle

import subprocess

import ROOT
from TTH.MEAnalysis.samples_base import chunks
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
from TTH.Plotting.Datacards.MakeCategory import make_datacard

import numpy as np
import math

from datetime import datetime
import json
import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3f

####
# Configuation
####

def basic_job_status(jobs, workers=0):
    status = [j.status for j in jobs]
    status_counts = dict(Counter(status))
    
    sys.stdout.write("\033[K") # Clear this line
    sys.stdout.write("\033[92mstatus\033[0m {4:.2f}%\tq={0}\ts={1}\tf={2}\tE={3}\tw={5}\n".format(
        status_counts.get("queued", 0),
        status_counts.get("started", 0),
        status_counts.get("finished", 0),
        status_counts.get("failed", 0),
        100.0 * status_counts.get("finished", 0) / sum(status_counts.values()),
        workers
    ))
    sys.stdout.write("\033[F") # Cursor up one line

def get_workers_sge():
    """Gets the IDs of the running workers as reported by SGE.
    
    Returns:
        list: List of the running worker IDs
    """
    try:
        ret = subprocess.check_output("qstat | grep rq_worker", shell=True)
    except subprocess.CalledProcessError:
        logging.getLogger('launcher').error("no rq_worker SGE jobs running")
        return []
    lines = ret.split("\n")
    ids = []
    for line in lines:
        if len(line)>0:
            spl = line.split()
            _id = int(spl[0])
            ids += [_id]
    return ids

def waitJobs(jobs, redis_conn, qmain, qfail, num_retries=0, callback=basic_job_status):
    """Given a list of redis jobs, wait for them to finish and retrieve the results.
    
    Args:
        jobs (list of redis jobs): The jobs that we want to do
        redis_conn (Connection): The redis connection
        qmain (Queue): The queue on which to do work
        qfail (Queue): The queue on which failed jobs end up on
        num_retries (int, optional): The number of times to retry a failed job
        callback (function, optional):  a function jobs -> output that will be called at every polling iteration 
    
    Returns:
        TYPE: Description
    
    Raises:
        Exception: Description
    """
    done = False
    istep = 0
    perm_failed = []
    workflow_failed = False

    while not done:
        logging.getLogger('launcher').debug("queues: main({0}) failed({1})".format(len(qmain), len(qfail)))
        logging.getLogger('launcher').debug("--- all")
        
        #Check for workers that have been lost
        workers = Worker.all(connection=redis_conn)
        running_worker_ids = get_workers_sge()
        for worker in workers:
            ret = redis_conn.hgetall(worker.key)
            if not int(worker._name) in running_worker_ids:
                logging.getLogger('launcher').error(
                    "worker {0} running job {1} has died".format(worker._name, ret.get("current_job", None))
                )
                redis_conn.delete(worker.key)
                cur_job = ret.get("current_job", None)
                if cur_job:
                    logging.getLogger('launcher').error("cancelling job {0}".format(cur_job))
                    #rq.cancel_job(cur_job, redis_conn)
                    #qfail.requeue(cur_job)

        for job in jobs:
            job.refresh()
            if job.is_failed:
                logging.getLogger('launcher').debug("failed id={0} status={1} meta={2} args={3}".format(job.id, job.status, job.meta, job.args))

                #resubmit job if failed
                if job.meta["retries"] < num_retries:
                    job.meta["retries"] += 1
                    logging.getLogger('launcher').info("requeueing job {0}".format(job.id))
                    logging.getLogger('launcher').error("job error: {0}".format(job.exc_info))
                    qfail.requeue(job.id)
                else:
                    #job failed permanently, abort workflow
                    job.refresh()
                    perm_failed += [job]
                    raise Exception("job {0} failed with exception {1}".format(
                        job,
                        job.exc_info
                    ))
            
            #This can happen if the worker died
            if job.status is None:
                print "Job id={0} status is None, probably worker died, trying to requeue".format(
                    job.id
                )
                qfail.requeue(job.id)

            #if the job is done, create a unique hash from the job arguments that will be
            #used to "memoize" or store the result in the database
            if job.is_finished:
                job.refresh()
                key = (job.func.func_name, job.meta["args"])
                if job.meta["args"] != "": 
                    hkey = hash(str(key))
                    if not redis_conn.exists(hkey):
                        logging.getLogger('launcher').debug("setting key {0} in db".format(hkey))
                        redis_conn.set(hkey, pickle.dumps((job.result, job.key)))
            if job.is_started:
                logging.getLogger('launcher').debug("started id={0} status={1} meta={2} args={3}".format(job.id, job.status, job.meta, job.args))

        #count the job statuses 
        status = [j.status for j in jobs]
        status_counts = dict(Counter(status))
        logging.getLogger('launcher').debug(status_counts)

        #fail the workflow if any jobs failed permanently
        if len(perm_failed) > 0:
            logging.getLogger('launcher').error("--- fail queue has {0} items".format(len(qfail)))
            for job in qfail.jobs:
                workflow_failed = True
                logging.getLogger('launcher').error("job {0} failed with message:\n{1}".format(job.id, job.exc_info))
                qfail.remove(job.id)
        
        #workflow is done if all jobs are done
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break

        time.sleep(1)
        
        if not callback is None:
            callback(jobs, len(running_worker_ids))
        istep += 1

    if workflow_failed:
        raise Exception("workflow failed, see errors above")

    #fetch the results
    results = [j.result for j in jobs]
    return results

class JobMemoize:
    """
    Fake job instance with manually configured properties
    """
    def __init__(self, result, func, args, meta, started_at, ended_at):
        self.result = result
        self.status = "finished"
        self.func = func
        self.args = args
        self.meta = meta
        self.ended_at = ended_at
        self.started_at = started_at

    def refresh(self):
        pass

    @property
    def is_failed(self):
        return False

    @property
    def is_started(self):
        return False

    @property
    def is_finished(self):
        return True

def enqueue_nomemoize(queue, **kwargs):
    return queue.enqueue_call(**kwargs)

def enqueue_memoize(queue, **kwargs):
    """
    Check if result already exists in redis DB, then return it, otherwise compute it.
    """
    key = (kwargs.get("func").func_name, kwargs.get("meta")["args"])
    hkey = hash(str(key))
    logging.getLogger('launcher').debug("checking for key {0} -> {1}".format(hkey, str(key)))
    if redis_conn.exists(hkey):
        res, job_key = pickle.loads(redis_conn.get(hkey))
        res2 = redis_conn.hgetall(job_key)
        logging.getLogger('launcher').debug("found key {0}, res={1}".format(hkey, res))


        #job may have been forgotten by scheduler
        if res2.has_key("started_at") and res2.has_key("ended_at"):
            return JobMemoize(
                res, kwargs.get("func"), kwargs.get("args"), kwargs.get("meta"),
                datetime.strptime(res2["started_at"], "%Y-%m-%dT%H:%M:%SZ"),
                datetime.strptime(res2["ended_at"], "%Y-%m-%dT%H:%M:%SZ")
            )
        else:
            return JobMemoize(
                res, kwargs.get("func"), kwargs.get("args"), kwargs.get("meta"),
                None,
                None
            ) 
    else:
        logging.getLogger('launcher').debug("didn't find key, enqueueing")
        return queue.enqueue_call(**kwargs)

class Task(object):
    def __init__(self, workdir, name, analysis):
        self.workdir = workdir
        self.name = name
        self.analysis = analysis

    def run(self, inputs, redis_conn, qmain, qfail):
        jobs = {}
        return jobs

    def get_analysis_config(self, workdir = None):
        if not workdir:
            workdir = self.workdir
        return os.path.join(workdir, "analysis.pickle")

    def save_state(self):
        self.analysis.serialize(self.get_analysis_config())

    def load_state(self, workdir):
        self.analysis = self.analysis.deserialize(
            self.get_analysis_config(workdir)
        )

class TaskValidateFiles(Task):
    def __init__(self, workdir, name, analysis):
        """Given an analysis, creates a counter task that can be executed
        
        Args:
            workdir (string): A directory where the code will execute
            name (string): Name of the task, can be anything
            analysis (Analysis): The Analysis object as constructed from the config
        """
        super(TaskValidateFiles, self).__init__(workdir, name, analysis)
    
    def run(self, inputs, redis_conn, qmain, qfail):
        all_jobs = []
        jobs = {}
        
        for sample in self.analysis.samples:
            #create the jobs that will count the events in this sample
            _jobs = TaskValidateFiles.getGoodFiles(sample, qmain)
            jobs[sample.name] = _jobs
            all_jobs += _jobs

        #wait for the jobs to complete
        waitJobs(all_jobs, redis_conn, qmain, qfail, 0)

        #Count the total number of generated events per sample and save it
        for sample in self.analysis.samples:
            good_files = []
            for job in jobs[sample.name]:
                good_files += job.result
            logging.getLogger('launcher').info("TaskValidateFiles: sample {0} had {1} files, {2} are good".format(
                sample.name,
                len(sample.file_names),
                len(good_files),
            ))
            
            #save list of bad files
            bad_files = set(sample.file_names) - set(good_files)
            with open(self.workdir + "/{0}_bad.txt".format(sample.name), "w") as fi:
                for badfi in bad_files:
                    fi.write(badfi + "\n")
            sample.file_names = good_files
        self.save_state()
    
    @staticmethod
    def getGoodFiles(sample, queue):

        jobs = []
        if len(sample.file_names) == 0:
            raise Exception("No files specified for sample {0}".format(sample.name))

        #split the sample input files into a number of chunks based on the prescribed size
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            jobs += [
                enqueue_memoize(
                    queue,
                    func = validateFiles,
                    args = (inputs, ),
                    timeout = 2*60, #if job didn't finish in 2 minutes, consider lost
                    ttl = -1,
                    result_ttl = -1, #result lives 2h
                    meta = {"retries": 5, "args": str((inputs, ))}
                )
            ]
        logging.getLogger('launcher').info("getGoodFiles: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskNumGen(Task):
    """Counts the number of generated events for a sample
    """
    def __init__(self, workdir, name, analysis):
        """Given an analysis, creates a counter task that can be executed
        
        Args:
            workdir (string): A directory where the code will execute
            name (string): Name of the task, can be anything
            analysis (Analysis): The Analysis object as constructed from the config
        """
        super(TaskNumGen, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)
        all_jobs = []
        jobs = {}
        #Loop over all the samples defined in the analysis
        for sample in self.analysis.samples:
            jobs[sample.name] = []
            if not sample.schema == "mc":
                continue
            #create the jobs that will count the events in this sample
            _jobs = TaskNumGen.getGeneratedEvents(sample, qmain)
            jobs[sample.name] = _jobs
            all_jobs += _jobs

        #wait for the jobs to complete
        waitJobs(all_jobs, redis_conn, qmain, qfail, 0)

        #Count the total number of generated events per sample and save it
        for sample in self.analysis.samples:
            ngen = sum(
                [j.result.get("Count", 0) for j in jobs[sample.name]]
            )
            sample.ngen = int(ngen)
            logging.getLogger('launcher').info("sample.ngen {0} = {1}".format(sample.name, sample.ngen))
        self.save_state()
        return jobs

    @staticmethod
    def getGeneratedEvents(sample, queue):
        """Given a sample with a list of files, count the number of generated events in this sample
        This method is asynchronous, meaning it won't wait until the jobs are done.

        Args:
            sample (Sample): The input sample
            queue (Queue): Redis queue
        
        Returns:
            list of rq jobs: The jobs that will return the result
        """
        jobs = []
        if len(sample.file_names) == 0:
            raise Exception("No files specified for sample {0}".format(sample.name))

        #split the sample input files into a number of chunks based on the prescribed size
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            jobs += [
                enqueue_memoize(
                    queue,
                    func = count,
                    args = (inputs, ),
                    timeout = 10*60,
                    ttl = -1,
                    result_ttl = -1,
                    meta = {"retries": 5, "args": str((inputs, ))}
                )
            ]
        logging.getLogger('launcher').info("getGeneratedEvents: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparsinator(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparsinator, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        all_jobs = []
        jobs = {}
        for sample in self.analysis.samples:
            if not sample.name in [p.input_name for p in self.analysis.processes]:
                logging.getLogger('launcher').info("Skipping sample {0} because matched to any process".format(
                    sample.name
                ))
                continue
            logging.getLogger('launcher').info("Submitting sample {0} ngen={1}".format(sample.name, sample.ngen))
            jobs[sample.name] = TaskSparsinator.runSparsinator_async(
                self.get_analysis_config(workdir),
                sample,
                self.workdir
            )
            all_jobs += jobs[sample.name]
        logging.getLogger('launcher').info("waiting on sparsinator jobs")
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=self.status_callback)
        self.save_state()
        return jobs

    @staticmethod
    def status_callback(jobs, workers=0):

        basic_job_status(jobs, workers)

        res = []
        samples = set()
        runtimes = {}
        for job in jobs:
            sample_name = job.args[2]
            if not runtimes.has_key(sample_name):
                runtimes[sample_name] = []            
            k = (sample_name, job.status)
            if job.is_finished:
                if not job.ended_at is None:
                    runtimes[sample_name] += [
                        (job.ended_at - job.started_at).total_seconds()
                    ]
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            s += " | {0:.2f}s".format(np.mean(runtimes[sample]))
            stat.write(s + "\n")
        stat.close()

    @staticmethod
    def runSparsinator_async(config_path, sample, workdir):
        jobs = []
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            ofname = "{0}/sparse/{1}/sparse_{2}.root".format(
                workdir, sample.name, ijob
            )
            jobs += [
                enqueue_memoize(
                    qmain,
                    func = sparse,
                    args = (config_path, inputs, sample.name, ofname),
                    timeout = 1*60*60,
                    ttl = -1,
                    result_ttl = -1,
                    meta = {"retries": 2, "args": str((inputs, sample.name))}
                )
            ]
        logging.getLogger('launcher').info("runSparsinator: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparseMerge(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparseMerge, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        all_jobs = []
        jobs_by_sample = {}

        for sample in self.analysis.samples:
            
            if not sample.name in inputs.keys():
                print "Skipping sample", sample.name
                continue

            jobs_by_sample[sample.name] = []
            sample_results = [os.path.abspath(job.result) for job in inputs[sample.name]]
            logging.getLogger('launcher').info("sparsemerge: submitting merge of {0} files for sample {1}".format(len(sample_results), sample.name))
            outfile = os.path.abspath("{0}/sparse/sparse_{1}.root".format(workdir, sample.name))

            for ijob, sample_inputs in enumerate(chunks(sample_results, 100)):
                job = enqueue_memoize(
                    qmain,
                    func = mergeFiles,
                    args = (outfile + "." + str(ijob), sample_inputs),
                    timeout = 20*60,
                    ttl = -1,
                    result_ttl = -1,
                    meta = {"retries": 0, "args": sample_inputs}
                )
                jobs_by_sample[sample.name] += [job]
            all_jobs += jobs_by_sample[sample.name]
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        results = [j.result for j in all_jobs]
        logging.getLogger('launcher').info("sparsemerge: {0}".format(results))
        logging.getLogger('launcher').info("sparsemerge: merging final sparse out of {0} files".format(len(results)))
        final_merge = os.path.abspath("{0}/merged.root".format(workdir))
        job = enqueue_memoize(
            qmain,
            func = mergeFiles,
            args = (final_merge, results),
            timeout = 20*60,
            ttl = -1,
            result_ttl = -1,
            meta = {"retries": 2, "args": ("final", final_merge, results)}
        )
        waitJobs([job], redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        self.save_state()
        return final_merge

    @staticmethod
    def status_callback(jobs, workers=0):

        basic_job_status(jobs, workers)

        res = []
        samples = set()
        for job in jobs:
            sample_name = job.args[0]
            k = (sample_name, job.status)
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            stat.write(s + "\n")
        stat.close()

class TaskCategories(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskCategories, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)
       
        jobs = []
        #make all the datacards for all the categories
        for cat in self.analysis.categories:
            print "enqueueing {0}".format(cat.full_name)
            job = enqueue_memoize(
                qmain,
                func = makecategory,
                args = (workdir, analysis, cat, inputs),
                timeout = 20*60,
                ttl = -1,
                result_ttl = -1,
                meta = {"retries": 2, "args": ("categories", workdir, cat.full_name)}
            )
            jobs += [job]
        print "waiting on {0} jobs".format(len(jobs))
        waitJobs(jobs, redis_conn, qmain, qfail, callback=basic_job_status)

        # hadd Results
        cat_names = list(set([cat.name for cat in self.analysis.categories]))

        for cat_name in cat_names:
            logging.getLogger('launcher').info("hadd-ing: {0}".format(cat_name))
            
            process = subprocess.Popen(
                "hadd {0}/categories/{1}.root {0}/categories/{1}/*/*.root".format(workdir, cat_name),
                shell=True,
                stdout=subprocess.PIPE
            )
            process.communicate()

        # move the shape text files into the right place
        process = subprocess.Popen(
            "mv {0}/categories/*/*/*.txt {0}/categories/".format(workdir),
            shell=True,
            stdout=subprocess.PIPE
        )

        time.sleep(60) #NFS

        result = "{0}/categories".format(workdir)
        self.save_state()
        return result

class TaskPlotting(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskPlotting, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        from plots import run_plots
        self.load_state(self.workdir)
       
        run_plots(
            workdir,
            self.analysis,
            inputs,
            redis_conn,
            qmain,
            qfail
        )

class TaskLimits(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskLimits, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        # Prepare jobs
        all_jobs = []
        try:
            os.makedirs("{0}/limits".format(self.workdir))
        except OSError as e:
            logging.getLogger('launcher').error(e)
        #copy datacard files and root input files to limit directory 
        os.system("cp {0}/categories/shapes*.txt {0}/limits/".format(self.workdir))
        os.system("cp {0}/categories/*/*/*.root {0}/limits/".format(self.workdir))

        for group in self.analysis.groups.keys():
            logging.getLogger('launcher').info("submitting limit jobs for {0}".format(group))
            all_jobs += [
                qmain.enqueue_call(
                    func = makelimits,
                    args = [
                        "{0}/limits".format(self.workdir),
                        self.analysis,
                        [group]
                    ],
                    timeout = 10*60*60,
                    ttl = -1,
                    result_ttl = -1,
                    meta = {"retries": 0, "args": ""})]
            
        limits = waitJobs(all_jobs, redis_conn, qmain, qfail)
        lims_tot = {}
        for lim in limits:
            lims_tot.update(lim)

        of = open(self.workdir + "/limits.json", "w")
        of.write(json.dumps(lims_tot, indent=2))
        of.close()

        self.save_state()

class TaskTables(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskTables, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        self.load_state(self.workdir)

        of = open(self.workdir + "/yields.csv", "w")
        for groupname, group in self.analysis.groups.items():
            limit_categories = [c for c in group if c.do_limit]
            for cat in limit_categories:
                tf = ROOT.TFile(self.workdir + "/limits/{0}.root".format(cat.full_name))
                for proc in cat.out_processes:

                    #get the nominal yield
                    h = tf.Get("{0}__{1}".format(proc, cat.full_name))
                    ih = 0
                    e = ROOT.Double()
                    if h:
                        ih = h.IntegralAndError(1, h.GetNbinsX(), e)

                    #Find the prefit uncertainties on the yields
                    #Find all the yield uncertainties resulting from shape modifications
                    #symmetrize and add in quadrature
                    syst_yield_diff = {"stat": e}

                    if proc in cat.shape_uncertainties.keys():
                        for syst in cat.shape_uncertainties[proc].keys():
                            yields_updown = {}
                            for sdir in ["Up", "Down"]:
                                h = tf.Get("{0}__{1}__{2}".format(proc, cat.full_name, syst+sdir))
                                yields_updown[sdir] = 0
                                if h:
                                    yields_updown[sdir] = ih - h.Integral()
                            yield_sym = math.sqrt(yields_updown["Up"]**2 + yields_updown["Down"]**2)
                            syst_yield_diff[syst] = yield_sym
                        #Find the uncertainties from simple normalization variations
                    if proc in cat.scale_uncertainties.keys():
                        for syst in cat.scale_uncertainties[proc].keys():
                            sc = cat.scale_uncertainties[proc][syst]

                            #if uncertainty is a simple number, instead of a up/down variation
                            if isinstance(sc, float):
                                syst_yield_diff[syst] = (cat.scale_uncertainties[proc][syst] - 1.0) * ih

                    logging.getLogger('launcher').debug("syst {0}".format(syst_yield_diff))
                    tot_yield_diff = math.sqrt(sum([x**2 for x in syst_yield_diff.values()]))
                    of.write(";".join([
                        groupname,
                        cat.full_name,
                        proc,
                        "{0:.2f}".format(ih),
                        "{0:.2f}".format(syst_yield_diff["stat"]),
                        "{0:.2f}".format(tot_yield_diff)]
                    ) + "\n")
        of.close()

def make_workdir():
    workflow_id = datetime.now().isoformat().replace(":", "-").replace(".", "-") + "_" + str(uuid.uuid4())
    workdir = "results/{0}".format(workflow_id)
    os.makedirs(workdir)
    return workdir

if __name__ == "__main__":

    filelog = logging.FileHandler('launcher.log')
    filelog.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    filelog.setFormatter(formatter)
    logging.getLogger('launcher').addHandler(filelog)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('launcher').addHandler(console)

    logging.getLogger('').handlers[0].setLevel(logging.ERROR)
    logging.getLogger('launcher').setLevel(logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )
    parser.add_argument(
        '--hostname',
        action = "store",
        help = "Redis hostname",
        type = str,
        default = socket.gethostname()
    )
    parser.add_argument(
        '--port',
        action = "store",
        help = "Redis port",
        type = int,
        default = 6379
    )
    parser.add_argument(
        '--queue',
        action = "store",
        help = "Job queue",
        type = str,
        default = "EXISTING"
    )
    parser.add_argument(
        '--workdir',
        action = "store",
        help = "working directory",
        type = str,
        default = None, 
    )
    
    parser.add_argument(
        '--sparsefile',
        action = "store",
        help = "Input sparse file",
        type = str,
        default = None,
    )
    parser.add_argument(
        '--numgen',
        action = "store_true",
        help = "Run step that gets the number of generated events",
    )
    
    args = parser.parse_args()
   
    new_workflow = True
    if not args.workdir:
        workdir = make_workdir()
    else:
        new_workflow = False
        workdir = args.workdir
    logging.getLogger('launcher').info("starting workflow {0}".format(workdir))

    queue_kwargs = {}
    if args.queue == "SYNC":
        queue_kwargs["async"] = False
    # Tell RQ what Redis connection to use
    redis_conn = Redis(host=args.hostname, port=args.port)
    qmain = Queue("default", connection=redis_conn, **queue_kwargs)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    #clean queues in case they are full
    if len(qmain) > 0:
        logging.getLogger('launcher').warning("main queue has jobs, emptying")
        qmain.empty()

    if len(qfail) > 0:
        logging.getLogger('launcher').warning("fail queue has jobs, emptying")
        qfail.empty()

    #Cancel all running jobs at the workers
    workers = Worker.all(connection=redis_conn)
    for worker in workers:
        ret = redis_conn.hgetall(worker.key)
        cur_job = ret.get("current_job", None)
        if cur_job:
            rq.cancel_job(cur_job, redis_conn)
    
    if args.config.endswith("cfg"):
        analysis = analysisFromConfig(args.config)
    elif args.config.endswith("pickle"):
        analysis = Analysis.deserialize(args.config)
    else:
        Exception("Unknown analysis input file")

    tasks = []


    inputs = []
    if not args.sparsefile and args.numgen:
        tasks += [
            TaskValidateFiles(workdir, "VALIDATE", analysis),
            TaskNumGen(workdir, "NGEN", analysis),
        ]

    #Create histogram file using sparsinator.py
    #this can run several hours
    if not args.sparsefile:
        tasks += [
            TaskSparsinator(workdir, "SPARSE", analysis),
            TaskSparseMerge(workdir, "MERGE", analysis),
        ]
    #load pre-existing histogram file
    else:
        inputs = args.sparsefile

    tasks += [
        TaskCategories(workdir, "CAT", analysis),
        TaskPlotting(workdir, "PLOT", analysis),
        TaskLimits(workdir, "LIMIT", analysis),
        TaskTables(workdir, "TABLES", analysis)
    ]


    #create first analysis pickle file
    if new_workflow:
        tasks[0].save_state()

    for task in tasks:
        res = task.run(inputs, redis_conn, qmain, qfail)
        inputs = res
