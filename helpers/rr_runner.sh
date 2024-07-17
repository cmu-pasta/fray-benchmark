#!/bin/bash

TRACE_DIR="$1"
shift
TIMEOUT=${RR_TIMEOUT:-600}
COMMAND="$@"
ITERATION=1
EXIT_STATUS=0
START_TIME=$(date +%s)
while [ $EXIT_STATUS -eq 0 ]; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

    if [ $ELAPSED_TIME -ge $TIMEOUT ]; then
        echo "Timeout expired after $ELAPSED_TIME seconds"
        break
    fi

    echo "Starting iteration $ITERATION"
    rm -rf $TRACE_DIR
    OUTPUT=$($COMMAND)
    EXIT_STATUS=$?
    echo "$OUTPUT"
    if echo "$OUTPUT" | grep -q "Deadlock detected"; then
        exit -1
    fi
    if echo "$OUTPUT" | grep -q "Program has been forced to exit from deadlock"; then
        exit -1
    fi
    ITERATION=$((ITERATION + 1))
done
exit $EXIT_STATUS
