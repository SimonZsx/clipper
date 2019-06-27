from __future__ import absolute_import, division, print_function
import logging
import docker
import tempfile
import requests
from requests.exceptions import RequestException
import json
import pprint
import time
import re
import os
import tarfile
import sys
from cloudpickle import CloudPickler
import pickle
import numpy as np


from google.protobuf.json_format import MessageToDict

if sys.version_info < (3, 0):
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    PY3 = False
else:
    from io import BytesIO as StringIO
    PY3 = True

import grpc

from .rpc import model_pb2_grpc
from .rpc import model_pb2

from .rpc import prediction_pb2_grpc
from .rpc import prediction_pb2

from .rpc import management_pb2
from .rpc import management_pb2_grpc

from .container_manager import CONTAINERLESS_MODEL_IMAGE, ClusterAdapter
from .exceptions import ClipperException, UnconnectedException
from .version import __version__, __registry__
from . import graph_parser

DEFAULT_LABEL = []
DEFAULT_PREDICTION_CACHE_SIZE_BYTES = 33554432
CLIPPER_TEMP_DIR = "/tmp/clipper"  # Used Internally for Test; Not Windows Compatible

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%y-%m-%d:%H:%M:%S',
    level=logging.INFO)

# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%y-%m-%d:%H:%M:%S',
#     level=logging.INFO)

logger = logging.getLogger(__name__)

deploy_regex_str = "[a-z0-9]([-a-z0-9]*[a-z0-9])?\Z"
deployment_regex = re.compile(deploy_regex_str)


def _validate_versioned_model_name(name, version):
    if deployment_regex.match(name) is None:
        raise ClipperException(
            "Invalid value: {name}: a model name must be a valid DNS-1123 "
            " subdomain. It must consist of lower case "
            "alphanumeric characters, '-' or '.', and must start and end with "
            "an alphanumeric character (e.g. 'example.com', regex used for "
            "validation is '{reg}'".format(name=name, reg=deploy_regex_str))
    if deployment_regex.match(version) is None:
        raise ClipperException(
            "Invalid value: {version}: a model version must be a valid DNS-1123 "
            " subdomain. It must consist of lower case "
            "alphanumeric characters, '-' or '.', and must start and end with "
            "an alphanumeric character (e.g. 'example.com', regex used for "
            "validation is '{reg}'".format(
                version=version, reg=deploy_regex_str))


