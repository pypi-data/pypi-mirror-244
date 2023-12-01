set -x
# source activate PyTorch-1.8
# bash exp/tests/setup_env.sh

bucket=${1:-bucket-3690}


pip install tl2

# install pytorch
cache_dir=/cache/pypi/torch1120_cu102_py37
python -m tl2.modelarts.scripts.copy_tool \
  -s s3://$bucket/ZhouPeng/pypi/torch1120_cu102_py37 -d $cache_dir -t copytree

if [ -d "${cache_dir}" ]
then
    for filename in $cache_dir/*.whl; do
    pip install $filename

#   for pyrender
    sudo sed -i "s@http://.*archive.ubuntu.com@http://10.155.96.21:8081@g" /etc/apt/sources.list
    sudo sed -i "s@http://.*security.ubuntu.com@http://10.155.96.21:8081@g" /etc/apt/sources.list
    sudo apt-get update
    sudo apt install -y libosmesa6-dev freeglut3-dev xauth

done
else
    echo "Directory ${cache_dir} does not exists."
#    pip3 install torch==1.11.0 torchvision==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu113
fi
# end install pytorch

#pip install --verbose -e knn_cuda_lib/
#pip install --verbose -e PyMAF-exp/
#pip install --verbose -e eg3d-exp/

# order matters
pip install -r requirements.txt
pip install -I pyrender==0.1.45
pip install -I pyopengl==3.1.6
pip install -I pyglet==2.0b1


if [ -d "tl2_lib" ]
then
    pip uninstall -y tl2
fi





