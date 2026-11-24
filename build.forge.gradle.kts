import dev.kikugie.stonecutter.controller.task.StonecutterTaskMutexService

// Forge 1.18.2 - 1.20.1 through ModDevGradle Legacy (the jar is reobfuscated to SRG names)
plugins {
    id("net.neoforged.moddev.legacyforge")
}

val modId: String = sc.properties["mod.id"]
val modVersion: String = sc.properties["mod.version"]
val mc: String = sc.current.version

// DO NOT set group = ...! (Stonecutter projects share it)
version = "$mc-$modVersion"
base.archivesName = "$modId-forge"

val requiredJava: JavaVersion = JavaVersion.VERSION_17

dependencies {
    // Generates the refmap that maps the mixin targets to SRG names
    annotationProcessor("org.spongepowered:mixin:${sc.properties["deps.mixin"]}:processor")
    // Farmer's Delight is published in SRG names: modImplementation remaps it for compiling and dev runs
    modImplementation("maven.modrinth:farmers-delight:${sc.properties["deps.fd"]}")
}

legacyForge {
    enable {
        forgeVersion = sc.properties["deps.forge_loader"]
    }

    mods {
        register(modId) {
            sourceSet(sourceSets.main.get())
        }
    }

    runs {
        register("server") {
            gameDirectory = rootProject.file("run/forge-$mc")
            server()
        }
    }
}

mixin {
    add(sourceSets.main.get(), "$modId.refmap.json")
    config("$modId.mixins.json")
}

// Per-version data (recipes, advancements, tags, pack.mcmeta) written by tools/gen.py
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
            "loader_range" to sc.properties["deps.loader_range"], "forge_range" to sc.properties["deps.forge_range"],
            "fd_range" to sc.properties["deps.fd_range"], "java" to "JAVA_${requiredJava.majorVersion}",
        )
        inputs.properties(props)
        filesMatching("META-INF/mods.toml") { expand(props) }
        filesMatching("*.mixins.json") {
            expand(props)
            // Forge needs the refmap: SRG names at runtime
            filter { if (it == "{") """{ "refmap": "$modId.refmap.json",""" else it }
        }
        exclude("fabric.mod.json", "META-INF/neoforge.mods.toml")
    }

    jar {
        manifest.attributes("MixinConfigs" to "$modId.mixins.json")
    }

    named("createMinecraftArtifacts") {
        dependsOn("stonecutterGenerate")
        // Forge recompiling multiple versions in parallel can slow down the system
        usesService(StonecutterTaskMutexService.create(gradle, name))
    }

    register<Copy>("buildAndCollect") {
        group = "build"
        description = "Builds the reobfuscated mod jar and copies it to build/libs/<mod version>/ of the root project"
        from(named<Jar>("reobfJar").flatMap { it.archiveFile })
        into(rootProject.layout.buildDirectory.dir("libs/$modVersion"))
    }
}
