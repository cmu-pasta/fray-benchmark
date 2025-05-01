import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
plugins {
  kotlin("jvm") version "2.0.0"
  id("io.github.goooler.shadow") version "8.1.7"
}

repositories {
  mavenCentral()
  mavenLocal()
}

dependencies {
  implementation("org.junit.platform:junit-platform-console-standalone:1.11.3")
  api("org.ow2.asm:asm:9.7")
  api("org.ow2.asm:asm-tree:9.7")
  api("org.ow2.asm:asm-commons:9.7")
  api("org.ow2.asm:asm-util:9.7")
  compileOnly("org.pastalab.fray:fray-runtime:0.4.3")
}

kotlin {
  jvmToolchain(21)
}

tasks.named<ShadowJar>("shadowJar") {
  // In Kotlin DSL, setting properties is done through Kotlin property syntax.
//    isEnableRelocation = true
  relocate("org.objectweb.asm", "cmu.pasta.fray.instrumentation.asm")
  manifest {
    attributes(mapOf("Premain-Class" to "org.pastalab.fray.junit.RecorderKt"))
  }
}