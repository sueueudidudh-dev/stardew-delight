pluginManagement {
    repositories {
        mavenCentral()
        gradlePluginPortal()
        maven("https://maven.fabricmc.net/") { name = "FabricMC" }
        maven("https://maven.neoforged.net/releases/") { name = "NeoForged" }
        // maven.kikugie.dev is not reachable from every network: Stonecutter comes from the Gradle Plugin Portal
    }
}

plugins {
    // https://stonecutter.kikugie.dev/
    id("dev.kikugie.stonecutter") version "0.10"
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

stonecutter {
    create(rootProject) {
        // One Gradle project per Minecraft version + loader: versions/<version>-<loader>
        fun match(version: String, vararg loaders: String) {
            for (loader in loaders) {
                // Minecraft before 26.1 is obfuscated: Fabric needs the remapping variant of Loom there
                val script = if (loader == "fabric" && version.startsWith("1.")) "build.fabric-remap.gradle.kts" else "build.$loader.gradle.kts"
                version("$version-$loader", version).buildscript(script)
            }
        }

        // Every target has a matching Farmer's Delight release (Refabricated on Fabric)
        match("26.3", "fabric")
        match("26.2", "fabric")
        match("26.1", "fabric")
        match("1.21.11", "fabric")
        match("1.21.10", "fabric")
        match("1.21.8", "fabric")
        match("1.21.5", "fabric")
        match("1.21.1", "fabric", "neoforge")
        match("1.20.1", "fabric", "forge")
        match("1.19.2", "forge")
        match("1.18.2", "forge")
    }
}

/**
 * Optional mirror for maven.neoforged.net (it is not reachable from some networks).
 * Enable it locally in ~/.gradle/gradle.properties: sk.neoforgedMirror=https://maven.creeperhost.net/
 */
gradle.lifecycle.beforeProject {
    val neoforgedMirror: java.net.URI? = providers.gradleProperty("sk.neoforgedMirror").orNull?.let(java.net.URI::create)
    if (neoforgedMirror != null) {
        repositories.withType(MavenArtifactRepository::class.java).configureEach {
            if (url.host == "maven.neoforged.net") url = neoforgedMirror
        }
    }

    repositories {
        // Farmer's Delight (Forge/NeoForge) and Farmer's Delight Refabricated (Fabric) come from Modrinth
        exclusiveContent {
            forRepository { maven("https://api.modrinth.com/maven") { name = "Modrinth" } }
            filter { includeGroup("maven.modrinth") }
        }
    }
}

rootProject.name = "Stardew Delight"
