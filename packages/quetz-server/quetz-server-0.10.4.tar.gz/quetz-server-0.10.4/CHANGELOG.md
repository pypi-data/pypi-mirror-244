# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

## 0.10.4

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.10.3...1a42ed273aa5fd6746df674c9542e539ff32f9a3))

### Bugs fixed

- Address issues of missing `bucket_name` in `s3fs` paths [#673](https://github.com/mamba-org/quetz/pull/673) ([@RobinHolzingerQC](https://github.com/RobinHolzingerQC))
- Pin `typer` to address issues in argument defaults [#672](https://github.com/mamba-org/quetz/pull/672) ([@RobinHolzingerQC](https://github.com/RobinHolzingerQC))

### Maintenance and upkeep improvements

- Fix linting [#678](https://github.com/mamba-org/quetz/pull/678) ([@RobinHolzingerQC](https://github.com/RobinHolzingerQC))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-11-22&to=2023-12-04&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-11-22..2023-12-04&type=Issues) | [@RobinHolzingerQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3ARobinHolzingerQC+updated%3A2023-11-22..2023-12-04&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 0.10.3

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.10.2...cbc3914575bf05050c97c241f003d1712f85043e))

### Bugs fixed

- Ignore missing `info/files` file [#671](https://github.com/mamba-org/quetz/pull/671) ([@wolfv](https://github.com/wolfv))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-09-28&to=2023-11-22&type=c))

[@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2023-09-28..2023-11-22&type=Issues)

## 0.10.2

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.10.1...3cbd27a2356c9ff07fc80fef5888acb71fc2d7f7))

### Bugs fixed

- Fix set user roles when role is None [#669](https://github.com/mamba-org/quetz/pull/669) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-09-28&to=2023-09-28&type=c))

[@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-09-28..2023-09-28&type=Issues)

## 0.10.1

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.10.0...ef6836a7c887dc97a89d8b5cce4472a03740b692))

### Bugs fixed

