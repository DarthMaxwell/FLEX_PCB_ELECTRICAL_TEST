# FLEX_PCB_ELECTRICAL_TEST
2025 Bachelor's project at HVL with the ATLAS group in UIB, in coordination with UIO.  
This repository is dedicated to the electrical testing part of the quality control testing for the FLEX PCBs.  
*(IDK how much info we should put here)*

---

## SETUP

### Prerequisites
- **DAQ970A** with multiplexer card properly wired up to a 40-pin connector  
- **Keithley Model 2400** *(WILL CHANGE TO ANOTHER HIGH VOLTAGE TOOL)*  
- **Adapter board** and its ribbon cables *(IDK IF WE GOT A NAME FOR THIS)*
- Minimum **Python 3.9.6** *(THIS IS JUST WHAT I HAVE, NOT A REAL MINIMUM)*  

### STEP 1 - Install NI-VISA for the Keithley Model 2400  
*(COULD CHANGE SO DON’T WANNA ADD TEXT HERE)*

Follow the steps from this [link](https://www.ni.com/en/support/downloads/drivers/download.ni-488-2.html?srsltid=AfmBOoqgh0lgB955pOPCkuwX9M7VUnNrGW0I8cZiu6bDadTudPAP7k8L).

### STEP 2 - Install VISA for the DAQ970A  
Follow the steps from this [link](https://www.keysight.com/us/en/lib/software-detail/driver/daq970-data-acquisition-system-python-instrument-drivers.html).

### STEP 3 - Install PyVISA  
This is the Python library we use to send SCPI commands.  
```bash
pip install pyvisa
```

### Step 4 - Pysical setup
1. Plug th DAQ into the adapter card with the 40pin connector and your computer with the usb cable.
2. Plug the Keithley Model 2400 in the apapter card and your computer with the usb cable.
3. Plug in the barcode reader

### Step 5 - Clone the repo
```bash
git clone https://github.com/DarthMaxwell/FLEX_PCB_ELECTRICAL_TEST.git
```

### Step 6 - Updateting scipt
Aftter plugging in the usb ports you need to make sure the addresses are still currect. You do this by... maybe make another scipt for this idk. Now you are able to start testing.

---

## OPERATION
Assuming the setup is finished.

### Step 1: Connect the FLEX PCB to the apapter board.
There is a layout on the adapter board for how the FLEX PCB should be.
1. Slide the FLEX PCB into position connecting the middle ribben cable as you do so.
2. Take the the other two ribben cables and connect then to their respective sides of the FLEX PCB. Simply push down gently to make the connection.

### Step 2: Running the script
1. Open your terminal and navigate to the script's directory.
2. Run the Python scipt
```Bash
electrical_test.py
```
3. The script will prompt you to scan the FLEX PCB. You can either use a barcode scanner on the barcode or manually type in the ID of the FLEX PCB you are testing.
4. It will print out information to show results and progress.
5. Once finished, it will create a JSON with the name of the FLEX PCB ID given.

### Step 3: Disconnect the FLEX PCB
1. Disconnect the two ribben cables on the sides by gently lifting up on them
2. Slide the FLEX PCB away from disconnecting the middle ribben cable.
