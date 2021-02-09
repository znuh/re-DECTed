# SDR code

## hardware requirements
* needs a gnuradio-supported SDR with 2.4MS/s samplerate
* needs a tuner with support for the DECT frequency range
* rtlsdr with E4000 tuner works
* rtlsdr with more popular R820T tuner **does not work** (can't tune to DECT frequency range)
* tested with **bladeRF** and **rtlsdr w/ E4000 tuner**
* should work with **hackRF** as well

## software requirements
* needs GNUradio
* needs a dummy0 network device

# usage
* make
* create dummy0 interface: *sudo modprobe dummy* or *sudo ip link add dummy0 type dummy*
* start the dummy0 interface: *sudo ifconfig dummy0 up*
* run dectrcv as root: *sudo ./dectrcv*
* start the SDR part: 
    * If you use gnuradio version <= 3.7 : *./dectrx_37.py*
    * If you use gnuradio version >= 3.8 : *./dectrx_38.py*
* set channel, gain values and ppm
* enjoy the DECT packets in **wireshark**

# multichannel
If you want to use the multichannel feature you have to adjust the number of channels in the `dectrcv.c`.

# example
![screenshot](dectrx.png)
