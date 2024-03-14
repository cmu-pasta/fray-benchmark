SYSTEM_PROMPT_TEMPLATE = """
You are a world class programmer who can transpile C to Java programs.
"""

TRANSPILE_PROMPT_TEMPLATE = """
Here is a C file named {file_name} that uses multithreading:
```C
{program}
```
Task:
Translate this file to Java with the class name {class_name} and package name `example`. Try to keep all identifiers consistent with the original file, and make sure the logic is the same. Use the same 
concurrency primitives as the original program. For example, if there is a `pthread_cond_signal`, use the Java `java.util.concurrent.Condition.signal`. Do not use any
executor services in Java. Remember certain Java specific rules hold, e.g. you cannot call Object.wait without holding the monitor for the object. 

Try to follow the `Thread1 implements Runnable` style of defining the logic for each thread when transpiling.

At the top of the Java file, add a comment that says the following:
Translated from: https://github.com/mc-imperial/sctbench/blob/d59ab26ddaedcd575ffb6a1f5e9711f7d6d2d9f2/benchmarks/concurrent-software-benchmarks/{file_name}

Use the following output format:
```java
package cmu.pasta.sfuzz.benchmark.sctbench;

public class {class_name}
  // Transpiled code 
```
"""