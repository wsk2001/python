# Python 임의의 웹 페이지에서 텍스트를 추출하기

텍스트 마이닝을 하는 데에 있어 텍스트 데이터를 수집하는것은 아주 중요합니다. 아무리 휘황찬란한 텍스트 분석 기술이 있어도 분석할 텍스트가 없다면 쓸모가 없으니깐요. 과거였다면 대량의 텍스트 데이터를 구하는게 어려운 작업이었겠지만, 현재는 다행히도 웹으로부터 (정제되지는 않았지만) 수많은 텍스트를 구할 수 있습니다. 

웹 페이지에서 텍스트를 추출하는 작업은 의외로 간단합니다. 웹 페이지들은 HTML이라는 마크업 랭귀지로 구성되어 있고, 여기에서 필요한 텍스트만을 뽑아오는건 HTML 파서나 정규표현식 등을 이용해 쉽게 이뤄질 수 있기 때문입니다. 다만 문제는 우리가 보는 웹 페이지에는 실제 알맹이보다 다양한 껍데기들이 많다는 것입니다.



![img](./images/9925C33E5BDE721028.jpg)

위 사진은 한 신문사의 기사 페이지입니다. 이 페이지의 알맹이는 기사 내용이 있는 부분이겠지만, 실제로 다른 메뉴나 관련 기사, 광고와 같은 껍데기 부분도 전체 페이지에서 꽤나 큰 비중을 차지하고 있습니다. 따라서 그냥 HTML 코드에서 텍스트만 추출한다면 불필요한 부분이 너무 많이 추출될 것입니다.



물론 최신 HTML5를 따라 시맨틱에 따라 태그를 잘 부여하고 SEO가 잘 되어 있다면, 충분히 본문과 내비게이션, 광고들을 구분하여 수집할 수 있습니다. 이런 태그적인 특성과 머신러닝을 활용하여 본문만 추출해내는 라이브러리도 있습니다. 



https://boilerpipe-web.appspot.com/



불행히도 국내 사이트들 중 많은 수는 표준과는 동떨어져 있어서 이런 방법으로 처리하기 어려운 경우가 많습니다. 따라서 웹 페이지에서 적절한 내용을 추출하기 위해서는 사이트마다 실제 본문이 위치한 부분을 찾아내어 그 부분만 추출하도록 해야하는데, 이게 꽤나 수작업이 들어가는 부분이죠. 이걸 어느 정도 자동화할 수 있을까요? 사람들이 본문과 기타 메뉴, 광고들을 구분하듯이, 자동적으로 프로그램이 본문만 구별해낼 수 있을까요?



## 관찰

### 1. 같은 사이트 내의 페이지들은 구조적으로 유사하다

한 사이트 내의 여러 페이지들은 디자인이 유사합니다. 매 페이지마다 구조나 디자인이 다르다면 이 페이지를 방문하는 이용자들은 혼란에 빠질 수 밖에 없습니다. 따라서 틀은 같지만 내용만 다르게 구성되어 있죠. 이 말은 즉, 페이지 내에서 변하는 부분과 변하지 않는 부분이 있다는 것입니다. 변하지 않는 부분은 메뉴와 같은 부분입니다. 우리가 관심이 없는 부분이죠. 반면 변하는 부분은 본문이거나 관련 기사거나 광고겠죠. 

즉 유사한 페이지들과 현재 페이지를 비교하면 현재 페이지에서 변하지 않는 부분을 찾아낼 수 있고, 이 부분을 잘라버려서 1차적으로 필터링 할 수 있을 겁니다.

### 2. 광고나 관련 페이지 메뉴에는 항상 링크가 걸려 있다

이들은 그 성격상 항상 링크가 달려있을 수 밖에 없습니다. 따라서 만약 링크로만 구성된 엘리먼트들이 모여있다면, 이것은 광고거나 관련 페이지로 내비게이션을 하는 부분일 가능성이 높습니다. 우리가 읽는 본문에는 링크(<a> 태그로 감싸진 부분)가 적고, 일반 문장들이 많겠죠(<p>태그로 로 감싸진 부분). 따라서 태그적인 특성을 가지고 이 부분이 본문인지 아닌지 가늠해볼 수 있을 겁니다.

## 원시적인 알고리즘

위의 관찰들을 바탕으로 본문일것 같은 부분만을 추출하는 알고리즘을 정리해보면 다음과 같겠습니다.



**본문 템플릿 구축**

1. 입력 페이지에서 같은 사이트 내의 다른 페이지로 연결되는 링크를 모두 찾는다.
   (이 링크들은 아마 사이트 내 유사 페이지로 연결될 가능성이 높으므로 이를 골라내기 위함입니다.)
2. 연결되는 모든 페이지를 가져와서 HTML을 파싱한다. 가져온 페이지들 중에 동일한 내용의 페이지가 있을 경우 제거한다.
3. 가져온 페이지들의 HTML 엘리먼트 들의 ID를 가져온다. 이 중 일정 횟수 이상 공통되는 ID만 골라낸다.
   (여러 페이지에서 공통으로 쓰이는 엘리먼트 ID들은 해당 페이지의 템플릿을 구성하는 ID일 겁니다. 즉 뼈대라고 할 수 있겠죠)
4. 공통되는 ID들에 포함된 내용이 페이지들마다 다른지 확인한다. 대부분의 페이지에서 동일한 내용을 가지고 있는 ID라면 본문 후보에서 제거한다.
   (여러 페이지에서 동시에 등장하며, 그 내용이 동일한 엘리먼트들은 껍데기에 해당할 가능성이 높습니다.)
5. 엘리먼트 내에 링크의 비율이 높은 경우, 본문 후보에서 제거한다.
   (이런 엘리먼트는 광고나 내비게이션일 가능성이 높습니다.)
6. 남은 본문 후보의 ID들을 저장한다.

이제 우리는 본문으로 추정되는 부분의 ID를 추출해냈으니, 실제 웹페이지의 본문 추출은 다음과 같이 진행할 수 있습니다.

**본문 추출**

1. 해당 사이트의 본문 템플릿이 구축되어 있는지 체크한다. 구축되어 있지 않다면, 위의 알고리즘을 통해 본문 템플릿을 구축한다.
2. 본문 템플릿으로부터 본문 후보 ID를 가져온다. 웹 페이지를 가져오고, 해당 후보 ID에 해당하는 부분의 텍스트만 추출한다.
3. 추가적인 후처리 실시 후 텍스트를 반환한다.



본문 템플릿은 같은 사이트 내에서는 통용될 수 있으므로, 캐싱을 하는것이 유리하겠습니다.





## 코드

