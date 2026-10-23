- Source: https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/pages/related-resources/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Related Resources

The resources provided below are useful references for those interested in learning more about the topics covered in the course.

### UNIX®

- Ritchie, Dennis M., and Ken L.Thompson. “[The UNIX® Time-Sharing System](https://dl.acm.org/doi/abs/10.1145/361011.361061).” *Bell System Technical Journal* 57, no. 6 part 2 (1974): 1905–30. You read this paper in 6.033.
- Ritchie, Dennis M. “[The Evolution of the Unix® Time-sharing System](http://dx.doi.org/10.1002/j.1538-7305.1984.tb00054.x).” 1984.
- Kernighan, Brian, and Dennis Ritchie. *The C Programming Language*. 2nd ed. Prentice Hall, 1988. ISBN: 9780131103627.

### x86 Emulation

- [QEMU](http://www.qemu.org/)—A fast and popular x86 platform and CPU emulator.
  - [User Manual](http://wiki.qemu.org/Qemu-doc.html)
- [Bochs](http://bochs.sourceforge.net/)—A more mature, but quirkier and much slower x86 emulator. Bochs is generally a more faithful emulator of real hardware than QEMU.
  - [User Manual](http://bochs.sourceforge.net/doc/docbook/user/index.html)
  - [Debugger Reference](http://bochs.sourceforge.net/doc/docbook/user/internal-debugger.html)

### x86 Assembly Language

- [*PC Assembly Language*](http://www.drpaulcarter.com/pcasm/), Paul A. Carter, July 2006.
- [*Intel® 80386 Programmer’s Reference Manual*](http://www.logix.cz/michal/doc/i386/), 1987 (HTML®). Much shorter than the full current Intel® Architecture manuals below, but describes all processor features used in 6.828.
- [*IA-32 Intel® Architecture Software Developer’s Manuals*](http://www.intel.com/content/www/us/en/processors/architectures-software-developer-manuals.html), Intel®, 2007. Download the following manuals:
  - Volume I: Basic Architecture
  - Volume 2A: Instruction Set Reference, A–M
  - Volume 2B: Instruction Set Reference, N–Z
  - Volume 3: System Programming Guide
- Multiprocessor References:
  - [MP specification](http://www.intel.com/design/archives/processors/pro/docs/242016.htm)
  - [IO APIC](http://www.intel.com/design/chipsets/specupdt/290710.htm)
- [AMD64 Architecture Programmer’s Manual](https://refspecs.linuxfoundation.org/LSB_3.1.0/LSB-Core-AMD64/LSB-Core-AMD64/normativerefs.html). Covers both the “classic” 32-bit x86 architecture and the new 64-bit extensions supported by the latest AMD and Intel® processors.
- Writing Inline Assembly Language with GCC:
  - [Brennan’s Guide to Inline Assembly](http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html), Brennan “Mr. Wacko” Underwood
  - [Inline assembly for x86 in Linux®](http://www.cristal.univ-lille.fr/~marquet/ens/ctx/doc/l-ia.html), Bharata B. Rao, IBM®
  - [GCC-Inline-Assembly-HOWTO](http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html), Sandeep. S
- Loading x86 Executables in the ELF Format:
  - Tool Interface Standard (TIS) Executable and Linking Format (ELF). The definitive standard for the ELF format.

### PC Hardware Programming

- General PC Architecture Information:
  - [Phil Storrs PC Hardware book](http://web.archive.org/web/20040603021346/http:/members.iweb.net.au/~pstorr/pcbook/), Phil Storrs, December 1998.
  - [Bochs technical hardware specifications directory](http://bochs.sourceforge.net/techdata.html).
- General BIOS and PC Bootstrap:
  - [BIOS Central](http://www.bioscentral.com/)
  - [BIOS Services and Software Interrupts](http://www.pcguide.com/ref/mbsys/bios/funcServices-c.html), Roger Morgan, 1997.
  - [“El Torito” Bootable CD-ROM Format Specification](http://support.microsoft.com/kb/167685), Phoenix / IBM®, January 1995.
- VGA Display - kern / console.c
  - [VESA BIOS Extension (VBE) 3.0 (PDF)](http://www.cs.utexas.edu/~dahlin/Classes/UGOS/reading/vbe3.pdf), [Video Electronics Standards Association](http://www.vesa.org/), September 1998.
  - [VGADOC](http://read.seas.harvard.edu/cs261/2011/references.html), Finn Thøgersen, 2000.
  - [Free VGA Project](http://www.osdever.net/FreeVGA/home.htm), J. D. Neal, 1998.
- Keyboard and Mouse - kern / console.c
  - [Adam Chapweske’s Resources](http://www.computer-engineering.org/index.html)
- 8253/8254 Programmable Interval Timer (PIT) - inc / timerreg.h
  - [82C54 CHMOS Programmable Interval Timer](http://www.intel.com/design/archives/periphrl/docs/23124406.htm), Intel®, October 1994.
  - Data Solutions 8253/8254 Tutorial, Data Solutions.
- 8259/8259A Programmable Interrupt Controller (PIC) - kern / picirq.*
  - [8259A Programmable Interrupt Controller](http://bochs.sourceforge.net/techdata.html), Intel®, December 1988.
- Real-Time Clock (RTC) - kern / kclock.*
  - [Phil Storrs PC Hardware book](http://web.archive.org/web/20040603021346/http:/members.iweb.net.au/~pstorr/pcbook/), Phil Storrs, December 1998. In particular:
    - [Understanding the CMOS](http://web.archive.org/web/20040603150111/members.iweb.net.au/~pstorr/pcbook/book5/cmos.htm)
    - [A list of what is in the CMOS](http://web.archive.org/web/20040603005903/members.iweb.net.au/~pstorr/pcbook/book5/cmoslist.htm)
  - CMOS Memory Map, Padgett Peterson, May 1996. ([TXT](http://bochs.sourceforge.net/techspec/CMOS-reference.txt))
  - [M48T86 PC Real-Time Clock](http://www.alldatasheet.com/datasheet-pdf/pdf/22981/STMICROELECTRONICS/M48T86.html), ST Microelectronics, April 2004.
- 16550 UART Serial Port - kern / console.c
  - PC16550D Universal Asynchronous Receiver / Transmitter with FIFOs, National Semiconductor, 1995.
  - [Technical Data on 16550](http://byterunner.com/16550.html), Byterunner Technologies.
  - [Interfacing the Serial / RS232 Port](http://users.utcluj.ro/~baruch/sie/labor/RS232/serial.pdf), Craig Peacock, August 2001.
- IEEE 1284 Parallel Port - kern / console.c
  - [Parallel Port Central](http://janaxelson.com/parport.htm), Jan Axelson.
  - [IEEE 1284 - Updating the PC Parallel Port](http://zone.ni.com/devzone/cda/tut/p/id/3466), National Instruments.
  - [Interfacing the Standard Parallel Port](http://pascal.hansotten.com/uploads/electronics/parallel.pdf), Craig Peacock, August 2001.
- IDE Hard Drive Controller - fs / ide.c
  - AT Attachment with Packet Interface - 6 (working draft), ANSI, December 2001.
  - Programming Interface for Bus Master IDE Controller, Brad Hosler, Intel®, May 1994.
  - [The Guide to ATA / ATAPI documentation](http://www.cs.utexas.edu/~dahlin/Classes/UGOS/reading/ide.html), Constantine Sapuntzakis, January 2002.
- Sound Cards (not supported in 6.828 kernel, but you’re welcome to do it as a challenge problem!)
  - Signal Processing using Sound Cards
  - [Sound Blaster Series Hardware Programming Guide (PDF)](http://pdos.csail.mit.edu/6.828/2008/readings/hardware/SoundBlaster.pdf), Creative Technology, 1996.
  - 8237A High Performance Programmable DMA Controller, Intel®, September 1993.
  - [Sound Blaster 16 Programming Document](http://homepages.cae.wisc.edu/~brodskye/sb16doc/sb16doc.html), Ethan Brodsky, June 1997.
- E100 Network Interface Card
  - Intel 8255x 10 / 100 Mbps Ethernet Controller Family Open Source Software Developer Manual
  - 82559ER Fast Ethernet PCI Controller Datasheet
- E1000 Network Interface Card
  - PCI / PCI-X Family of Gigabit Ethernet Controllers Software Developer’s Manual
