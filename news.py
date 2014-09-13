#!/usr/bin/env python


from BeautifulSoup import BeautifulSoup as bs
import hashlib


def to_str(var):
    if var == None:
        return 'null'
    return '"' + var + '"'

class news_class:
    """
        This is the news class for every news. No method included, only the
        attributes that matters are kept
    """

    title                = None
    description          = None
    image                = None
    source_modified_time = None
    url                  = None

    def sha1(self):
        h = hashlib.sha1()
        h.update(self.json())
        return h.digest()

    def sha1_hex(self):
        h = hashlib.sha1()
        h.update(self.json())
        return h.hexdigest()

    def md5(self):
        h = hashlib.md5()
        h.update(self.json())
        return h.digest()

    def md5_hex(self):
        h = hashlib.md5()
        h.update(self.json())
        return h.hexdigest()

    def json(self, json_obj = None):
        """
            Supply parameter json_obj to assign new content, updating
            existing data. If json_obj is not specified, return current
            fields as JSON object to caller.
        """
        if json_obj == None:

            o  = '{"title":%s,'      % (to_str(self.title))
            o += '"description":%s,' % (to_str(self.description))
            o += '"image":%s,'       % (to_str(self.image))
            o += '"url":%s,'         % (to_str(self.url))
            o += '"utime":%s'        % (to_str(self.source_modified_time))
            o += '}'

            return o
        else:
            """ to be implemented """
            return '{}'

class tags_hunter(bs):

    def get_title(self):
        return self.title.text.encode('utf-8')

    def get(self, pattern):
        m = self.findAll('meta')
        for n in m:
            for attr in n.attrs:
                a, v = attr

                # <meta http-equiv="Content-Type" content="text/html; charset=big5">
                # <meta       name="description"  content="my description"/>
                # <meta      name="keywords"      content="keyword1, kw2"/>
                #         [0][0]    [0][1]        [1][0]   [1][1]

                #print 'attr: ' + a.encode('utf-8') + ', value: ' + v.encode('utf-8')

                if n.attrs[0][0] == 'name' and n.attrs[0][1] == pattern and n.attrs[1][0] == 'content':
                    return n.attrs[1][1].encode('utf-8').replace('\n', '')
                if n.attrs[0][0] == 'property' and n.attrs[0][1] == pattern and n.attrs[1][0] == 'content':
                    return n.attrs[1][1].encode('utf-8').replace('\n', '')
        return None

    def get_news(self):
        N = news_class()

        N.title                 = self.get_title()

        N.description           = self.get('description')
        if N.description == None:
            N.descripton        = self.get('og:description')
        N.image                 = self.get('og:image')
        N.url                   = self.get('og:url')
        N.source_modified_time  = self.get('og:updated_time')

        return N
    
def dump(o):
    print("--------- obj dump ---------")
    for attr in dir(o):
        if hasattr( o, attr ):
            print("obj.%s = %s" % ( attr, getattr( o, attr ) ) )

if __name__ == "__main__":

    import sys
    import pprint
    
    pp = pprint.pformat

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            try:
                f = open( arg, "rb" )
                content = f.read()
                f.close()

                h = tags_hunter(content)
            except:
                print "failed to open file", sys.exc_info()[0]
                raise
    else:
        h = tags_hunter( '<html><head><title>my title</title><meta http-equiv="Content-Type" content="text/html; charset=big5"><meta name="description" content="my description"/><meta name="keywords" content="keyword1, kw2"/></head></html>' )

    print h.get_title()
    print h.get('description')
    print h.get('og:url')

    news = h.get_news()
    dump( news )
    print news.json()
    print news.md5_hex()
    print news.sha1_hex()
