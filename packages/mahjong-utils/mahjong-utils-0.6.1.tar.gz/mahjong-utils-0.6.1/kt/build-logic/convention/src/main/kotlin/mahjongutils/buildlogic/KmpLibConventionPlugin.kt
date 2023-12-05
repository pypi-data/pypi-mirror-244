package mahjongutils.buildlogic

import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar
import org.gradle.api.GradleException
import org.gradle.api.JavaVersion
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.api.plugins.JavaApplication
import org.gradle.kotlin.dsl.*
import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension
import org.jetbrains.kotlin.gradle.targets.jvm.KotlinJvmTarget
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

class KmpLibConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        with(pluginManager) {
            apply(libs.findPlugin("kotlin-multiplatform").get().get().pluginId)
            apply(libs.findPlugin("kotlin-serialization").get().get().pluginId)
            apply(libs.findPlugin("jetbrains-dokka").get().get().pluginId)
            apply(libs.findPlugin("kotlinx-kover").get().get().pluginId)
        }

        configure<KotlinMultiplatformExtension> {
            jvm {
                testRuns["test"].executionTask.configure {
                    useJUnitPlatform()
                    testLogging {
                        events("passed", "skipped", "failed")
                    }
                }
                afterEvaluate {
                    registerShadowJar(
                        project = target,
                        target = this@jvm,
                        mainClassName = extensions.findByType<JavaApplication>()?.mainClass?.get()
                    )
                }
            }
            js(IR) {
                browser()
                nodejs()
            }

            val hostOs = System.getProperty("os.name")
            val isMingwX64 = hostOs.startsWith("Windows")
            val isAarch64 = System.getProperty("os.arch") == "aarch64"
            when {
                hostOs == "Mac OS X" -> {
                    if (isAarch64) {
                        macosArm64("native")
                    } else {
                        macosX64("native")
                    }
                }

                hostOs == "Linux" -> {
                    if (isAarch64) {
                        linuxArm64("native")
                    } else {
                        linuxX64("native")
                    }
                }

                isMingwX64 -> mingwX64("native")
                else -> throw GradleException("Host OS is not supported in Kotlin/Native.")
            }

            sourceSets {
                val commonTest by getting {
                    dependencies {
                        implementation(kotlin("test"))
                    }
                }
            }
        }

        tasks.withType<KotlinCompile>().configureEach {
            kotlinOptions {
                jvmTarget = JavaVersion.VERSION_11.toString()
            }
        }
    }

    fun registerShadowJar(project: Project, target: KotlinJvmTarget, mainClassName: String? = null) = with(project) {
        with(target) {
            // We get the name from the target here to avoid conflicting
            // with the name of the compilation unit
            val targetName = name
            // Access the main compilation
            // We only want to create ShadowJar
            // for the main compilation of the target, not the test
            compilations.named("main") {
                // Access the tasks
                tasks {
                    // Here we register our custom ShadowJar task,
                    // it's being prefixed by the target name
                    val shadowJar = register<ShadowJar>("${targetName}ShadowJar") {
                        // Allows our task to be grouped alongside with other build task
                        // this is only for organization
                        group = "build"
                        // This is important, it adds all output of the build to the fat-jar
                        from(output)
                        // This tells ShadowJar to merge all jars in runtime environment
                        // into the fat-jar for this target
                        configurations = listOf(runtimeDependencyFiles)
                        // Here we configure the name of the resulting fat-jar file
                        // appendix makes sure we append the target name before the version
                        archiveAppendix.set(targetName)
                        // classifier is appended after the version,
                        // it's a common practice to set this classifier to fat-jars
                        archiveClassifier.set("all")

                        // Apply the main class name attribute
                        if (mainClassName != null) {
                            manifest {
                                attributes("Main-Class" to mainClassName)
                            }
                        }

                        // This instruction tells the ShadowJar plugin to combine
                        // ServiceLoader files together, this is needed because
                        // a lot of Kotlin libs uses service files and
                        // they would break without this instruction
                        mergeServiceFiles()
                    }

                    // Finally, we get the normal jar task for this target
                    // and tells kotlin to execute our recently created ShadowJar task
                    // after the normal jar task completes
                    getByName("${targetName}Jar") {
                        finalizedBy(shadowJar)
                    }
                }
            }
        }
    }
}