import uuid
from typing import List, Tuple
import re

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x
    
def extract_code(text: str) -> List[Tuple[str, str]]:
    """Extract code from a text.

    Args:
        text (str): The text to extract code from.

    Returns:
        list: A list of tuples, each containing the language and the code.
          If there is no code block in the input text, the language would be "unknown".
          If there is code block but the language is not specified, the language would be "".
    """

    # Extract both multi-line and single-line code block, separated by the | operator
    # `{3}(\w+)?\s*([\s\S]*?)`{3}: Matches multi-line code blocks.
    #    The (\w+)? matches the language, where the ? indicates it is optional.
    # `([^`]+)`: Matches inline code.
    # code_pattern = re.compile(r"`{3}(\w+)?\s*([\s\S]*?)`{3}|`([^`]+)`")
    code_pattern = re.compile(r"`{3}(\w+)?\s*([\s\S]*?)`{3}")
    code_blocks = code_pattern.findall(text)

    # Extract the individual code blocks and languages from the matched groups
    extracted = []
    for lang, group1 in code_blocks:
        if group1:
            extracted.append((lang.strip(), group1.strip()))
        else:
            extracted.append('', group1.strip())

    return extracted

from typing import List, Dict, Tuple, Optional, Union, Callable
import re
import time
from hashlib import md5
import logging
import os
import sys

logger = logging.getLogger(__name__)

CODE_BLOCK_PATTERN = r"```(\w*)\n(.*?)\n```"
WORKING_DIR = os.path.join(os.getcwd(), "extensions")
UNKNOWN = "unknown"
TIMEOUT_MSG = "Timeout"
DEFAULT_TIMEOUT = 600
WIN32 = sys.platform == "win32"
PATH_SEPARATOR = WIN32 and "\\" or "/"


def save_code(
    code: Optional[str] = None,
    filename: Optional[str] = None,
    work_dir: Optional[str] = None,
    lang: Optional[str] = "java",
) -> Tuple[int, str, str]:
    """Save code.

    Args:
        code (Optional, str): The code to execute.
            If None, the code from the file specified by filename will be executed.
            Either code or filename must be provided.
        timeout (Optional, int): The maximum execution time in seconds.
            If None, a default timeout will be used. The default timeout is 600 seconds. On Windows, the timeout is not enforced when use_docker=False.
        filename (Optional, str): The file name to save the code or where the code is stored when `code` is None.
            If None, a file with a randomly generated name will be created.
            The randomly generated file will be deleted after execution.
            The file name must be a relative path. Relative paths are relative to the working directory.
        work_dir (Optional, str): The working directory for the code execution.
            If None, a default working directory will be used.
            The default working directory is the "extensions" directory under
            "path_to_autogen".
        lang (Optional, str): The language of the code. Default is "python".

    Returns:
        int: 0 if the code executes successfully.
        str: The error message if the code fails to execute; the stdout otherwise.
        image: The docker image name after container run when docker is used.
    """
    try:
        if all((code is None, filename is None)):
            error_msg = f"Either {code=} or {filename=} must be provided."
            logger.error(error_msg)
            raise AssertionError(error_msg)

        original_filename = filename
        if WIN32 and lang in ["sh", "shell"]:
            lang = "sh"
        if filename is None:
            code_hash = md5(code.encode()).hexdigest()
            # create a file with a automatically generated name
            filename = f"tmp_code_{code_hash}.{'java' if lang.startswith('java') else lang}"
        else:
            filename = f"{filename}.{'java' if lang.startswith('java') else lang}"
        if work_dir is None:
            work_dir = WORKING_DIR
        
        lines = code.split("\n")  
        if lines[0].startswith("package"): 
            package_line = lines[0].split(" ")[1].strip(";")  
            split_text = package_line.split(".")
            save_dir = os.path.join(work_dir, *split_text)  
            os.makedirs(save_dir, exist_ok=True)  
        else:
            raise Exception("The first line must start with 'package'.")  

        filepath = os.path.join(save_dir, filename)
        file_dir = os.path.dirname(filepath)
        os.makedirs(file_dir, exist_ok=True)
        if code is not None:
            with open(filepath, "w", encoding="utf-8") as fout:
                fout.write(code)

        return (0, f'save {lang} to {filename}')
    except Exception as e:
        return (1, str(e))
    
