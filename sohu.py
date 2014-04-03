#!/usr/bin/env python

__all__ = ['sohu_download']

from common import *
from store import get_useful_url_count, get_useful_urls, insert_sohu

def real_url(host, prot, file, new):
    url = 'http://%s/?prot=%s&file=%s&new=%s' % (host, prot, file, new)
    start, _, host, key, _, _, _, _ = get_html(url).split('|')
    return '%s%s?key=%s' % (start[:-1], new, key)

def sohu_download(url, merge=True):
    vid = r1('vid\s*=\s*[\'\"](\d+)[\'\"]', get_html(url))
    #print 111111111111111111111111111111, vid
    assert vid
    import json
    # loads Simple conversion
    data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
    print 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid
    host = data.get('allot', None)
    if not host:
        data = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s' % vid))
    host = data.get('allot')
    prot = data['prot']
    real_urls = []
    data = data['data']
    title = data['tvName']
    size = sum([int(bt) for bt in data['clipsBytes']])
    assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
    for file, new in zip(data['clipsURL'], data['su']):
        real_urls.append(real_url(host, prot, file, new))
    assert data['clipsURL'][0].endswith('.mp4')
    sohu_data = {
        'url': url,
        'vid': vid,
        'title':title,
        'host': host,
        'prot': prot,
        'real_urls': real_urls,
        'data': data,
    }
    insert_sohu(sohu_data)
    download_urls(real_urls, title, 'mp4', total_size=size, refer=url, merge=merge)

def sohu_main(download_count):
    useful_url_count = int(get_useful_url_count())
    download_count = int(download_count)
    can_download_count = download_count if download_count <= useful_url_count else useful_url_count
    useful_urls = get_useful_urls(can_download_count)
    print 'you carn download %s moives' %can_download_count
    for url in useful_urls:
        print url.get('url')
        sohu_download(url.get('url'))
