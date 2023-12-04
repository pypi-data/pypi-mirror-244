from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from copy import copy
from os import kill, getpid
from queue import Queue, Empty
from threading import Lock
from time import sleep, time
from types import GeneratorType
from typing import Literal, Union
from requests import models
from .api import post, get
from traceback import format_exc
from objprint import add_objprint
from .Response import Response


def error_print(error):
    print(f"\033[91m{error}\033[0m")


Item = type('Item', (dict,), {})  # 传输数据对象


class BadResponse(models.Response):
    def __init__(self, status=600, text=b'{}'):
        super().__init__()
        self.status_code = status  # 状态
        self._content = text  # 空的数据


class Pipeline(metaclass=ABCMeta):  # 存储管道类
    @abstractmethod
    def save_data(self, item: dict): pass

    @abstractmethod
    def close(self): pass


@add_objprint
class Request:  # 请求对象类
    def __init__(self):
        self.url = None
        self.cookies: dict = {}
        self.headers: dict = {}
        self.data: dict = {}
        self.proxies = None
        self.callback = None  # 回调函数
        self._method = 'GET'  # 请求方法
        self.index: int = 0  # 请求索引
        self.retry: int = 0  # 重试次数
        self.info: str = ''  # 输出提示信息
        self.timeout = None  # 请求等待时间

    def make_request(self):
        """发起请求"""
        response_ = self.method_map(**self.options())
        return response_

    @property
    def method_map(self):
        """请求映射"""
        if self._method in ['POST', 'JSON_POST']:
            return post
        else:
            return get

    def options(self):
        """请求参数封装"""
        common_options: dict = {'url': self.url, 'cookies': self.cookies, 'headers': self.headers,
                                'proxies': self.proxies, 'timeout': self.timeout}
        if self._method == 'GET':
            common_options['params'] = self.data
        elif self._method == 'POST':
            common_options['data'] = self.data
        else:
            common_options['json'] = self.data
        return common_options

    @property
    def method(self) -> str:
        return self._method

    @method.setter
    def method(self, value: Literal['GET', 'POST', 'JSON_POST']) -> None:
        if value.upper() not in ['GET', 'POST', 'JSON_POST']:
            raise TypeError("The type of data requested is unknown, Available types:['GET', 'POST', 'JSON_POST']")
        self._method = value.upper()

    def copy(self):
        return copy(self)


class ThreadPool:  # 线程类
    save_class = None  # 爬虫存储类
    concurrency = 16  # 并发数量
    for_index_range = (1, 2)  # 初始循环区间

    random_user_agent = False  # 随机请求头
    timeout = None  # 等待时间
    request_sleep = 0  # 请求间隔/秒

    retry_request = False  # 重试请求
    retry_interval = 1  # 重试间隔/秒
    retry_time = 3  # 重试次数/次

    print_out = True  # 控制台运行信息
    print_result = True  # 运行结果输出
    fail_request_log = False  # 失败请求记录日志

    def __init__(self):
        self._qsize = 150  # 队列大小
        self.fail_request = 0  # 失败请求数量
        self.fail_request_list = []
        self.queue_ = Queue(self._qsize)  # 队列
        self.lock = Lock()  # 锁
        self.request_obj = False  # 请求对象 用于判断请求是否已经完成
        self.producer = Producer(self)  # 创建生产者
        self.consumer = Consumer(self)  # 创建消费者
        self.start()

    def run(self):
        self.producer.start_request_(self.start_requests)  # 生产者启动

        self.consumer.run()  # 消费者启动

        self.producer.wait()  # 等待生产者完成

        # 生产者完成，通知消费者没有数据就可以停止
        self.request_obj = True

        self.consumer.wait()  # 等待消费者线程完成

    def start(self):
        start_time = time()
        self.run()
        stop_time = time()

        if self.print_result:  # 结果输出
            print(f'result:[总用时:{round(stop_time - start_time, 2)}秒 '
                  f'请求次数:{self.producer.request_index} 失败请求:{self.fail_request}]')

        if self.fail_request_log:  # 失败请求存储
            from re import sub
            with open('fail_request_log.txt', 'w+', encoding='utf-8') as file:
                for fail_request in self.fail_request_list:
                    fail_request_str = sub('\x1b\[\d+m', "", str(fail_request))
                    file.write(f'{fail_request_str}\n')

    def pre_request_callback(self, request):
        """预请求回调"""
        if not self.random_user_agent:
            return  # 是否使用随机请求头
        from random import choice
        from .user_agent import USER_AGENT_LIST
        request.headers['User-Agent'] = choice(USER_AGENT_LIST)

    @abstractmethod
    def start_requests(self, request: Request, index: int):
        pass

    @abstractmethod
    def parse(self, item: Item, request_: Request, response: Response):
        pass


