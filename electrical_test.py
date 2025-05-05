import pyvisa
import time
import json

"""
Static Configuration Variables

DAQ_ADDRESS (str): VISA address for the Keysight DAQ970A Data Acquisition System.
KEI_ADDRESS (str): VISA address for the Keithley 487 Picoammeter / Voltage Source

DEFAULT_TIMEOUT (int): Number of read attempts before failing a measurement.
    Used instead of a time-based timeout to allow capacitive channels time to stabilize.

LIMIT_LOW (List[float or None]): Minimum acceptable values per channel index.
    If a value is None, no lower limit is enforced on that channel.
        
LIMIT_HIGH (List[float or None]): Maximum acceptable values per channel index.
    If a value is None, no upper limit is enforced on that channel.

HV_LIMIT_LOW (float): Global low threshold for high-voltage current measurements (in Amps).
HV_LIMIT_HIGH (float): Global high threshold for high-voltage current measurements (in Amps).

HI_LO (List[str]): Descriptive names for each measurement channel or channel pair.

VOLTAGE (List[Tuple[int, int]]): Expected voltage direction or test limits per measurement pair.
    Each tuple corresponds to a direction (e.g., 0 to -300 V, -300 to 0 V).
"""
DAQ_ADDRESS = "USB0::0x2A8D::0x5101::MY58031367::0::INSTR"
KEI_ADDRESS = "GPIB0::22::INSTR"
DEFAULT_TIMEOUT = 15
LIMIT_LOW =  [None, None, 8000,  1000000, 1000000, 1000000, 1000000, None, None, 1000000, 1000000, 1000000, 90,  1000000, 1000000, 8000,  1000000, 1000000]
LIMIT_HIGH = [2,    2,    12000, None,    None,    None,    None,    2,    2,    None,    None,    None,    110, None,    None,    15000, None,    None]
HV_LIMIT_LOW = -2e-7
HV_LIMIT_HIGH = 2e-7
HI_LO = ["VRET-VRET_S", "VRET-Vref", "VRET-HV_RET", "VRET-VIN", "VRET-CMD_N,GTXi_N", "VRET-NTC,LP_EN", "VRET-GND_C", "VIN-VIN_S", "VIN-Vsen", "VIN-CMD_N,GTXi_N", "VIN-NTC,LP_EN", "VIN-GND_C", "CMD_N,GTXi_N-CMD_P,GTXi_P", "CMD_N,GTXi_N-NTC,LP_EN", "CMD_N,GTXi_N-GND_C", "NTC,LP_EN-NTC_RET,MUX", "NTC,LP_EN-GND_C", "GND-GND_C"]
VOLTAGE = [(0,-300), (-300, 0), (0, 300), (300, 0)]

"""
Global Variables

passedRES (bool): Flag indicating whether all resistance tests have passed.
    Initialized to True; set to False if any resistance test fails.

passedHV (bool): Flag indicating whether all high-voltage current tests have passed.
    Initialized to True; set to False if any HV test fails.

daq (object or None): Placeholder for the DAQ970A instrument controller object.
kei (object or None): Placeholder for the Keithley instrument controller object.
"""
passedRES = True
passedHV = True
daq = None
kei = None

