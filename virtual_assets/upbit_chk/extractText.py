# 임의의 웹 페이지에서 텍스트를 추출하기
# 출처: https://bab2min.tistory.com/618
class AutoExtractor:
    """
    임의의 웹 페이지에서 본문으로 추정되는 부분만 추출하는 클래스입니다.
    """

    def __init__(self):
        import re, pickle, os
        self.reID = re.compile(''' id=("[^"']+"|'[^']+')''', re.I)
        self.reClass = re.compile(''' class=("[^"']+"|'[^']+')''', re.I)
        self.reIdClass = re.compile(''' (id|class)=("[^"']+"|'[^']+')''', re.I)
        self.reNewline = re.compile('[\r\n]{2,}')
        self.templateCachePath = 'elementTemplate/'
        self.commonThreshold = 0.4
        self.maxLookup = 10
        try:
            os.mkdir(self.templateCachePath)
        except:
            pass
        self.elementTemplateCache = {}

    def isHomomorph(self, values):
        from collections import Counter
        l = list(values)
        return Counter(l).most_common(1)[0][1] >= len(l) * self.commonThreshold

    @staticmethod
    def commonest(values):
        from collections import Counter
        return Counter(values).most_common(1)[0][0]

    def findSimilarPage(self, url, dUrl=None):
        '''url과 유사한 페이지를 찾는 함수'''

        import urllib, urllib.request, urllib.parse, bs4, re
        o = urllib.parse.urlparse(url)
        html, url = self.fetchHTML(dUrl if dUrl else url)
        url = re.sub('#.*$', '', url)
        url = re.sub('\?$', '', url)
        soup = bs4.BeautifulSoup(html, "lxml")
        links = set([url])
        base = ''
        # first, try pages with different parameters only
        for a in soup.select('a'):
            try:
                if not a['href'] or a['href'].startswith('#') or a['href'].startswith('javascript:'): continue
                href = re.sub('#.*$', '', a['href'])
                href = re.sub('\?$', '', href)
                t = urllib.parse.urlparse(href)
                if (not t.scheme or t.scheme == o.scheme) \
                        and (not t.netloc or t.netloc == o.netloc) \
                        and ((not t.netloc and not t.path) or t.path == o.path):
                    links.add(urllib.parse.urljoin(url, href))
                    base = o.scheme + '://' + o.netloc + o.path
            except:
                pass
        # second, try pages with different subdirectory
        if len(links) <= 3:
            for a in soup.select('a'):
                try:
                    if not a['href'] or a['href'].startswith('#') or a['href'].startswith('javascript:'): continue
                    t = urllib.parse.urlparse(a['href'])
                    if (not t.scheme or t.scheme == o.scheme) \
                            and (not t.netloc or t.netloc == o.netloc):
                        links.add(urllib.parse.urljoin(url, a['href']))
                        base = o.scheme + '://' + o.netloc
                except:
                    pass
        # if there are no urls related, go deep searching
        if len(links) <= 3 and not dUrl:
            deepSearchList = set()
            for a in soup.select('a'):
                try:
                    if not a['href'] or a['href'].startswith('#') or a['href'].startswith('javascript:'): continue
                    t = urllib.parse.urlparse(a['href'])
                    deepSearchList.add(urllib.parse.urljoin(url, a['href']))
                except:
                    pass
            try:
                deepSearchList.remove(url)
            except:
                pass
            for d in deepSearchList:
                newLinks, newBase = self.findSimilarPage(url, d)
                if len(newLinks) > 1:
                    links |= set(newLinks)
                    base = newBase
                    break
        return [url] + list(links - set([url])), base

    def fetchHTML(self, url):
        '''웹 페이지를 가져오는 함수'''
        import urllib, urllib.request, urllib.parse, random
        try:
            t = urllib.parse.urlparse(url)
            params = [(k, v[0]) for k, v in urllib.parse.parse_qs(t.query).items()]
            url = t.scheme + '://' + t.netloc + t.path + '?' + urllib.parse.urlencode(params)
            headerList = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko']
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': random.sample(headerList, 1)[0]
                }
            )
            f = urllib.request.urlopen(req)
            newUrl = f.geturl()
            rawbytes = f.read()
            f.close()
            try:
                return self.refineDuplicatedHTMLId(rawbytes.decode('utf-8')), newUrl
            except UnicodeDecodeError:
                return self.refineDuplicatedHTMLId(rawbytes.decode('euc-kr')), newUrl
        except:
            raise RuntimeError('Cannot open ' + url)

    def refineDuplicatedHTMLId(self, html):
        '''일부 비표준 사이트에서는 엘리먼트 ID를 중복해서 사용합니다.
        이 경우 각 ID를 유니크하게 바꿔주는 함수'''
        import re
        dups = {}
        from collections import Counter
        for k, v in Counter(id[1:-1] for id in self.reID.findall(html)).most_common():
            if v <= 1: break
            dups[k] = v
        for id, n in dups.items():
            for i in range(n):
                html = re.sub(''' id=('%s'|"%s")''' % (id, id), ' id="%s___%d"' % (id, i), html, 1)
        return html

    class IdTree:
        def __init__(self, id='', depth=0):
            self.id = id
            self.depth = depth
            self.children = []
            self.idMap = {}

        def __repr__(self):
            return "IdTree('%s', %d)" % (self.id, self.depth)

        def makeTree(self, ids, element):
            for el in element.children:
                if not el.name: continue
                try:
                    id = '#' + el['id']
                    if id in ids:
                        child = AutoExtractor.IdTree(id, self.depth + 1)
                        child.makeTree(ids, el)
                        self.children.append(child)
                        continue
                except:
                    try:
                        id = '.' + '.'.join(el['class'])
                        if id in ids:
                            child = AutoExtractor.IdTree(id, self.depth + 1)
                            child.makeTree(ids, el)
                            self.children.append(child)
                            continue
                    except:
                        pass
                self.makeTree(ids, el)

        def traverse(self, func):
            for child in self.children:
                func(child)
                child.traverse(func)

        def hasDescendant(self, id):
            for child in self.children:
                if child.id == id: return True
                if child.hasDescendant(id): return True
            return False

    def buildIdTree(self, soup, ids):
        tree = AutoExtractor.IdTree()
        tree.makeTree(set(ids), soup)
        tree.traverse(lambda node: tree.idMap.__setitem__(node.id, node))
        return tree

    def findDifferentElement(self, urls):
        '''urls 페이지들에서 공통적으로 등장하지만 내용물은 다른 본문 후보를 추출하는 함수'''
        from collections import Counter
        import bs4
        # load web pages
        pages = []
        for url in urls:
            try:
                pages.append(self.fetchHTML(url)[0])
            except:
                pass
            time.sleep(0.75)

        soups = []
        duplTest = {}
        # parse html and remove unneccesaries
        for i, page in enumerate(pages):
            soup = bs4.BeautifulSoup(page, "lxml")
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            [s.extract() for s in soup('iframe')]
            [s.extract() for s in soup('a')]
            [s.extract() for s in soup('li')]
            [s.extract() for s in soup('header')]
            [s.extract() for s in soup('footer')]
            t = soup.text.strip()
            if t not in soups: duplTest[t] = i
            soups.append(soup)

        # find common id
        idCnt = Counter()
        for i, page in enumerate(pages):
            if i not in duplTest.values(): continue
            idCnt.update(set('#' + id[1:-1] for id in self.reID.findall(page)))
            classes = Counter(re.sub(' +', '.', ' ' + cls[1:-1]) for cls in self.reClass.findall(page))
            idCnt.update(k for k, v in classes.items() if v == 1)
        commonID = [id for id, n in idCnt.most_common() if n >= len(pages) * self.commonThreshold]

        # check text variants of each id
        pageIdTexts = {}
        pageIdRests = {}
        pageIdTextFix = {}
        for cmd_id in commonID:
            texts = []
            for page in soups:
                el = page.select_one(cmd_id)
                texts.append(el.text.strip() if el else '')
                pageIdTexts[cmd_id] = texts

        # remove elements with common text
        for cmd_id, values in list(pageIdTexts.items()):
            if self.isHomomorph(values):
                del pageIdTexts[cmd_id]
                continue

        # remove elements with common text except children elements
        tree = self.buildIdTree(soups[0], commonID)

        def calcRest(node):
            if not node.children: return
            texts = []
            for page in soups:
                el = page.select_one(node.id)
                if el:
                    for child in node.children:
                        t = el.select_one(child.id)
                        if t: page.body.insert_after(t.extract())
                texts.append(el.text.strip() if el else '')
            pageIdRests[node.id] = texts

        tree.traverse(calcRest)

        for cmd_id, values in pageIdRests.items():
            try:
                if self.isHomomorph(values): del pageIdTexts[cmd_id]
            except:
                pass

        ids = list(pageIdTexts.keys())
        ids = [id for id in ids if tree.idMap.get(id)]
        ids.sort(key=lambda id: tree.idMap[id].depth)
        uniqs = []
        for idA in ids:
            if any(map(lambda id: tree.idMap[id].hasDescendant(idA), uniqs)): continue
            uniqs.append(idA)
        idOrder = []
        for m in self.reIdClass.finditer(pages[0]):
            if m.group(1) == 'id':
                cmd_id = '#' + m.group(2)[1:-1]
            elif m.group(1) == 'class':
                cmd_id = re.sub(' +', '.', ' ' + m.group(2)[1:-1])
            if cmd_id in commonID: idOrder.append(cmd_id)
        uniqs.sort(key=idOrder.index)

        # detect common prefix & suffix
        for cmd_id in uniqs:
            values = pageIdTexts[cmd_id]
            i = 0
            j = 0
            while i < len(values[0]) and self.isHomomorph(v[i] if i < len(v) else '' for v in values):
                i += 1
            while -j < len(values[0]) and self.isHomomorph(v[j - 1] if -j < len(v) else '' for v in values):
                j -= 1
            pageIdTextFix[cmd_id] = AutoExtractor.commonest(v[:i] for v in values), AutoExtractor.commonest(
                v[j:] for v in values)
        return [(u, pageIdTextFix[u]) for u in uniqs]

    def waitOpenFile(self, path):
        import os.path, time
        if not os.path.exists(path) or not os.path.isfile(path): return
        for _ in range(10):
            try:
                f = open(path, 'rb')
                return f
            except IOError:
                time.sleep(10)
        raise IOError("Failed to open '%s'" % path)

    def getElementTemplate(self, url, maxLookup=0):
        '''본문 템플릿을 캐싱하고 가져오는 함수'''
        import time, pickle, os, re
        if maxLookup == 0: maxLookup = self.maxLookup
        # first, search in memory
        for k, v in self.elementTemplateCache.items():
            if url.startswith(k): return v

        # second, search in local file
        try:
            nurl = re.sub('[:/]', '_', url)
            for name in os.listdir(self.templateCachePath):
                if nurl.startswith(name):
                    with self.waitOpenFile(self.templateCachePath + name) as f:
                        base, elements = pickle.load(f)
                        self.elementTemplateCache[base] = elements
                        return elements
        except:
            pass

        # else, build and save template
        ls, base = self.findSimilarPage(url)
        with open(self.templateCachePath + re.sub('[:/]', '_', base), 'wb') as f:
            if len(ls) < 3: raise RuntimeError("Lack of related pages to make template")
            elements = self.findDifferentElement(ls[:maxLookup])
            self.elementTemplateCache[base] = elements
            pickle.dump((base, elements), f)
        return elements

    def extractText(self, url):
        '''위의 함수들을 종합하여, 실제 본문을 추출해주는 함수'''
        import bs4
        html, url = self.fetchHTML(url)
        soup = bs4.BeautifulSoup(html, "lxml")
        tmplt = self.getElementTemplate(url)
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        [s.extract() for s in soup('iframe')]
        [s.extract() for s in soup('a')]
        [s.extract() for s in soup('li')]
        [s.extract() for s in soup('header')]
        [s.extract() for s in soup('footer')]
        text = ''
        for el in tmplt:
            node = soup.select_one(el[0])
            if not node: continue
            t = node.text.strip()
            if t.startswith(el[1][0]): t = t[len(el[1][0]):]
            if t.endswith(el[1][1]): t = t[:-len(el[1][1])]
            text += t + '\n'
        return self.reNewline.sub('\n', text.strip()), url


if __name__ == "__main__":
    import sys, re, time, traceback

    ae = AutoExtractor()
    txt, url = ae.extractText(sys.argv[1])
    print(url, re.sub('\s+', ' ', txt), sep='\t')
