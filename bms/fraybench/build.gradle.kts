plugins {
    id("java")
    id("org.pastalab.fray.gradle") version "0.1.3"
}

group = "org.pastalab.fray.benchmark.fraybench"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
    maven {
        url = uri("https://maven.pkg.github.com/cmu-pasta/fray")
        credentials {
            username = extra["gpr.user"] as String? ?: System.getenv("USERNAME")
            password = extra["gpr.key"] as String? ?: System.getenv("TOKEN")
        }
    }
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
    dependsOn("frayTest")
}