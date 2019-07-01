import os, sys
import json
import argparse
sys.path.append(os.path.abspath("/clipper/process_log"))
import process_log

"""
MODE: clipper, bigball, withoutProxy, withProxy
NETWORK: localhost, swarm, clipper
"""
PROC_OK, PROC_ERR = 0, 1

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
            start_cmd = "python3 "+ self.start_app if "py" in self.start_app else self.start_app
            print("> " + start_cmd)
            oFlow = os.popen(start_cmd)
            thisLine = oFlow.readline()
            while(thisLine != ""):
                print(thisLine,end='')
                thisLine = oFlow.readline()
            oFlow.close()
            print("\n"+"-"*20+"\nApplication started up")
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
        
        frontend_cmd = "python3 " + self.frontend
        frontend_cmd += " ".join(["  --"+arg+" "+val for arg,val in self.frontend_param.items()])
        print("> "+frontend_cmd)
        try:
            os.system(frontend_cmd)
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
            os.system("python3 /clipper/cliipper_admin/auto_set_ip.py")
        return PROC_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App name, mode and network')
    parser.add_argument('--appName','-n',help='name of the app',dest='appName',required=True)
    parser.add_argument('--mode','-m',help='mode',dest='mode',required=True,
                        choices=['clipper','withoutProxy','bigball','withProxy'],default='withProxy')
    parser.add_argument('--network','--net',default='localhost',choices=['localhost','swarm','clipper'],dest='net')
    parser.add_argument('--refresh','-r',action='store_true',dest='refresh')

    with open('json/json_example.json') as config:
    #should be json/json_ + parser.parse_args().appName +.json
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

    if err_flag == 1:
        print("ERROR OCCURED, STOP DEPLOYMENT", end=': ')  
    
    print("Log processing...")
    process_log.log_generator(test.get_mode()=="bigball", 
                              system=test.get_mode(), 
                              log_file="./process_log/"+test.get_appName()+".log")
    
    print("Close all the containers")
    if test.get_network() == 'localhost':
        print("> python3 /clipper/clipper_admin/stop_all.py")
        os.system("python3 /clipper/clipper_admin/stop_all.py")
    else:
        print("> python3 /clipper/clipper_admin/cluster_stop_all.py")
        os.system("python3 /clipper/clipper_admin/cluster_stop_all.py")
