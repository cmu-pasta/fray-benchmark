#!/bin/bash

jenv local 11
echo $(javac -version)
if [ ! ${experiment_root} ]
then
    echo "experiment_root is unset in the shell"
    echo "please set experiment_root to point to your experiment directory"
    echo "see README for more information:"
    exit 2
fi

if test $# -ne 2
    then \
        echo Usage:
        echo install.sh comp_dir target_bug
        echo comp_dir: orig
        echo "target_bug: Bug directory's name"
        exit 0
fi

subject_dir=${experiment_root}/JaConTeBe
echo removing old files
rm -f -r ${subject_dir}/source/*
rm -f ${subject_dir}/outputs/*

if test $1 = "orig"
then
     echo copying files for orig version
     cp -a ${subject_dir}/versions.alt/$2/orig/* ${subject_dir}/source 
else
    echo orig is the only option currently available
    exit 0
fi
cd ${subject_dir}/source

echo compiling application

find . -name "*.java" | xargs javac -cp ${subject_dir}/versions.alt/lib/$2.jar

