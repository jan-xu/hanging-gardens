# Hanging Gardens

Repository for CE186 project: Babylon - Hanging Gardens

**Hanging Gardens** is a design project that seeks to design, prototype and test a smart indoors hydroponics system. This was done for the *CE 186 Design of Cyber-Physical Systems* at University of California, Berkeley in Fall Term 2018, supervised by Professor Scott Moura. The project focuses on the following topics:

1. The prototyping of a smart hydroponics system, with associated hardware, cyber layer and web visualization;
2. The aim of outperforming conventional agriculture using our intended system by optimizing its water usage and energy requirements, given its upscaling;
3. The aim of outperforming other hydroponic systems using our intended system by optimizing its energy requirements and simple operation, given its upscaling.

For more contextual information, refer to the ```Final Report.pdf``` located in the *Report* folder.

![alt text](https://raw.githubusercontent.com/jan-xu/hanging-gardens/master/png/hanginggardens.png "Final design")

### Contents
This repository includes the .py-files of the employed system architecture and the source code for the microcontroller (Arduino). A brief technical description of the constituents of the program is followed below:

```Microcontroller/Microcontroller.ino```: This sketch, written in C, is the first point of contact for received data from sensors and last sender of actuation commands. It attributes the data from each sensor with a predefined tag (-1 for left photoresistor, -2 for right photoresistor etc.), and sends that tag together with the data point to the web application through the serial monitor. The microcontroller also fully controls the flushing procedure, ensuring robustness whilst the hydroponic system is changing water, preventing any communication mishaps such as failing to turn off the pump, for instance.

```Python/WebApp.py```: Sets up and runs the main Python-based web application that reads and sends data to and from the Arduino. It interacts indirectly with the local server through the user-defined ServerRequests module, and with the Arduino through a serial port set up with the Arduino.

```Python/ServerRequests.py```: A Python module that solely contains functions that carry out HTML/JSON request commands, such as GET, PUT and POST, with the web server.

```Python/wallflower_pico_server.py```: Web server hosted by the microframework Flask. It sets up a local web interface through the usage of supplementary HTML code, supported by CSS and JavaScript code rendering the web visualization dynamic and user-friendly. It also handles the data storage in an SQLite database, where both raw and processed data is collected.

```Python/DataAnalysis.py```: A Python module that contains functions for data processing and interpretation of raw data into actuator settings. It is served by the ServerRequests module and called on by the web application.

A diagram of how every module is related to one another is seen below.

![alt text](https://raw.githubusercontent.com/jan-xu/hanging-gardens/master/png/connectivitydiagram.png "System Architecture")
