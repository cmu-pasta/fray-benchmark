BASEDIR=$(dirname $0)

cd $BASEDIR/tools/rr
mkdir build
cd build
cmake -Ddisable32bit=ON -DCMAKE_BUILD_TYPE=Release  ../
make -j24

