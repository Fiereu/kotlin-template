plugins {
    `kotlin-dsl`
}

repositories {
    mavenCentral()
    gradlePluginPortal()
}

dependencies {
    // Lets the convention plugins apply the Kotlin Gradle plugin.
    implementation(libs.kotlin.gradle.plugin)
    // Exposes the generated `libs` catalog accessors to the precompiled
    // convention plugins under src/main/kotlin.
    implementation(files(libs.javaClass.superclass.protectionDomain.codeSource.location))
}
