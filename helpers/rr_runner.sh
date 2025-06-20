#!/usr/bin/env bash
export PATH="/run/current-system/sw/bin:$PATH"

EXPLORE_MODE=0
if [ "$1" == "-e" ]; then
    EXPLORE_MODE=1
    shift
fi
TRACE_DIR="$1"
shift
TIMEOUT=${RR_TIMEOUT:-600}
COMMAND="$@"
ITERATION=1
EXIT_STATUS=0
START_TIME=$(date +%s%3N)
while [ $EXIT_STATUS -eq 0 ] || [ $EXPLORE_MODE -eq 1 ];  do

    echo "Starting iteration $ITERATION"
    rm -rf $TRACE_DIR
    EXIT_STATUS=0
    OUTPUT=$($COMMAND)
    if ! echo "$COMMAND" | grep -q "jacontebe"; then
        EXIT_STATUS=$?
    fi
    echo "$OUTPUT"
    break
    if echo "$OUTPUT" | grep -q "Deadlock detected"; then
        EXIT_STATUS=-1
    fi
    if echo "$OUTPUT" | grep -q "Finished test: Bug has been reproduced successfully."; then
        EXIT_STATUS=-1
    fi
    if echo "$OUTPUT" | grep -q "Program has been forced to exit from deadlock"; then
        EXIT_STATUS=-1
    fi
    if echo "$OUTPUT" | grep -q "Detected suspicious forever waiting bug"; then
        EXIT_STATUS=-1
    fi
    CURRENT_TIME=$(date +%s%3N)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))
    if [ $EXIT_STATUS -ne 0 ]; then
        echo "Error found at iter: $ITERATION, Elapsed time: $ELAPSED_TIME"
    fi
    if [ $ELAPSED_TIME -ge $((TIMEOUT * 1000)) ]; then
        echo "Timeout expired after $ELAPSED_TIME seconds"
        break
    fi
    ITERATION=$((ITERATION + 1))
done
exit $EXIT_STATUS
