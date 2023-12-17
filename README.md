"# CS495_SoundControlledLighting" 

Helpful links:

###EXPENSIVE MICROPHONE###
https://www.amazon.com/Microphone-Gooseneck-Universal-Compatible-CGS-M1/dp/B08M37224H/ref=sr_1_11?keywords=usb+microphone+raspberry+pi&qid=1674491726&sr=8-11

###BREADBOARDS###
https://www.amazon.com/risingsaplings-Breadboard-Solderless-Universal-Contacts/dp/B08WX51DQ9/ref=sr_1_15?keywords=Raspberry%2BPi%2BBreadboard&qid=1674492026&sr=8-15&th=1

###CHEAPER MICROPHONE###
https://www.amazon.com/SunFounder-Microphone-Raspberry-Recognition-Software/dp/B01KLRBHGM/ref=sr_1_3?keywords=usb+microphone+raspberry+pi&qid=1674491726&sr=8-3

###3D PRINTER SOFTWARE###
https://www.makerbot.com/3d-printers/cloudprint/

###TURNING A PI INTO A KEYBOARD###
https://mtlynch.io/key-mime-pi/

###ETC ELEMENT 2 LIGHTBOARD MANUAL###
https://www.etcconnect.com/WorkArea/DownloadAsset.aspx?id=10737502836

###USB EXTENSION CORD###
https://www.amazon.com/BlueRigger-Female-Active-Extension-Repeater/dp/B005LJKEXS/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=Ogg0E&content-id=amzn1.sym.1bcf206d-941a-4dd9-9560-bdaa3c824953&pf_rd_p=1bcf206d-941a-4dd9-9560-bdaa3c824953&pf_rd_r=8GF75C332TJ2PJ7N38QV&pd_rd_wg=L5jM8&pd_rd_r=29f0fd36-06d3-4c96-8533-c857726b2507&pd_rd_i=B005LJKEXS

###MCP3008 CHIP###
https://www.amazon.com/gp/product/B00NAY3RB2/ref=ox_sc_act_title_1?smid=AM0JQO74J587C&psc=1

###POTENTIOMETER CIRCUIT###
https://projects.raspberrypi.org/en/projects/physical-computing/13




_________________________________________________________________________________________________________________________________________________________




Brief description:

This project is used to accept 4 microphone inputs and turn on and off lights connected to an ETC Element 2 lightboard based on the decibel level  of the mics compared to a decibel threshold either set by a potentiometer manually, or through machine learning. The program uses the USB-C port to send out keyboard inputs to control the ETC Element 2. To activate machine learning, turn potentiometer all the way to the left.

Packages used:
  
  numpy: 
  
      pip install numpy
  
  pyaudio: 
  
      sudo apt-get install portaudio19-dev && pip install pyaudio
  
  spidev: 
  
      sudo apt-get install spidev

***BEFORE RUNNING***

Enable SPI by going to Raspberry Pi configuration, then interfaces, and enabling the SPI switch seen in this image:

![image](https://user-images.githubusercontent.com/98055163/231603554-bace0d26-9717-41e5-b7ee-f2aa633e769a.png)


TO RUN:

***ONE TIME SETUP***

    cp script.sh ~/script.sh
    cd key-mime-pi
    sudo ./enable_usb_hid
    sudo reboot

***RUN EVERY TIME***

Within ~/Documents/CS495_SoundControlledLighting/:

    ~./script.sh
    python3 2MicsSprint2.py

Congrats! The program is now running!
