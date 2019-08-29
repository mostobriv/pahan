from traffic.configurator import Configurator
from traffic.masta import Masta


# def main():
    # traffic_slicer = Slicer()
    # traffic_crawler = Crawler(os.path.abspath('dumps'))
    # task1 = traffic_slicer.slice_pcap_tshark('dumps/small_pcap_file.pcap')
    # task2 = traffic_crawler.crawl()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait([task1, task2]))
    # loop.close()

if __name__ == '__main__':
    m = Masta.from_configurator(Configurator())
    m.run()