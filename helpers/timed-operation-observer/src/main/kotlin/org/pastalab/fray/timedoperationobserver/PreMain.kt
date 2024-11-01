package org.pastalab.fray.timedoperationobserver

import org.pastalab.fray.runtime.Runtime
import java.lang.instrument.Instrumentation

fun premain(arguments: String, instrumentation: Instrumentation) {
    val observer = Observer(arguments)
    Runtime.DELEGATE = observer
    observer.registeredThread.add(Thread.currentThread())
}
