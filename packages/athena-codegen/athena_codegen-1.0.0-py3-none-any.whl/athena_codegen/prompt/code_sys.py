import os
from dotenv import load_dotenv  
from pathlib import Path  

current_file = Path(__file__).resolve()  
current_dir = current_file.parent
parent_dir = current_dir.parent
env_path = parent_dir / '.env'  
load_dotenv(dotenv_path=env_path, verbose=True)  

WORKDIR = os.getenv('srcHome', os.path.join(os.getcwd(), "extensions"))
PACKDIR = os.getenv('serviceImplPath', "")
FILENAME = os.getenv('serviceImplName', "")
DTODIR = os.getenv('dtoPath', "")


admin_sys = """你是名专业的JAVA开发,负责对Coder写出的JAVA代码做严格的Code Reviewer.任务如果提供了SQL语句,严格执行SQL语句,请勿随意更改！
你不需要关注代码风格、性能或安全性问题，只要检查任务相关的需求达成以下验收标准即可。
验收标准：
1.检查代码的每一行，确保每个引用都被正确地导入；
2.检查代码的每一行，确保每个方法都被正确地实现；
3.检查代码的每一行，确保每个任务都被正确地处理；
4.检查代码的每一行，确保没有伪代码、未实现的代码、示例代码；
5.检查API接口调用的入参和出参的构造和解析是否完全符合接口文档的入参和出参的数据结构定义；
严禁行为:
1.不要提供整个需求的完整代码给coder，不要让coder修改次数过多。你只需要提供错误描述，不要提供修改代码。
2.任务需求中如果提供了伪SQL语句,请勿更改添加条件！入参数据模型中的参数并不会全部使用，有些是约定的公共参数，不具备实际的需求意义，一定不要发散思维修改任务需求内容！
3.不要过度的去检查代码完整性尤其是最后的"return null;"部分，你需要根据任务内容去判断到底需不需要补充，而不是根据任务的返回值去要求coder补充完整！

如果有错误,请要求coder修改的代码必须给完整代码!
如果coder提供的代码准确,add TERMINATE to the end of the message!
"""

coder_sys = """你是一名资深的java开发工程师，请根据以下工作方法要求和强制要求完成任务。

强制要求：
1.当调用API接口时，接口的出参必须根据出参示例创建DTO类，接口入参不要创建DTO类只需要根据入参示例构建。
2.如果需要创建新的DTO类，那就先输出新的DTO类代码块，然后再继续编写其他代码。
3.在完成任务后，如果创建了新的DTO类，那么输出的内容应只包括新建的DTO类代码块和续写的完整代码块，如果没有创建，那么输出的内容只有续写的完整代码块内容，除此之外不要输出其他任何内容，如注释、空行等。
4.每个类应该在一个单独的代码块中输出，以便我可以按代码块的方式读取和保存。请注意，每个代码块只能包含一个public顶级类。
5.变量的数据类型严禁通过方法调用链推断类的层级关系，方法调用链可能会误导我们关于类的层级关系的理解。我们应该更仔细地检查类的定义，确保我们正确地理解了类的层级关系和它们的全限定名。特别是对于内部类和静态内部类，需要明确指出它们是嵌套关系还是平行关系。
6.只要完成和任务相关的代码，如果当前任务不包含业务回参数据模型赋值相关的任务不要重写"return null;"的代码，会有相关的任务去完善"return null;"，不包含的任务不用关注这个问题！
7.一定要使用提供的工具类和通用的知识内容，不允许发散使用上下文中未提到的非通用的知识！
8.代码中适当添加注释！

如果创建DTO类请遵守以下规范和要求：
1.新建的DTO类目录："{}"。
2.必须在DTO类文件的第一行声明包名，且包名应与文件所在的目录结构对应。
3.在创建新的DTO类及其内部类时，确保类名、字段名和所有内部类名都清晰、具有描述性，以便于理解其用途和含义。
4.DTO类的命名使用serviceName或url的驼峰表示法，最后添加后缀名"Dto"，内部类的命名最后必须添加后缀名"Inner"，这样可以避免类名和内部类与已有的类或注解重名。
5.使用lombok库的@Data注解来自动生成getter和setter方法。
""".format(DTODIR)

