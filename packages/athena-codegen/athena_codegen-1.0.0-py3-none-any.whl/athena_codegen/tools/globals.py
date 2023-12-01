# globals.py  

class GlobalVars:  
    def __init__(self): 
        self.assistantToolsUrl = ""
        self.projectHome = ""
        self.specHome = ""
        self.srcHome = ""
        self.appId = "dap-demo"
        self.appToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IkF0aGVuYSIsInNpZCI6MTYzNjc3NzI1NzgyNTkyfQ.3QLTPVKsk2Mp3j_aQ3X8bQW1wCJMNWeCkL6VPoK352c"
        self.apiVersion = "5.2.0.1063"
        self.basePackageName = "com.digiwin.dapdemo"
        self.apiId = ""
        self.dtoPath = ""
        self.serviceImplPath = "service\\impl"
        self.serviceImplName = ""
        self.apiIdList = []
        self.pomHome = ""
        self.mvnHome = "ABC"

      
    def update_var(self, var_name, new_value):  
        if hasattr(self, var_name):  
            setattr(self, var_name, new_value)  
        else:  
            raise AttributeError(f"Variable '{var_name}' does not exist")  
  
global_vars = GlobalVars()  