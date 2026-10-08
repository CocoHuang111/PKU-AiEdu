> 检索摘要：6.334 Power Electronics（Spring 2007，Graduate）的「Related Resources」。页内标题：Related Resources；PSPICE Simulation Information；(Almost) Ideal Diode Model；PSIM Power Electronics Simulator；More Free Resources。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/pages/related-resources/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Related Resources

### PSPICE Simulation Information

Download the Microsim (now known as Orcad) DesignLab Release 8 Evaluation version, containing both Schematics and PSpice for PCs. A more up-to-date version can be downloaded from [OrCAD](http://www.orcad.com/).

[Spice tutorial](http://homepage.seas.upenn.edu/~jan/spice/spice.overview.html) (courtesy of University of Pennsylvania Department of Electrical Engineering). In particular, see [How to Get Started with PSpice](http://homepage.seas.upenn.edu/~jan/spice/spice.guide.html).

#### (Almost) Ideal Diode Model

idealdiode.lib ([LIB](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/idealdiode/)) – If you’re creating your circuit with the “Schematics” tool, incorporate this library into “Schematics” as follows: Select Analysis -> Library and Include Files. Type the filename idealdiode.lib in the filename box (including the path to the file), and click Add Library. If you’re creating your circuit using a standard textfile netlist, add the following lines to your file:

`X1 (node 1) (node 2) diode_ideal`
`.lib idealdiode.lib`

idealdiode.slb ([SLB](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/idealdiode-1/)) – If you’re creating your circuit with the “Schematics” tool, incorporate this *symbol* library into “Schematics” as follows: Select Options -> Editor Configuration. Select the Library Settings button, and then add the file idealdiode.slb. If you’re creating your circuit using a standard textfile netlist, you do NOT need this file.

Half-wave rectifier with freewheeling diode and Commutating Inductance ([CIR](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/halfwave/))

Full-wave rectifier with Commutating Inductance and Current Source Load ([CIR](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/fullwave/))

Full-wave rectifier with RL Load ([CIR](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/rl_load/))

Another SPICE simulator that may be used is LTSPICE/SwitcherCAD III, developed by Linear Technology.

### PSIM Power Electronics Simulator

Try out the PSIM power electronics simulator for free! A demo version is available from [POWERSIM](http://www.powersimtech.com/).

### More Free Resources

The Power Supply Manufacturer database is dedicated to designers of Switch Mode Power Supplies, and features:

- How to design a Switch Mode Power Supply, including software tools and examples.
- How to simulate a power supply. See PSpice simulation waveforms on their SMPS Simulation page.
- Lists of companies manufacturing power supplies.
- Information regarding SMPS components and component suppliers.
- Various technical articles.
