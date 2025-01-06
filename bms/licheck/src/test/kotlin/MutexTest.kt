import MutexTest.t1
import MutexTest.t2
import kotlinx.coroutines.*
import kotlinx.coroutines.Dispatchers.Default
import kotlinx.coroutines.sync.Mutex

object MutexTest  {

  val mutex = Mutex()

  suspend fun t1() {
    mutex.lock()
    mutex.unlock()
  }

  suspend fun t2() {
    mutex.lock()
    mutex.lock()
  }
}

fun main() {
  CoroutineScope(Default).launch { t1() }
  CoroutineScope(Default).launch { t2() }
}
