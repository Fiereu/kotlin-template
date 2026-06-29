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

| Question            | Description                                                     |
| ------------------- | -------------------------------------------------------------- |
| `project_name`      | Human-readable project name                                    |
| `project_group`     | Maven group / base package (e.g. `de.fiereu.myapp`)            |
| `gradle_version`    | Gradle version used by the wrapper                             |
| `kotlin_version`    | Kotlin version pinned in the version catalog                   |
| `java_version`      | Java toolchain version Kotlin targets                          |
| `kotlin_convention` | Add a `kotlin-conventions` plugin in `buildSrc`                |
| `kotest_convention` | Add a `test-conventions` plugin in `buildSrc` wiring up Kotest |
| `kotest_version`    | Kotest version pinned in the version catalog (asked if enabled)|
| `spotless_convention` | Add a `spotless-conventions` plugin (ktlint formatting)      |
| `spotless_version`  | Spotless plugin version pinned in the catalog (asked if enabled)|
| `sonarlint_convention`| Add a `sonarlint-conventions` plugin (remal SonarLint)      |
| `sonarlint_version` | SonarLint plugin version pinned in the catalog (asked if enabled)|

## Convention plugins

When enabled, shared build logic is extracted into precompiled script plugins
under `buildSrc/`:

- **`kotlin-conventions`** applies the Kotlin JVM plugin, repositories and the
  JVM toolchain. The app's `build.gradle.kts` applies it instead of configuring
  Kotlin inline.
- **`test-conventions`** builds on `kotlin-conventions` and wires up
  [Kotest](https://kotest.io/) (JUnit Platform + Kotest dependencies from the
  catalog), plus a sample `ExampleTest`.
- **`spotless-conventions`** applies [Spotless](https://github.com/diffplug/spotless)
  with ktlint for `*.kt` and `*.gradle.kts` files (`spotlessCheck` / `spotlessApply`).
- **`sonarlint-conventions`** applies the
  [remal SonarLint](https://github.com/remal-gradle-plugins/sonarlint) plugin,
  which hooks SonarLint analysis into `check`. It disables `kotlin:S106` so the
  sample app's `println` doesn't fail the build. Drop that once you add logging.

The Kotest convention builds on the Kotlin one, so enabling it requires
`kotlin_convention`. The Spotless and SonarLint conventions are independent and
work whether Kotlin is configured via its convention or inline. If every toggle
is off, Kotlin is configured inline in `build.gradle.kts` and no `buildSrc/` is
generated.

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
├── buildSrc/                     # only if a convention is enabled
│   └── src/main/kotlin/
│       ├── kotlin-conventions.gradle.kts
│       ├── test-conventions.gradle.kts
│       ├── spotless-conventions.gradle.kts
│       └── sonarlint-conventions.gradle.kts
├── src/main/kotlin/<group>/Main.kt
└── src/test/kotlin/<group>/ExampleTest.kt   # only with Kotest
```