``` python
class AutoExtractor:
    '''
    임의의 웹 페이지에서 본문으로 추정되는 부분만 추출하는 클래스입니다.
    '''
    def __init__(self):
        import re, pickle, os
        self.reID = re.compile(''' id=("[^"']+"|'[^']+')''', re.I)
        self.reClass = re.compile(''' class=("[^"']+"|'[^']+')''', re.I)
        self.reIdClass = re.compile(''' (id|class)=("[^"']+"|'[^']+')''', re.I)
        self.reNewline = re.compile('[\r\n]{2,}')
        self.templateCachePath = 'elementTemplate/'
        self.commonThreshold = 0.4
        self.maxLookup = 10
        try: os.mkdir(self.templateCachePath)
        except: pass
        self.elementTemplateCache = {}
 
    def isHomomorph(self, values):
        from collections import Counter
        l = list(values)
        return Counter(l).most_common(1)[0][1] >= len(l) * self.commonThreshold
 
    @staticmethod
    def commonest(values):
        from collections import Counter
        return Counter(values).most_common(1)[0][0]
 
    def findSimilarPage(self, url, dUrl = None):
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
            try: deepSearchList.remove(url)
            except: pass
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
            headerList = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
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
        def __init__(self, id = '', depth = 0):
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
                    except: pass
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
        tree.traverse(lambda node:tree.idMap.__setitem__(node.id, node))
        return tree
 
    def findDifferentElement(self, urls):
        '''urls 페이지들에서 공통적으로 등장하지만 내용물은 다른 본문 후보를 추출하는 함수'''
        from collections import Counter
        import bs4
        # load web pages
        pages = []
        for url in urls:
            try: pages.append(self.fetchHTML(url)[0])
            except: pass
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
        for id in commonID:
            texts = []
            for page in soups:
                el = page.select_one(id)
                texts.append(el.text.strip() if el else '')
                pageIdTexts[id] = texts
 
        # remove elements with common text
        for id, values in list(pageIdTexts.items()):
            if self.isHomomorph(values):
                del pageIdTexts[id]
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
 
        for id, values in pageIdRests.items():
            try:
                if self.isHomomorph(values): del pageIdTexts[id]
            except: pass
 
        ids = list(pageIdTexts.keys())
        ids = [id for id in ids if tree.idMap.get(id)]
        ids.sort(key=lambda id:tree.idMap[id].depth)
        uniqs = []
        for idA in ids:
            if any(map(lambda id:tree.idMap[id].hasDescendant(idA), uniqs)): continue
            uniqs.append(idA)
        idOrder = []
        for m in self.reIdClass.finditer(pages[0]):
            if m.group(1) == 'id':
                id = '#' + m.group(2)[1:-1]
            elif m.group(1) == 'class':
                id = re.sub(' +', '.', ' ' + m.group(2)[1:-1])
            if id in commonID: idOrder.append(id)
        uniqs.sort(key=idOrder.index)
 
        # detect common prefix & suffix
        for id in uniqs:
            values = pageIdTexts[id]
            i = 0
            j = 0
            while i < len(values[0]) and self.isHomomorph(v[i] if i < len(v) else '' for v in values):
                i += 1
            while -j < len(values[0]) and self.isHomomorph(v[j-1] if -j < len(v) else '' for v in values):
                j -= 1
            pageIdTextFix[id] = AutoExtractor.commonest(v[:i] for v in values), AutoExtractor.commonest(v[j:] for v in values)
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
 
    def getElementTemplate(self, url, maxLookup = 0):
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
        except: pass
 
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
```

코드가 길지만 복잡한 기법이 사용된 건 없습니다...!

## 실제 결과

위의 AutoExtractor 함수를 이용하여 본문을 추출한 것, 그냥 HTML에서 텍스트만 추출한 것, 서문에 소개한 boilerpipe 라이브러리를 이용한 경우를 비교해보았습니다.

