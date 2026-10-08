> 检索摘要：16.682 Prototyping Avionics（Spring 2006，Undergraduate）的「Projects」。页内标题：Projects；Project Description；Deliverables；Example Projects；Proposal。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/16-682-prototyping-avionics-spring-2006/pages/projects/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Projects

### Project Description

The final project will put to work a majority of the concepts and tools you have learned in the class. The project can be individual or in teams of two people.

The final project involves:

1. Design of a circuit using the theory tools from the first part of class
2. Capture of the schematic of the circuit
3. Layout of a 2-layer PCB for the circuit
4. Assembly of the PCB
5. Testing
6. Documenting the operation of the circuit and your experiences

The electronic circuit must feature as a minimum:

- Digital control devices (digital logic gates, microcontrollers, FPGA’s, etc)
- At least one analog circuit for input or output (op-amps, transistors, filters)
- Power regulation. The power input can be selected from:
  - Batteries (preferred)
  - An AC transformer - you cannot work on the 120Vac part, only the low voltage part
  - An unregulated DC transformer and/or power supply

The design must be simple and adhere to the following limits:

- A maximum of 30 parts/components (excluding bypass capacitors and pull-up/down resistors)
- No components of more than 30 pins
- No “ball grid array” (BGA) components
- A maximum of 3 operating voltages

While there is no obvious/deterministic method to figure out exactly how complex the board will be, note that all project PCB’s will be limited to:

- 2 layers (top and bottom)
- Round holes
- “Normal” shapes

### Deliverables

The following must be delivered for the project:

1. Schematic
  - Schematic - a full schematic of the project
  - Bill of materials - the list of all components, including package and ordering information
2. Layout
  - Layout file - the CAD file with the circuit board layout
  - Layout plots - 1:1 printouts of individual layers and combined board
  - Manufacturing files - the files which will be used to manufacture the PCB
3. Documentation
  - Circuit documentation - a document which is effectively a “data sheet” for your circuit (more details on documentation will be provided later)
  - Experience documentation - a document which describes your experience in designing, building, and testing the circuit
4. Circuit
  - If your layout files are ready in time for manufacturing, you will turn in your actual PCB (which you can keep later) for evaluation (assembly and operation); otherwise you will turn in another previously designed circuit

### Example Projects

- Motion Control
  - Closed loop control of multiple motors
    - For multi-DOF robot arms
    - To drive 4+ wheels
- Sensing
  - Force feedback sensor
  - Electronic “wall”
- Communications
  - Digital wireless system integration

### Proposal

The proposal in Week #8 should include:

1. A description of the project in words, stating what your system is going to do and how you plan to implement it
2. A block diagram of the circuit design (black box design without full detail)
3. A set of specifications that define in detail:
  - Inputs and outputs (whether electrical or physical)
  - What tests will be used to prove that it functions properly

The proposal should be typewritten.
