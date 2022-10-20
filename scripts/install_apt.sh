pushd /tmp
apt-get download python3-apt
dpkg -x python3-apt_1.6.5ubuntu0.7_arm64.deb python3-apt
popd

cp -r /tmp/python3-apt/usr/lib/python3/dist-packages/* $1/lib/python3.6/site-packages/

pushd $1/lib/python3.6/site-packages/
mv apt_pkg.cpython-36m-aarch64-linux-gnu.so apt_pkg.so
mv apt_inst.cpython-36m-aarch64-linux-gnu.so apt_inst.so
popd