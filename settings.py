
FLAG_FORMAT = '\w{31}='


SLICER = {
    'type': 'traffic.slicer.Slicer',
    'args': [
        'dumps'
    ]
}


CRAWLER = {
    'type': 'traffic.crawler.Crawler',
    'args': [
        'streams'
    ]
}