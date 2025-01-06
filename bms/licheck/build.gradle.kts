plugins {
  id("java")
  kotlin("jvm") version "2.0.0"
}

repositories {
  mavenCentral()
}

dependencies {
  testImplementation(platform("org.junit:junit-bom:5.10.2"))
  testImplementation("org.junit.jupiter:junit-jupiter")
  testRuntimeOnly("org.junit.platform:junit-platform-launcher")
  testImplementation("org.jctools:jctools-core:3.1.0")
  testImplementation("com.googlecode.concurrent-trees:concurrent-trees:2.6.1")
  implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.5.0")
}

tasks.register<Copy>("copyDependencies") {
  from(configurations.testRuntimeClasspath)
  into("${layout.buildDirectory.get().asFile}/dependency")
}


