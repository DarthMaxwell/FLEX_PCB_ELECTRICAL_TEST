# FLEX_PCB_ELECTRICAL_TEST

2025 Bachelor's project at HVL with the ATLAS group in UiB, in coordination with UiO.  
This repository is dedicated to the electrical testing part of the quality control process for the FLEX PCBs.

## Installation

It is assumed the physical side of the setup is complete. This will go over installing the drivers required for the script to run.

### Install Python

Follow instructions from this [link](https://www.python.org/downloads/). Make sure it's compatible with the DAQ970A Python drivers mentioned below.

### Install NI-VISA

Follow instructions from this [link](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOor1kbHcnE5zmGIr423cQzTclPztI1KKWyR7TktfFbwVOumgcrwB#565016).

### Install DAQ970A Python Drivers

Follow instructions from this [link](https://www.keysight.com/us/en/lib/software-detail/driver/daq970-data-acquisition-system-python-instrument-drivers.html).

### Install PyVISA

```
pip install pyvisa
```

### Clone Git Repository

```
git clone https://github.com/DarthMaxwell/FLEX_PCB_ELECTRICAL_TEST.git
```

You might need to change the USB addresses for the instruments in the script based on where you plugged them into your computer.

## Test Procedure

### Step 1: Prepare the work area and ESD protection

Keep the area clean and dry. Turn on both instruments and make sure they are connected to the computer. Wear antistatic nitrile gloves and use an ESD bracelet. Handle PCBs with care.

### Step 2: Select correct adapter board

Identify the adapter board by name and PCB outline. If the correct adapter board is already connected, proceed to step 6. If you don't need to disconnect the other adapter board, go to step 4.

### Step 3: Disconnect adapter board

Disconnect the high-voltage cable first. Open the latches on the 40-pin connector and pull the cable straight up.

### Step 4: Connect the 40-pin cable

Make sure the locks on both sides of the connector are fully open. Line up the notches and press down until the locks are fully closed. Ensure the cable is properly connected with no gap in between.

### Step 5: Connect the high-voltage cable

Press the cable all the way into the connector—there is no lock. The direction you connect it does not matter.

### Step 6: Unpack the PCB from its antistatic bag and place it on the adapter board

It is very important to wear the ESD band and antistatic gloves. Avoid contact with conductive traces and sensitive components. Do not bend the PCB or use excessive force (very little force is needed). Follow the outline for correct positioning. Use plastic tools if necessary.

### Step 7: Connect the three ribbon cables

#### Middle cable:

Open the ribbon connector.  
Insert the cable without closing the connector.

#### Outer cables:

While the middle connector is loosely attached, adjust and gently press down the two side connectors.

#### Middle cable (again):

Ensure the middle cable is properly inserted and close the lock.

### Step 8: Start the script from terminal or IDE

Enter the PCB ID by scanning the barcode or entering it manually. The script performs Resistance Tests and Current Leakage Tests. Results are saved automatically in the folder with the script.

### Step 9: Disconnect PCB

Wear antistatic gloves and have your ESD band on. Carefully detach the two outer ribbon cables. Open the middle latch and pull the PCB straight out (do not bend).

### Step 10: Store PCB

Place the PCB back in the antistatic bag and store it in the dry cabinet.

---

## Ready for the next test.
