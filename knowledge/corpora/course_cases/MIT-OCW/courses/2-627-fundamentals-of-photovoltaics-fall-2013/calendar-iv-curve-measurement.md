- Source: https://ocw.mit.edu/courses/2-627-fundamentals-of-photovoltaics-fall-2013/pages/calendar-readings/iv-curve-measurement/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Calendar & Readings IV Curve Measurement

We will be measuring the IV characteristics of a solar cell using a homemade Arduino-based USB-powered sourcemeter that connects to your personal laptop computer.

Documentation: [Build Your Own Sourcemeter](http://pv.mit.edu/home/education/resources-for-educators/build-your-own-sourcemeter/)

#### Installing Laptop Drivers

Before class, you should follow these instructions to install the proper driver in your laptop.

Go to the [Virtual COM Port Drivers](http://www.ftdichip.com/Drivers/VCP.htm) webpage (Future Technology Devices International, Ltd.)

Select the appropriate driver for your operating system. Download and save it somewhere you can find it again.

For Windows installation:

When you connect the board, Windows should initiate the driver installation process (if you haven’t used the computer with an Arduino board before).

The Add New Hardware wizard will open:

- When asked Can Windows connect to Windows Update to search for software? select No, not this time. Click Next.
- Select Install from a list or specified location (Advanced) and click Next.
- Make sure that Search for the best driver in these locations is checked; uncheck Search removable media; check Include this location in the search and browse to the drivers/FTDI USB Drivers directory of the Arduino distribution. (The latest version of the drivers can be found on the FTDI website.) Click next.
- The wizard will search for the driver and then tell you that a “USB Serial Converter” was found. Click finish.
- The new hardware wizard will appear again. Go through the same steps and select the same options and location to search. This time, a “USB Serial Port” will be found.
- You can check that the drivers have been installed by opening the Windows Device Mananger (in the Hardware tab of System control panel). Look for a “USB Serial Port” in the Ports section; that’s the Arduino board.

For Mac installation:

Double-click the ‘FTDIUSBSerialDriver mpkg’ icon and follow the instructions in the installer. You’ll need to restart your computer after installing the drivers.
