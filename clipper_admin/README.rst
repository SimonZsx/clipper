Clipper
========

Library for creating and managing a Clipper model serving Cluster.

To learn more about Clipper visit the website http://clipper.ai or check out the project on GitHub https://github.com/ucbrise/clipper.

You can contact the developers at <clipper-dev@googlegroups.com>

How to deploy APPs
---------------------------

- On local host

``python3 general_start.py --dag [[DAG_FORMATTED_FILE]] --name [[APP_NAME]]``

One may replace the ``--dag`` by ``-d`` and ``--name`` by ``-n``

- With multiple hosts

``python3 auto_set_ip.py``

``python3 cluster_general_start.py --dag [[DAG_FORMATTER_FILE]] --name [[APP_NAME]]``