"""
Writes a dictionary to a JSON file with pretty formatting.

Args:
    data (dict): The data to be written to the JSON file.
    filename (str): The name of the file to write to (including .json extension).

Returns:
    None
"""
def createJSON(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

"""
Safely reads a resistance measurement from the DAQ970A on a specified channel.

Retries the read operation in case of communication errors.

Args:
    channel (int): The DAQ channel number to read from.
    retries (int): Number of retry attempts in case of failure (default is 1).

Returns:
    float or None: The resistance reading in Ohms as a float if successful, otherwise None.
"""
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

"""
Safely reads a current measurement from the Keithley 487.

Cleans the response string by removing non-numeric indicators (e.g., "NDCI") 
and retries the operation in case of communication errors.

Args:
    retries (int): Number of retry attempts in case of failure (default is 1).

Returns:
    float or None: The current reading in Amps as a float if successful, otherwise None.
"""
def safeReadKEI(retries=1):
    for _ in range(retries):
        try:
            res = kei.read()
            return float(res.replace("NDCI","").strip())
        except Exception as e:
            print("Error: {}, retrying...".format(e))
            time.sleep(1)
    return None

"""
Tests a specific DAQ970A channel for resistance within specified limits.

Repeatedly reads resistance from the channel, allowing time for capacitors to stabilize. Passes if a valid reading is within limits 
before timeout.

Args:
    channel (int): The DAQ channel number to test.
    lowerLimit (float or None): Minimum acceptable resistance value (Ohms). 
        If None, no lower limit is applied.
    upperLimit (float or None): Maximum acceptable resistance value (Ohms). 
        If None, no upper limit is applied.
    timeout (int): Number of attempts before declaring failure (default is DEFAULT_TIMEOUT).

Returns:
    float or None: The final resistance reading from the channel in Ohms.
        Will still return the value even if the test fails.

Notes:
    - Updates the global `passedRES` flag to False if the test fails.
"""
def testChannel(channel, lowerLimit, upperLimit, timeout=DEFAULT_TIMEOUT):
    global passedRES

    while (timeout):
        res = safeReadDAQ(channel)

        if (res is not None):
            if ( (lowerLimit is None or lowerLimit < res) and (upperLimit is None or res < upperLimit) ):
                print("Channel {} passed - {}ohms".format(channel, res))
                return res
        time.sleep(0.1)
        timeout -= 1

    passedRES = False
    print("Channel {} failed - {}ohms".format(channel, res))
    return res

"""
Applies a voltage sweep from start to end using the Keithley 487
and checks whether the resulting current is within defined HV limits.

Args:
    start (int): Starting voltage value (in volts).
    end (int): Ending voltage value (in volts). The function will sweep 
        in 10V steps from start to end.

Returns:
    float or None: The final measured current in Amps. Returns None if 
        the current read fails or cannot be parsed.

Notes:
    - Updates the global `passedHV` flag to False if the current is out of range.
    - Waits 1 second between voltage steps to allow the signal to settle.
"""
def testCurrent(start, end):
    global passedHV
    step = -10 if end < start else 10

    for v in range(start, end + step, step):
        kei.write('V{},1,1X'.format(v))
        time.sleep(1)

    current = safeReadKEI()

    if not (HV_LIMIT_LOW < current and current < HV_LIMIT_HIGH):
        print("Voltage {}V -> {}V failed - {}A".format(start, end, current))
        passedHV = False
        return current

    print("Voltage {}V -> {}V passed - {}A".format(start, end, current))
    return current

"""
Main execution function for running electrical tests on a flex PCB component.

This script performs two sets of tests:
    1. Resistance measurements across predefined DAQ970A channels.
    2. High-voltage current checks using the Keithley 487.
"""
def main():
    global daq
    global kei
    resistance = []
    current = []

    # Prompts user to scan a component name/ID.
    component = input("Scan flex: ")

    # Get timestamps and prints a message indicating the start of the test, including the component name and timestamp.
    start = time.time()
    date = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
    print ("Starting test for {} at {}".format(component, date))

    # Initializes VISA communication with the DAQ970A and Keithley instruments.
    rm = pyvisa.ResourceManager()
    daq = rm.open_resource(DAQ_ADDRESS)
    kei = rm.open_resource(KEI_ADDRESS)

    # Configures the DAQ970A
    daq.write("*RST")
    daq.timeout = 10000

    # Resistance measurements across predefined DAQ970A channels.
    resistance = [
        testChannel(c,l,u) for c, l, u in zip(range(101,119), LIMIT_LOW, LIMIT_HIGH)
    ]

    # Resets the DAQ970A
    daq.write("*RST")

    # Configures the Keithley 487
    kei.write_termination = '\n'
    kei.read_termination = '\n'
    kei.write('L0X\nK0X\nC0X\nG0X\nO1X')

    # High-voltage current test using the Keithley 487
    current = [testCurrent(s, e) for s, e in VOLTAGE]

    # Turn off output on the Keithley 487
    kei.write('O0X')

    # Close the communication channel to the Keithley and the DAQ970A
    kei.close()
    daq.close()

    # Resistance test JSON structure
    ELRES_JSON = {
        "component": component,
        "test": "Electrical_RES",
        "institution": "UNIBERGEN",
        "date": date,
        "prefix": "",
        "passed": passedRES,
        "results": {
            "channel": HI_LO,
            "resistance": resistance,
            "limit-low": LIMIT_LOW,
            "limit-high": LIMIT_HIGH,
        }
    }

    # High-voltage test JSON structure
    ELHV_JSON = {
        "component": component,
        "test": "Electrical_HV",
        "institution": "UNIBERGEN",
        "date": date,
        "prefix": "",
        "passed": passedHV,
        "results": {
            "voltage": [y for (x, y) in VOLTAGE],
            "current": current,
            "limits": [HV_LIMIT_LOW, HV_LIMIT_HIGH]
        }
    }

    # Saves JSON reports (resistance and HV current) with timestamped filenames.
    createJSON(ELRES_JSON, "{}-resistance-{}.json".format(component, date.split('T')[0]))
    createJSON(ELHV_JSON, "{}-highvoltage-{}.json".format(component, date.split('T')[0]))

    # Outputs elapsed time
    print("Time elapsed {}m {}s".format((int)((time.time() - start) / 60), round((time.time() - start) % 60, 2)))

if __name__=="__main__":main()