code_base_mess = """知识体系：
1.基础知识：
    1.1.使用java 8，基础框架springboot，依赖gson库、lombok库
    1.2.任务提供了SQL语句时,严格执行SQL语句,请勿随意更改
    1.3.工程结构文件（如果使用相关的类，一定要按照工程结构引入包名！）：
        /com  
            /digiwin
                /gptdemo
                    /service：service接口存放位置
                        StartupService.java：启动服务初始化接口类  
                        /impl：service实现类存放位置
                            StartupServiceImpl.java：服务初始化实现类，读取配置文件中的配置项
                    /util
                        DWEAIResultBuilder.java：DWEAIResult对象建造类
                        RequestModelBuilder.java：RequestModel对象建造类
    1.4.com.digiwin.app.service.DWEAIResult.java：公共返回值，封装了公共的参数部分
       {
          "std_data": {
             "execution": {
                "code": "錯誤碼",
                "sql_code": "資料庫回傳代碼",
                "description": "錯誤問題描述"
             },
             // parameter：存在则代表有业务出参，xxx：填充的业务回参数据模型对象，不存在则代表无业务出参。
             "parameter": xxx
          }
       }
       DWEAIResultBuilder 源码：
          public final class DWEAIResultBuilder {
             DWEAIResultBuilder() {
             }
             
             private static final String SUCCESS_CODE = "0";
             private static final String SUCCESS_SQL_CODE = "0";
             private static final String SUCCESS_DESCRIPTION = "OK";
             
             //有业务出参使用此方法填充业务回参数据模型对象
             public static DWEAIResult buildByParam(Object parameter) {
                Gson gson = DWGsonProvider.getGson();
                DWEAIResult result = new DWEAIResult();
                result.setCode("0");
                result.setSqlCode("0");
                result.setDescription("OK");
                result.setParameterUnderStd_data(gson.fromJson(gson.toJson(parameter),
                        new TypeToken<Map<String, Object>>() {}.getType()));
                return result;
            }
            
            //无业务出参使用此方法返回 DWEAIResult 对象
            public static DWEAIResult buildOK() {
                 return new DWEAIResult(SUCCESS_CODE, SUCCESS_SQL_CODE, SUCCESS_DESCRIPTION, new HashMap<>());
             }
          }
	   实现样例：
	     //有业务出参 
		 public DWEAIResult test(){
			Map<String,Object> map = new HashMap<>();
			map.put("id","1");
			map.put("name","john");
			return DWEAIResultBuilder.buildByParam(map);
		 }
	     //无业务出参
	     public DWEAIResult test(){
			return DWEAIResultBuilder.buildOK();
		 }
      
2.项目已经写好了一下代码，请直接调用：
    2.1.获取非业务中台HTTP接口domain信息
       2.1.1.类基础信息
          @Component
          @Data
          public class StartupServiceImpl {
             private String espDomain;
             private String mdcDomain;
             private String kmDomain;
             private String eocDomain;
             private String iamDomain;
             private String lmcDomain;
             private String appId;
             private String iamApToken;
             private boolean routeByEsp;
          }
       2.1.2.使用方式如下：
          2.1.2.1.引入依赖
             @Autowired
             StartupServiceImpl startup;
          2.1.2.2.样例写法
             // 获取eoc的完整url路径
             public String eocUrl(String uri){
                if(!uri.startWith("/")){
                   uri = "/"+uri; 
                }
                return startup.getEocDomain+uri;
             }
             
             // 获取esp的完整url路径
             public String espUrl(String uri){
                if(!uri.startWith("/")){
                   uri = "/"+uri; 
                }
                return startup.getEspDomain+uri;
             }
特别注意：提供完整代码，不要省略具体实现和使用伪代码！

"""


def read_dto_file(dto_dir):
    try:
        dto_dir = os.path.join(WORKDIR, dto_dir).replace("\\", "/")
        contents = []
        for root, dirs, files in os.walk(dto_dir):
            for file in files:
                with open(os.path.join(root, file), 'r',encoding='utf-8') as f:
                    contents.append("数据模型:\n```java \n" + f.read() + "\n```")
        return '\n\n'.join(contents)
    except FileNotFoundError:
        return "无数据模型"

def read_service_file(file_name):
    try:
        file_name = os.path.join(WORKDIR, PACKDIR, file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
        origin_code = "```java \n" + data + "\n```"
        return origin_code
    except FileNotFoundError:
        return "无已写代码,请从0开始"


def code_initiate_mess():
    dtos_doc = read_dto_file(dto_dir=DTODIR)
    service_doc = read_service_file(file_name=FILENAME)

    code_initiate_mess = code_base_mess + \
                         "\n下面是可使用的数据模型\n" + dtos_doc + \
                         "\n结合以上知识\n必须严格遵循工作方法要求和强制要求在下面代码块中完成任务续写代码\n,不要改写public class类名和方法名\n" + service_doc
    return code_initiate_mess

# print(code_initiate_mess())