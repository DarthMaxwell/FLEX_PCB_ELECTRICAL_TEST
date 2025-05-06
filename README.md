# FLEX_PCB_ELECTRICAL_TEST
2025 Bachelor's project at HVL with the ATLAS group in UIB, in coordination with UIO.  
This repository is dedicated to the electrical testing part of the quality control testing for the FLEX PCBs.  

## OPERATION

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