def save_code_blocks(code_blocks, work_dir=None):
    """Execute the code blocks and return the result."""
    all_exitcode = 0
    logs_all = ""
    for i, code_block in enumerate(code_blocks):
        lang, code = code_block
        if lang in ["java", "Java"]:
            pattern = re.compile(r"public class (\w+)")  
            match = pattern.search(code)  
            filename = None
            if match:  
                filename = match.group(1)
            exitcode, logs = save_code(code=code, filename=filename, work_dir=work_dir, lang=lang)
        else:
            # In case the language is not supported, we return an error message.
            exitcode, logs = (
                1,
                f"unknown language {lang}"
            )

        logs_all += "\n" + logs
        if exitcode != 0:
            all_exitcode = 1
            print(colored(f"\n>>>>>>>> UNKNOWN CODE BLOCK {i} (inferred language is {lang})","red",),flush=True)
            continue
        print(colored(f"\n>>>>>>>> SAVE CODE BLOCK {i} (inferred language is {lang})","green",),flush=True)
    return all_exitcode, logs_all

if __name__ == '__main__':
    test_text = """
```java
package com.digiwin.gptdemo.service.impl;

import com.digiwin.app.dao.DWDao;
import com.digiwin.app.data.DWDataSetOperationOption;
import com.digiwin.app.service.DWEAIResult;
import com.digiwin.gptdemo.dto.demoptcathenapotlimitmanagementget.DemoPtcAthenapotLimitManagementGetParam;
import com.digiwin.gptdemo.dto.demoptcathenapotlimitmanagementget.DemoPtcAthenapotLimitManagementGetResult;
import com.digiwin.gptdemo.service.DemoPtcAthenapotLimitManagementGetService;
import com.digiwin.gptdemo.util.DWEAIResultBuilder;
import org.springframework.beans.factory.annotation.Autowired;

import javax.validation.Valid;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DemoPtcAthenapotLimitManagementGetServiceImpl implements DemoPtcAthenapotLimitManagementGetService {

    @Autowired
    private DWDao dao;

    @Override
    public DWEAIResult get(Map<String, Object> headers,
                           @Valid DemoPtcAthenapotLimitManagementGetParam messageBody) throws Exception {
        // SQL 语句
        String sql = "SELECT id, min_percentage, max_percentage, class_interval_name, class_interval_no, tenantsid, tenant_id, create_by, create_date, modified_by, modified_date, version, deleted FROM cim_limit_management";

        // 创建sql操作option对象
        DWDataSetOperationOption option = new DWDataSetOperationOption();
        // 设置租户开关-关闭
        option.setTenantEnabled(false);
        // 使用dao的查询操作取得数据
        List<Map<String,Object>> datas = dao.select(option, sql);

        // 将查询结果封装到DemoPtcAthenapotLimitManagementGetResult对象中
        DemoPtcAthenapotLimitManagementGetResult result = new DemoPtcAthenapotLimitManagementGetResult();
        result.setQueryResult(new ArrayList<>());
        for (Map<String, Object> data : datas) {
            DemoPtcAthenapotLimitManagementGetResult.QueryResult queryResult = new DemoPtcAthenapotLimitManagementGetResult.QueryResult();
            queryResult.setClassIntervalName((String) data.get("class_interval_name"));
            queryResult.setId((String) data.get("id"));
            queryResult.setMinPercentage((java.math.BigDecimal) data.get("min_percentage"));
            queryResult.setMaxPercentage((java.math.BigDecimal) data.get("max_percentage"));
            result.getQueryResult().add(queryResult);
        }

        // 将结果封装到DWEAIResult对象中并返回
        return DWEAIResultBuilder.buildByParam(result);
    }
}
```
"""
    extracted = extract_code(test_text)
    print(extracted)
    exitcode, logs_all = save_code_blocks(extracted)
    print(colored(logs_all, "green"))