import os, platform, getpass
print("Nom : "+os.name+"\n"
    "Systeme : "+platform.system()+"\n"
    "Kernel : "+ platform.release() + "\n"
    "User : "+getpass.getuser() + "\n"
    "Default path : "+ os.getcwd())