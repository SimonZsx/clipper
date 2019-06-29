import os

class App:
    def __init__(self, name, mode="local", 
                             network="clipper",
                             images=[],
                             refresh="",
                             start_app="/clipper/clipper_admin/cluster_simple_dag.py",
                             dag_file="/clipper/applications/simpledag/dag_formatted",
                             frontend="/clipper/clipper_admin/concrrent_frontend_client.py",
                             frontend_param={"worker":"1", "system":"outsystem", "port":"22223", "ip":"172.0.0.0"}):
        self.appName = name
        self.mode = mode # can be "clipper", "local", "bigball", "wo_porxy"
        self.in_swarm = False if network=='localhost' else False
        self.images = images
        self.refresh_image_cmd = ["docker image pull "+img for img in self.images] if refresh=="" else [].append(refresh)
        self.start_app = " --dag ".join([start_app, dag_file])
        self.frontend = frontend
        self.frontend_param = frontend_param

    def refresh_image(self):
        try:
            for cmd in self.refresh_image_cmd:
                print("> "+cmd)
                oFlow = os.popen(cmd)
                print(oFlow.read())
                oFlow.close()
        except:
            print("Fail to refresh image: Check the configuration")

    def start(self):
        try:
            print("> python3 "+self.start_app)
            oFlow = os.popen("python3 "+self.start_app)
            thisLine = oFlow.readline()
            while(thisLine != ""):
                print(thisLine,end='')
                if("frontend container" in thisLine):
                    self.frontend_param["ip"] = thisLine
                    #TODO: Fetch the ip from the returned string
                thisLine = oFlow.readline()
            oFlow.close()
            print("\n"+"-"*20+"\nApplication started up")
        except:
            print("Fail to start the application: Check the configuration")

    def start_frontend(self):
        frontend_cmd = self.frontend
        frontend_cmd += " ".join(["  --"+arg+" "+val for arg,val in self.frontend_param.items()])
        print("> "+frontend_cmd)
        try:
            os.system(frontend_cmd)
        except:
            print("Fail to run the frontend: ", self.frontend, "with: ", self.frontend_param,"\nCheck configuration")
        
    def get_appName(self):
        return self.appName
    
    def get_mode(self):
        return self.mode

    def prepare_for_clipper(self):
        if(self.in_swarm and self.mode == "clipper"):
            print("> python3 /clipper/cliipper_admin/auto_set_ip.py")
            os.system("python3 /clipper/cliipper_admin/auto_set_ip.py")

if __name__ == '__main__':
    refresh_image = False
    network = 'localhost'

    test = App('SIMPLE_APP',
                mode='local',
                network='localhost',
                images=["zsxhku/simple_dag:container"+str(i) for i in range(0,6)],
                start_app="/clipper/clipper_admin/imagequery_concrrent_client.py",
                frontend="/clipper/clipper_admin/imagequery_concrrent_client.py")
    test.prepare_for_clipper()

    if(refresh_image):
        print("Images to be refreshed")
        test.refresh_image()

    print("Deploy the applications")
    test.start()

    print("Start the frontend service")
    test.start_frontend()

    print("Close all the containers")
    if network == 'localhost':
        print("> python3 /clipper/clipper_admin/stop_all.py")
        os.system("python3 /clipper/clipper_admin/stop_all.py")
    else:
        print("> python3 /clipper/clipper_admin/cluster_stop_all.py")
        os.system("python3 /clipper/clipper_admin/cluster_stop_all.py")