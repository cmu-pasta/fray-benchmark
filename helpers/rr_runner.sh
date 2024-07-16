TIMEOUT="$1"
TRACE_DIR="$2"
shift
shift
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
    $COMMAND
    EXIT_STATUS=$?
    ITERATION=$((ITERATION + 1))
done
EXIT_STATUS=$?
echo $EXIT_STATUS
exit $EXIT_STATUS