class ClipperConnection(object):
    def __init__(self, container_manager):

        self.connected = False
        self.cm = container_manager

        #############TEST################

        self.runtime_dag = ""

        self.lock = False

        #################################


        self.logger = ClusterAdapter(logger, {
            'cluster_name': self.cm.cluster_identifier
        })

    def start_clipper(self,
                      mgmt_frontend_image='{}/management_frontend:{}'.format(
                          __registry__, __version__),
                      cache_size=DEFAULT_PREDICTION_CACHE_SIZE_BYTES):

        try:
            self.cm.start_clipper(mgmt_frontend_image)
                        
            # while True:
            #     try:
            #         query_frontend_url = "http://{host}/metrics".format(
            #             host=self.cm.get_query_addr())
            #         mgmt_frontend_url = "http://{host}/admin/ping".format(
            #             host=self.cm.get_admin_addr())
            #         for name, url in [('query frontend', query_frontend_url), 
            #                          ('management frontend', mgmt_frontend_url)]:
            #             r = requests.get(url, timeout=5)
            #             if r.status_code != requests.codes.ok:
            #                 raise RequestException(
            #                     "{name} end point {url} health check failed".format(name=name, url=url))
            #         break
            #     except RequestException as e:
            #         self.logger.info("Clipper still initializing: \n {}".format(e))
            #         time.sleep(1)
            self.logger.info("Clipper is running")
            self.connected = True
        except ClipperException as e:
            self.logger.warning("Error starting Clipper: {}".format(e.msg))
            raise e

    def connect(self):
        """Connect to a running Clipper cluster."""

        self.cm.connect()
        self.connected = True
        self.logger.info(
            "Successfully connected to Clipper cluster at {}".format(
                self.cm.get_query_addr()))

  
    def build_and_deploy_DAG(self,
                             name,
                             version,
                             dag_description,
                             labels):
        if not self.connected:
            raise UnconnectedException()
        

    def build_and_deploy_model(self,
                               name,
                               version,
                               input_type,
                               model_data_path,
                               base_image,
                               labels=None,
                               container_registry=None,
                               num_replicas=1,
                               batch_size=-1,
                               pkgs_to_install=None):

        if not self.connected:
            raise UnconnectedException()
        image = self.build_model(name, version, model_data_path, base_image,
                                 container_registry, pkgs_to_install)
        self.deploy_model(name, version, input_type, image, labels,
                          num_replicas, batch_size)

    def build_model(self,
                    name,
                    version,
                    model_data_path,
                    base_image,
                    container_registry=None,
                    pkgs_to_install=None):

        version = str(version)

        _validate_versioned_model_name(name, version)

        run_cmd = ''
        if pkgs_to_install:
            run_as_lst = 'RUN apt-get -y install build-essential && pip install'.split(
                ' ')
            run_cmd = ' '.join(run_as_lst + pkgs_to_install)
        with tempfile.NamedTemporaryFile(
                mode="w+b", suffix="tar") as context_file:
            # Create build context tarfile
            with tarfile.TarFile(
                    fileobj=context_file, mode="w") as context_tar:
                context_tar.add(model_data_path)
                # From https://stackoverflow.com/a/740854/814642
                try:
                    df_contents = StringIO(
                        str.encode(
                            "FROM {container_name}\n{run_command}\nCOPY {data_path} /model/\n".
                            format(
                                container_name=base_image,
                                data_path=model_data_path,
                                run_command=run_cmd)))
                    df_tarinfo = tarfile.TarInfo('Dockerfile')
                    df_contents.seek(0, os.SEEK_END)
                    df_tarinfo.size = df_contents.tell()
                    df_contents.seek(0)
                    context_tar.addfile(df_tarinfo, df_contents)
                except TypeError:
                    df_contents = StringIO(
                        "FROM {container_name}\n{run_command}\nCOPY {data_path} /model/\n".
                        format(
                            container_name=base_image,
                            data_path=model_data_path,
                            run_command=run_cmd))
                    df_tarinfo = tarfile.TarInfo('Dockerfile')
                    df_contents.seek(0, os.SEEK_END)
                    df_tarinfo.size = df_contents.tell()
                    df_contents.seek(0)
                    context_tar.addfile(df_tarinfo, df_contents)
            # Exit Tarfile context manager to finish the tar file
            # Seek back to beginning of file for reading
            context_file.seek(0)
            image = "{cluster}-{name}:{version}".format(
                cluster=self.cm.cluster_identifier, name=name, version=version)
            if container_registry is not None:
                image = "{reg}/{image}".format(
                    reg=container_registry, image=image)
            docker_client = docker.from_env()
            self.logger.info(
                "Building model Docker image with model data from {}".format(
                    model_data_path))
            image_result, build_logs = docker_client.images.build(
                fileobj=context_file, custom_context=True, tag=image)
            for b in build_logs:
                if 'stream' in b and b['stream'] != '\n':  #log build steps only
                    self.logger.info(b['stream'].rstrip())

        self.logger.info("Pushing model Docker image to {}".format(image))
        for line in docker_client.images.push(repository=image, stream=True):
            self.logger.debug(line)
        return image


    def deploy_model(self,
                     name,
                     version,
                     input_type,
                     image,
                     labels=None,
                     num_replicas=1,
                     batch_size=-1):
        if not self.connected:
            raise UnconnectedException()
        version = str(version)
        _validate_versioned_model_name(name, version)
        self.cm.deploy_model(
            name=name,
            version=version,
            input_type=input_type,
            image=image,
            num_replicas=num_replicas)
        # self.register_model(
        #     name,
        #     version,
        #     input_type,
        #     image=image,
        #     labels=labels,
        #     batch_size=batch_size)
        self.logger.info("Done deploying model {name}:{version}.".format(
            name=name, version=version))


    def connect_host(self, host_ip, host_port):
        self.cm.connect_host(host_ip, "2375")


    def add_model(self,
                  model_name,
                  model_version, 
                  image, 
                  input_type="string", 
                  output_type="string", 
                  stateful=False):

        modelinfo = management_pb2.ModelInfo(modelname=model_name,
                                             modelversion=model_version,
                                             image=image,
                                             inputtype=input_type,
                                             outputtype=output_type,
                                             stateful=stateful).SerializeToString()
                                             
        self.cm.grpc_client("zsxhku/grpcclient", "--addmodel %s %s %s "%("localhost","33333", modelinfo))

        return 

    def deploy_DAG(self, name, version, dag_description=None, runtime=""):


        if not self.connected:
            raise UnconnectedException()

       # model_info = self.get_all_models()

        dag_description_ = dag_description

        #self.logger.info("dag_description: %s"%(dag_description_))

        #if(dag_description==None):
        #    dag_description_=self.get_dag_description()

        nodes_list = graph_parser.get_all_nodes(dag_description_)

        
        container_info = []
        proxy_info = []
        backup_info = []

        count = 1
        for model_info in nodes_list:

            model_name,model_version,model_image = graph_parser.get_name_version(model_info)

            container_name, container_id, host = self.cm.add_replica(model_name, model_version, "22222", model_image, runtime=runtime)
            self.logger.info("Started %s with container %s:%s (HOST:%s)"%(model_name, container_name, container_id, host))
            container_ip = self.cm.get_container_ip(host, container_id)
            proxy_name, proxy_id = self.cm.set_proxy("mxschen/ai-proxy:latest", container_name, container_ip, host)
            ## get the ip of the instances 
            proxy_ip = self.cm.get_container_ip(host, proxy_id)

            proxy_info.append([proxy_name,proxy_id,proxy_ip])
            container_info.append([container_name, container_id, container_ip])


            if graph_parser.is_stateful(model_info):
                backup_name, backup_id, backup_host = self.cm.add_replica(model_name, model_version, "22222", model_image)
                self.logger.info("[Backup] Started %s with container %s:%s (HOST:%s)"%(model_name, backup_name, backup_id, backup_host))
                backup_ip = self.cm.get_container_ip(backup_host, backup_id)
                backup_proxy_name, backup_proxy_id = self.cm.set_proxy("mxschen/ai-proxy:latest", backup_name, backup_ip, backup_host)
                backup_proxy_ip= self.cm.get_container_ip(backup_host, backup_proxy_id)
                backup_info.append([backup_name, backup_id, backup_ip, backup_proxy_name, backup_proxy_id, backup_proxy_ip])
            else:
                backup_info.append([])

            #self.cm.check_container_status(host, container_id, 0.3, 20)
            #self.cm.check_container_status(host, proxy_id, 0.3, 20)

            #time.sleep(25)

            #self.logger.info("proxy_ip:%s"%(proxy_ip))

            self.cm.grpc_client("zsxhku/grpcclient", "--setmodel %s %s %s %s %s %s"%(proxy_ip, "22223", container_name, count, container_ip, "22222" ))
            self.logger.info('[DEPLOYMENT] Finished setting model info to proxy')
            if(graph_parser.is_stateful(model_info)):
                self.cm.grpc_client("zsxhku/grpcclient", "--setmodel %s %s %s %s %s %s"%(backup_info[-1][-1], "22223", backup_info[-1][0], count, backup_info[-1][2], "22222" ))
                self.logger.info('[DEPLOYMENT][Backup] Finished setting model info to proxy')
            count += 1
            

            # self.cm.grpc_client("zsxhku/grpcclient", "--setproxy %s %s %s %s"%(container_ip, "22222", proxy_name, "22223"))
            # self.logger.info('[DEPLOYMENT] Finished setting proxy info to model')
            # if(graph_parser.is_stateful(model_info)):
            #    self.cm.grpc_client("zsxhku/grpcclient", "--setproxy %s %s %s %s"%(backup_info[-1][2], "22222", backup_info[-1][3], "22223"))
            #    self.logger.info('[DEPLOYMENT][Backup] Finished setting proxy info to model')
 
        runtime_dag_id = name+version+str(1)

        ## Starting frontend 
        frontend_name, frontend_container_id = self.cm.add_frontend("localhost", "mxschen/frontend",runtime_dag_id, proxy_info[0][2], "22223", max_workers=2048)

        frontend_ip = self.cm.get_container_ip("localhost", frontend_container_id)

        frontend_info = [frontend_name, frontend_container_id, frontend_ip]

        self.logger.info("[DEPLOYMENT] ################ Started Frontend #################")
        #expand the dag description with the model/proxy instances info 
        expanded_dag = graph_parser.expand_dag(dag_description_, name, version, container_info, proxy_info, backup_info, frontend_info)

        self.runtime_dag = expanded_dag



        # TODO: need to modularize
        self.cm.grpc_client("zsxhku/grpcclient", "--addruntimedag %s %s %s %s %s %s %s"%('1', name, version, 'old' , self.cm.admin_ip, self.cm.admin_port, expanded_dag))


        self.logger.info("Added new runtime DAG to admin daemon\n%s"%(expanded_dag))

        #tells the proxy runtime dag info
        for tup in proxy_info:
            proxy_name = tup[0]
            proxy_id = tup[1]
            proxy_ip = tup[2]

            self.cm.grpc_client("zsxhku/grpcclient", "--setdag %s %s %s"%(proxy_ip, "22223", expanded_dag))
            self.logger.info('[DEPLOYMENT] Finished setting DAG for proxy {proxy_name} '.format(proxy_name=proxy_name))

        #tells the backups runtime dag info
        for tup in backup_info:
            if tup:
                self.cm.grpc_client("zsxhku/grpcclient", "--setdag %s %s %s"%(tup[-1], "22223", expanded_dag))
                self.logger.info('[DEPLOYMENT][Backup] Finished setting DAG for proxy {proxy_name} '.format(proxy_name=tup[-1]))



        return


    def inspect_instance(self):
        """Fetches performance metrics from the running Clipper cluster.

        Returns
        -------
        str
            The JSON string containing the current set of metrics
            for this instance. On error, the string will be an error message
            (not JSON formatted).

        Raises
        ------
        :py:exc:`clipper.UnconnectedException`
        :py:exc:`clipper.ClipperException`
        """
        


    def get_query_addr(self):
        """Get the IP address at which the query frontend can be reached request predictions.

        Returns
        -------
        str
            The address as an IP address or hostname.

        Raises
        ------
        :py:exc:`clipper.UnconnectedException`
            versions. All replicas for each version of each model will be stopped.
        """

        if not self.connected:
            raise UnconnectedException()
        return self.cm.get_query_addr()

    def stop_models(self, model_names):
        """Stops all versions of the specified models.

        This is a convenience method to avoid the need to explicitly list all versions
        of a model when calling :py:meth:`clipper_admin.ClipperConnection.stop_versioned_models`.

        Parameters
        ----------
        model_names : list(str)
            A list of model names. All replicas of all versions of each model specified in the list
            will be stopped.

        Raises
        ------
        :py:exc:`clipper.UnconnectedException`
            versions. All replicas for each version of each model will be stopped.
        """
        # if not self.connected:
        #     raise UnconnectedException()
        # model_info = self.get_all_models(verbose=True)
        # model_dict = {}
        # for m in model_info:
        #     if m["model_name"] in model_names:
        #         if m["model_name"] in model_dict:
        #             model_dict[m["model_name"]].append(m["model_version"])
        #         else:
        #             model_dict[m["model_name"]] = [m["model_version"]]
        # self.cm.stop_models(model_dict)
        # pp = pprint.PrettyPrinter(indent=4)
        # self.logger.info(
        #     "Stopped all containers for these models and versions:\n{}".format(
        #         pp.pformat(model_dict)))

    def stop_versioned_models(self, model_versions_dict):
        """Stops the specified versions of the specified models.

        Parameters
        ----------
        model_versions_dict : dict(str, list(str))
            For each entry in the dict, the key is a model name and the value is a list of model

        Raises
        ------
        :py:exc:`clipper.UnconnectedException`
            versions. All replicas for each version of each model will be stopped.

        Note
        ----
        This method will stop the currently deployed versions of models if you specify them. You
        almost certainly want to use one of the other stop_* methods. Use with caution.
        """
        # if not self.connected:
        #     raise UnconnectedException()
        # self.cm.stop_models(model_versions_dict)
        # pp = pprint.PrettyPrinter(indent=4)
        # self.logger.info(
        #     "Stopped all containers for these models and versions:\n{}".format(
        #         pp.pformat(model_versions_dict)))

    def stop_inactive_model_versions(self, model_names):
        """Stops all model containers serving stale versions of the specified models.

        For example, if you have deployed versions 1, 2, and 3 of model "music_recommender"
        and version 3 is the current version::

            clipper_conn.stop_inactive_model_versions(["music_recommender"])

        will stop any containers serving versions 1 and 2 but will leave containers serving
        version 3 untouched.

        Parameters
        ----------
        model_names : list(str)
            The names of the models whose old containers you want to stop.

        Raises
        ------
        :py:exc:`clipper.UnconnectedException`
        """
        # if not self.connected:
        #     raise UnconnectedException()
        # model_info = self.get_all_models(verbose=True)
        # model_dict = {}
        # for m in model_info:
        #     if m["model_name"] in model_names and not m["is_current_version"]:
        #         if m["model_name"] in model_dict:
        #             model_dict[m["model_name"]].append(m["model_version"])
        #         else:
        #             model_dict[m["model_name"]] = [m["model_version"]]
        # self.cm.stop_models(model_dict)
        # pp = pprint.PrettyPrinter(indent=4)
        # self.logger.info(
        #     "Stopped all containers for these models and versions:\n{}".format(
        #         pp.pformat(model_dict)))

    def stop_all_model_containers(self):
        """Stops all model containers started via Clipper admin commands.

        This method can be used to clean up leftover Clipper model containers even if the
        Clipper management frontend or Redis has crashed. It can also be called without calling
        ``connect`` first.
        """
        self.cm.stop_all_model_containers()
        self.logger.info("Stopped all Clipper model containers")

    def stop_all(self, graceful=True):
        """Stops all processes that were started via Clipper admin commands.

        This includes the query and management frontend Docker containers and all model containers.
        If you started Redis independently, this will not affect Redis. It can also be called
        without calling ``connect`` first.

        If graceful=False, Clipper will issue Docker Kill if it's in the Docker Mode. This parameter
        will take not effect in Kubernetes.
        """
        self.cm.stop_all(graceful=graceful)
        self.logger.info(
            "Stopped all Clipper cluster and all model containers")

