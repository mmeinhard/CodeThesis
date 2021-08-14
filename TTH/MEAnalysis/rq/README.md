## Running the analysis via requeue

The basic concept of the requeue (rq) based analysis environment is that you have workers
running on batch slots awaiting their instructions. The workflow controller is a
single python script running on a UI node, communicating to the workers over a server
program running on the UI. The workflow is a set of chained python commands, each of which
is submitted to the server and then dispatched to one of the workers.

~~~
            t3ui02          |   worker nodes
---------------------------------------------
launcher.py <-> server <----|---> rq-worker0
                           ...
                   ^--------|---> rq-worker2
~~~

In any terminal that you're using, use the rq-aware python environment using
`source env.sh`.

Then, in one terminal, start the server using `./server.sh 6379`, where `6379` is a port you choose for the UI. No two users can be using the same port on the same machine.

In another terminal, submit some rq jobs using `sub.sh`. Then, start the workflow using `python launcher.py --config ../data/default.cfg`.
