from xml.dom import minidom

data = []
wor_arr = []
lor_arr = []
fer_arr = []
ores = -1
blocks = -1


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


def process_input():
    c_wor = []
    c_lor = []

    for line in data:
        match line[1]:
            case 'Worker':
                c_wor.append(int(line[2]))
            case 'Lorry':
                c_lor.append(int(line[2]))

    mylist1 = list(dict.fromkeys(c_wor))
    mylist2 = list(dict.fromkeys(c_lor))

    mylist1.sort()
    mylist2.sort()

    for x in range(0, len(mylist1)):
        worker = []
        ore = []
        block = []
        worker.append(ore)
        worker.append(block)
        wor_arr.append(worker)

    for x in range(0, len(mylist2)):
        lorry = []
        load_time = []
        tp_time = []
        lorry.append(load_time)
        lorry.append(tp_time)
        lor_arr.append(lorry)

    for line in data:
        match line[1]:
            case 'Worker':
                # TODO worker 4 fastest - run the loop first
                if int(line[2]) >= len(wor_arr):
                    worker = []
                    ore = []
                    block = []
                    worker.append(ore)
                    worker.append(block)
                    wor_arr.append(worker)
                    if line[3] == 'ore':
                        wor_arr[int(line[2])][0].append(int(line[4]))
                    elif line[3] == 'block':
                        wor_arr[int(line[2])][1].append(int(line[4]))
                    else:
                        print('Worker job in time ' + line[0] + ' not recognised.')
                        exit(1)
                else:
                    if line[3] == 'ore':
                        wor_arr[int(line[2])][0].append(int(line[4]))
                    elif line[3] == 'block':
                        wor_arr[int(line[2])][1].append(int(line[4]))
                    else:
                        print('Worker job in time ' + line[0] + ' not recognised.')
                        exit(1)

            case 'Lorry':
                # TODO lorry fastest
                if int(line[2]) >= len(lor_arr):
                    lorry = []
                    load_time = []
                    tp_time = []
                    lorry.append(load_time)
                    lorry.append(tp_time)
                    lor_arr.append(lorry)
                    if line[3] == 'full':
                        lor_arr[int(line[2])][0].append(int(line[4]))
                    if line[3] == 'go' or line[3] == 'end':
                        lor_arr[int(line[2])][1].append(int(line[4]))
                    else:
                        print('Lorry job in time ' + line[0] + ' not recognised.')
                        exit(2)
                else:
                    if line[3] == 'full':
                        lor_arr[int(line[2])][0].append(int(line[4]))
                    if line[3] == 'go' or line[3] == 'end':
                        lor_arr[int(line[2])][1].append(int(line[4]))
                    else:
                        print('Lorry job in time ' + line[0] + ' not recognised.')
                        exit(2)


if __name__ == '__main__':
    read_input_file()
    process_input()
    write_to_xml()
