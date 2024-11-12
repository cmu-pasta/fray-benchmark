package org.pastalab.fray.junit

import org.pastalab.fray.runtime.Delegate


class JunitRuntimeDelegate : Delegate() {
  override fun onThreadStart(t: Thread?) {
    Recorder.logThread()
  }
}
