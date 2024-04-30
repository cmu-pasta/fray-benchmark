#!/bin/bash
RANDOM_RUNS=1 #number of random search; default is 1
TIMELIMIT=1 #let the clock tick to ensure each random search is unique

USAGE="Usage: $0 target_test  search_type [number_of_runs] [-v]\ntarget_test: test name\rsearch_type: default/random\
    \nnumber_of_runs (optional): number of times JPF is invoked \n-v (optional): flag to print JPF's detail messages"

if [ "`echo "\t"`" == "\\t" ]
then
    ECHOE="echo -e"
else
    ECHOE="echo"
fi

if [ ! ${jpf_root} ]
then
    echo "jpf_root is unset in the shell"
    echo "please set jpf_root to point to your JPF installation"
    echo "see README for more information:"
    exit 2
fi

if [ ! ${experiment_root} ]
then
    echo "experiment_root is unset in the shell"
    echo "please set experiment_root to point to your experiment directory"
    echo "see README for more information:"
    exit 2
fi

if test $# -lt 2
then
    $ECHOE $USAGE
    exit 0
fi

if test $# -eq 3
then
    if test $3 = "-v"
    then
        flag=" -log -show"
    else
        case ${3} in
            *[!0-9]* )
                echo "number of JPF runs is non-numeric" >&2
                $ECHOE $USAGE >&2
                exit 5
                ;;
        esac
    RANDOM_RUNS=$3
	fi
fi

if test $# -eq 4
then
    if test $4 = "-v"
    then
        flag=" -log -show"
    else
        echo "-v is expected. Program will run without showing JPF detail information."
    fi
fi
    
subject_dir=${experiment_root}/JaConTeBe/
cd ${subject_dir}

if test $2 = "default"
then
    echo Invoking JPF
    ${jpf_root}/bin/jpf testplans.alt/jpfscripts/$1.jpf ${flag}>&1 | tee outputs/$1.log
else 
    if test $2 = "random" 
    then
        echo Invoking JPF
         #if using expect to limit the amount of time spent on a search
         #set the TIMEOUT value below to the number of seconds
         #the search should run and uncomment
        TIMEOUT=3600
        X=0 #loop counter
        Z=$RANDOM_RUNS #number of runs per test case
        while [ $X -lt $Z ]
        do
            seed=$RANDOM
            echo "Seed: $seed"
              #Example of how to run JPF using expect to limit search time
              #run JPF using expect - uncomment next four lines
              #expect -c "set timeout $TIMEOUT; set log_file ${subject_dir}/outputs/accountJPF${seed}.log; spawn \
              #${jpf_root}/bin/jpf +classpath=${subject_dir}/source \
              #+cg.randomize_choices=path +cg.seed=${seed} \
              #Main 1 1 12 2>&1 |; log_file ${subject_dir}/outputs/accountJPF${seed}.log; expect; log_file" \
              #run JPF without expect
              #comment out the following 4 lines if using expect above
            ${jpf_root}/bin/jpf testplans.alt/jpfscripts/$1.jpf\
                +randomize_choices=1 +cg.seed=$seed ${flag}\
                >&1 | \
                tee outputs/$1$seed.log 
            X=$((X+1))
              #Random run requires a clock tick to make sure a new random
              #number is generated
        sleep $TIMELIMIT
        done
    fi
fi