|                      | http://www.hani.co.kr/arti/politics/politics_general/868638.html?_fr=mt0 |
| -------------------- | ------------------------------------------------------------ |
| HTML에서 텍스트 추출 | 광고 광고닫기 한겨레 메뉴 아이콘 기타서비스 로그인아이콘 검색창 열기검색창 닫기 지만원 “5·18 진상 조사위원 시켜줘”…한국당 ‘골머리’ 지만원 “5·18 진상 조사위원 시켜줘”…한국당 ‘골머리’ ‘가정폭력 스토킹 살해’ 딸 잃은 엄마 “이 나라서 살 수 있을까” ‘가정폭력 스토킹 살해’ 딸 잃은 엄마 “이 나라서 살 수 있을까” 한국영화계의 ‘큰 별’지다…배우 신성일 별세 한국영화계의 ‘큰 별’지다…배우 신성일 별세 ‘목포의 눈물’ 부르던 미누가 외친다 “스탑 크랙다운” ‘목포의 눈물’ 부르던 미누가 외친다 “스탑 크랙다운” 조사받은 피해자 “양진호 죄의식 무뎌져…법 심판 받아야” 조사받은 피해자 “양진호 죄의식 무뎌져…법 심판 받아야” 김정은, 중국 예술단 공연 관람…시진핑 방북 분위기 조성? 김정은, 중국 예술단 공연 관람…시진핑 방북 분위기 조성? 11월 첫째주 한겨레 그림판 모아보기 11월 첫째주 한겨레 그림판 모아보기 김정숙 여사, 첫 단독 외국 국빈방문…2호기 타고 인도로 김정숙 여사, 첫 단독 외국 국빈방문…2호기 타고 인도로 이낙연 “정부 맞춤형 일자리, 현장에선 수요 높아” 이낙연 “정부 맞춤형 일자리, 현장에선 수요 높아” 경제사회노동위, ‘민주노총 없이’ 22일 출범 경제사회노동위, *(하략)* |
| AutoExtractor        | 광고 본문 광고 자유한국당은 박근혜를 넘어설 수 있을까 등록 :2018-11-02 19:39수정 :2018-11-04 10:27 [토요판] 다음주의 질문 박근혜 전 대통령이 지난해 3월22일 검찰 조사를 받은 뒤 귀가하고 있다. 사진공동취재단 “(박근혜 전 대통령의) 탄핵에 앞장서고 당에 침을 뱉으며 저주하고 나간 사람들이 한마디 반성도 하지 않고 돌아왔다”, “박근혜 전 대통령이 무엇을 잘못해서 탄핵을 받았나. 탄핵백서를 만들어달라.” (홍문종 자유한국당 의원) 자유한국당의 금기어, ‘박근혜’와 ‘탄핵’이 지난 31일 공식회의 석상에 드디어 등장했다. 한국 보수 세력을 ‘궤멸’로 몰아넣은 박 전 대통령에 대한 재평가 요구가 당 내에서 공식화된 셈이다. 대표적인 친박근혜계(친박계)인 홍 의원은 다음 날엔 “당의 분수령이 됐다고 하는 탄핵에 대해 자신이 무엇을 잘못했는지, 분명하고 확실한 이정표를 만들어야 한다”며 이른바 ‘복당파’들의 고해성사까지 요구했다. 쇄신 대상으로 지목돼 온 친박계가 이렇게 공개적으로 ‘탄핵 재평가’를 요구하며 기세를 올리는 것은 다음달 치러질 원내대표 선거와 내년 2월로 예상되는 당 대표 선거를 겨냥한 것이다. 특히 2020년 총선의 공천권을 행사하게 될 차기 대표는 의원들의 생사여탈권을 갖고 있다. 친박계도, 박근혜 탄핵을 주장하며 탈당했다 돌아온 ‘복당파’도 자신의 명운을 좌우하게 될 당 대표 선거에 손놓고 있을 수는 없다. 친박 쪽은 ‘박근혜’라는 비빌 언덕이 있다. 친박계 쪽은 이번 6·13 지방선거의 결과에서 역설적으로 희망을 확인했다고 한다. 당시 당선자 지도가 파란색(더불어민주당)으로 물들었지만, 박 전 대통령의 핵심 지지기반인 대구·경북 지역은 그 와중에 ‘신의’를 지켰다. 대구·경북이 살아있고 극렬 지지층인 ‘태극기 부대’가 존재하는 이상, 친박계는 언제든 재기를 꿈꿀 수 있다는 것이다. 일각에서 제기되는 ‘박근혜 사면설’ 역시 이들의 기대를 키우는 요인이다. 전두환·노태우 전 대통령은 지난 1997년 대법원으로부터 각각 무기징역과 징역 17년을 선고받았지만, 전 전 대통령은 2년20일, 노 전 대통령은 2년1개월을 복역한 뒤 김영삼 정부의 사면조처로 풀려났다. ‘전직 대통령의 복역 기간은 2년’이라는 대전제 아래, 2017년 3월31일 구속된 박 전 대통령 역시 늦어도 내년 하반기 안에는 사면될 것이라는 주장이다. 박근혜 탄핵을 주장하며 탈당했다 돌아온 복당파는 현재 당의 주류이지만 앞날을 가늠할 수 없다. 당 쇄신을 위해 영입된 김병준 혁신비상대책위원장은 “새로운 보수 가치 정립”이 가장 중요하다고 주장했지만, 황교안 전 국무총리, 오세훈 전 서울시장, 원희룡 제주지사 등을 만나며 ‘무차별적’ 영입과 세불리기에만 열을 올리고 있다. 탄핵 재평가 요구에는 “갈등이 심할 때 갈등을 한 순간에 덮을 수 없다. 새로운 우산 아래 조금씩 덮어가야 한다”며 알듯 모를듯한 말만 남겼다. 복당파의 대표 선수인 김성태 원내대표는 당 대표 출마를 위해 태극기부대의 심기를 거스르지 않으려 애를 쓰는 모습이다. 투표권이 있는 책임당원에 가입한 태극기 부대원이 지방선거 이후 8000여명에 이른다니 눈치를 보지 않을 수 없다. 자유한국당이 박근혜를 넘어서지 않으면, 이들이 연일 강조하는 보수대통합은 요원해 보인다. 자유한국당이 망가진 원인이 박 전 대통령의 헌정 유린과 국정 실패 때문인데, 이들에게 면죄부를 주자는 주장에 ‘합리적 보수’가 동조할 순 없다. 자유한국당 복당파의 한 의원은 “친박계는 우리가 박 전 대통령의 탄핵을 주장했기 때문에 보수가 망했다고 생각한다. 같이 가기 쉽지 않다”고 토로했다. 자유한국당의 가까운 미래가 ‘통합’ 아니라 ‘분열’이라는 관측이 힘을 얻는 이유다. 최혜정 정치팀장 후원하기 응원해주세요, 더 깊고 알찬 기사로 보답하겠습니다 진실을 알리고 평화를 지키는 데 소중히 쓰겠습니다. 연재 광고 광고 섹션기사 광고 광고 정치 |
| BoilerPipe           | 자유한국당은 박근혜를 넘어설 수 있을까 등록 :2018-11-02 19:39수정 :2018-11-04 10:27 페이스북 [토요판] 다음주의 질문 박근혜 전 대통령이 지난해 3월22일 검찰 조사를 받은 뒤 귀가하고 있다. 사진공동취재단 “(박근혜 전 대통령의) 탄핵에 앞장서고 당에 침을 뱉으며 저주하고 나간 사람들이 한마디 반성도 하지 않고 돌아왔다”, “박근혜 전 대통령이 무엇을 잘못해서 탄핵을 받았나. 탄핵백서를 만들어달라.” (홍문종 자유한국당 의원) 자유한국당의 금기어, ‘박근혜’와 ‘탄핵’이 지난 31일 공식회의 석상에 드디어 등장했다. 한국 보수 세력을 ‘궤멸’로 몰아넣은 박 전 대통령에 대한 재평가 요구가 당 내에서 공식화된 셈이다. 대표적인 친박근혜계(친박계)인 홍 의원은 다음 날엔 “당의 분수령이 됐다고 하는 탄핵에 대해 자신이 무엇을 잘못했는지, 분명하고 확실한 이정표를 만들어야 한다”며 이른바 ‘복당파’들의 고해성사까지 요구했다. 쇄신 대상으로 지목돼 온 친박계가 이렇게 공개적으로 ‘탄핵 재평가’를 요구하며 기세를 올리는 것은 다음달 치러질 원내대표 선거와 내년 2월로 예상되는 당 대표 선거를 겨냥한 것이다. 특히 2020년 총선의 공천권을 행사하게 될 차기 대표는 의원들의 생사여탈권을 갖고 있다. 친박계도, 박근혜 탄핵을 주장하며 탈당했다 돌아온 ‘복당파’도 자신의 명운을 좌우하게 될 당 대표 선거에 손놓고 있을 수는 없다. 친박 쪽은 ‘박근혜’라는 비빌 언덕이 있다. 친박계 쪽은 이번 6·13 지방선거의 결과에서 역설적으로 희망을 확인했다고 한다. 당시 당선자 지도가 파란색(더불어민주당)으로 물들었지만, 박 전 대통령의 핵심 지지기반인 대구·경북 지역은 그 와중에 ‘신의’를 지켰다. 대구·경북이 살아있고 극렬 지지층인 ‘태극기 부대’가 존재하는 이상, 친박계는 언제든 재기를 꿈꿀 수 있다는 것이다. 일각에서 제기되는 ‘박근혜 사면설’ 역시 이들의 기대를 키우는 요인이다. 전두환·노태우 전 대통령은 지난 1997년 대법원으로부터 각각 무기징역과 징역 17년을 선고받았지만, 전 전 대통령은 2년20일, 노 전 대통령은 2년1개월을 복역한 뒤 김영삼 정부의 사면조처로 풀려났다. ‘전직 대통령의 복역 기간은 2년’이라는 대전제 아래, 2017년 3월31일 구속된 박 전 대통령 역시 늦어도 내년 하반기 안에는 사면될 것이라는 주장이다. 박근혜 탄핵을 주장하며 탈당했다 돌아온 복당파는 현재 당의 주류이지만 앞날을 가늠할 수 없다. 당 쇄신을 위해 영입된 김병준 혁신비상대책위원장은 “새로운 보수 가치 정립”이 가장 중요하다고 주장했지만, 황교안 전 국무총리, 오세훈 전 서울시장, 원희룡 제주지사 등을 만나며 ‘무차별적’ 영입과 세불리기에만 열을 올리고 있다. 탄핵 재평가 요구에는 “갈등이 심할 때 갈등을 한 순간에 덮을 수 없다. 새로운 우산 아래 조금씩 덮어가야 한다”며 알듯 모를듯한 말만 남겼다. 복당파의 대표 선수인 김성태 원내대표는 당 대표 출마를 위해 태극기부대의 심기를 거스르지 않으려 애를 쓰는 모습이다. 투표권이 있는 책임당원에 가입한 태극기 부대원이 지방선거 이후 8000여명에 이른다니 눈치를 보지 않을 수 없다. 자유한국당이 박근혜를 넘어서지 않으면, 이들이 연일 강조하는 보수대통합은 요원해 보인다. 자유한국당이 망가진 원인이 박 전 대통령의 헌정 유린과 국정 실패 때문인데, 이들에게 면죄부를 주자는 주장에 ‘합리적 보수’가 동조할 순 없다. 자유한국당 복당파의 한 의원은 “친박계는 우리가 박 전 대통령의 탄핵을 주장했기 때문에 보수가 망했다고 생각한다. 같이 가기 쉽지 않다”고 토로했다. 자유한국당의 가까운 미래가 ‘통합’ 아니라 ‘분열’이라는 관측이 힘을 얻는 이유다. 응원해주세요, 더 깊고 알찬 기사로 보답하겠습니다 후원하기 1,000원 |



