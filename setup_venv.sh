#!/bin/bash
echo "THIS SCRIPT IS SUPPOSED TO WORK ON THE LAMBDA SERVERS ONLY."
echo "Use it anywhere else at your own risk!"

srun --gres=gpu:1 --pty /bin/bash
echo "finished srun"

export PATH="/home/orenge3/miniconda3/bin:$PATH"
conda create -n tf1 python=3.7
source ~/miniconda3/etc/profile.d/conda.sh
echo "finished create"
conda activate tf1
echo "finished activate"
pip install tensorflow-gpu==1.15
echo "finished install "
mkdir ~/symlinks
echo "finished mkdir"
ln -s /usr/local/cuda/lib64/libcudart.so.10.2 ~/symlinks/libcudart.so.10.0
ln -s /usr/lib/x86_64-linux-gnu/libcublas.so.10 ~/symlinks/libcublas.so.10.0
ln -s /usr/local/cuda/lib64/libcufft.so.10 ~/symlinks/libcufft.so.10.0
ln -s /usr/local/cuda/lib64/libcurand.so.10 ~/symlinks/libcurand.so.10.0
ln -s /usr/local/cuda/lib64/libcusolver.so.10 ~/symlinks/libcusolver.so.10.0
ln -s /usr/local/cuda/lib64/libcusparse.so.10 ~/symlinks/libcusparse.so.10.0

echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:~/symlinks/" > ~/.bashrc
source ~/.bashrc

pip install -r requirements.txt