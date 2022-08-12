# Pleese  
**Pl**astic R**e**use R**e**minder **S**yst**e**m via Deep Learning Computer Vision


Clone it recursively to download our datasets and trained models in your Jetson mini-computer

`git clone --recursive https://github.com/emmerich-research/Pleese.git`


Next we need to setup all the dependencies with this command
```
chmod +x buildall.sh run.sh
./buildall.sh
```
you need to enter your Jetson password for sudo access

run the detection program it with 
```
./run.sh
```
or
```
sudo python3 plastic-detection.py
```
make sure your camera is available by running this command
```
ls /dev/video0
```
is a normal thing if it takes longer time at the first run.
