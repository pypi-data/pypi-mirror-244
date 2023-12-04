import os

from pytestifyx.driver.api import BaseRequest
from pytestifyx.driver.web import BasePage
from pytestifyx.config import pytestifyx_str
from pytestifyx.utils.requests.requests_config import Config


class TestCase:

    def setup_method(self, method):
        # 每个测试方法执行前，重置配置
        self.config = Config()

    @classmethod
    def setup_class(cls):
        print(pytestifyx_str)
        print('------------------------------用例测试启动🚀🚀🚀------------------------------')

    @staticmethod
    def page(play: object, name: str = None):
        print('首次运行会下载浏览器驱动⏬，请耐心等待⌛️')
        os.system('python -m playwright install')
        return BasePage(play, name=name)

    def api(self, path, func_name, config, params, **kwargs):
        return BaseRequest().base(path, func_name, config, params, **kwargs)
