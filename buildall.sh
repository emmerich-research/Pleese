cd jetson-inference
mkdir build && cd build
sudo cmake ..
sudo make install
sudo ldconfig
cd .. && cd python/training/detection/ssd
pip3 installi -r requirements.txt
cd ../../../../..