|                      | http://gall.dcinside.com/board/view/?id=mathematics&no=274871 |
| -------------------- | ------------------------------------------------------------ |
| HTML에서 텍스트 추출 | 통합검색 바로가기본문영역 바로가기상단 메뉴 바로가기 디시인사이드 갤러리 갤러리 & 통합검색 m.갤러리갤로그뉴스만두몰이벤트로그인 갤러리 m.갤러리갤로그뉴스이벤트만두몰디시위키 어제 1,528,393 댓글 등록 어제 737,852 게시글 등록 수학 갤러리연관 갤러리(0/2) 갤주소 복사 차단설정 갤러리 이용안내 최근 방문 갤러리수학이전 고전게임중세게임닌텐도 스위치프로그래밍최근 방문 갤러리가 없습니다. 아티야의 HLF 강연에 대해 ㅇㅅㅇ(49.174) 09-21 15:42:02 조회 4519 추천 8 댓글 0 내가 먼저 아티야 소식을 가져와놓고 이렇게 말하는 것도 우습지만, 내 생각에는 이 강연을 '무시'하는게 한때 거물이였던 아티야를 존중하면서도 모두에게 좋은 길인거 같음. 아티야가 위대한 수학자인건 누구도 부정할 수 없는 사실이지만, 최근의 아티야는 (공공연한 비밀이지만) 정신적으로 불안정한 상태라고 함. 그 결과로 Feit-Thompson Theorem과 Nonexistence of 6-spheres 관련 논란이 일어난거고. 게다가 HLF가 화제성을 모으기 위해 (정신적으로 불안한게 이미 알려진) 아티야가 강연을 하는걸 허가한거 아니냐는 얘기도 나오고... 아무튼 '무시'는 너무 강한 어감일지 모르겠지만, 그냥 이번 강연에 높은 기대치를 갖지는 않는게 좋을거 같아. 여담으로, 아티야가 2016년에 한 인터뷰에서는; "My reputation is established as a mathematician. If I make a mess of it now, people will say, “All right, he was a good mathematician, but at the end of his life he lost his marbles.” A friend of mine, John Polkinghorne, left physics just as I was going in; he went into the church and became a theologian. We had a discussion on my 80th birthday and he said to me, “You’ve got nothing to lose; you just go ahead and think what you think.” And that’s what I’ve been doing. I’ve got all the medals I need. What could I lose? So that’s why I’m prepared to take a gamble that a young researcher wouldn’t be prepared to take." 라고는 했지만, 아티야가 이번 일 때문에 크랭크로 기억되지 않을까 걱정되긴 함... 8 고정닉 0 0 힛추공유신고 전체 리플 0개 등록순 댓글닫기 새로고침 닉네임 비밀번호 타인의 권리를 침해하거나 명예를 훼손하는 댓글은 운영원칙 및 관련 법률에 제재를 받을 수 있습니다. Shift+Enter 키를 동시에 누르면 줄바꿈이 됩니다. 디시콘 등록 등록+추천 전체글 개념글 수정 삭제 글쓰기 갤러리 리스트 번호 제목 글쓴이 날짜 조회 추천 공지 수학 관련 사진과 내용이 있어야 합니다. [101] 운영자 06/01/18 39594 27 282816 형들 선형대수학 대각전개 너무 어려운데? ㅇㅇ(211.218) 11/04 3 0 282815 product랑 multiplication이랑 어떤 의미 차이가 있음? 좆빼미갤로그로 이동합니다. 11/04 12 0 282814 유리함수 점근선의 교점 (a.b) 에서 a=b이면 [1] ㅇㅇ(27.115) 11/04 13 0 282813 기계공 졸업하면 뭐하냐 heyday(174.225) 11/04 10 0 282812 그럼 닭다리는 짝수인데 사람이 홀수면 어카냐 [4] 베컴(110.70) 11/04 52 0 282811 적통잘하는사람있으면 도와주세요ㅠㅠ [1] 도와줘(223.33) 11/04 31 0 282810 이중적분 질문좀요 행님덜... [1] ㅇㅇ(52.119) 11/04 47 0 282809 치킨 시켰을 때 닭다리 나혼자 다먹는 게 이기적임? [3] 베컴(110.70) 11/04 39 0 282808 (꿀잼주의) 그로센딕과 세르가 대수학자인 이유 아크메easy갤로그로 이동합니다. *(하략)* |
| AutoExtractor        | 내가 먼저 아티야 소식을 가져와놓고 이렇게 말하는 것도 우습지만, 내 생각에는 이 강연을 '무시'하는게 한때 거물이였던 아티야를 존중하면서도 모두에게 좋은 길인거 같음.아티야가 위대한 수학자인건 누구도 부정할 수 없는 사실이지만, 최근의 아티야는 (공공연한 비밀이지만) 정신적으로 불안정한 상태라고 함. 그 결과로 Feit-Thompson Theorem과 Nonexistence of 6-spheres 관련 논란이 일어난거고. 게다가 HLF가 화제성을 모으기 위해 (정신적으로 불안한게 이미 알려진) 아티야가 강연을 하는걸 허가한거 아니냐는 얘기도 나오고...아무튼 '무시'는 너무 강한 어감일지 모르겠지만, 그냥 이번 강연에 높은 기대치를 갖지는 않는게 좋을거 같아.여담으로, 아티야가 2016년에 한 인터뷰에서는;"My reputation is established as a mathematician. If I make a mess of it now, people will say, “All right, he was a good mathematician, but at the end of his life he lost his marbles.”A friend of mine, John Polkinghorne, left physics just as I was going in; he went into the church and became a theologian. We had a discussion on my 80th birthday and he said to me, “You’ve got nothing to lose; you just go ahead and think what you think.” And that’s what I’ve been doing. I’ve got all the medals I need. What could I lose? So that’s why I’m prepared to take a gamble that a young researcher wouldn’t be prepared to take."라고는 했지만, 아티야가 이번 일 때문에 크랭크로 기억되지 않을까 걱정되긴 함... 추천검색 추천 비추천 8 0 개념 추천 개념 비추천 0 힛추 공유 신고 댓글 영역 전체 리플 0개 등록순 최신순 답글수 등록순정렬 기준선택 답글 펼침 설정 댓글닫기 새로고침 닉네임 비밀번호 타인의 권리를 침해하거나 명예를 훼손하는 댓글은 운영원칙 및 관련 법률에 제재를 받을 수 있습니다. Shift+Enter 키를 동시에 누르면 줄바꿈이 됩니다. 디시콘 디시콘이란 등록 등록+추천 전체글 개념글 수정 삭제 글쓰기 하단 갤러리 리스트 영역 왼쪽 컨텐츠 영역 갤러리 리스트 영역 갤러리 리스트 번호 제목 글쓴이 날짜 조회 추천 공지 운영자 06/01/18 39594 27 282820 ㅇㅇ(223.62) 11/04 9 0 282819 ㅇㅇ(111.118) 11/04 14 0 282818 ㅇㅇ(52.119) 11/04 13 0 282817 기계학습테러(185.220) 11/04 26 0 282816 ㅇㅇ(211.218) 11/04 15 0 282815 좆빼미 11/04 20 0 282814 ㅇㅇ(27.115) 11/04 26 0 282813 heyday(174.225) 11/04 16 0 282812 베컴(110.70) 11/04 55 0 282811 도와줘(223.33) 11/04 48 0 282810 ㅇㅇ(52.119) 11/04 71 0 282809 베컴(110.70) 11/04 42 0 282808 아크메easy 11/04 49 3 282807 독방(174.225) 11/04 19 0 282806 ㅇㅇㅇ(211.223) 11/04 47 0 282805 매미(174.225) 11/04 29 0 282804 매미(174.225) 11/04 30 0 282803 v8v8(174.225) 11/04 68 0 282801 v8v8(174.225) 11/04 44 0 282800 v8v8(174.225) 11/04 16 0 282799 Zadkiel 11/04 43 0 282798 ㅇㅇ(221.142) 11/04 23 0 282797 v1v2b3(174.225) 11/04 19 0 282796 ㅇㅇ(112.149) 11/04 27 0 282795 ㅇㅇ(58.123) 11/04 45 1 282794 v1v2b3(174.225) 11/04 44 0 282793 듀에르(39.7) 11/04 78 0 282792 ㅇㅇ(211.36) 11/04 43 0 282790 ㅇㅇ(175.114) 11/04 61 |
| BoilerPipe           | 수학 갤러리 연관 갤러리(0/2) 연관 갤러리 열기 갤주소 복사 ㅇㅅㅇ(49.174) 09-21 15:42:02 조회 4532 추천 8 댓글 0 내가 먼저 아티야 소식을 가져와놓고 이렇게 말하는 것도 우습지만, 내 생각에는 이 강연을 '무시'하는게 한때 거물이였던 아티야를 존중하면서도 모두에게 좋은 길인거 같음. 아티야가 위대한 수학자인건 누구도 부정할 수 없는 사실이지만, 최근의 아티야는 (공공연한 비밀이지만) 정신적으로 불안정한 상태라고 함. 그 결과로 Feit-Thompson Theorem과 Nonexistence of 6-spheres 관련 논란이 일어난거고. 게다가 HLF가 화제성을 모으기 위해 (정신적으로 불안한게 이미 알려진) 아티야가 강연을 하는걸 허가한거 아니냐는 얘기도 나오고... 아무튼 '무시'는 너무 강한 어감일지 모르겠지만, 그냥 이번 강연에 높은 기대치를 갖지는 않는게 좋을거 같아. 여담으로, 아티야가 2016년에 한 인터뷰에서는; "My reputation is established as a mathematician. If I make a mess of it now, people will say, “All right, he was a good mathematician, but at the end of his life he lost his marbles.” A friend of mine, John Polkinghorne, left physics just as I was going in; he went into the church and became a theologian. We had a discussion on my 80th birthday and he said to me, “You’ve got nothing to lose; you just go ahead and think what you think.” And that’s what I’ve been doing. I’ve got all the medals I need. What could I lose? So that’s why I’m prepared to take a gamble that a young researcher wouldn’t be prepared to take." 라고는 했지만, 아티야가 이번 일 때문에 크랭크로 기억되지 않을까 걱정되긴 함... 추천 비추천 |



