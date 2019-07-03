import os, sys
import json, argparse
from datetime import datetime
sys.path.append(os.path.abspath("/clipper/process_log"))
sys.path.append(os.path.abspath("/clipper/clipper_admin"))
import process_log
import stop_all, cluster_stop_all
import general_start, cluster_general_start
import auto_set_ip

"""
MODE: clipper, bigball, withoutProxy, withProxy
NETWORK: localhost, swarm, clipper
"""
PROC_OK, PROC_ERR = 0, 1

log_timeStamp = datetime.now().strftime("%y%m%d_%H%M%S") 

class App:
    def __init__(self, name, mode="withProxy", 
                             network="clipper",
                             images=[],
                             refresh="",
                             start_app="/clipper/clipper_admin/simple_dag.py",
                             start_app_argv="--dag /clipper/applications/simpledag/dag_formatted",
                             frontend="/clipper/clipper_admin/concrrent_frontend_client.py",
                             frontend_param={"worker":"1", "system":"outsystem", "port":"22223", "ip":"172.0.0.0"}):
        self.appName = name
        self.network = network
        self.mode = mode # can be "clipper", "bigball", "withoutProxy" or "withProxy"
        self.in_swarm = False if network=='localhost' else True
        self.images = images
        self.refresh_image_cmd = ["docker image pull "+img for img in self.images] if refresh=="" else refresh.split(',')
        self.start_app = " ".join([start_app, start_app_argv])
        self.frontend = frontend
        self.frontend_param = frontend_param

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

    def start(self):
        try:
            if self.mode == "withProxy":
                self.start_app = self.start_app.split()[-1] # get rid of "--dag"
                if self.in_swarm:
                    cluster_general_start.start(self.start_app, self.appName)
                else:
                    general_start.start(self.start_app, self.appName)
            else:
                os.system(self.start_app)
            return PROC_OK
        except:
            print("Fail to start the application: Check the configuration")
            return PROC_ERR

    def start_frontend(self):
        if self.frontend == "" :
            print("Current mode does not support a frontend enquire")
            return PROC_OK
        
        print("Front End @ ", self.frontend_param["ip"], "Enter \'y\' to confirm, \'n\' to inspect or enter the IP manually")
        ch = input()
        if ch!='y' and ch!='n':
            self.frontend_param["ip"] = ch
        elif ch=='n':
            os.system("docker inspect c0 | grep \"IPAddress\"")
            self.frontend_param["ip"] = input("please enter ip now: ")
        
        if "py" in self.frontend:
            frontend_cmd = "python3 " + self.frontend
        else:
            frontend_cmd = self.frontend
        
        frontend_cmd += " ".join(["  --"+arg+" "+val for arg,val in self.frontend_param.items()])
        print("> "+frontend_cmd+"\nStoring logs, please wait")
        try:
            f = open(self.get_log_name(), "w")
            
            oFlowLog = os.popen(frontend_cmd)
            senct = oFlowLog.readline()
            while senct != "":
                print(senct, end="")
                f.write(senct)
                senct = oFlowLog.readline()
            f.close()
            oFlowLog.close()
            return PROC_OK
        except:
            print("Fail to run the frontend: ", self.frontend, "with: ", self.frontend_param,"\nCheck configuration")
            return PROC_ERR
        
    def get_appName(self):
        return self.appName
    
    def get_mode(self):
        return self.mode
    
    def get_network(self):
        return self.network

    def prepare_for_clipper(self):
        if self.in_swarm and self.mode == "withProxy" :
            print("> python3 /clipper/cliipper_admin/auto_set_ip.py")
            auto_set_ip.ip_setter()
        return PROC_OK
    
    def get_log_name(self):
        return "./process_log/"+log_timeStamp+self.appName+"_"+self.mode+".log"

def write_container_log(application,container_tags):
    for container in container_tags:
        print("Fetching logs @", container)
        logFlow = os.popen("docker inspect " + container)
        buff = logFlow.read()
        logFlow.close()
        with open("c"+container+application.get_log_name(), 'w') as logFlow:
            logFlow.write(buff)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App name, mode and network')
    parser.add_argument('--appName','-n',help='name of the app',dest='appName',required=True)
    parser.add_argument('--mode','-m',help='mode',dest='mode',required=True,
                        choices=['clipper','withoutProxy','bigball','withProxy'],default='withProxy')
    parser.add_argument('--network','--net',default='localhost',choices=['localhost','swarm','clipper'],dest='net')
    parser.add_argument('--refresh','-r',action='store_true',dest='refresh')

    with open('json/'+parser.parse_args().appName+'.json') as config:
        data = json.load(config)

    refresh_image = bool(parser.parse_args().refresh)
    err_flag = 0

    test = App(parser.parse_args().appName,
                mode=parser.parse_args().mode,
                network=parser.parse_args().net,
                images=data["images"][parser.parse_args().mode],
                refresh=data["buildFilePath"][parser.parse_args().mode],
                start_app=data["frontendServerPath"][parser.parse_args().mode],
                start_app_argv = data["frontendServerArgs"][parser.parse_args().mode],
                frontend=data["frontendClientPath"][parser.parse_args().mode],
                frontend_param=data['frontendClientParams'][parser.parse_args().mode])
    test.prepare_for_clipper()

    if (refresh_image):
        print("Images to be refreshed")
        err_flag = test.refresh_image()

    if err_flag == 0:
        print("Deploy the applications")
        err_flag = test.start()

    if err_flag == 0:
        print("Start the frontend service")
        err_flag = test.start_frontend()

    if err_flag == 0: 
        os.system("docker ps | grep -v proxy")
        container_tags = input("Enter the tags of containers you would like to inspect").split()
        if(len(container_tags)!=0):
            write_container_log(test, container_tags)
        print("Log processing, @", test.get_log_name())
        try:
            process_log.analyze_log(data["appName"]=="imagequery", 
                                    system=test.get_mode(), 
                                    log_file=test.get_log_name(),
                                    num_containers=data["num_containers"])
        except:
            print("Fail to handle the log processing.")
    
    if err_flag == 1:
        print("ERROR OCCURED, STOP DEPLOYMENT", end=': ')  
    
    print("Close all the containers")
    if test.get_network() == 'localhost':
        stop_all.stop_all_containers()
    else:
        cluster_stop_all.stop_all_containers()
