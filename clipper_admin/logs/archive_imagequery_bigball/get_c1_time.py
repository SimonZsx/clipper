import os
print("here")
os.system("arr=\"`docker ps -a | grep c1_speechRecog | head -n 2 | cut -d\" \" -f1`\"")
os.system("echo $arr")


