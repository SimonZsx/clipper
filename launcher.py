import os

"""
MODE: clipper, bigball, wo_proxy
NETWORK: localhost, swarm, clipper
"""
PROC_OK, PROC_ERR = 0, 1

class App:
    def __init__(self, name, mode="local", 
                             network="clipper",
                             images=[],
                             refresh="",
                             start_app="/clipper/clipper_admin/simple_dag.py",
                             start_app_argv="--dag /clipper/applications/simpledag/dag_formatted",
                             frontend="/clipper/clipper_admin/concrrent_frontend_client.py",
                             frontend_param={"worker":"1", "system":"outsystem", "port":"22223", "ip":"172.0.0.0"}):
        self.appName = name
        self.mode = mode # can be "clipper", "bigball", "wo_porxy"
        self.in_swarm = False if network=='localhost' else False
        self.images = images
        self.refresh_image_cmd = ["docker image pull "+img for img in self.images] if refresh=="" else [].append(refresh)
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
            print("> python3 "+self.start_app)
            oFlow = os.popen("python3 "+self.start_app)
            thisLine = oFlow.readline()
            while(thisLine != ""):
                print(thisLine,end='')

                if(self.mode=='clipper' and "-frontend-" in thisLine):
                    self.frontend_param["ip"] = thisLine.split(',')[-1]
                
                thisLine = oFlow.readline()
            oFlow.close()
            print("\n"+"-"*20+"\nApplication started up")
            return PROC_OK
        except:
            print("Fail to start the application: Check the configuration")
            return PROC_ERR

    def start_frontend(self):
        if self.mode != 'clipper' and self.mode != 'wo_proxy':
            print("Current mode does not support a frontend enquire")
            return PROC_OK
        
        if self.frontend_param["ip"]=="172.0.0.0":
            print("IP is not detected, please enter manually:", end='\t')
            self.frontend_param["ip"]=input()
        
        frontend_cmd = self.frontend
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

    def prepare_for_clipper(self):
        if self.in_swarm and self.mode == "clipper" :
            print("> python3 /clipper/cliipper_admin/auto_set_ip.py")
            os.system("python3 /clipper/cliipper_admin/auto_set_ip.py")
        return PROC_OK

if __name__ == '__main__':
    refresh_image = False
    network = 'localhost'
    err_flag = 0

    test = App('SIMPLE_APP',
                mode='local',
                network='localhost',
                images=["zsxhku/simple_dag:container"+str(i) for i in range(0,6)],
                start_app="/clipper/clipper_admin/imagequery_concrrent_client.py",
                start_app_argv = '--dag /clipper/applivations/simpledag/dag_formatted',
                frontend="/clipper/clipper_admin/imagequery_concrrent_client.py")
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
    print("Close all the containers")
    if network == 'localhost':
        print("> python3 /clipper/clipper_admin/stop_all.py")
        os.system("python3 /clipper/clipper_admin/stop_all.py")
    else:
        print("> python3 /clipper/clipper_admin/cluster_stop_all.py")
        os.system("python3 /clipper/clipper_admin/cluster_stop_all.py")
