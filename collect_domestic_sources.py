"""Read one public directory, keeping route-topic labels and URLs only."""
import json,re,urllib.request
from html.parser import HTMLParser
from pathlib import Path
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.url=None;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.url=dict(attrs).get('href');self.parts=[]
 def handle_data(self,data):
  if self.url:self.parts.append(data)
 def handle_endtag(self,tag):
  if tag=='a' and self.url:self.links.append({'title':re.sub(r'\s+',' ',''.join(self.parts)).strip(),'url':self.url});self.url=None
if __name__=='__main__':
 url='https://www.8264.com/'
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HikingAtlasResearch/1.0'}),timeout=20) as response:
  raw=response.read();match=re.search(rb'charset=["\s]*([\w-]+)',raw[:10000],re.I);encoding=match.group(1).decode() if match else response.headers.get_content_charset() or 'gb18030';html=raw.decode(encoding,errors='strict')
 parser=Links();parser.feed(html);items=[r for r in parser.links if '/youji/list-' in r['url'] and r['title']]
 path=Path(__file__).resolve().parent/'domestic-source-discovery.json';path.write_text(json.dumps({'source':url,'encoding':encoding,'items':items},ensure_ascii=False,indent=2),encoding='utf-8');print('Public route-topic links collected:',len(items))
