function check_env()
{
    if [ ! ${experiment_root} ]
    then
        echo "experiment_root is unset in the shell"
        echo "please set experiment_root to point to your experiment directory"
        echo "see README for more information:"
        exit 2
    fi
    subject_dir=${experiment_root}/JaConTeBe
    cd ${subject_dir}
}

function run() 
{
    runtime_dependencies=./versions.alt/lib/${test_name}.jar:./source
    java ${Opt} -cp ${runtime_dependencies} ${class_to_run} $*>&1|tee  ${subject_dir}/outputs/${test_name}.log
}

check_env