- Fix oauth2 revoke functionality [#665](https://github.com/mamba-org/quetz/pull/665) ([@wolfv](https://github.com/wolfv))
- Fix docs rest model [#661](https://github.com/mamba-org/quetz/pull/661) ([@mbestipa](https://github.com/mbestipa))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-09-11&to=2023-09-28&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-09-11..2023-09-28&type=Issues) | [@mbestipa](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ambestipa+updated%3A2023-09-11..2023-09-28&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2023-09-11..2023-09-28&type=Issues)

## 0.10.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.9.2...0854d442d1b20b7eb90e023eef27527b722fbcc6))

### Enhancements made

- Fix postgres pool size [#657](https://github.com/mamba-org/quetz/pull/657) ([@beenje](https://github.com/beenje))
- Migrate to Pydantic v2 [#656](https://github.com/mamba-org/quetz/pull/656) ([@beenje](https://github.com/beenje))

### Bugs fixed

- Fix double upload bug and improve test [#663](https://github.com/mamba-org/quetz/pull/663) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Add migration script for scoped API keys [#655](https://github.com/mamba-org/quetz/pull/655) ([@beenje](https://github.com/beenje))
- Fix crash when uploading a package through scoped API key [#647](https://github.com/mamba-org/quetz/pull/647) ([@gabm](https://github.com/gabm))
- Consider packages.conda for index update and channel mirroring [#638](https://github.com/mamba-org/quetz/pull/638) ([@YYYasin19](https://github.com/YYYasin19))

### Maintenance and upkeep improvements

- Pin pydantic\<2 [#653](https://github.com/mamba-org/quetz/pull/653) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Make upload routes consistent with each other [#635](https://github.com/mamba-org/quetz/pull/635) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-06-21&to=2023-09-11&type=c))

[@AndreasAlbertQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AAndreasAlbertQC+updated%3A2023-06-21..2023-09-11&type=Issues) | [@beenje](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Abeenje+updated%3A2023-06-21..2023-09-11&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-06-21..2023-09-11&type=Issues) | [@gabm](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Agabm+updated%3A2023-06-21..2023-09-11&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-06-21..2023-09-11&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2023-06-21..2023-09-11&type=Issues) | [@YYYasin19](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AYYYasin19+updated%3A2023-06-21..2023-09-11&type=Issues)

## 0.9.2

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.9.1...efd519fd840304fb73fe6fd31ee4ae7f010ab1a2))

### Bugs fixed

- Remove DB dependency for health endpoint [#652](https://github.com/mamba-org/quetz/pull/652) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Do not pass pooling arguments to sqlite [#641](https://github.com/mamba-org/quetz/pull/641) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))

### Maintenance and upkeep improvements

- Use PEP-593 Annotated for options and arguments in CLI commands [#644](https://github.com/mamba-org/quetz/pull/644) ([@rominf](https://github.com/rominf))
- Bump pyright-python version [#643](https://github.com/mamba-org/quetz/pull/643) ([@rominf](https://github.com/rominf))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-06-20&to=2023-06-21&type=c))

[@AndreasAlbertQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AAndreasAlbertQC+updated%3A2023-06-20..2023-06-21&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-06-20..2023-06-21&type=Issues) | [@rominf](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Arominf+updated%3A2023-06-20..2023-06-21&type=Issues)

## 0.9.1

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.9.0...13f588cc16560c78927e4b2406a77958a62d5ca6))

### Bugs fixed

- Fix event loop errors [#650](https://github.com/mamba-org/quetz/pull/650) ([@janjagusch](https://github.com/janjagusch))

### Maintenance and upkeep improvements

- Checkout source code from fork [#651](https://github.com/mamba-org/quetz/pull/651) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-06-05&to=2023-06-20&type=c))

[@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-06-05..2023-06-20&type=Issues)

## 0.9.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.8.0...935be5b02961e952396ca1fac20e073ec8907062))

### Enhancements made

- Add async friendly upload [#626](https://github.com/mamba-org/quetz/pull/626) ([@ivergara](https://github.com/ivergara))

### Maintenance and upkeep improvements

- Run CI on main branch [#637](https://github.com/mamba-org/quetz/pull/637) ([@janjagusch](https://github.com/janjagusch))
- Add GCS env vars [#636](https://github.com/mamba-org/quetz/pull/636) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-06-01&to=2023-06-05&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-06-01..2023-06-05&type=Issues) | [@ivergara](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Aivergara+updated%3A2023-06-01..2023-06-05&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-06-01..2023-06-05&type=Issues)

## 0.8.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.7.0...b1ac607ed0900b6242519cd452e92539f83a6721))

### Enhancements made

- Sanitize DB urls before printing [#633](https://github.com/mamba-org/quetz/pull/633) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Make sqlalchemy pool settings configurable [#632](https://github.com/mamba-org/quetz/pull/632) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Avoid exposing the Postgres credentials [#628](https://github.com/mamba-org/quetz/pull/628) ([@sbivol](https://github.com/sbivol))
- Add sampler profiling [#623](https://github.com/mamba-org/quetz/pull/623) ([@ivergara](https://github.com/ivergara))

### Maintenance and upkeep improvements

- Fix pre-commit / micromamba interplay [#634](https://github.com/mamba-org/quetz/pull/634) ([@AndreasAlbertQC](https://github.com/AndreasAlbertQC))
- Add osx-arm64 version for testing on newer apple devices [#631](https://github.com/mamba-org/quetz/pull/631) ([@YYYasin19](https://github.com/YYYasin19))
- Migrate to setup-micromamba [#627](https://github.com/mamba-org/quetz/pull/627) ([@pavelzw](https://github.com/pavelzw))
- Move configurations to `pyproject.toml` [#624](https://github.com/mamba-org/quetz/pull/624) ([@SauravMaheshkar](https://github.com/SauravMaheshkar))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-04-11&to=2023-06-01&type=c))

[@AndreasAlbertQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AAndreasAlbertQC+updated%3A2023-04-11..2023-06-01&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-04-11..2023-06-01&type=Issues) | [@ivergara](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Aivergara+updated%3A2023-04-11..2023-06-01&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-04-11..2023-06-01&type=Issues) | [@martinRenou](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AmartinRenou+updated%3A2023-04-11..2023-06-01&type=Issues) | [@pavelzw](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Apavelzw+updated%3A2023-04-11..2023-06-01&type=Issues) | [@SauravMaheshkar](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3ASauravMaheshkar+updated%3A2023-04-11..2023-06-01&type=Issues) | [@sbivol](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Asbivol+updated%3A2023-04-11..2023-06-01&type=Issues) | [@YYYasin19](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AYYYasin19+updated%3A2023-04-11..2023-06-01&type=Issues)

## 0.7.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.6.3...bc0ac65796d14083ae587eba103d6d60250759ff))

### Enhancements made

- Add endpoints for health checks [#622](https://github.com/mamba-org/quetz/pull/622) ([@janjagusch](https://github.com/janjagusch))

### Maintenance and upkeep improvements

- Fix pyright errors [#621](https://github.com/mamba-org/quetz/pull/621) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-04-05&to=2023-04-11&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-04-05..2023-04-11&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-04-05..2023-04-11&type=Issues)

## 0.6.3

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.6.2...794eccb91e775e3ff3466839dbfe65a226926615))

### Bugs fixed

- Cast starlette URL to str [#618](https://github.com/mamba-org/quetz/pull/618) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-02-20&to=2023-04-05&type=c))

[@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-02-20..2023-04-05&type=Issues)

## 0.6.2

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.6.1...daa8d07d62703601ca236fe4bfaaa23132f781dd))

### Bugs fixed

- Fix unbound variables [#609](https://github.com/mamba-org/quetz/pull/609) ([@janjagusch](https://github.com/janjagusch))

### Maintenance and upkeep improvements

- Enable pyright reportMissingImports [#615](https://github.com/mamba-org/quetz/pull/615) ([@janjagusch](https://github.com/janjagusch))
- Enable pyright reportMissingModuleSource [#614](https://github.com/mamba-org/quetz/pull/614) ([@janjagusch](https://github.com/janjagusch))
- Enable pyright reportOptionalMemberAccess [#613](https://github.com/mamba-org/quetz/pull/613) ([@janjagusch](https://github.com/janjagusch))
- Enable pyright reportOptionalOperand [#612](https://github.com/mamba-org/quetz/pull/612) ([@janjagusch](https://github.com/janjagusch))
- Enable pyright reportOptionalSubscript [#611](https://github.com/mamba-org/quetz/pull/611) ([@janjagusch](https://github.com/janjagusch))
- Enable pyright reportPrivateImportUsage [#610](https://github.com/mamba-org/quetz/pull/610) ([@janjagusch](https://github.com/janjagusch))
- Add prettier pre-commit hook [#608](https://github.com/mamba-org/quetz/pull/608) ([@janjagusch](https://github.com/janjagusch))
- Add pyright pre-commit hook [#607](https://github.com/mamba-org/quetz/pull/607) ([@janjagusch](https://github.com/janjagusch))
- Try to fix ReadTheDocs 2 [#605](https://github.com/mamba-org/quetz/pull/605) ([@janjagusch](https://github.com/janjagusch))
- Fix ReadTheDocs [#604](https://github.com/mamba-org/quetz/pull/604) ([@janjagusch](https://github.com/janjagusch))
- Move SQL authenticator plugin to own repo [#593](https://github.com/mamba-org/quetz/pull/593) ([@simonbohnen](https://github.com/simonbohnen))
- Remove old `quetz-client` [#589](https://github.com/mamba-org/quetz/pull/589) ([@simonbohnen](https://github.com/simonbohnen))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-02-16&to=2023-02-20&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2023-02-16..2023-02-20&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2023-02-16..2023-02-20&type=Issues) | [@simonbohnen](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Asimonbohnen+updated%3A2023-02-16..2023-02-20&type=Issues)

## 0.6.1

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.6.0...ff885bc0de3505329a6f15adc9c51e112e50c887))

### Maintenance and upkeep improvements

- Remove xattr as hard dependency [#602](https://github.com/mamba-org/quetz/pull/602) ([@SimonBohnenQC](https://github.com/SimonBohnenQC))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2023-02-16&to=2023-02-16&type=c))

[@SimonBohnenQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3ASimonBohnenQC+updated%3A2023-02-16..2023-02-16&type=Issues)

## 0.6.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.5.0...822c9244f13c16d84ff44bd6492a6c2f48e9b4aa))

### Enhancements made

- Remove frontend [#565](https://github.com/mamba-org/quetz/pull/565) ([@wolfv](https://github.com/wolfv))

### Bugs fixed

- Fix upload endpoint [#597](https://github.com/mamba-org/quetz/pull/597) ([@simonbohnen](https://github.com/simonbohnen))
- Fix upload endpoint [#594](https://github.com/mamba-org/quetz/pull/594) ([@simonbohnen](https://github.com/simonbohnen))

### Maintenance and upkeep improvements

- Update check-release action to v2 [#601](https://github.com/mamba-org/quetz/pull/601) ([@janjagusch](https://github.com/janjagusch))
- Make `quetz` compatible with SQLAlchemy 2.0 [#598](https://github.com/mamba-org/quetz/pull/598) ([@simonbohnen](https://github.com/simonbohnen))
- Update pre-commit versions [#592](https://github.com/mamba-org/quetz/pull/592) ([@wolfv](https://github.com/wolfv))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-12-16&to=2023-02-16&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2022-12-16..2023-02-16&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2022-12-16..2023-02-16&type=Issues) | [@simonbohnen](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Asimonbohnen+updated%3A2022-12-16..2023-02-16&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-12-16..2023-02-16&type=Issues)

## 0.5.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.4.4...7f77638aa4b94d6eeb3a18158ee6f9184061ef74))

### Enhancements made

- no file or directory mandatory [#558](https://github.com/mamba-org/quetz/pull/558) ([@brichet](https://github.com/brichet))
- Add an API for paginated package versions [#556](https://github.com/mamba-org/quetz/pull/556) ([@brichet](https://github.com/brichet))
- Implement multiple languages support for the TermsOfServices [#552](https://github.com/mamba-org/quetz/pull/552) ([@martinRenou](https://github.com/martinRenou))
- Adds a new endpoint to check if the user already signed the TOS [#548](https://github.com/mamba-org/quetz/pull/548) ([@hbcarlos](https://github.com/hbcarlos))
- Fix / consistent usage of f-strings [#538](https://github.com/mamba-org/quetz/pull/538) ([@riccardoporreca](https://github.com/riccardoporreca))
- Add upload endpoint [#533](https://github.com/mamba-org/quetz/pull/533) ([@atrawog](https://github.com/atrawog))
- Add SQL authenticator [#508](https://github.com/mamba-org/quetz/pull/508) ([@janjagusch](https://github.com/janjagusch))

### Bugs fixed

- Remove `httpx` pin, fix tests, & test plugins individually [#574](https://github.com/mamba-org/quetz/pull/574) ([@simonbohnen](https://github.com/simonbohnen))
- Fix sqlauth error parsing [#569](https://github.com/mamba-org/quetz/pull/569) ([@simonbohnen](https://github.com/simonbohnen))
- Fix update route in SQL Authenticator [#568](https://github.com/mamba-org/quetz/pull/568) ([@simonbohnen](https://github.com/simonbohnen))
- fix OpenAPI spec. by allowing "nullable" values [#564](https://github.com/mamba-org/quetz/pull/564) ([@kuepe-sl](https://github.com/kuepe-sl))
- fix package_versions.version_order database field after package version deletion [#562](https://github.com/mamba-org/quetz/pull/562) ([@kuepe-sl](https://github.com/kuepe-sl))
- fix path in HTML templates [#561](https://github.com/mamba-org/quetz/pull/561) ([@kuepe-sl](https://github.com/kuepe-sl))
- Fixes CI [#559](https://github.com/mamba-org/quetz/pull/559) ([@hbcarlos](https://github.com/hbcarlos))
- Fix/several typo errors [#557](https://github.com/mamba-org/quetz/pull/557) ([@brichet](https://github.com/brichet))
- Fixes issues and tests on indexes [#555](https://github.com/mamba-org/quetz/pull/555) ([@brichet](https://github.com/brichet))
- Remove an uploaded package whose filename does not match the package name [#554](https://github.com/mamba-org/quetz/pull/554) ([@brichet](https://github.com/brichet))
- Remove package from repodata.json [#551](https://github.com/mamba-org/quetz/pull/551) ([@brichet](https://github.com/brichet))
- channels with dots in their name cause a crash in indexing [#541](https://github.com/mamba-org/quetz/pull/541) ([@gabm](https://github.com/gabm))

### Maintenance and upkeep improvements

- Fixes CI [#559](https://github.com/mamba-org/quetz/pull/559) ([@hbcarlos](https://github.com/hbcarlos))
- Fixes issues and tests on indexes [#555](https://github.com/mamba-org/quetz/pull/555) ([@brichet](https://github.com/brichet))

### Other merged PRs

- Add docker badge to README [#547](https://github.com/mamba-org/quetz/pull/547) ([@dhirschfeld](https://github.com/dhirschfeld))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-05-19&to=2022-12-16&type=c))

[@atrawog](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Aatrawog+updated%3A2022-05-19..2022-12-16&type=Issues) | [@baszalmstra](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Abaszalmstra+updated%3A2022-05-19..2022-12-16&type=Issues) | [@brichet](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Abrichet+updated%3A2022-05-19..2022-12-16&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2022-05-19..2022-12-16&type=Issues) | [@dhirschfeld](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Adhirschfeld+updated%3A2022-05-19..2022-12-16&type=Issues) | [@gabm](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Agabm+updated%3A2022-05-19..2022-12-16&type=Issues) | [@hbcarlos](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ahbcarlos+updated%3A2022-05-19..2022-12-16&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2022-05-19..2022-12-16&type=Issues) | [@kuepe-sl](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Akuepe-sl+updated%3A2022-05-19..2022-12-16&type=Issues) | [@martinRenou](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3AmartinRenou+updated%3A2022-05-19..2022-12-16&type=Issues) | [@riccardoporreca](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ariccardoporreca+updated%3A2022-05-19..2022-12-16&type=Issues) | [@simonbohnen](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Asimonbohnen+updated%3A2022-05-19..2022-12-16&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-05-19..2022-12-16&type=Issues)

## 0.4.4

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.4.3...fb4bc9049dfd2de0233d8ae61dd5962e7e2b616e))

### Enhancements made

- improve logging [#534](https://github.com/mamba-org/quetz/pull/534) ([@wolfv](https://github.com/wolfv))
- Log post_index_creation exceptions [#532](https://github.com/mamba-org/quetz/pull/532) ([@atrawog](https://github.com/atrawog))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-05-11&to=2022-05-19&type=c))

[@atrawog](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Aatrawog+updated%3A2022-05-11..2022-05-19&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-05-11..2022-05-19&type=Issues)

## 0.4.3

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.4.2...42f9b9dca2f37058bc193fed890cd9524117576f))

### Enhancements made

- allow upload usage without conda-verify installed [#524](https://github.com/mamba-org/quetz/pull/524) ([@wolfv](https://github.com/wolfv))
- log errors of background tasks [#523](https://github.com/mamba-org/quetz/pull/523) ([@wolfv](https://github.com/wolfv))

### Bugs fixed

- fix compatibility with latest starlette [#530](https://github.com/mamba-org/quetz/pull/530) ([@wolfv](https://github.com/wolfv))
- fix proxy channels noarch and gzip repodata [#529](https://github.com/mamba-org/quetz/pull/529) ([@wolfv](https://github.com/wolfv))
- Fix PAM authentication log message [#526](https://github.com/mamba-org/quetz/pull/526) ([@riccardoporreca](https://github.com/riccardoporreca))
- fix mamba 0.23.0 compat [#525](https://github.com/mamba-org/quetz/pull/525) ([@wolfv](https://github.com/wolfv))
- Use infodata['size'] for s3fs [#521](https://github.com/mamba-org/quetz/pull/521) ([@atrawog](https://github.com/atrawog))

### Maintenance and upkeep improvements

- Move httpx as dependency [#507](https://github.com/mamba-org/quetz/pull/507) ([@fcollonval](https://github.com/fcollonval))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-04-07&to=2022-05-11&type=c))

[@atrawog](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Aatrawog+updated%3A2022-04-07..2022-05-11&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2022-04-07..2022-05-11&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Afcollonval+updated%3A2022-04-07..2022-05-11&type=Issues) | [@riccardoporreca](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ariccardoporreca+updated%3A2022-04-07..2022-05-11&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-04-07..2022-05-11&type=Issues)

## 0.4.2

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.4.1...4c65023b11c1ee1bf4c3351429c9cb365e10b6ba))

### Bugs fixed

- Fix gcs region config entry [#517](https://github.com/mamba-org/quetz/pull/517) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-04-06&to=2022-04-06&type=c))

[@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2022-04-06..2022-04-06&type=Issues)

## 0.4.1

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.4.0...bd2d1fc0a8c99d90662645b9bf485f940ae06e8a))

### Enhancements made

- Make GCS bucket location configurable [#512](https://github.com/mamba-org/quetz/pull/512) ([@janjagusch](https://github.com/janjagusch))

### Maintenance and upkeep improvements

- Fix CI [#513](https://github.com/mamba-org/quetz/pull/513) ([@janjagusch](https://github.com/janjagusch))
- small test refactor, skip harvester tests on python 3.10 [#505](https://github.com/mamba-org/quetz/pull/505) ([@wolfv](https://github.com/wolfv))
- Unpin h2 [#500](https://github.com/mamba-org/quetz/pull/500) ([@janjagusch](https://github.com/janjagusch))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-03-14&to=2022-04-06&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2022-03-14..2022-04-06&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2022-03-14..2022-04-06&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-03-14..2022-04-06&type=Issues)

## 0.4.0

([Full Changelog](https://github.com/mamba-org/quetz/compare/v0.3.0...5f2832c0b39ef56c44c17a0460bc876ae350fae8))

### Enhancements made

- update all js [#501](https://github.com/mamba-org/quetz/pull/501) ([@wolfv](https://github.com/wolfv))
- attempt to fix CI [#497](https://github.com/mamba-org/quetz/pull/497) ([@wolfv](https://github.com/wolfv))
- Allow deleting channel members and changing role of existing members [#495](https://github.com/mamba-org/quetz/pull/495) ([@janjagusch](https://github.com/janjagusch))
- Bump url-parse from 1.4.7 to 1.5.10 in /quetz_frontend [#491](https://github.com/mamba-org/quetz/pull/491) ([@dependabot](https://github.com/dependabot))
- Make cache timeout for GCS configurable [#490](https://github.com/mamba-org/quetz/pull/490) ([@SophieHallstedtQC](https://github.com/SophieHallstedtQC))
- Bump follow-redirects from 1.11.0 to 1.14.8 in /quetz_frontend [#487](https://github.com/mamba-org/quetz/pull/487) ([@dependabot](https://github.com/dependabot))
- Bump ajv from 6.12.2 to 6.12.6 in /quetz_frontend [#486](https://github.com/mamba-org/quetz/pull/486) ([@dependabot](https://github.com/dependabot))
- Bump node-sass from 4.14.1 to 7.0.0 in /quetz_frontend [#485](https://github.com/mamba-org/quetz/pull/485) ([@dependabot](https://github.com/dependabot))
- Bump ssri from 6.0.1 to 6.0.2 in /quetz_frontend [#484](https://github.com/mamba-org/quetz/pull/484) ([@dependabot](https://github.com/dependabot))
- Bump postcss from 7.0.32 to 7.0.39 in /quetz_frontend [#482](https://github.com/mamba-org/quetz/pull/482) ([@dependabot](https://github.com/dependabot))

### Bugs fixed

- make mamba solver work with latest mamba release [#496](https://github.com/mamba-org/quetz/pull/496) ([@wolfv](https://github.com/wolfv))

### Maintenance and upkeep improvements

- fix some pytest and sqlalchemy warnings [#502](https://github.com/mamba-org/quetz/pull/502) ([@wolfv](https://github.com/wolfv))
- update all js [#501](https://github.com/mamba-org/quetz/pull/501) ([@wolfv](https://github.com/wolfv))

### Other merged PRs

- Bump path-parse from 1.0.6 to 1.0.7 in /quetz_frontend [#498](https://github.com/mamba-org/quetz/pull/498) ([@dependabot](https://github.com/dependabot))
- Bump lodash from 4.17.19 to 4.17.21 in /quetz_frontend [#483](https://github.com/mamba-org/quetz/pull/483) ([@dependabot](https://github.com/dependabot))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/mamba-org/quetz/graphs/contributors?from=2022-02-04&to=2022-03-14&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Acodecov-commenter+updated%3A2022-02-04..2022-03-14&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Adependabot+updated%3A2022-02-04..2022-03-14&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Ajanjagusch+updated%3A2022-02-04..2022-03-14&type=Issues) | [@SophieHallstedtQC](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3ASophieHallstedtQC+updated%3A2022-02-04..2022-03-14&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Amamba-org%2Fquetz+involves%3Awolfv+updated%3A2022-02-04..2022-03-14&type=Issues)
