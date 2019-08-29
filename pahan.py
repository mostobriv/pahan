import os
# from web import app
from traffic.slicer import Slicer
from traffic.crawler import Crawler
# import configrurator


def main():
    # web_task            = WebApp()
    traffic_slicer = Slicer()
    traffic_crawler = Crawler(os.path.abspath('dumps'))
    traffic_slicer.slice_pcap_tshark('dumps/small_pcap_file.pcap')
    # traffic_slicer.slice_pcap_tshark('dumps/big_pcap_file.pcap')
    traffic_crawler.crawl()
    # traffic_crawler     = traffic_crawler.from_configurator(Configurator())

if __name__ == '__main__':
    main()