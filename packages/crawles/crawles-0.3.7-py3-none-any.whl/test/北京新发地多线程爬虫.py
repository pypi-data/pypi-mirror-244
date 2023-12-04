# coding = utf-8
import crawles


class AAA(crawles.Pipeline):
    def __init__(self):
        pass

    def save_data(self, item: dict):
        pass

    def close(self):
        pass


class ThreadSpider(crawles.ThreadPool):
    save_class = None
    for_index_range = (1, 3)  # 初始循环区间
    retry_request = True
    timeout = 3
    fail_request_log = True

    def start_requests(self, request, index):
        request.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.xinfadi.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'X-Requested-With': 'XMLHttpRequest',
        }
        request.data = {
            'current': index,
            'limit': '20',
            'prodCatid': '',
            'prodName': '',
            'prodPcatid': '',
            'pubDateEndTime': '',
            'pubDateStartTime': '',
        }
        request.url = 'http://www.xinfadi.com.cn/getPriceData.html'
        request.method = 'POST'  # GET POST JSON_POST
        yield request

    def parse(self, item, request, response):
        item['text'] = response.json()
        # crawles.op(request)


ThreadSpider()
