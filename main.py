from xml.dom import minidom

data = []


def write_to_xml():
    root = minidom.Document()

    xml = root.createElement('Simulation')
    xml.setAttribute('duration', data[-1][0])
    root.appendChild(xml)

    bad = root.createElement('blockAverageDuration')
    bad.setAttribute('totalCount', 'AB')
    bad.appendChild(root.createTextNode('CD'))
    xml.appendChild(bad)

    rad = root.createElement('resourceAverageDuration')
    rad.setAttribute('totalCount', 'EF')
    rad.appendChild(root.createTextNode('GH'))
    xml.appendChild(rad)

    faw = root.createElement('ferryAverageWait')
    faw.setAttribute('trips', 'IJ')
    faw.appendChild(root.createTextNode('KL'))
    xml.appendChild(faw)

    workers = root.createElement('Workers')
    xml.appendChild(workers)

    # TODO - 4 workers
    worker = root.createElement('Worker')
    worker.setAttribute('id', 'MN')
    workers.appendChild(worker)

    # TODO - 4 workers
    res = root.createElement('resources')
    res.appendChild(root.createTextNode('OP'))
    worker.appendChild(res)

    # TODO - 4 workers
    res = root.createElement('workDuration')
    res.appendChild(root.createTextNode('QR'))
    worker.appendChild(res)

    vehicles = root.createElement('Vehicles')
    xml.appendChild(vehicles)

    # TODO - more
    vehicle = root.createElement('Vehicle')
    vehicle.setAttribute('id', 'ST')
    vehicles.appendChild(vehicle)

    # TODO - more
    lt = root.createElement('loadTime')
    lt.appendChild(root.createTextNode('UV'))
    vehicle.appendChild(lt)

    # TODO - more
    tt = root.createElement('transportTime')
    tt.appendChild(root.createTextNode('WX'))
    vehicle.appendChild(tt)

    xml_str = root.toprettyxml(indent="\t")

    save_path_file = "output.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


def read_input_file():
    with open("input.txt") as file:
        for line in file:
            line = line.rstrip()
            data.append(line.split(';'))


if __name__ == '__main__':
    read_input_file()
    write_to_xml()
