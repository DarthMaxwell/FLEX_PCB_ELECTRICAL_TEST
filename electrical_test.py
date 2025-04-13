import pyvisa
import time
import json

# Static variables
# DO WE NEED NIVISA ANYMORE?? i htink for the drivers
DAQ_ADDRESS = "USB0::0x2A8D::0x5101::MY58031367::0::INSTR"
KEI_ADDRESS = "GPIB0::22::INSTR"
DEFAULT_TIMEOUT = 15
LIMIT_LOW =  [None, None, 8000,  1000000, 1000000, 1000000, 1000000, None, None, 1000000, 1000000, 1000000, 90,  1000000, 1000000, 8000,  1000000, 1000000]
LIMIT_HIGH = [2,    2,    12000, None,    None,    None,    None,    2,    2,    None,    None,    None,    110, None,    None,    15000, None,    None]
HI_LO = ["VRET-VRET_S", "VRET-Vref", "VRET-HV_RET", "VRET-VIN", "VRET-CMD_N,GTXi_N", "VRET-NTC,LP_EN", "VRET-GND_C", "VIN-VIN_S", "VIN-Vsen", "VIN-CMD_N,GTXi_N", "VIN-NTC,LP_EN", "VIN-GND_C", "CMD_N,GTXi_N-CMD_P,GTXi_P", "CMD_N,GTXi_N-NTC,LP_EN", "CMD_N,GTXi_N-GND_C", "NTC,LP_EN-NTC_RET,MUX", "NTC,LP_EN-GND_C", "GND-GND_C"]
VOLTAGE = [(0,-300), (-300, 0), (0, 300), (300, 0)]

# Global vairabled
passedRES = True
passedHV = True
daq = None
kei = None

#BASSICLY IF THE RESULTS HAVE A NONE IN THEM THEN THAT MEANS SOMTHING IN THE MACHINE FAILED
#We use 1 retry to speed things up cuase we will still try 10 times before we move on
# CAN USE CHAT TO WRITE LITTLE FUNCTION EXPLANTIONS

def createJSON(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# A function to query the #daq and catch any erros so the whole program wont crash.
def safeReadDAQ(channel, retries=1):
    for _ in range(retries):
        try:
            res = daq.query("MEAS:RES? (@{})".format(channel))
            return float(res)
        except Exception as e:
            print("Error: {}, retrying...".format(e))
            time.sleep(1)
            daq.clear()
    return None

def safeReadKEI(retries=1):
    for _ in range(retries):
        try:
            res = kei.read()
            return float(res.replace("NDCI","").strip())
        except Exception as e:
            print("Error: {}, retrying...".format(e))
            time.sleep(1)
            #kei.clear() # is this possible or ?
    return None

def testChannelLowerLimit(channel, lowerLimit, timeout=DEFAULT_TIMEOUT):
    global passed

    while (timeout):
        res = safeReadDAQ(channel)

        if (res is not None):
            if (res > lowerLimit):
                print("Channel {} passed - {}ohms".format(channel, res))
                return res
                
        timeout -= 1

    passed = False
    print("Channel {} failed - {}ohms".format(channel, res))
    return res

def testChannelUpperLimit(channel, upperLimit, timeout=DEFAULT_TIMEOUT):
    global passed

    while(timeout):
        res = safeReadDAQ(channel)

        if (res is not None):
            if (res < upperLimit):
                print("Channel {} passed - {}ohms".format(channel, res))
                return res
                
        timeout -= 1

    passed = False
    print("Channel {} failed - {}ohms".format(channel, res))
    return res

def testChannelBothLimits(channel, lowerLimit, upperLimit, timeout=DEFAULT_TIMEOUT):
    global passed

    while (timeout):
        res = safeReadDAQ(channel)

        if (res is not None):
            if (lowerLimit < res and res < upperLimit):
                print("Channel {} passed - {}ohms".format(channel, res))
                return res
                
        timeout -= 1

    passed = False
    print("Channel {} failed - {}ohms".format(channel, res))
    return res

def testCurrent(start, end):
    global passed
    step = -10 if end < start else 10

    for v in range(start, end + step, step): #end + step??
        kei.write('V{},1,1X'.format(v))
        time.sleep(1)

        # DO WE NEED ALL THESE
        # CAN I SEND MULTIPLE COMMANDS AT ONCE
    kei.write('F0X')
    kei.write('B0X')
    kei.write('R0X')
    kei.write('DX')

    kei.write('T5X')

    current = safeReadKEI()

    if not (-2e-7 < current and current < 2e-7):
        print("Voltage {}V -> {}V failed - {}A".format(start, end, current))
        passed = False
        return current

    print("Voltage {}V -> {}V passed - {}A".format(start, end, current))
    return current

def main():
    global daq
    global kei
    resistance = []
    current = []

    component = input("Scan flex: ")
    start = time.time()
    date = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
    print ("Starting test for {} at {}".format(component, date))

    rm = pyvisa.ResourceManager()
    daq = rm.open_resource(DAQ_ADDRESS)
    kei = rm.open_resource(KEI_ADDRESS)

    # DAQ configuration
    # MIGHT BE ABLE TO SEND ALL THESE AT ONCE
    daq.write("*RST")
    daq.timeout = 10000
    daq.write("CONF:RES (@{})".format(range(101,119)))

    # we can use list comprehention to make it faster as now we dont have to have an append call everytime can use more memory but propably not a problem
    resistance = [
        testChannelUpperLimit(c, u) if l is None else
        testChannelLowerLimit(c, l) if u is None else
        testChannelBothLimits(c, l, u)
        for c, l, u in zip(range(101,119), LIMIT_LOW, LIMIT_HIGH)
    ]

    #Short all the channels on the DAQ
    #DOES THIS WORK?? and is it needed
    #daq.write("ROUT:CLOS (@118)")
    daq.write("*RST")

    #Configure the kei 487 thang
    #DO WE NEED ALL THESE THINGS LIKE???
    #With the write terminatino could i just have a big string and then have \n between each one??
    kei.write_termination = '\n'
    kei.read_termination = '\n'
    kei.write('L0X')
    kei.write('K0X')
    kei.write('C0X')
    kei.write('G0X')
    kei.write('O1X') # turn on the flow i gueess can look at document later

    current = [testCurrent(s, e) for s, e in VOLTAGE]

    #turn off it sending power the keithley

    kei.close()
    daq.close()

     #JSON Section
    #MIGHT NEED TO GO OVER THIS WITH SIMEN
    ELRES_JSON = {
        "component": component,
        "test": "Electrical_RES",
        "institution": "UNIBERGEN",
        "date": date,
        "prefix": "",
        "passed": passedRES,
        "HI-LO": HI_LO,
        "RES": {
            "resistance": resistance,
            "limit-low": LIMIT_LOW,
            "limit-hight": LIMIT_HIGH,
        }
    }

    ELHV_JSON = {
        "component": component,
        "test": "Electrical_HV",
        "institution": "UNIBERGEN",
        "date": date,
        "prefix": "",
        "passed": passedHV,
        "HV": {
            "current": current,
            "range": [-2e-07, 2e-07],
            "voltage": [y for (x, y) in VOLTAGE]
        }
    }

    createJSON(ELRES_JSON, "{}ELRES{}.json".format(component, date.split('T')[0]))
    createJSON(ELHV_JSON, "{}ELHV{}.json".format(component, date.split('T')[0]))
    print("Time elapsed {}m {}s".format((int)((time.time() - start) / 60), round((time.time() - start) % 60, 2)))

if __name__=="__main__":main()
