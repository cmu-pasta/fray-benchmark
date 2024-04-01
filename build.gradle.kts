plugins {
    id("java")
}

group = "cmu.pasta.sfuzz.benchmark"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.register<JavaExec>("run") {
    val sfuzz = "/Users/aoli/repos/sfuzz"
    val agentPath = if (System.getProperty("os.name").lowercase().contains("mac")) {
        "${sfuzz}/jvmti/build/cmake/native_release/mac-aarch64/cpp/libjvmti.dylib"
    } else {
        "${sfuzz}/jvmti/build/cmake/native_release/linux-amd64/cpp/libjvmti.so"
    }
    val core = "$sfuzz/core/build/libs/core-1.0-SNAPSHOT-all.jar"
    val instrumentation = "$sfuzz/instrumentation/build/libs/instrumentation-1.0-SNAPSHOT-all.jar"
    val testName = properties["testName"] as String? ?: "AccountBad"
    mainClass.set("cmu.pasta.sfuzz.core.MainKt")
    classpath = files(core, instrumentation) + sourceSets["main"].runtimeClasspath
    args = listOf("cmu.pasta.sfuzz.benchmark.sctbench.cs.$testName", "main", "-o",
        "${layout.buildDirectory.get().asFile}/report", "--scheduler",
        "random", "--logger", "csv", "--iter", "1000")
    jvmArgs("-agentpath:$agentPath")
    jvmArgs("-javaagent:$instrumentation")
    jvmArgs("-ea")
}
