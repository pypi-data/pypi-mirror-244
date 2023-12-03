# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdevtoolslight',
 'sfdevtoolslight.devTools',
 'sfdevtoolslight.observability',
 'sfdevtoolslight.observability.logging_json',
 'sfdevtoolslight.observability.logstash',
 'sfdevtoolslight.storage',
 'sfdevtoolslight.storage.documentDBStorage',
 'sfdevtoolslight.storage.objectStorage',
 'sfdevtoolslight.storage.relationalDBStorage',
 'sfdevtoolslight.storage.timeseriesDBStorage']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'openpyxl>=3.1.2,<4.0.0',
 'sqlalchemy>=2.0.23,<3.0.0']

setup_kwargs = {
    'name': 'sfdevtoolslight',
    'version': '1.2.0',
    'description': '',
    'long_description': '## How to publish to pypi\n```bash\n# set up pypi token\npoetry config pypi-token.pypi my-token\n\n# build the project\npoetry build\n\n# publish the project\npoetry publish\n\n# DONE\n```\n\n## Generate source code from protobuf\n```bash\n$ poetry add grpcio-tools\n$ poetry add grpcio\n$ cd sfdevtools/\n$ poetry run python -m grpc_tools.protoc -I ./grpc_protos --python_out=./grpc_protos/ --grpc_python_out=./grpc_protos/ ./grpc_protos/peacock.proto\n```\n\n## Demo example\n### Double check lock for singleton\n```python\nimport sfdevtools.observability.log_helper as lh\nimport logging\nlogger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)\n# create class X\nclass X(SDC):\n    pass\n\n# create class Y\nclass Y(SDC):\n    pass\n\nA1, A2 = X.instance(), X.instance()\nB1, B2 = Y.instance(), Y.instance()\n\nassert A1 is not B1\nassert A1 is A2\nassert B1 is B2\n\nlogger.info(\'A1 : {}\'.format(A1))\nlogger.info(\'A2 : {}\'.format(A2))\nlogger.info(\'B1 : {}\'.format(B1))\nlogger.info(\'B2 : {}\'.format(B2))\n```\n\n### Send log to logstash\n```python\nlogger = lh.init_logger(logger_name="connection_tester_logger"\n                        , is_json_output=False\n                        , is_print_to_console=True\n                        , is_print_to_logstash=True\n                        , logstash_host="<the host name>"\n                        , logstash_port=5960\n                        , logstash_user_tags=["Test001", "Test002"])\nlogger.info("Test Message from test")\nlogger.error("Test Message from test")\nlogger.warning("Test Message from test")\n```\n\n### Simple function pool\n```python\nimport sfdevtools.observability.log_helper as lh\nimport sfdevtools.devTools.FuncFifoQ as FuncFifoQ\nfrom functools import partial\nfrom time import sleep\n\nlogger = lh.init_logger(logger_name="test_func_fifo_q", is_print_to_console=True, is_json_output=False)\nfunc_q: FuncFifoQ.FuncFifoQ = FuncFifoQ.FuncFifoQ(logger=logger, pool_size=10)\nfunc_q.start_q()\nfor i in range(10):\n    func_q.push_func(partial(self.__func_test_foo, i, "hi"))\n\nlogger.info("Before sleep")\nsleep(2)\nlogger.info("After sleep")\n\nfunc_q.stop_q()\n```\n\nExpected output:\n```bash\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:test_func_fifo_q:144] [MainThread:92105] Before sleep\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-4:92105] Hi from thread: 0\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-8:92105] Hi from thread: 1\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-3:92105] Hi from thread: 2\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-2:92105] Hi from thread: 3\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-9:92105] Hi from thread: 4\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-5:92105] Hi from thread: 5\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-7:92105] Hi from thread: 6\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-10:92105] Hi from thread: 7\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-6:92105] Hi from thread: 8\n2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-1:92105] Hi from thread: 9\n2023-02-13 13:50:50,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:test_func_fifo_q:146] [MainThread:92105] After sleep\n2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-7:92105] End\n2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-5:92105] End\n2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-4:92105] End\n2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-10:92105] End\n2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-1:92105] End\n2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-3:92105] End\n2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-8:92105] End\n2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-6:92105] End\n2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-2:92105] End\n2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-9:92105] End\n```\n',
    'author': 'SulfredLee',
    'author_email': 'sflee1112@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
