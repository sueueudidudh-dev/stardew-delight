import dev.kikugie.stonecutter.controller.task.StonecutterTaskMutexService

plugins {
    id("net.neoforged.moddev")
}

val modId: String = sc.properties["mod.id"]
val modVersion: String = sc.properties["mod.version"]
val mc: String = sc.current.version

// DO NOT set group = ...! (Stonecutter projects share it)
version = "$mc-$modVersion"
base.archivesName = "$modId-neoforge"

val requiredJava: JavaVersion = when {
    sc.current.parsed >= "26.1" -> JavaVersion.VERSION_25
    else -> JavaVersion.VERSION_21
}

dependencies {
    implementation("maven.modrinth:farmers-delight:${sc.properties["deps.fd"]}")
}

neoForge {
    version = sc.properties["deps.neo_loader"]

    mods {
        register(modId) {
            sourceSet(sourceSets.main.get())
        }
    }

    runs {
        register("server") {
            gameDirectory = rootProject.file("run/neoforge-$mc")
            server()
        }
    }
}

// Per-version data (recipes, advancements, tags) written by tools/gen.py
sourceSets.named("main") { resources.srcDir(project.file("generated")) }

java {
    targetCompatibility = requiredJava
    sourceCompatibility = requiredJava
    toolchain {
        vendor = JvmVendorSpec.ADOPTIUM
        languageVersion = JavaLanguageVersion.of(requiredJava.majorVersion)
    }
}

tasks {
    withType<JavaCompile>().configureEach { options.encoding = "UTF-8" }

    processResources {
        val props = mapOf(
            "id" to modId, "name" to sc.properties["mod.name"], "version" to modVersion,
            "author" to sc.properties["mod.author"], "minecraft" to sc.properties["mod.mc_compat"],
            "loader_range" to sc.properties["deps.loader_range"], "neo_range" to sc.properties["deps.neo_range"],
            "fd_range" to sc.properties["deps.fd_range"], "java" to "JAVA_${requiredJava.majorVersion}",
        )
        inputs.properties(props)
        filesMatching(listOf("META-INF/neoforge.mods.toml", "*.mixins.json")) { expand(props) }
        exclude("fabric.mod.json", "META-INF/mods.toml")
    }

    named("createMinecraftArtifacts") {
        dependsOn("stonecutterGenerate")
        // NeoForge recompiling multiple versions in parallel can slow down the system
        usesService(StonecutterTaskMutexService.create(gradle, name))
    }

    register<Copy>("buildAndCollect") {
        group = "build"
        description = "Builds the mod jar and copies it to build/libs/<mod version>/ of the root project"
        from(jar.flatMap { it.archiveFile })
        into(rootProject.layout.buildDirectory.dir("libs/$modVersion"))
    }
}
