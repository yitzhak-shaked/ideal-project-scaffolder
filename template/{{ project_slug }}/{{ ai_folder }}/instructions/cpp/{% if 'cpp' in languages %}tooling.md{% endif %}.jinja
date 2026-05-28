# C/C++ tooling

CMake is the lingua franca; we use it. Pair it with a real package
manager so dependencies aren't a global-install nightmare.

## Build system: CMake (with presets)

- **CMake 3.25+** for the modern command set.
- Use **`CMakePresets.json`** to define configure/build/test variants.
  Presets are committed; they replace a wiki page of "run cmake with
  these flags".
- Out-of-tree builds only: `cmake -S . -B build`. Never `cmake .`.

Recommended preset shape:

```jsonc
{
  "version": 6,
  "configurePresets": [
    {
      "name": "default",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE":     "RelWithDebInfo",
        "CMAKE_CXX_STANDARD":   "20",
        "CMAKE_CXX_EXTENSIONS": "OFF",
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      }
    },
    { "name": "debug",   "inherits": "default", "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" } },
    { "name": "release", "inherits": "default", "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" } },
    {
      "name": "asan", "inherits": "debug",
      "cacheVariables": { "CMAKE_CXX_FLAGS": "-fsanitize=address,undefined -fno-omit-frame-pointer" }
    }
  ],
  "buildPresets":     [{ "name": "default", "configurePreset": "default" }],
  "testPresets":      [{ "name": "default", "configurePreset": "default", "output": { "outputOnFailure": true } }]
}
```

Then: `cmake --preset default && cmake --build --preset default`.

## The commands you need

| Action | Recipe | Underlying |
| --- | --- | --- |
| Configure | `just cpp-configure` | `cmake --preset default` (or `cmake -S . -B build`) |
| Build | `just cpp-build` | `cmake --build --preset default` |
| Test | `just cpp-test` | `ctest --preset default` (or `ctest --test-dir build`) |
| Run a single test | — | `ctest --test-dir build -R 'name_regex' -V` |
| Format | — | `clang-format -i $(find src include -name '*.[hc]pp')` |
| Lint | — | `clang-tidy -p build src/...` (with project `.clang-tidy`) |
| Install (system) | — | `cmake --install build --prefix /usr/local` |

The `.clang-format` and `.clang-tidy` files live at the repo root.

## Generator

- **Ninja** if available — much faster than Make, well-supported by
  CMake. The presets above pick it.
- On Windows without Ninja, Visual Studio generators work but slower.

## Package management: vcpkg or Conan

CMake doesn't manage dependencies; pick one of the two real C++
package managers and stick with it.

### vcpkg (recommended for most cases)

- Manifest mode: a `vcpkg.json` in the repo declares dependencies.
- A `vcpkg-configuration.json` pins the registry baseline.
- Integration: `-DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake`
  (often in `CMakePresets.json`).
- Updating: bump the baseline in `vcpkg-configuration.json`.

### Conan

- A `conanfile.txt` or `conanfile.py` lists dependencies and options.
- Integration: `CMakeDeps` + `CMakeToolchain` generators.
- More flexibility (per-package options, complex builds), more
  ceremony.

**Commit:** `vcpkg.json` / `vcpkg-configuration.json` *or*
`conanfile.txt` + `conan.lock`. Treat them like any other lockfile.

## Compiler

- **Recent GCC, Clang, or MSVC.** Pin a minimum version in the README
  and CI. C++20 features need GCC ≥ 11, Clang ≥ 14, MSVC ≥ 19.30.
- For cross-compilation, define a CMake toolchain file and reference
  it from a preset.
- For embedded: GCC arm-none-eabi or LLVM embedded toolchain;
  Embedded-specific overrides in `embedded.toolchain.cmake`.

## Sanitisers — always on in CI

Build in CI with at least:

- **ASan** (`-fsanitize=address`) — heap/stack memory errors.
- **UBSan** (`-fsanitize=undefined`) — undefined behaviour.

For concurrency-heavy code, also:

- **TSan** (`-fsanitize=thread`) — data races. Run as a separate
  build (TSan and ASan can't coexist).

## Static analysis

- **clang-tidy** in CI — fail the build on new findings. Project
  `.clang-tidy` configures which checks to run.
- **Include-what-you-use** as a separate CI pass when feasible.
- **cppcheck** as a complementary opinion.

## Anti-patterns

- ❌ Calling `g++` / `clang++` directly with hand-typed flags. Use
  CMake.
- ❌ Vendoring a copy of zlib/boost/etc. in the repo. Use the
  package manager.
- ❌ Building in-source (`cmake .`). Always `-S . -B build`.
- ❌ Hardcoding `-O3` etc. in `CMakeLists.txt`. Use `CMAKE_BUILD_TYPE`
  and let the user / preset choose.
- ❌ A README that says "to build, run a, b, c, d, and don't forget
  the -DTHIS_FLAG". Encode it as a preset.
