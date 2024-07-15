TRACE_DIR="$1"
shift
COMMAND="$@"
ITERATION=1
EXIT_STATUS=0
while [ $EXIT_STATUS -eq 0 ]; do
  echo "Starting iteration $ITERATION"
  rm -rf $TRACE_DIR
  $COMMAND
  EXIT_STATUS=$?
  ITERATION=$((ITERATION + 1))
done
EXIT_STATUS=$?
echo $EXIT_STATUS
exit $EXIT_STATUS