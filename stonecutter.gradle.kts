plugins {
    id("dev.kikugie.stonecutter")
    id("net.neoforged.moddev") version "2.0.148" apply false
    id("net.neoforged.moddev.legacyforge") version "2.0.148" apply false
}

// The version the sources in src/ are written for (switch it with the Stonecutter IDE actions or `Set active project`)
stonecutter active "26.3-fabric"

// See https://stonecutter.kikugie.dev/wiki/config/params
stonecutter parameters {
    val (version, loader) = current.project.split('-', limit = 2)

    // Version- and loader-specific values from stonecutter.properties.toml
    properties {
        tags(version, loader)
    }

    // `//? if fabric {` / `//? if forge {` / `//? if neoforge {` in the sources
    constants {
        match(loader, "fabric", "neoforge", "forge")
    }

    replacements {
        // Minecraft 1.21.11 renamed ResourceLocation to Identifier
        string(current.parsed >= "1.21.11") {
            replace("ResourceLocation", "Identifier")
        }
    }
}
