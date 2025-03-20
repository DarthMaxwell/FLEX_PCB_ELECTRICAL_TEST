import pyvisa
import time
import json

def main():
    DEFAULT_TIMEOUT = 10
    # The Channel is used as the index
    LIMIT_LOW =  [None, None, 8000,  1000000, 1000000, 1000000, 1000000, None, None, 1000000, 1000000, 1000000, 90,  1000000, 1000000, 8000,  1000000, 1000000]
    LIMIT_HIGH = [2,    2,    12000, None,    None,    None,    None,    2,    2,    None,    None,    None,    110, None,    None,    15000, None,    None]
    HI_LO = ["VRET-VRET_S", "VRET-Vref", "VRET-HV_RET", "VRET-VIN", "VRET-CMD_N,GTXi_N", "VRET-NTC,LP_EN", "VRET-GND_C", "VIN-VIN_S", "VIN-Vsen", "VIN-CMD_N,GTXi_N", "VIN-NTC,LP_EN", "VIN-GND_C", "CMD_N,GTXi_N-CMD_P,GTXi_P", "CMD_N,GTXi_N-NTC,LP_EN", "CMD_N,GTXi_N-GND_C", "NTC,LP_EN-NTC_RET,MUX", "NTC,LP_EN-GND_C", "GND-GND_C"]
    VOLTAGE = [-200, 0, 200, 0] #SHOULD BE 300 INSTEAD of 200

    results = []
    current = []
    passed = True

    def safe_query(cmd, retries=3):
        for _ in range(retries):
            try:
                res = daq.query(cmd)
                return float(res)
            except Exception as e:
                print(f"Error: {e}, retrying...")
                time.sleep(1)
                daq.clear()
        return None

    def testChannelLowerLimit(channel, lowerLimit):
        passed #maybe we dont need global now can test rn tho
        timeout = DEFAULT_TIMEOUT

        while (timeout):
            res = safe_query("MEAS:RES? (@{})".format(channel))

            if (res is not None):
                if (res > lowerLimit):
                    print("Channel {} passed - {}".format(channel, res))
                    passed = passed and True
                    return res
                
            timeout -= 1

        passed = passed and False
        print("Channel {} failed - {}".format(channel, res))
        return res

    def testChannelUpperLimit(channel, upperLimit):
        passed
        timeout = DEFAULT_TIMEOUT

        while(timeout):
            res = safe_query("MEAS:RES? (@{})".format(channel))

            if (res is not None):
                if (res < upperLimit):
                    print("Channel {} passed - {}".format(channel, res))
                    passed = passed and True
                    return res
                
            timeout -= 1

        passed = passed and False
        print("Channel {} failed - {}".format(channel, res))
        return res

    def testChannelBothLimits(channel, lowerLimit, upperLimit):
        passed
        timeout = DEFAULT_TIMEOUT

        while (timeout):
            res = safe_query("MEAS:RES? (@{})".format(channel))

            if (res is not None):
                if (lowerLimit < res and res < upperLimit):
                    print("Channel {} passed - {}".format(channel, res))
                    passed = passed and True
                    return res
                
            timeout -= 1

        passed = passed and False
        print("Channel {} failed - {}".format(channel, res))
        return res

    def testCurrent(voltage):
        passed

        keithley.write(":SOUR:VOLT {}".format(voltage))
        keithley.write(":OUTP ON")
        time.sleep(0.5)
        res = keithley.query(":MEAS:CURR?")
        current = float(res.split(",")[1])

        if (0.0000002 < current and current < -0.0000002):
            passed = False
            print("Voltage {} failed - {}".format(voltage, current))
            return current

        print("Voltage {} passed - {}".format(voltage, current))
        return current

    component = input("Scan flex: ")
    date = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
    print ("Starting test for {} at {}".format(component, date))

    rm = pyvisa.ResourceManager()
    daq = rm.open_resource("USB0::0x2A8D::0x5101::MY58031367::0::INSTR")

    daq.write("*RST")
    daq.timeout = 10000
    daq.write("CONF:RES (@{})".format(range(101,118)))

    start = time.time()

    zipped = list(zip(range(101,118), LIMIT_LOW, LIMIT_HIGH))

    for (c, l, u) in zipped:
        if (l is None):
            #Test upper
            res = testChannelUpperLimit(c,u)
        elif (u is None):
            #test lower
            res = testChannelLowerLimit(c, l)
        else:
            res = testChannelBothLimits(c, l, u)

        results.append(res)

    #Short all the channels on the DAQ
    daq.write(":ROUT:TERN:ALL SHORT")

    # KEITHLEY part just at 200v rn so might need to fix later
    rm = pyvisa.ResourceManager(r"C:\Windows\System32\visa32.dll")
    keithley = rm.open_resource("GPIB0::24::INSTR")

    keithley.write("*RST")
    keithley.write(":SOUR:FUNC VOLT")
    keithley.write(":SOUR:VOLT:RANG 200") # might need to change this

    for v in VOLTAGE:
        current.append(testCurrent(v))

    keithley.write(":OUTP OFF")
    keithley.close()
    daq.close()

    print("Time elapsed {}m {}s".format((int)((time.time() - start) / 60), round((time.time() - start) % 60, 2)))

    result_data = {
        "component": component,
        "test": "electrical",
        "institution": "UNIBERGEN",
        "date": date,
        "prefix": "",
        "passed": passed,
        "HI-LO": HI_LO,
        "results": {
            "resistance": results,
            "limit-low": LIMIT_LOW,
            "limit-hight": LIMIT_HIGH,
            "current": current
        }
    }

    filename = "{}.json".format(component)
    with open(filename, "w") as json_file:
        json.dump(result_data, json_file, indent=4)

    print("Json file created with results for {} at {}".format(component, filename))

if __name__=="__main__":main()