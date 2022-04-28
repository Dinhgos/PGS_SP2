import re
from xml.dom import minidom

data = []
wor_arr = []
lor_arr = []
fer_arr = []
# AB - block, EF - ores
res = []


def average(l):
    avg = sum(l) / len(l)
    return str(avg)


def get_bad():
    suma = 0

    for worker in wor_arr:
        for bl_time in worker[1]:
            suma += bl_time

    global res
    result = suma / int(res[0])

    return str(result)


def get_rad():
    suma = 0

    for worker in wor_arr:
        for ores_time in worker[0]:
            suma += ores_time

    global res
    result = suma / int(res[1])

    return str(result)


def write_to_xml():
    root = minidom.Document()

    xml = root.createElement('Simulation')
    xml.setAttribute('duration', data[-1][0])
    root.appendChild(xml)

    global res
    bad = root.createElement('blockAverageDuration')
    bad.setAttribute('totalCount', res[0])
    bad.appendChild(root.createTextNode(get_bad()))
    xml.appendChild(bad)

    rad = root.createElement('resourceAverageDuration')
    rad.setAttribute('totalCount', res[1])
    rad.appendChild(root.createTextNode(get_rad()))
    xml.appendChild(rad)

    faw = root.createElement('ferryAverageWait')
    faw.setAttribute('trips', str(len(fer_arr)))
    faw.appendChild(root.createTextNode(average(fer_arr)))
    xml.appendChild(faw)

    workers = root.createElement('Workers')
    xml.appendChild(workers)

    for id_wor, wor in enumerate(wor_arr):
        worker = root.createElement('Worker')
        worker.setAttribute('id', str(id_wor))
        workers.appendChild(worker)

        res = root.createElement('resources')
        res.appendChild(root.createTextNode(str(len(wor[0]))))
        worker.appendChild(res)

        res = root.createElement('workDuration')
        res.appendChild(root.createTextNode(str(sum(wor[1]))))
        worker.appendChild(res)

    vehicles = root.createElement('Vehicles')
    xml.appendChild(vehicles)

    for id_lor, lor in enumerate(lor_arr):
        vehicle = root.createElement('Vehicle')
        vehicle.setAttribute('id', str(id_lor))
        vehicles.appendChild(vehicle)

        lt = root.createElement('loadTime')
        lt.appendChild(root.createTextNode(str(lor[0][0])))
        vehicle.appendChild(lt)

        tt = root.createElement('transportTime')
        tt.appendChild(root.createTextNode(str(sum(lor[1]))))
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
    tmp = re.findall(r'\b\d+\b', data[0][3])
    global res
    res = tmp

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

    for i in range(0, len(mylist1)):
        worker = []
        ore = []
        block = []
        worker.append(ore)
        worker.append(block)
        wor_arr.append(worker)

    for i in range(0, len(mylist2)):
        lorry = []
        load_time = []
        tp_time = []
        lorry.append(load_time)
        lorry.append(tp_time)
        lor_arr.append(lorry)

    for line in data:
        match line[1]:
            case 'Worker':
                if line[3] == 'ore':
                    wor_arr[int(line[2])][0].append(int(line[4]))
                elif line[3] == 'block':
                    wor_arr[int(line[2])][1].append(int(line[4]))
                else:
                    print('Worker job in time ' + line[0] + ' not recognised.')
                    exit(1)

            case 'Lorry':
                if line[3] == 'full':
                    lor_arr[int(line[2])][0].append(int(line[4]))
                elif line[3] == 'go' or line[3] == 'end':
                    lor_arr[int(line[2])][1].append(int(line[4]))
                else:
                    print('Lorry job in time ' + line[0] + ' not recognised.')
                    exit(2)

            case 'Ferry':
                fer_arr.append(int(line[4]))


if __name__ == '__main__':
    read_input_file()
    process_input()
    write_to_xml()
