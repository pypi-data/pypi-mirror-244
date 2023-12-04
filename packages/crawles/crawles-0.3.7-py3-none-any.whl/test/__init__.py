# coding = utf-8
import crawles

url = 'https://cs.lianjia.com/ershoufang/'

cookies = {
    'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1701668342',
    'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1700655283,1700721804,1701261973,1701668342',
    '_ga': 'GA1.2.427412909.1701668344',
    '_ga_4JBJY7Y7MX': 'GS1.2.1701668344.1.0.1701668344.0.0.0',
    '_gid': 'GA1.2.413357999.1701668344',
    '_jzqa': '1.981802551013793700.1700485320.1701261974.1701668343.7',
    '_jzqc': '1',
    '_jzqckmp': '1',
    '_qzja': '1.1200595011.1700485320657.1701261974291.1701668343011.1701261974291.1701668343011.0.0.0.37.7',
    '_qzjc': '1',
    '_qzjto': '1.1.0',
    '_smt_uid': '655b58c6.5c1f4d9f',
    'lianjia_uuid': 'b5bb5fe9-3bde-4d27-b458-5e8ba4c2bdcb',
    'select_city': '430100',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218becd2cb3aa-066576e70284d8-26031d51-1327104-18becd2cb3b52d%22%2C%22%24device_id%22%3A%2218becd2cb3aa-066576e70284d8-26031d51-1327104-18becd2cb3b52d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
    'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNGQ4ZjJjNzg0NTIxZTU0NTYyNmI1YmY0MmJmY2YwOTBiMGVmZDc1YjhjOTE0NmE5MTA3YjNkYmNjZjRlZjU5YzgxMmMwODBkZTA2ZGQzMDYxZDk4YTkwMGViMDliMmZhOGY2NDgzOTdlYWNiNDM4MzViZTBhYmFjMzM1N2QzOGQwNDkzNzBjMjg2ZWY5YmUyMzIxMGI2MzQ1MjQyNDI2NjJiOTcyNDI5ZjQ3NDIzMTgwNjBlMjM1MTE3M2ZiZGUwMWJlNGJkOTU4MTZhOWQ1ZjcwMGI5MmJkNDNjMmY0NjVkNDUwZWQ5ODFiMmNlYmE1NTdmYmVkNjAwMzQxNjg3YlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjNTc5MTQzOVwifSIsInIiOiJodHRwczovL2NzLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

params = {
}

# 当前时间戳: 1701671494.0264153
response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.save('链家网.html'))
