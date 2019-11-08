from traffic.configurator import Configurator
from traffic.master import Master

if __name__ == '__main__':
    m = Master.from_configurator(Configurator())
    m.run()