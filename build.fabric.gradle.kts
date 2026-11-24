// Fabric for unobfuscated Minecraft (26.1+). Obfuscated versions use build.fabric-remap.gradle.kts.
plugins {
    id("net.fabricmc.fabric-loom") version "1.20.0-alpha.31"
}

val modId: String = sc.properties["mod.id"]
val modVersion: String = sc.properties["mod.version"]
val mc: String = sc.current.version

// DO NOT set group = ...! (Stonecutter projects share it)
version = "$mc-$modVersion"
base.archivesName = "$modId-fabric"

val requiredJava: JavaVersion = JavaVersion.VERSION_25

loom {
    runConfigs.all {
        ideConfigGenerated(false)
        runDir("../../run/fabric-$mc")
    }
}

dependencies {
    minecraft("com.mojang:minecraft:$mc")

    implementation("net.fabricmc:fabric-loader:${sc.properties["deps.fabric_loader"]}")
    implementation("net.fabricmc.fabric-api:fabric-api:${sc.properties["deps.fabric_api"]}")
    implementation("maven.modrinth:farmers-delight-refabricated:${sc.properties["deps.fd"]}")
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
            "java" to "JAVA_${requiredJava.majorVersion}",
        )
        inputs.properties(props)
        filesMatching(listOf("fabric.mod.json", "*.mixins.json")) { expand(props) }
        exclude("META-INF/neoforge.mods.toml", "META-INF/mods.toml")
    }

    register<Copy>("buildAndCollect") {
        group = "build"
        description = "Builds the mod jar and copies it to build/libs/<mod version>/ of the root project"
        from(jar.flatMap { it.archiveFile })
        into(rootProject.layout.buildDirectory.dir("libs/$modVersion"))
    }
}
