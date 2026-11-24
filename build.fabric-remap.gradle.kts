// Fabric for obfuscated Minecraft (before 26.1): Mojang mappings + remapping. 26.1+ uses build.fabric.gradle.kts.
plugins {
    id("fabric-loom") version "1.20.0-alpha.31"
}

val modId: String = sc.properties["mod.id"]
val modVersion: String = sc.properties["mod.version"]
val mc: String = sc.current.version

// DO NOT set group = ...! (Stonecutter projects share it)
version = "$mc-$modVersion"
base.archivesName = "$modId-fabric"

val requiredJava: JavaVersion = when {
    sc.current.parsed >= "26.1" -> JavaVersion.VERSION_25
    sc.current.parsed >= "1.20.5" -> JavaVersion.VERSION_21
    else -> JavaVersion.VERSION_17
}

loom {
    runConfigs.all {
        ideConfigGenerated(false)
        runDir("../../run/fabric-$mc")
    }
}

dependencies {
    minecraft("com.mojang:minecraft:$mc")
    // Applies Mojang Mappings on obfuscated versions
    mappings(loom.officialMojangMappings())

    modImplementation("net.fabricmc:fabric-loader:${sc.properties["deps.fabric_loader"]}")
    modImplementation("net.fabricmc.fabric-api:fabric-api:${sc.properties["deps.fabric_api"]}")
    modImplementation("maven.modrinth:farmers-delight-refabricated:${sc.properties["deps.fd"]}")
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
        from(remapJar.flatMap { it.archiveFile })
        into(rootProject.layout.buildDirectory.dir("libs/$modVersion"))
    }
}
