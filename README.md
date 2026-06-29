# kotlin-template

A [Copier](https://copier.readthedocs.io/) template for bootstrapping Kotlin/JVM
projects. It generates a raw Gradle project wired up with a
[version catalog](https://docs.gradle.org/current/userguide/version_catalogs.html)
and a pinned Gradle wrapper.

## Usage

```sh
copier copy --trust gh:fiereu/kotlin-template path/to/new-project
```

`--trust` is required because choosing a license runs a generation task (see
[License](#license) below).

Copier will prompt for:

| Question            | Description                                                     |
| ------------------- | -------------------------------------------------------------- |
| `project_name`      | Human-readable project name                                    |
| `project_group`     | Maven group / base package (e.g. `de.fiereu.myapp`)            |
| `project_layout`    | `single` module or `multi` module                              |
| `module_name`       | Name of the default module for multi-module (asked then, default `core`) |
| `gradle_version`    | Gradle version used by the wrapper                             |
| `kotlin_version`    | Kotlin version pinned in the version catalog                   |
| `java_version`      | Java toolchain version Kotlin targets                          |
| `kotlin_convention` | Add a `kotlin-conventions` plugin in `buildSrc`                |
| `test_framework`    | Test framework for the `test-conventions` plugin (`none` / `kotest`) |
| `kotest_version`    | Kotest version pinned in the catalog (asked when Kotest chosen)|
| `spotless_convention` | Add a `spotless-conventions` plugin (ktlint formatting)      |
| `spotless_version`  | Spotless plugin version pinned in the catalog (asked if enabled)|
| `sonarlint_convention`| Add a `sonarlint-conventions` plugin (remal SonarLint)      |
| `sonarlint_version` | SonarLint plugin version pinned in the catalog (asked if enabled)|
| `agent_instructions`| Generate an `AGENTS.md` for AI coding agents                   |
| `agent_links`       | Which agent tools get a file linking back to `AGENTS.md`       |
| `license`           | License to generate (`none`, `MIT`, `Apache-2.0`, `BSD-3-Clause`, `GPL-3.0`, `AGPL-3.0`, `MPL-2.0`) |
| `author_name`       | Copyright holder (blank uses your git `user.name`)             |
| `github_actions`    | Generate GitHub Actions workflows for testing and formatting   |

## Project layout

`project_layout` controls the module structure:

- **`single`** keeps the application at the repository root (`build.gradle.kts`
  and `src/` directly under it).
- **`multi`** puts the application in a module subdirectory (default `core`,
  set via `module_name`) and `include`s it from `settings.gradle.kts`. Add more
  modules as sibling directories. Run the app with `./gradlew run`, which
  resolves to the module's `run` task.

## Convention plugins

When enabled, shared build logic is extracted into precompiled script plugins
under `buildSrc/`:

- **`kotlin-conventions`** applies the Kotlin JVM plugin, repositories and the
  JVM toolchain. The app's `build.gradle.kts` applies it instead of configuring
  Kotlin inline.
- **`test-conventions`** builds on `kotlin-conventions` and wires up the test
  framework chosen via `test_framework` (currently
  [Kotest](https://kotest.io/): JUnit Platform + Kotest dependencies from the
  catalog), plus a sample `ExampleTest`. Pick `none` to skip it. The choice is
  designed to be extended. Adding a framework is a new entry under `choices:`
  in `copier.yml` plus a branch in the convention and sample test.
- **`spotless-conventions`** applies [Spotless](https://github.com/diffplug/spotless)
  with ktlint for `*.kt` and `*.gradle.kts` files (`spotlessCheck` / `spotlessApply`).
- **`sonarlint-conventions`** applies the
  [remal SonarLint](https://github.com/remal-gradle-plugins/sonarlint) plugin,
  which hooks SonarLint analysis into `check`. It disables `kotlin:S106` so the
  sample app's `println` doesn't fail the build. Drop that once you add logging.

The test convention builds on the Kotlin one, so choosing a framework other than
`none` requires `kotlin_convention`. The Spotless and SonarLint conventions are independent and
work whether Kotlin is configured via its convention or inline. If every toggle
is off, Kotlin is configured inline in `build.gradle.kts` and no `buildSrc/` is
generated.

## AI agent instructions

With `agent_instructions` enabled, the project gets an **`AGENTS.md`** containing
the actual build/test/format/check instructions (tailored to the conventions you
picked). It's the single source of truth.

Each tool selected in `agent_links` gets a **symlink** back to it, so there's no
duplicated content to keep in sync:

- Claude Code -> `CLAUDE.md`
- GitHub Copilot -> `.github/copilot-instructions.md`
- Gemini CLI -> `GEMINI.md`

Adding another tool later is one entry under `agent_links` `choices:` plus a
symlink in the template. (Symlink reproduction relies on `_preserve_symlinks` in
`copier.yml`. Note that symlinks need a Git/OS that supports them.)

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

## License

This template does not vendor any license texts. When you pick a `license`, a
generation task fetches that license from the
[GitHub Licenses API](https://docs.github.com/en/rest/licenses) and writes it to
`LICENSE`, filling in the current year and `author_name` (or your git
`user.name` when left blank). This needs `--trust`, Python 3, and network
access. Choose `none` to skip it.

## Continuous integration

With `github_actions` enabled, the project gets GitHub Actions workflows under
`.github/workflows/`. Both set up the chosen JDK with Temurin and run through the
Gradle wrapper with `gradle/actions/setup-gradle` caching:

- **`test.yml`** runs `./gradlew test` on pushes to `main`/`master` and on pull
  requests (generated when a test framework is chosen).
- **`format.yml`** runs `./gradlew spotlessApply` on pushes to `main`/`master`
  and on open pull request branches, then commits the result as
  `chore: apply spotless formatting` when there are changes (generated when
  Spotless is enabled). It needs `contents: write`. Pushes from forked-repo pull
  requests cannot be committed back, so the commit step is skipped there.

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
├── AGENTS.md                     # only with agent_instructions
├── CLAUDE.md -> AGENTS.md        # symlinks, per agent_links
├── GEMINI.md -> AGENTS.md
├── .github/
│   ├── copilot-instructions.md -> ../AGENTS.md   # per agent_links
│   └── workflows/                # only with github_actions
│       ├── test.yml
│       └── format.yml
├── src/main/kotlin/<group>/Main.kt          # single-module layout
└── src/test/kotlin/<group>/ExampleTest.kt   # only with Kotest
```

In multi-module layout, `build.gradle.kts` and `src/` move under the module
directory instead (e.g. `core/build.gradle.kts`, `core/src/main/kotlin/...`),
and the root keeps only `settings.gradle.kts`.
