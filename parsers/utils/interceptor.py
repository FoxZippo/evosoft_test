USER_AGENT_HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
ACCEPT_HEADER = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'


def interceptor(request):
    """ Changes request headers """
    request.headers['User-Agent'] = USER_AGENT_HEADER
    request.headers['Accept'] = ACCEPT_HEADER
