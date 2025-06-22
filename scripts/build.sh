SCRIPT_PATH=$(realpath "$0")
BASEDIR=$(dirname $SCRIPT_PATH)/..

echo $BASEDIR


cd $BASEDIR/tools/fray
if [ ! -d "result" ] || [ -z "$(ls -A result 2>/dev/null)" ]; then
    nix build
else
    echo "Skipping nix build - result folder exists and is not empty"
fi


cd $BASEDIR/tools/rr
rm -rf build
mkdir build
cd build
cmake -Ddisable32bit=ON -DCMAKE_BUILD_TYPE=Release  ../
make -j24

cd $BASEDIR/tools/jpf-core
export JAVA_HOME=$JDK11_HOME
./gradlew buildJars --no-daemon
export JAVA_HOME=$JDK21_HOME


cd $BASEDIR

python3 -m fray_benchmark build sctbench
python3 -m fray_benchmark build jacontebe
python3 -m fray_benchmark build lucene
python3 -m fray_benchmark build kafka
python3 -m fray_benchmark build guava
python3 -m fray_benchmark build lincheck 
