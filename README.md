# FLEX_PCB_ELECTRICAL_TEST
2025 Bachlors project at HVL with ATLAS group in UIB. Can add more later

## SETUP
We assume you already have python 3.9.6 or newer THIS IS JUST WHAT I HAVE NOT A REAL MINIMUM

### STEP 1 - Install NI-VISA
This is for controlling the Highvoltage power supply (grab some text form that link)
https://www.ni.com/en/support/downloads/drivers/download.ni-488-2.html?srsltid=AfmBOoqgh0lgB955pOPCkuwX9M7VUnNrGW0I8cZiu6bDadTudPAP7k8L

### STEP 2 - Install VISA
This allows us to talk to the DAQ970. Note that a prerequisite is IO Libraries Suite. Both can be found below in the link. 
https://www.keysight.com/us/en/lib/software-detail/driver/daq970-data-acquisition-system-python-instrument-drivers.html

### STEP 3 - Install pyvisa
This is the python library we use to send the SCPI commands.
```bash
pip install pyvisa
```

### Step 4 - Pysical setup
Here are are assuming the DAQ extention car is already wired up. Plug the 40 pin conenctor into the apapter card make sure to plug it in currectly by matching up the triangles.
Turn on and plug the DAQ and Model 2400 into your computer. Plug in the barcode scaner in your computer too.

### Step 5 - Clone the repo
Clone the repository PUT COMMAND BELOW

### Step 6 - Updateting scipt
Aftter plugging in the usb ports you need to make sure the addresses are still currect. You do this by... maybe make another scipt for this idk. Now you are able to start testing.

## OPERATION
Here we are assuming you have plugged in the DAQ970 and Model 2400 into you computer and if nececssary have updated their respective address in the code. It is also assumed that the 40pin connector from the DAQ is plugged into the apapter board. We also assume you turned both machines on. High voltage boi plugged in too but maybe we just assume that u have finished the setup section

### Step 1: Connect the FLEX PCB to the apapter board.
more details
Lay the FLEX PCB as the outline on the apapter board shows and connect the three ribbin cables to there respective conectors.

### Step 2: Running the script
Open your terminal and find your way to the scipt. Run the python scipt
```Bash
electrical_test.py
```
It will prompt you to scan the flex. You can use a barcode scaner on th barcode or manually type in the ID of the FLEX PCB you are testing.
It will then run thought the test printing out if a channel has passed or failed with the resistance measured. It will also print out when testing the volatge. !!!!MAYBE JUST SAY IT WILL PRINT OUT UPDATING INFRO TO KEEP YOU IN THE LOOP OF WHT HAPPENING TO KEEP PROGRESS
When the script is finished it will create a json with the name of the FLEX PCB ID given.

### Step 3: Disconnect the FLEX PCB
Disconnect the FLEX PCB by lifting up the the 2 ribben connectors on the edge and then you can pull the FLEX PCB away disconnecting the middle ribben cable.
