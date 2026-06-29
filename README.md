# kotlin-template

A [Copier](https://copier.readthedocs.io/) template for bootstrapping Kotlin/JVM
projects. It generates a raw Gradle project wired up with a
[version catalog](https://docs.gradle.org/current/userguide/version_catalogs.html)
and a pinned Gradle wrapper.

## Usage

```sh
copier copy gh:fiereu/kotlin-template path/to/new-project
```

Copier will prompt for:

| Question         | Description                                          |
| ---------------- | ---------------------------------------------------- |
| `project_name`   | Human-readable project name                          |
| `project_group`  | Maven group / base package (e.g. `de.fiereu.myapp`)  |
| `gradle_version` | Gradle version used by the wrapper                   |
| `kotlin_version` | Kotlin version pinned in the version catalog         |
| `java_version`   | Java toolchain version Kotlin targets                |

After generation:

```sh
cd path/to/new-project
./gradlew run
```

## Updating

Generated projects keep a `.copier-answers.yml` file, so you can pull in later
template changes with:

```sh
copier update
```

## What you get

```
.
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── gradle/
│   ├── libs.versions.toml        # version catalog
│   └── wrapper/                  # pinned Gradle wrapper
├── gradlew / gradlew.bat
└── src/main/kotlin/<group>/Main.kt
```
