from traffic.configurator import Configurator
from traffic.masta import Masta

if __name__ == '__main__':
    m = Masta.from_configurator(Configurator())
    m.run()