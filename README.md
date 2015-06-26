# LUMA
LED User Manipulated Apparatus
------------------------------
LUMA at its core is a fancy area lighting system, with some LEDs at one end and a web interface at the other, and
a robust lighting protocol in the middle.

Features
--------
* **Simple extensability:** Want another completely independent light fixture? Just add a new strip to an existing 
LUMA client (Up to 5 fixtures per client), or an entirely new client.
* **Robust lighting definition:** Describe lighting color patterns as waveforms of brightness over time.
* **Easy-to-use interface:** Search for a light, and draw some waves.
* **For public and private use:** Permission to view/edit lights is whitelisted. If you want to have a client
for your room while your favorite dorm organization wants to string up some lights in the hall, you can
rest easy knowing that permission to control your room is not as widespread as that of the hall.
* **RESTful API:** Interactions with the server are done with via a simple RESTful API. Write an app, control
your lights from a toilet or committee meeting. Or get creative!

Structure
---------
LUMA consists of three easily configured main components:
* Client
* Server
* Interface

Let's start with the client. Each client is a Raspberry Pi (The client code can be easily ported to your tiny 
computer of choice) with an attached PWM module. The PWM modules have 16 pins, and with one pin per color channel
and three channels per light, we can attach up to five lighting fixtures per client.

The server is a simple Flask machine that listens to requests and updates with a RESTful API. It also serves the
web interface as a matter of convienience.

The web interface is a Angular.JS application. It uses canvases to allow users to draw brightness waveforms.
Not much more to be said.