|                      | https://bab2min.tistory.com/253?                             |
| -------------------- | ------------------------------------------------------------ |
| HTML에서 텍스트 추출 | Login Home Tags Guestbook Recents 나의 큰 O는 logx야.. 적분史 프로그래밍 소리 언어 수업노트 잉여 그냥 공부 Home 언어 어원 이야기  어원 이야기 60. 택시(taxi)와 세금(tax)의 관계 Posted by 적분 ∫2tdt=t²+c 발행 비공개로 변경합니다 Modify Modify (new window) Trackback Delete 2012.11.17 23:54 언어/어원 이야기 어릴적에는 taxi라는 이름이 전혀 이상하게 느껴지지 않았는데, 영어 공부를 하면서 tax가 세금이라는 뜻인걸 알게 되었습니다. 그후로 택시를 볼때마다 '저게 도대체 세금이랑 무슨 상관이 있길래 이름이 taxi인거지?'하면서 갸우뚱거렸죠ㅋ 근데 이제는 갸우뚱거리지 않아도 됩니다! 그 이유를 알았으니깐요~ 현재 사용되는 taxi는 taxicab의 줄임말입니다. 이제는 taxi라는 표현이 더 익숙하지만, 처음에는 taxicab으로 사용되었다는걸 알아둘 필요가 있습니다. (혹은 taxicab을 줄여서 cab이라고 부르기도 합니다. 역시 의미는 택시!) 그러면 taxicab은 어떻게 만들어진 말일까요? taxicab 역시 두 단어가 합쳐지고 줄여져서 만들어진 것입니다. taximeter cabriolet에서 앞부분의 taxi와 cab만 따온것이지요. 먼저 cabriolet의 의미부터 살펴보자면, 이는 프랑스어에서 건너온 말로, 원래는 '말 한 마리가 끄는 마차'를 가리키는 말이었으나, 자동차가 발명된 이후로 '윗 부분이 네모난 자동차'들을 가리키는 말로 사용되었습니다. 그렇다면 taximeter는 뭘까요? 이놈의 정체는 택시 안에서 열심히 달리고 있는 말... taximeter 의 정체... (cabriolet이 원래 마차라는 뜻이라서 그런것일까요? 택시 미터기에서 달리고 있는 동물은 말!이네요ㅋ 아니면 그냥 우연의 일치일수도... 저 말이 세상에서 가장 무서운 말이라죠ㅋ) taximeter는 taxa meter로써, 뒤의 meter는 '측정도구'라는 의미지요. 앞의 taxa는 우리가 흔히 아는 tax로써, 세금, 요금이라는 뜻입니다. 즉 taximeter는 요금측정기라는 뜻이고, 이런 요금 측정기가 달려있는 자동차가 taxicab인것이지요.  8sns신고 카카오스토리 트위터 페이스북 '언어 > 어원 이야기' 카테고리의 다른 글 어원 이야기 63. 세미나(Seminar)가 뭔가요? (0) 어원 이야기 62. Z는 제트인가 지인가 (2) 어원 이야기 61. 파마와 덴뿌라의 공통점! (0) 어원 이야기 60. 택시(taxi)와 세금(tax)의 관계 (1) 어원 이야기 59. lamp와 lantern (0) 어원 이야기 58. 마법(magic)의 어원은? (0) 어원 이야기 57. 젤리(jelly)와 감기(cold) (0) Trackback: 0 Comment: 1 내용을 입력하세요. Favicon of http://konn.tistory.comBlogIconKonn 2013.11.16 21:33 신고 아.. 결국 택시는 택스와 관계가 없었던 거군요 ㅋㅋ 예전에 무슨 연관이 있는건 아닐까 하면서 혹시 세금을 운송하던 마차나 차량같은 것에서 유래한 것이 아닌가 혼자 추측해봤는데 아니었군요.ㅋ 1 ··· 358 359 360 361 362 363 364 365 366 ··· 608 Writer *(하략)* |
| AutoExtractor        | Posted by 적분 ∫2tdt=t²+c 2012.11.17 23:54 언어/어원 이야기 어릴적에는 taxi라는 이름이 전혀 이상하게 느껴지지 않았는데, 영어 공부를 하면서 tax가 세금이라는 뜻인걸 알게 되었습니다. 그후로 택시를 볼때마다 '저게 도대체 세금이랑 무슨 상관이 있길래 이름이 taxi인거지?'하면서 갸우뚱거렸죠ㅋ 근데 이제는 갸우뚱거리지 않아도 됩니다! 그 이유를 알았으니깐요~현재 사용되는 taxi는 taxicab의 줄임말입니다. 이제는 taxi라는 표현이 더 익숙하지만, 처음에는 taxicab으로 사용되었다는걸 알아둘 필요가 있습니다. (혹은 taxicab을 줄여서 cab이라고 부르기도 합니다. 역시 의미는 택시!) 그러면 taxicab은 어떻게 만들어진 말일까요? taxicab 역시 두 단어가 합쳐지고 줄여져서 만들어진 것입니다. taximeter cabriolet에서 앞부분의 taxi와 cab만 따온것이지요.먼저 cabriolet의 의미부터 살펴보자면, 이는 프랑스어에서 건너온 말로, 원래는 '말 한 마리가 끄는 마차'를 가리키는 말이었으나, 자동차가 발명된 이후로 '윗 부분이 네모난 자동차'들을 가리키는 말로 사용되었습니다.그렇다면 taximeter는 뭘까요? 이놈의 정체는 택시 안에서 열심히 달리고 있는 말...taximeter 의 정체...(cabriolet이 원래 마차라는 뜻이라서 그런것일까요? 택시 미터기에서 달리고 있는 동물은 말!이네요ㅋ 아니면 그냥 우연의 일치일수도... 저 말이 세상에서 가장 무서운 말이라죠ㅋ)taximeter는 taxa meter로써, 뒤의 meter는 '측정도구'라는 의미지요. 앞의 taxa는 우리가 흔히 아는 tax로써, 세금, 요금이라는 뜻입니다. 즉 taximeter는 요금측정기라는 뜻이고, 이런 요금 측정기가 달려있는 자동차가 taxicab인것이지요. 공감sns신고 ' > ' 카테고리의 다른 글 (0) 2014.04.12 (2) 2013.07.12 (0) 2013.04.18 (1) 2012.11.17 (0) 2012.11.16 (0) 2012.11.09 (0) 2012.11.02 이 댓글을 비밀 댓글로 댓글 달 |
| BoilerPipe           | 나의 큰 O는 logx야.. 2012.11.17 23:54 언어/어원 이야기 언어/어원 이야기 어릴적에는 taxi라는 이름이 전혀 이상하게 느껴지지 않았는데, 영어 공부를 하면서 tax가 세금이라는 뜻인걸 알게 되었습니다. 그후로 택시를 볼때마다 '저게 도대체 세금이랑 무슨 상관이 있길래 이름이 taxi인거지?'하면서 갸우뚱거렸죠ㅋ 근데 이제는 갸우뚱거리지 않아도 됩니다! 그 이유를 알았으니깐요~ 현재 사용되는 taxi는 taxicab의 줄임말입니다. 이제는 taxi라는 표현이 더 익숙하지만, 처음에는 taxicab으로 사용되었다는걸 알아둘 필요가 있습니다. (혹은 taxicab을 줄여서 cab이라고 부르기도 합니다. 역시 의미는 택시!) 그러면 taxicab은 어떻게 만들어진 말일까요? taxicab 역시 두 단어가 합쳐지고 줄여져서 만들어진 것입니다. taximeter cabriolet에서 앞부분의 taxi와 cab만 따온것이지요. 먼저 cabriolet의 의미부터 살펴보자면, 이는 프랑스어에서 건너온 말로, 원래는 '말 한 마리가 끄는 마차'를 가리키는 말이었으나, 자동차가 발명된 이후로 '윗 부분이 네모난 자동차'들을 가리키는 말로 사용되었습니다. 그렇다면 taximeter는 뭘까요? 이놈의 정체는 택시 안에서 열심히 달리고 있는 말... taximeter 의 정체... (cabriolet이 원래 마차라는 뜻이라서 그런것일까요? 택시 미터기에서 달리고 있는 동물은 말!이네요ㅋ 아니면 그냥 우연의 일치일수도... 저 말이 세상에서 가장 무서운 말이라죠ㅋ) taximeter는 taxa meter로써, 뒤의 meter는 '측정도구'라는 의미지요. 앞의 taxa는 우리가 흔히 아는 tax로써, 세금, 요금이라는 뜻입니다. 즉 taximeter는 요금측정기라는 뜻이고, 이런 요금 측정기가 달려있는 자동차가 taxicab인것이지요. 공감 |