class Producer(ThreadPoolExecutor):  # 生产者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        super().__init__(max_workers=pipeline.concurrency, *args, **kwargs)
        self.pipeline = pipeline
        self.request_index = 0  # 请求次数记录
        self.futures = []  # 任务表
        self.bad_response = BadResponse()

    def wait(self):  # 等待请求线程池完成
        while self.futures:
            try:
                completed = [future for future in self.futures if future.done()]
                [self.futures.remove(future) for future in completed]
            except KeyboardInterrupt:
                error_print('KeyboardInterrupt: The thread pool program was forcibly terminated!')
                kill(getpid(), 0)  # 结束当前进程

    @staticmethod
    def error_message(_):
        return error_print(format_exc())

    def callback_(self, request_: Request) -> None:
        self.pipeline.pre_request_callback(request_)  # 请求之前调用

        before_time = time()
        try:  # 请求
            response = request_.make_request()
            self.print_(response, request_, time() - before_time, error='')
        except Exception as e:
            self.print_(self.bad_response, request_, time() - before_time, error=e)
            return

        try:  # 回调函数调用
            generator: GeneratorType = request_.callback(Item(), request_, response)
        except Exception as e:
            return self.error_message(e)

        if generator is None:
            return  # 是否是生成器已经可用
        elif not isinstance(generator, GeneratorType):
            return error_print("TypeError: The returned object is not a generator, "
                               "use 'yield' as the return keyword")
        else:
            # 回调返回的生成器数据处理
            self.callback_generator_processing(generator, request_)

    def callback_generator_processing(self, generator: GeneratorType, request_: Request):
        try:  # 回调生成器处理
            for return_ in generator:
                if isinstance(return_, Request):  # 回调函数/管道数据判断
                    with self.pipeline.lock:  # 全局请求次数锁
                        self.request_index += 1
                        request_.index = self.request_index
                    self.futures.append(self.submit(self.callback_, request_.copy()))
                    sleep(self.pipeline.request_sleep)
                elif isinstance(return_, (Item, dict)):
                    self.pipeline.queue_.put(return_)
                else:
                    raise TypeError('The returned object is not a usable object')
        except Exception as e:
            return self.error_message(e)

    def print_(self, response: Union[Response, BadResponse], request_: Request, take_time, error) -> None:
        # 爬取信息显示
        with self.pipeline.lock:
            # 获取当前任务数量
            completed = [future if future.done() else None for future in self.futures]
            none_count = max(completed.count(None), 1) - 1

            print_dict = {
                'ID': str(request_.index),
                '状态': str(response.status_code),
                '待完成': str(none_count),
                '用时': f'{take_time:.2f}', '重试': None,
                'info': request_.info, 'error': error,
            }

            if response.status_code < 400:
                pass
            elif self.pipeline.retry_request and request_.retry < self.pipeline.retry_time:  # 运行重新尝试
                request_.retry += 1  # 是否进行重试
                sleep(self.pipeline.retry_interval)  # 重试请求间隔
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['重试'] = request_.retry
                self.futures.append(self.submit(self.callback_, request_.copy()))
            else:
                self.pipeline.fail_request_list.append(request_.copy())
                self.pipeline.fail_request += 1  # 请求失败纪录
                print_dict['状态'] = f'\x1b[1;31;3m{response.status_code}\x1b[0m'
                print_dict['error_data'] = request_.data
                print_dict['error_url'] = request_.url

            if self.pipeline.print_out:
                print('<' + '  '.join([f'{k}:{v}' for k, v in print_dict.items() if v]) + '>')

    def start_request_(self, start_requests) -> None:
        # 初始链接请求
        for index in range(*self.pipeline.for_index_range):
            request = Request()
            request.callback = self.pipeline.parse
            request.timeout = self.pipeline.timeout
            for request_ in start_requests(request, index):
                with self.pipeline.lock:
                    self.request_index += 1
                    request_.index = self.request_index
                self.futures.append(self.submit(self.callback_, request_))
                sleep(self.pipeline.request_sleep)


class Consumer(ThreadPoolExecutor):  # 消费者
    def __init__(self, pipeline: ThreadPool, *args, **kwargs):
        self.pipeline = pipeline
        self._consume_list = []  # 消费者列表
        self.timeout_ = 0.2  # 消费者超时断开
        self.save_class = pipeline.save_class  # 存储类
        self.concurrency = 10  # 消费者并发数量
        if self.save_class is not None:
            self.save_class = self.save_class()  # 存储类初始化
        super().__init__(max_workers=self.concurrency, *args, **kwargs)

    def run(self) -> None:
        """运行消费者"""
        if self.save_class:
            self._consume_list = [self.submit(self.data_save_) for _ in range(self.concurrency)]

    def wait(self) -> None:
        """等待线程完成"""
        if self.save_class:
            wait(self._consume_list, return_when=ALL_COMPLETED)
            self.save_class.close()  # 关闭文件存储

    def data_save_(self) -> None:  # 数据存储
        while True:
            try:
                items = self.pipeline.queue_.get(timeout=self.timeout_)
                if self.pipeline.save_class:
                    self.submit(self.save_class.save_data, items)
                else:
                    break
            except Empty:
                if self.pipeline.request_obj:  # 请求队列完成了，可以结束了
                    break
            except Exception as e:
                print(e)
