import getopt
import re
import sys
from os.path import exists
from xml.dom import minidom

'''
converts output from PGS1 to XML output
author Xuan Toan Dinh
version 01.05.2022
'''

data = []       # raw data from input
wor_arr = []    # list of workers
lor_arr = []    # list of lorrys
fer_arr = []    # list of ferrys
res = []        # 0 = AB - blocks, 1 = EF - ores


# average of list
def average(in_list):
    avg = sum(in_list) / len(in_list)
    return str(avg)


# calculates average time of 0 = ores / 1 = blocks
def get_average(index):
    suma = 0

    for worker in wor_arr:
        suma += sum(worker[index])

    global res
    result = suma / int(res[index])

    return str(result)


# writes the xml output from processed data
def write_to_xml(output_file):
    root = minidom.Document()

    xml = root.createElement('Simulation')
    xml.setAttribute('duration', data[-1][0])
    root.appendChild(xml)

    global res
    bad = root.createElement('blockAverageDuration')
    bad.setAttribute('totalCount', res[0])
    bad.appendChild(root.createTextNode(get_average(1)))
    xml.appendChild(bad)

    rad = root.createElement('resourceAverageDuration')
    rad.setAttribute('totalCount', res[1])
    rad.appendChild(root.createTextNode(get_average(0)))
    xml.appendChild(rad)

    faw = root.createElement('ferryAverageWait')
    faw.setAttribute('trips', str(len(fer_arr)))
    faw.appendChild(root.createTextNode(average(fer_arr)))
    xml.appendChild(faw)

    # writes workers
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

    # writes vehicles
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

    save_path_file = output_file

    with open(save_path_file, "w") as f:
        f.write(xml_str)


# reads data from input file and saves into data list
def read_input_file(path_to_file):
    if not exists(path_to_file):
        print('Input file does not exist.')
        sys.exit(3)

    # separates line into individual words and saves into data list
    with open(path_to_file) as file:
        for line in file:
            line = line.rstrip()
            data.append(line.split(';'))


# processes data into into global lists
def process_input():
    # get total number of blocks/ores
    tmp = re.findall(r'\b\d+\b', data[0][3])
    global res
    res.append(tmp[1])
    res.append(tmp[0])

    c_wor = []
    c_lor = []

    # get number of workers/lorry
    for line in data:
        match line[1]:
            case 'Worker':
                c_wor.append(int(line[2]))
            case 'Lorry':
                c_lor.append(int(line[2]))

    number_of_workers = list(dict.fromkeys(c_wor))
    number_of_lorry = list(dict.fromkeys(c_lor))

    # inserting workers into wor_arr list
    for i in range(0, len(number_of_workers)):
        worker = []
        ore = []
        block = []
        worker.append(ore)
        worker.append(block)
        wor_arr.append(worker)

    # inserting lorry into lor_arr
    for i in range(0, len(number_of_lorry)):
        lorry = []
        load_time = []
        tp_time = []
        lorry.append(load_time)
        lorry.append(tp_time)
        lor_arr.append(lorry)

    # fill lists with data from raw data list
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
                elif line[3] == 'go' or line[3] == 'end' or line[3] == 'ferry':
                    lor_arr[int(line[2])][1].append(int(line[4]))
                else:
                    print('Lorry job in time ' + line[0] + ' not recognised.')
                    exit(2)

            case 'Ferry':
                fer_arr.append(int(line[4]))


# parses command line arguments
def in_params(argv):
    input_file = ''
    output_file = ''

    # get parameters from command line
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Wrong command try:')
        print('python3 ./run_sp2.py -i <vstupni soubor> -o <vystupni soubor>')
        sys.exit(2)

    # sets input and output file name
    for opt, arg in opts:
        if opt == '-h':
            print('python3 ./run_sp2.py -i <vstupni soubor> -o <vystupni soubor>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    return input_file, output_file


# main starting function of program
if __name__ == '__main__':
    io_files = in_params(sys.argv[1:])
    read_input_file(io_files[0])
    process_input()
    write_to_xml(io_files[1])