|                      | http://ninetail03.egloos.com/1468032?                        |
| -------------------- | ------------------------------------------------------------ |
| HTML에서 텍스트 추출 | 이글루스 \| 로그인 Ninetailed Fantasia in Egloos ninetail03.egloos.com 포토로그 10년만에 키보드를 바꿨다 NET by 나인테일 2018/11/04 01:58 ninetail03.egloos.com/1468032 덧글수 : 1 로지텍 K780이라는 녀석으로 바꿨습니다. 업무용 키보드로는 아이솔레이션 타입의 팬타그래프를 선호하니다. 이 타입을 오래 쓰다보니 멤브레인이나 기계식은 손가락을 높이 들어올려 깊게 누른다는 느낌이 적응이 안 되네요. 아이솔레이션 팬타가 분명히 이전부터 시장에서 붐이었던 것은 사실입니다만 제대로 된 물건은 찾기가 힘들었던게 사실이죠. 5만원 이하의 저가 제품들이 대부분이고 도저히 정상적이라고 할 수가 없는 기괴한 키감을 가진 싸구려스런 물건들 뿐인지라... 그래서 돈을 더 주고서라도 좋은걸 사겠다고 뒤져봐도 딱히 좋은 물건이 안 나온단 말이죠. 아이락스도 그냥 그렇고.... 이 녀석을 제외하고 말이죠. 그런 이유로 애플 키보드 시리즈만 10년을 썼습니다. 유선 하나 무선 두개를 썼군요. 지금도 애플 키보드의 품질 자체에는 딱히 불만은 없습니다만 그렇다고는 해도 10년간 별다른 큰 발전이 없는 것도 사실이었죠. 근데 이런저런 이유로 써본 이번 로지텍은 요즘 로지텍 제품 특유의 멀티 페어링 기능을 제외하더라도 키보드의 품질 자체 만으로도 대단히 훌륭하네요. 애플 키보드가 여전히 싫진 않은데 이건 더 좋아요. 로지텍이 이걸? 아무리 팬타그래프라지만 그래도 키 위치가 애플보다는 약간 높은 편이고 그래서인지 누를때 쿠션감도 좀 더 있는 편입니다. 근데 이건 이거대로 굉장히 기분 좋은 느낌으로 타이핑을 할 수 있지 않나 하는 생각이 듭니다. 이건 취향에 달린 일이니 제 말이 맞다 라고 주장할 수는 없는 일이겠습니다만 일단 저는 굉장히 좋아요. 왼쪽 하단 키 위치도 맥과 윈도우 각각의 OS에 따라 변경되니 이건 이거대로 애플 맥 유저에겐 굉장히 편리하군요. 앞서 말씀드린 멀티 페어링 기능과 합쳐져 키보드 하나만으로 윈도우 PC와 맥을 커버할 수 있습니다. 좋아요 좋아. 그리고 가격도 반값 수준이네요. 단점이라면 이게 과연 팬타그래프가 맞나 싶을 정도로 굉장히 두껍고 무겁다는거. 기계식 키보드보다 더 무거운게 아닐까 싶은 생각도 듭니다. 도대체 속에 뭐가 들어있는거야? 책상 위에 얌전히 올려놓고 쓸 생각이라면 예쁘고 성능 좋은 착한 키보드가 되겠습니다만 노트북이니 태블릿이니 하는거에 엮어서 다닐 생각은 안 하시는게 좋습니다. 제가 구입한 780이외에 미니 사이즈로 나오는 380이라는 모델이 있는 모양인데 이건 운반을 염두에 두고 만든 모양이라 이 쪽의 무게는 잘 모르겠습니다. 아마 이거보다는 들고다닐만 하겠지요. 비슷한 설계라면 애플보다는 좀 더 무겁지 않을까 싶습니다만. 신고신고 퍼블리싱 및 추천 내보내기 밸리 : IT 2018/11/04 01:58 같은 카테고리의 글 트랙백(0) 덧글(1) 덧글 Barde 2018/11/04 14:36 # 해피해킹을 예전에 잘 사용했는데 팔아버려서 안타깝습니다... ※ 로그인 사용자만 덧글을 남길 수 있습니다. 이전글 : 안 오잖아 국무위원장 동지 이글루스 분점. by 나인테일 카테고리 전체(554) 애니메이션(39) 게임(40) NET(118) 시사(300) 일상(16) 바보(19) 거래(2) 미분류(20) *(하략)* |
| AutoExtractor        | 로지텍 K780이라는 녀석으로 바꿨습니다.업무용 키보드로는 아이솔레이션 타입의 팬타그래프를 선호하니다. 이 타입을 오래 쓰다보니 멤브레인이나 기계식은 손가락을 높이 들어올려 깊게 누른다는 느낌이 적응이 안 되네요.아이솔레이션 팬타가 분명히 이전부터 시장에서 붐이었던 것은 사실입니다만 제대로 된 물건은 찾기가 힘들었던게 사실이죠. 5만원 이하의 저가 제품들이 대부분이고 도저히 정상적이라고 할 수가 없는 기괴한 키감을 가진 싸구려스런 물건들 뿐인지라... 그래서 돈을 더 주고서라도 좋은걸 사겠다고 뒤져봐도 딱히 좋은 물건이 안 나온단 말이죠. 아이락스도 그냥 그렇고....이 녀석을 제외하고 말이죠.그런 이유로 애플 키보드 시리즈만 10년을 썼습니다. 유선 하나 무선 두개를 썼군요. 지금도 애플 키보드의 품질 자체에는 딱히 불만은 없습니다만 그렇다고는 해도 10년간 별다른 큰 발전이 없는 것도 사실이었죠. 근데 이런저런 이유로 써본 이번 로지텍은 요즘 로지텍 제품 특유의 멀티 페어링 기능을 제외하더라도 키보드의 품질 자체 만으로도 대단히 훌륭하네요. 애플 키보드가 여전히 싫진 않은데 이건 더 좋아요. 로지텍이 이걸?아무리 팬타그래프라지만 그래도 키 위치가 애플보다는 약간 높은 편이고 그래서인지 누를때 쿠션감도 좀 더 있는 편입니다. 근데 이건 이거대로 굉장히 기분 좋은 느낌으로 타이핑을 할 수 있지 않나 하는 생각이 듭니다. 이건 취향에 달린 일이니 제 말이 맞다 라고 주장할 수는 없는 일이겠습니다만 일단 저는 굉장히 좋아요.왼쪽 하단 키 위치도 맥과 윈도우 각각의 OS에 따라 변경되니 이건 이거대로 애플 맥 유저에겐 굉장히 편리하군요. 앞서 말씀드린 멀티 페어링 기능과 합쳐져 키보드 하나만으로 윈도우 PC와 맥을 커버할 수 있습니다. 좋아요 좋아.그리고 가격도 반값 수준이네요.단점이라면 이게 과연 팬타그래프가 맞나 싶을 정도로 굉장히 두껍고 무겁다는거. 기계식 키보드보다 더 무거운게 아닐까 싶은 생각도 듭니다. 도대체 속에 뭐가 들어있는거야? 책상 위에 얌전히 올려놓고 쓸 생각이라면 예쁘고 성능 좋은 착한 키보드가 되겠습니다만 노트북이니 태블릿이니 하는거에 엮어서 다닐 생각은 안 하시는게 좋습니다.제가 구입한 780이외에 미니 사이즈로 나오는 380이라는 모델이 있는 모양인데 이건 운반을 염두에 두고 만든 모양이라 이 쪽의 무게는 잘 모르겠습니다. 아마 이거보다는 들고다닐만 하겠지요. 비슷한 설계라면 애플보다는 좀 더 무겁지 않을까 싶습니다만. 포스트 메타 정보 퍼블리싱 및 추천 같은 카테고리의 글 덧글(1 |
| BoilerPipe           | Ninetailed Fantasia in Egloos 덧글수 : 2 로지텍 K780이라는 녀석으로 바꿨습니다. 업무용 키보드로는 아이솔레이션 타입의 팬타그래프를 선호하니다. 이 타입을 오래 쓰다보니 멤브레인이나 기계식은 손가락을 높이 들어올려 깊게 누른다는 느낌이 적응이 안 되네요. 아이솔레이션 팬타가 분명히 이전부터 시장에서 붐이었습니다만 제대로 된 물건은 찾기가 힘들었던게 사실이죠. 5만원 이하의 저가 제품들이 대부분이고 도저히 정상적이라고 할 수가 없는 기괴한 키감을 가진 싸구려스런 물건들 뿐인지라... 그래서 돈을 더 주고서라도 좋은걸 사겠다고 뒤져봐도 딱히 좋은 물건이 안 나온단 말이죠. 아이락스도 그냥 그렇고.... 이 녀석을 제외하고 말이죠. 그런 이유로 애플 키보드 시리즈만 10년을 썼습니다. 유선 하나 무선 두개를 썼군요. 지금도 애플 키보드의 품질 자체에는 딱히 불만은 없습니다만 그렇다고는 해도 10년간 별다른 큰 발전이 없는 것도 사실이었죠. 근데 이런저런 이유로 써본 이번 로지텍은 요즘 로지텍 제품 특유의 멀티 페어링 기능을 제외하더라도 키보드의 품질 자체 만으로도 대단히 훌륭하네요. 애플 키보드가 여전히 싫진 않은데 이건 더 좋아요. 로지텍이 이걸? 아무리 팬타그래프라지만 그래도 키 위치가 애플보다는 약간 높은 편이고 그래서인지 누를때 쿠션감도 좀 더 있는 편입니다. 근데 이건 이거대로 굉장히 기분 좋은 느낌으로 타이핑을 할 수 있지 않나 하는 생각이 듭니다. 이건 취향에 달린 일이니 제 말이 맞다 라고 주장할 수는 없는 일이겠습니다만 일단 저는 굉장히 좋아요. 왼쪽 하단 키 위치도 맥과 윈도우 각각의 OS에 따라 변경되니 이건 이거대로 애플 맥 유저에겐 굉장히 편리하군요. 앞서 말씀드린 멀티 페어링 기능과 합쳐져 키보드 하나만으로 윈도우 PC와 맥을 커버할 수 있습니다. 좋아요 좋아. 그리고 가격도 반값 수준이네요. 단점이라면 이게 과연 팬타그래프가 맞나 싶을 정도로 굉장히 두껍고 무겁다는거. 기계식 키보드보다 더 무거운게 아닐까 싶은 생각도 듭니다. 도대체 속에 뭐가 들어있는거야? 책상 위에 얌전히 올려놓고 쓸 생각이라면 예쁘고 성능 좋은 착한 키보드가 되겠습니다만 노트북이니 태블릿이니 하는거에 엮어서 다닐 생각은 안 하시는게 좋습니다. 제가 구입한 780이외에 미니 사이즈로 나오는 380이라는 모델이 있는 모양인데 이건 운반을 염두에 두고 만든 모양이라 이 쪽의 무게는 잘 모르겠습니다. 아마 이거보다는 들고다닐만 하겠지요. 비슷한 설계라면 애플보다는 좀 더 무겁지 않을까 싶습니다만. |



|                      | https://www.ppomppu.co.kr/zboard/view.php?id=car&page=1&divpage=137&no=726658 |
| -------------------- | ------------------------------------------------------------ |
| HTML에서 텍스트 추출 | 단축키북마크 뽐뿌게시판 이벤트게시판 구매게시판 질문/요청 자유게시판 생활정보 자유갤러리 IT/취업 사용기 장터 리스트 설정하기 뽐뿌  뽐뿌 이벤트 정보 커뮤니티 갤러리 장터 포럼 뉴스 상담실 김용진 로그인회원가입\|아이디비번찾기 자동차포럼 입니다.자동차에 대한 모든 것들을 공유하는 공간입니다. 자동차 견적 문의 및 영맨 소환은 [신차견적상담실]을 이용해주세요. 관련메뉴자전거포럼 \| 바이크포럼 \| 신차견적상담 \| 중고차장터 \| 보험상담 \| 중고차상담 \| 여행레저상담 블랙박스 설치 diy 문의입니다. 상시가 계속 안되네요 ㅜㅜ 8 공유 아이콘 분류: 질문 이름: RealBook 등록일: 2018-11-04 17:27 조회수: 136 / 추천수: 0 1541320027_5223_2F46A531_7BC9_4AFE_A183_008EE1EA6801.jpeg (156.6 KB) 시동 걸면 블랙박스가 켜지는데 시동을 끄면 블랙박스도 꺼집니다. 녹화를 중지합니다. 도 아니고 그냥 툭 꺼집니다. 상시전원을 쓰고 싶은데 계속 꺼집니다. 이게 도대체 이유를 몰라서 어떤 이유가 있을까요?*(하략)* |
| AutoExtractor        | 자동차에 대한 모든 것들을 공유하는 공간입니다. 자동차 견적 문의 및 영맨 소환은 을 이용해주세요. \| \| \| \| \| \| 블랙박스 설치 diy 문의입니다. 상시가 계속 안되네요 ㅜㅜ 8 분류: 질문 이름: 등록일: 2018-11-04 17:27 조회수: 134 / 추천수: 0 1541320027_5223_2F46A531_7BC9_4AFE_A183_008EE1EA6801.jpeg (156.6 KB) 시동 걸면 블랙박스가 켜지는데 시동을 끄면 블랙박스도 꺼집니다. 녹화를 중지합니다. 도 아니고 그냥 툭 꺼집니다. 상시전원을 쓰고 싶은데 계속 꺼집니다. 이게 도대체 이유를 몰라서 어떤 이유가 있을까요? 노란색선은 열선핸들 빨간색선은 전동시트에도 해보고 트렁크에도 해보는데 변화가 없습니다. 퓨즈가 나갔나 해서 접지 시켜놓고 송곳 같은걸로 찌르면 불 들어오는거 있죠? 그것도 해봤는데 입출력 표시 됩니다. 혹시라도 유리관 안에 퓨즈가 나갔나 봤는데 선이 끊어지면 나간거 아닌가요? 참고로 선은 안끊겨 있습니다. 무슨 문제가 있을까요? 차는 K5입니다. 본 게시글은 작성자에 의해 2018-11-04 17:28:45에 최종 수정되었습니다. (1회) [ 주소복사 http://www.ppomppu.co.kr/zboard/view.php?id=car&no=726658 ] 0 0 북마크 등록하기 기본 이메일 추천하기 뽐뿌( http://www.ppomppu.co.kr )에서 발송되어진 메일입니다. 블랙박스 설치 diy 문의입니다. 상시가 계속 안되네요 ㅜㅜ 클릭하시면 원본 글과 코멘트를 보실수 있습니다. http://www.ppomppu.co.kr/zboard/view.php?id=car&no=726658 ============================================================== 시동 걸면 블랙박스가 켜지는데시동을 끄면 블랙박스도 꺼집니다. 녹화를 중지합니다. 도 아니고그냥 툭 전송중입니다. 잠시만 기다려 주세요. 0 0 빨강이 acc이기때문에 시동꺼지면 작동안되는퓨즈에 물리시고 노랑이 상시이기때문에 시동꺼도 작동되는 퓨즈에 물리세요. 지감은 반대로 하신거같습니다 퓨즈박스 뚜껑에 붙은 퓨즈위치 사진올려보세요 빨강이 acc이기때문에 시동꺼지면 작동안되는퓨즈에 물리시고 노랑이 상시이기때문에 시동꺼도 작동되는 퓨즈에 물리세요. 지감은 반대로 하신거같습니다 퓨즈박스 뚜껑에 붙은 퓨즈위치 사진올려보세요 2018-11-0417:32:45 0 0 상시는 시거잭이나 테일램프에 물립니다 상시는 시거잭이나 테일램프에 물립니다 2018-11-0417:33:31 0 0 아이고 제가 바꿔서 해버렸군요 ㅜ 반대로 알고있었네요. 감사합니다. 아이고 제가 바꿔서 해버렸군요 ㅜ 반대로 알고있었네요. 감사합니다. 2018-11-0417:35:29 0 0 감사합니다. 시거잭으로 바꾸겠습니다. 감사합니다. 시거잭으로 바꾸겠습니다. 2018-11-0417:35:41 0 0 b+(노란색) 상시에 물리는거죠. 실내등 b+(노란색) 상시에 물리는거죠. 실내등 2018-11-0417:36:58 0 0 acc(빨강) 오디오에 물리세요 acc(빨강) 오디오에 물리세요 2018-11-0417:38:07 0 0 넵 답변 감사합니닷 넵 답변 감사합니닷 2018-11-0417:41:20 0 0 요즘차량은 실내등이 상시로 계속 유지안되는 차종도 있어서 비상등이 제일 만만합니다. acc는 라디오에 노이즈가 끼는경우도 있어서 전동시트 하시는게 나아보여요 요즘차량은 실내등이 상시로 계속 유지안되는 차종도 있어서 비상등이 제일 만만합니다. acc는 라디오에 노이즈가 끼는경우도 있어서 전동시트 하시는게 나아보여요 2018-11-0417:43:58 레벨9는 코멘트를 작성한 후 1분이 경과해야 새 코멘트를 작성할 수 있습니다. ■ ▼ 상대에게 상처를 줄 수 있는 댓글은 삼가주세요. (이미지 넣을 땐 미리 보기를 해주세요.) 직접적인 욕설 및 인격모독성 발언을 할 경우 제재가 될 수 있습니다. - 이미지추가 Copyright 2005-2018 ppomppu. All rights reserved Navigator |
| BoilerPipe           | 등록하기 등록하고 홈으로이메일 추천하기뽐뿌( http://www.ppomppu.co.kr )에서 발송되어진 메일입니다. 블랙박스 설치 diy 문의입니다. 상시가 계속 안되네요 ㅜㅜ 클릭하시면 원본 글과 코멘트를 보실수 있습니다. http://www.ppomppu.co.kr/zboard/view.php?id=car&no=726658 ============================================================== 시동 걸면 블랙박스가 켜지는데시동을 끄면 블랙박스도 꺼집니다. 녹화를 중지합니다. 도 아니고그냥 툭 *(본문 텍스트를 일부 날려버림)* |







테스트를 해봤는데, 역시 단순 HTML 텍스트 추출은 답이 없는 결과를 보여주고 있습니다. 본 포스팅의 알고리즘을 바탕으로 구현한 AutoExtractor의 결과는 조금 지저분하지만, 본문을 찾기는 찾아낸다 정도가 되겠군요. 마지막으로 [BoilerPipe](https://boilerpipe-web.appspot.com/)는 조금더 깔끔한 결과를 보여줍니다. 다만 뽐뿌 사이트의 경우 사이트 뼈대가 올드한 관계로 본문을 찾지 못하고 텍스트 일부만 엉뚱하게 가져오는 문제가 있습니다. AutoExtractor는 본문은 가져오긴하지만, 일부 불필요한 부분까지 읽어오고있구요. 

Java를 사용해 표준적인 웹 페이지를 긁어오는 작업이라면 boilerpipe가 제일 좋을 것으로 보입니다. 그렇지 않다면 AutoExtractor도 대체제로 쓸만할 것 같기도 하구요.



결과가 썩 깨끗하지는 않지만 재미있는 작업이었습니다.