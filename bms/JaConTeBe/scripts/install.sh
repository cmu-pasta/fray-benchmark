#!/bin/bash

echo $(javac -version)

if test $# -ne 2
    then \
        echo Usage:
        echo install.sh comp_dir target_bug
        echo comp_dir: orig
        echo "target_bug: Bug directory's name"
        exit 0
fi

subject_dir=$(realpath $(dirname $0))/..
target=$2
echo removing old files
rm -f -r ${subject_dir}/build/*
rm -f ${subject_dir}/outputs/*

if test $1 = "orig"
then
     echo copying files for orig version
     mkdir -p ${subject_dir}/build/$target
     cp -a ${subject_dir}/versions.alt/$target/orig/* ${subject_dir}/build/$target
else
    echo orig is the only option currently available
    exit 0
fi
cd ${subject_dir}/build/$target

echo compiling application
echo ${subject_dir}

find . -name "*.java" | xargs javac -cp ${subject_dir}/versions.alt/lib/$target.jar

