cd jetson-inference
mkdir build && cd build
sudo cmake ..
sudo make install
sudo ldconfig
cd .. && cd python/training/detection/ssd
wget https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth -O models/mobilenet-v1-ssd-mp-0_675.pth
pip3 installi -r requirements.txt
cd ../../../../..
