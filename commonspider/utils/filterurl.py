# parse.py
'''
此程序是为了筛选出有可用的url，由于耗时太长最好在服务器中运行，并且相应的要修改路径
'''
import requests
from retrying import retry
import pandas as pd
# import pysnooper


class FilterUrl(object):

    def get_url(self):

        df = pd.read_excel('/home/leite/cd_domains.xlsx')

        df_li = df['domain'].values

        urls = []
        for i in df_li:

            url = 'https://www.' + i + '/collections/best-sellers'
            # print(url)
            urls.append(url)

        return urls

    # @pysnooper.snoop('/home/hepburn/bestsellers/example/snooper.log')
    # 最大重试3次，3次全部报错，才会报错
    # @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        requests.packages.urllib3.disable_warnings()  # 防止出现warning信息
        response = requests.get(url, timeout=3, verify=False)
        # 状态码不是200，也会报错并重试
        assert response.status_code == 200
        return response

    def write_url(self, url):
        with open('/home/leite/usefulurl.csv', 'a') as f:
            f.write(url)
            f.write('\n')

    def parse_url(self, url):

        try:  # 进行异常捕获
            response = self._parse_url(url)
            # useful_url = url
        except Exception as e:
            print(e)
            # 报错返回None
            response = None
        return response

    def run(self):
        urlst = self.get_url()
        useful_urls = []
        for url in urlst:

            response = self.parse_url(url)
            if response:
                useful_url = url
                useful_urls.append(useful_url)
                self.write_url(url)
        print(len(useful_urls))


if __name__ == '__main__':
    filter = FilterUrl()
    filter.run()
