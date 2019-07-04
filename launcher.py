import os, sys
import json, argparse
from datetime import datetime
sys.path.append(os.path.abspath("/clipper/process_log"))
sys.path.append(os.path.abspath("/clipper/clipper_admin"))
import process_log
import stop_all, cluster_stop_all
import start_withproxy_frontend, cluster_general_start
import auto_set_ip

"""
MODE: clipper, bigball, withoutProxy, withProxy
NETWORK: localhost, swarm, clipper
"""
PROC_OK, PROC_ERR = 0, 1

log_timeStamp = datetime.now().strftime("%y%m%d_%H%M%S") 

class App:
    def __init__(self, 
                name, 
                mode="withProxy", 
                network="clipper",
                images=[],
                refresh="",
                frontend_server="/clipper/clipper_admin/simple_dag.py",
                frontend_server_args="--dag /clipper/applications/simpledag/dag_formatted",
                frontend_client="/clipper/clipper_admin/concrrent_frontend_client.py",
                frontend_client_param={"worker":"1", "system":"outsystem", "port":"22223", "ip":"172.0.0.0"}):
        self.appName = name
        self.network = network
        self.mode = mode # can be "clipper", "bigball", "withoutProxy" or "withProxy"
        self.in_swarm = False if network=='localhost' else True
        self.images = images
        self.refresh_image_cmd = ["docker image pull "+img for img in self.images] if refresh=="" else refresh.split(',')
        self.frontend_server = frontend_server
        self.frontend_server_args = frontend_server_args
        self.frontend_client = frontend_client
        self.frontend_client_param = frontend_client_param
    
    def prepare_for_clipper(self):
        if self.in_swarm and self.mode == "withProxy" :
            print("> python3 /clipper/cliipper_admin/auto_set_ip.py")
            auto_set_ip.ip_setter()
        return PROC_OK

    def refresh_image(self):
        try:
            for cmd in self.refresh_image_cmd:
                print("> "+cmd)
                oFlow = os.popen(cmd)
                print(oFlow.read())
                oFlow.close()
            return PROC_OK
        except:
            print("Fail to refresh image: Check the configuration")
            return PROC_ERR

    def start_frontend(self): # start frontend server
        try:
            if self.mode == "withProxy":
                dag_description = self.frontend_server_args.split()[-1] # the path to the dag_description/dag_formatted
                print(dag_description)
                if self.in_swarm:
                    cluster_general_start.start(self.frontend_server, self.appName)
                else:
                    start_withproxy_frontend.start(self.appName, dag_description)
            else:
                print(self.frontend_server)
                os.system(self.frontend_server)
            return PROC_OK
        except:
            print("Fail to start the application: Check the configuration")
            return PROC_ERR

    def run_frontend_client(self):  # start frontend client, or the run.sh for bigball
        # if self.frontend_client == "" :
        #     print("Current mode does not support a frontend enquire")
        #     return PROC_OK
        
        print("Default frontend server at ip: ", self.frontend_client_param["ip"], "\tEnter \'y\' to confirm, \'n\' to inspect and enter the IP manually")
        ch = input("Input: ")
        if ch!='y' and ch!='n':
            self.frontend_client_param["ip"] = ch
        elif ch=='n':
            os.system("docker inspect c0 | grep \"IPAddress\"")
            self.frontend_client_param["ip"] = input("Please enter ip: ")
        
        if "py" in self.frontend_client:
            frontend_client_cmd = "python3 " + self.frontend_client
        else:
            frontend_client_cmd = self.frontend_client

        print("Start running frontend client!")
        frontend_client_cmd += " ".join(["  --" + arg + " " + val for arg, val in self.frontend_client_param.items()])
        print("> " + frontend_client_cmd)

        try:
            f = open(self.get_client_log_file_path(), "w")
            oFlowLog = os.popen(frontend_client_cmd)
            senct = oFlowLog.readline()
            while senct != "":
                print(senct, end="")
                f.write(senct)
                senct = oFlowLog.readline()
            f.close()
            oFlowLog.close()
            return PROC_OK
        except:
            print("Fail to run ", self.frontend_client, "with: ", self.frontend_client_param)
            return PROC_ERR

    def write_container_logs(self, log_requests_str):
        log_requests = log_requests_str.split()
        if len(log_requests) == 0:
            print("No valid input, no log would be saved.")
        else:
            for request in log_requests:              # f9842338fdc5-c0
                docker_id = request.split("-")[0]     # f9842338fdc5
                container_id = request.split("-")[1]  # c0
                
                logFlow = os.popen("docker logs " + container_id)
                buff = logFlow.read()
                logFlow.close()

                log_file_name = self.appName + "_" + self.mode + "_" + container_id + "_" + log_timeStamp + ".log"
                log_file_path = os.path.join(".", 'process_log', log_file_name)

                print("{} saved as: {}".format(request, str(log_file_path)))
                logFlow = open(log_file_path, 'w')
                logFlow.write(buff)
                logFlow.close()

        
    def get_appName(self):
        return self.appName
    
    def get_mode(self):
        return self.mode
    
    def get_network(self):
        return self.network

    def get_client_log_file_name(self):
        client_log_file_name = self.appName + "_" + self.mode + "_client_" + log_timeStamp + ".log"
        return client_log_file_name

    def get_client_log_file_path(self):
        client_log_file_path = os.path.join(".", 'process_log', self.get_client_log_file_name)
        return client_log_file_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App name, mode and network')
    parser.add_argument('--appName','-n',help='name of the app',dest='appName',required=True)
    parser.add_argument('--mode','-m',help='mode',dest='mode',required=True,
                        choices=['clipper','withoutProxy','bigball','withProxy'], default='withProxy')
    parser.add_argument('--network','--net',default='localhost',choices=['localhost','swarm','clipper'],dest='net')
    parser.add_argument('--refresh','-r',action='store_true',dest='refresh')

    with open('json/'+parser.parse_args().appName+'.json') as config:
        data = json.load(config)

    refresh_image = bool(parser.parse_args().refresh)
    err_flag = 0

    app = App(parser.parse_args().appName,
                mode=parser.parse_args().mode,
                network=parser.parse_args().net,
                images=data["images"][parser.parse_args().mode],
                refresh=data["buildFilePath"][parser.parse_args().mode],
                frontend_server=data["frontendServerPath"][parser.parse_args().mode],
                frontend_server_args = data["frontendServerArgs"][parser.parse_args().mode],
                frontend_client=data["frontendClientPath"][parser.parse_args().mode],
                frontend_client_param=data['frontendClientParams'][parser.parse_args().mode])
    app.prepare_for_clipper()

    if (refresh_image):
        print("Refreshing images.")
        err_flag = app.refresh_image()

    if err_flag == 0:
        print("Start application frontend")
        err_flag = app.start_frontend()

    if err_flag == 0:
        print("Run the frontend client")
        err_flag = app.run_frontend_client()

    if err_flag == 0: 
        os.system("docker ps -a | grep -v Exited | grep -v -- -proxy")
        print("Enter the tags of containers you would like to inspect.")
        print("The format should be: [container_id]-[tag_you_want_for_log].")
        print("Exampel: f9842338fdc5-c1 => log for c1 will be saved at: ./process_log/appname_mode_c1_timestamp.log")
        log_requests_str = input()
        app.write_container_logs(log_requests_str)

        print("Log processing.")
        try:
            process_log.analyze_log(data["appName"] == "imagequery", 
                                    system=app.get_mode(), 
                                    log_file=app.get_client_log_file_path(),
                                    num_containers=data["num_containers"])
        except:
            print("Fail to handle the log processing.")
    
    if err_flag == 1:
        print("ERROR OCCURED, STOP DEPLOYMENT", end=': ')  
    
    print("Close all the containers")
    if app.get_network() == 'localhost':
        stop_all.stop_all_containers()
    else:
        cluster_stop_all.stop_all_containers()
