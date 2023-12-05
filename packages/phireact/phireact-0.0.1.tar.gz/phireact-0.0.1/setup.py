# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yorg_test',
 'yorg_test.core',
 'yorg_test.core.agents',
 'yorg_test.core.agents.data_scientist',
 'yorg_test.core.agents.software_engineer',
 'yorg_test.core.assistant',
 'yorg_test.core.assistant.prompt',
 'yorg_test.core.assistant.tools',
 'yorg_test.core.nodes',
 'yorg_test.core.nodes.code_runner',
 'yorg_test.core.nodes.data_analysis',
 'yorg_test.core.nodes.document_loader',
 'yorg_test.core.nodes.git',
 'yorg_test.core.nodes.github',
 'yorg_test.core.nodes.openai',
 'yorg_test.core.service',
 'yorg_test.utils',
 'yorg_test.utils.code_executor']

package_data = \
{'': ['*']}

install_requires = \
['include']

setup_kwargs = {
    'name': 'phireact',
    'version': '0.0.1',
    'description': 'test package for yorg',
    'long_description': '# YORG Test Package\n\nthis is a test package\n\n# test version\n\n## how to use\n\n- Set up test version package\n``` shell\npip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple yorg-test\n```\n- Set up openapikey\n(If you are in China, please set up a proxy to ensure that you can connect to openai.)\n```python\nimport os\n#os.environ[\'http_proxy\'] = \'http://127.0.0.1:10809\'  # 这里设置自己的代理端口号\n#os.environ[\'https_proxy\'] = \'http://127.0.0.1:10809\'  # 这里设置自己的代理端口号\nos.environ[\'OPENAI_CHAT_API_KEY\'] = \'sk-br3j7Gxxxxxxxxvt8r\'\n```\n- set up yaml file\nWe have some tools built in eg.code_interpreter,swe_tool\n\ntools.yaml\n```yaml\nYORG: 0.0.1\ninfo:\n  title: yorg_tools_document\n  description: yorg tool define document.\n  version: \'v1\'\ntools:\n  code_interpreter:\n    name: code_interpreter\n    entity_name: code_interpreter\n    summary: Run the code through code_interpreter and return the result of the code run. If your query is about math, computer science, or data science, you can use this tool to get the result of the code run.\n    parameters:\n      - name: code\n        description: code text that requires code_interpreter to run\n        required: true\n        parameter_schema:\n          type: string\n    responses:\n      success:\n        description: OK\n        content:\n          result:\n            type: string\n            description: the result of the code run\n  example_stateful_tool:\n    name: example_stateful_tool\n    entity_name: example_stateful_tool\n    summary: This tool is an example of a stateful tool. It will get two number from user input and return the sum of the two numbers.\n    parameters: []\n    responses: {}  \n  swe_tool:\n    name: sew_tool\n    entity_name: swe_tool\n    summary: SoftWare Engineer Agent(swe_tool) specializes in working with code files.\n    parameters: []\n    responses: {}  \n```\nTools are categorized into stateful tools and function tools,\nFunction tools can describe parameters and return values directly in tools.yaml\nFunctions can be registered using decorators\n```python\nfrom yorg_test.core.assistant.tools.tools import register_function_tool\n@register_function_tool\ndef code_test(code: str):\n    return {\n        "type": "success",\n        "content": {\n            "result": "Hello, World!",\n        },\n    }\n```\nIf it\'s a stateful tool you need to write an additional yaml file with a stateful description\n```yaml\nstart_stage: "init"\nfinish_stage: "finish"\nall_stages:\n  init:\n    name: "init"\n    next_stage_entry: \n      stage_1:\n        - name: x\n          required: true\n          parameter_schema:\n            type: number\n            description: "input value x"\n    need_llm_generate_parameters: false\n    need_llm_generate_response: false\n  stage_1:\n    name: "stage_1"\n    next_stage_entry: \n      stage_2:\n        - name: y \n          required: true\n          parameter_schema:\n            type: number\n            description: "input value y"\n    need_llm_generate_parameters: false \n    need_llm_generate_response: false\n  stage_2:\n    name: "stage_2"\n    next_stage_entry: \n      stage_3: []\n    need_llm_generate_parameters: false\n    need_llm_generate_response: false\n  stage_3:\n    name: "stage_3"\n    next_stage_entry: \n      finish: []\n    need_llm_generate_parameters: false\n    need_llm_generate_response: false\n  finish:\n    name: "finish"\n    next_stage_entry: {}\n    need_llm_generate_parameters: false\n    need_llm_generate_response: false\n```\nStateful tools can also be registered using decorators.\nThe yaml file is registered in init.\n```python\nfrom yorg_test.core.assistant.tools.tools import register_stateful_tool\nfrom yorg_test.core.assistant.tools.stateful_tool_entity import StatefulToolEntity\n@register_stateful_tool\nclass ExampleStatefulToolEntity(StatefulToolEntity):\n    """\n    This example tool entity is stateful, and it has 3 inner stages.\n\n    stage1: take integer x as input\n    stage2: take integer y as input\n    stage3: no input, return x + y\n    """\n    def __init__(self):\n        super().__init__("example_stateful_tool.yaml")\n    def _call(self, **kwargs):\n        if "goto" not in kwargs:\n            if self.current_stage.name == self.config.start_stage:\n                return {\n                    "type": "success",\n                    "content": {"message": "stateful tool is started"},\n                }\n            else:\n                return {\n                    "type": "error",\n                    "content": {"message": "please provide `goto` parameter"},\n                }\n        request_next_stage = kwargs["goto"]\n        if request_next_stage not in self.config.all_stages:\n            return {\n                "type": "error",\n                "content": {"message": f"stage {request_next_stage} not found"},\n            }\n        self.current_stage = self.config.all_stages[request_next_stage]\n        match self.current_stage.name:\n            case "stage_1":\n                return self._stage1(kwargs["x"])\n            case "stage_2":\n                return self._stage2(kwargs["y"])\n            case "stage_3":\n                return self._stage3()\n            case self.config.finish_stage:\n                return self._finish()\n            case _:\n                return {\n                    "type": "error",\n                    "content": {\n                        "message": f"stage {self.current_stage.name} not found"\n                    },\n                }\n    def _stage1(self, x: int):\n        self.x = x\n        return {"type": "success", "content": {"message": "stage1 done"}}\n    def _stage2(self, y: int):\n        self.y = y\n        return {"type": "success", "content": {"message": "stage2 done"}}\n    def _stage3(self):\n        return {"type": "success", "content": {"result": self.x + self.y}}\n    def _finish(self):\n        return {"type": "success", "content": {"message": "stateful tool is finished"}}\n```\n- run example\n\n```python\nimport yorg_test\nthreads = yorg_test.Threads.create(\'tools.yaml\')\nassistant = yorg_test.Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use swe tool auto fix code files", tools=[{\'type\':\'swe_tool\'}])\nprint(assistant.id)\n# 运行 Threads 对象\nresult = threads.run(assistant.id, "Use SoftWare Engineer Agent swe tool auto fix code files.")\nprint(result)\n\nresult = threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_1")\nprint(result)\n\nresult = threads.run(assistant.id, "add helloworld feature to readme",  goto="stage_2")\nprint(result)\n\nresult = threads.run(assistant.id, "focus_files_name_list = [README.md]", goto="stage_3")\nprint(result)\n\nresult = threads.run(assistant.id, "action=3", goto="stage_4")\nprint(result)\n\nresult = threads.run(assistant.id, "", goto="stage_5")\nprint(result)\n\nresult = threads.run(assistant.id, "action=0,action_idx=0", goto="stage_6")\nprint(result)\n\nresult = threads.run(assistant.id, "", goto="finish")\nprint(result)\n```\n\n',
    'author': 'zxy',
    'author_email': 'zhongxingyuemail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
