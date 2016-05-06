from scrapy.conf import settings
from scrapy import log
import random

'''
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        print "\n\n request.url : ", request.url
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)
            #this is just to check which user agent is being used for request
            spider.log(
                u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
                level=log.DEBUG
                )


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
'''

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        print "\n\n request in proxy : ", request
        request.meta['proxy'] = settings.get('HTTP_PROXY')

'''
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
        #like here request.meta['proxy'] = "https://YOUR_PROXY_IP:PORT"
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
'''