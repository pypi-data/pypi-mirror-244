from collections import deque, abc
from concurrent import futures

from scrapgo.core import SoupParser, RequestsBase, CachedRequests
from scrapgo.core.http import RequestsBase
from scrapgo.lib import pluralize

from .actions import resolve_link, ReduceMixin



class CrawlMixin(ReduceMixin, SoupParser):
    urlorders = None

    def crawl(self, _urlorders=None, _results=None, parent_response=None, _composed:dict=None, _context:dict=None, _composed_buffer:dict=None):

        if _urlorders is None:
            action, *rest = self.urlorders
        elif len(_urlorders) == 0:
            return 
        else:
            action, *rest = _urlorders
        
        _context = _context or dict()
        
        _composed = _composed or dict()
        _composed.setdefault(action.name, [])

        _composed_buffer = _composed_buffer or dict()
        _composed_buffer.setdefault(action.name, [])
        

        def build_requests():
            def __resolve(link):
                url = resolve_link(action, link, parent_response)
                return self.dispatch_fields(action, url)

            def _build_urls():
                links = self.dispatch_renderer(action, _results, parent_response, _context)
                for link in links:
                    url = __resolve(link)
                    if self.dispatch_urlfilter(action, url, _results, _context):
                        yield url

            def _build_payloads():
                yield from self.dispatch_payloader(action, _results, _context)
                
            def __build_kwargs(url, payload):
                cookies = self.dispatch_cookies(action)
                headers = self.dispatch_headers(action)
                payload = payload or None
                kwargs = dict(url=url, headers=headers, cookies=cookies)
                json_type = False
                if content_type := headers.get('Content-Type'):
                    if 'application/json' in content_type:
                        json_type = isinstance(payload, (dict, list))
                kwargs['json' if json_type else 'data'] = payload
                return kwargs
            for url in _build_urls():
                for payload in _build_payloads():
                    kwargs = __build_kwargs(url, payload)
                    yield kwargs
        
        def process_response(kwarg):
            def _retrieve(kw):
                try:
                    r = self.dispatch_response(action, **kw)
                except Exception as e:
                    self.dispatch_onfailure(action, e, parent_response, _results, _context, **kw)
                    raise
                else:
                    if self.dispatch_ignore_status_codes(action, r) is True:
                        return False
                    if not self.dispatch_response_filter(action, r, _results, _context):
                        return False
                    return r
                    
            def _parse(r):
                is_parsable = self._is_parsable(r)
                soup = self._load_soup(r.content) if is_parsable else r.content
                extracted = self.dispatch_extractor(action, soup, r, _results, _composed, _context)
                
                results, contexts = [], []
                for result_set in self.dispatch_parser(action, r, extracted, soup, _results, _composed, _context):
                    if result_set:
                        res, ctx = result_set
                        results += pluralize(res)
                        contexts.append(ctx)

                return results, contexts, r, is_parsable
            
            if (response:= _retrieve(kwarg)) is not False:
                return  _parse(response)
        
        requests_kwargs = build_requests()
        max_workers = self.settings.get('REQUEST_MAX_WORKERS')
        if action.workers:
            with futures.ThreadPoolExecutor(min(action.workers, max_workers)) as excutor:
                processeds = excutor.map(process_response, requests_kwargs)
        else:
            processeds = map(process_response, requests_kwargs)

        rendered = False
        
        for results, contexts, response, is_parsable in filter(None, processeds):
            rendered = True
            _composed[action.name] += results
            _composed_buffer[action.name] += results
            context_one = contexts[0] if contexts else {}

            action.pipeline(results, response=response, context=_context)

            if not action.bfo or is_parsable:
                if action.follow_each:
                    for result, context in zip(results, contexts):
                        self.crawl(rest, result, response, _composed, _context=context, _composed_buffer=_composed_buffer)
                else:
                    self.crawl(rest, results, response,  _composed, _context=context_one, _composed_buffer=_composed_buffer)
            else:
                self.crawl(rest, _results, parent_response, _composed, _context=context_one, _composed_buffer=_composed_buffer)

        if not rendered and action.bfo:
            self.crawl(rest, _results, parent_response, _composed, _context=_context, _composed_buffer=_composed_buffer)
    
        if _urlorders is None:
            self.dispatch_compose(_composed)


class RequestsCrawler(CrawlMixin, RequestsBase):
    pass


class CachedRequestsCrawler(CrawlMixin, CachedRequests):
    pass
