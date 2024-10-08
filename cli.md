# Codemodder CLI Parameters

To guarantee a consistent user experience when using codemodder codemods, we offer a specification for what CLI parameters must be offered by any codemodder framework.

| Parameter | Description |
| --------- | ----------- |
| --help            | print help, then exit  |
| --list            | print codemod names, then exit |
| --describe        | print detailed codemod metadata, then exit |
| --output          | the output file to produce (optional) |
| --output-format   | the format for the data output file (codetf or diff) |
| --sarif           | comma-separated set of path(s) to SARIF file(s) to feed to the codemods |
| --contrast-vulnerabilities-xml | the path to a file containing the result of a call to the Contrast Assess XML export API |
| --sonar-issues-json | the path to a file containing output from Sonar's Issues API |
| --sonar-hotspots-json | the path to a file containing output from Sonar's Hotspots API |
| --defectdojo-findings-json | the path to a file containing output from DefectDojo's v2 Findings API |
| --path-include    | comma-separated, exact-match, set of UNIX glob patterns to include. In the case of a conflict with excludes, excludes are given precedence.|
| --path-exclude    | comma-separated, exact-match, set of UNIX glob patterns to exclude. In the case of a conflict with includes, excludes are given precedence.|
| --dry-run         | do everything except make changes to files|
| --codemod-include | comma-separated set of codemod ID(s) to include|
| --codemod-exclude | comma-separated set of codemod ID(s) to exclude|
| --verbose         | print more log messages|
| --log-format      | human (default), or json|
| --project-name    | a descriptive and ideally unique name for the project being scanned to capture in reporting |
| --version         | print the version of the codemodder framework, then exit|
| --parameter       | a parameter for individual codemod (can provide multiple)|
| --max-workers     | specify the maximum number of workers (threads) to use for parallel processing

## Specifying parameters
The codemods must run in the given format:

```
[executable] [arguments] <project directory>
```

The `executable` could involve multiple command line tokens (e.g., `npm run` or `java -jar my-codemod.jar`) in order to invoke the executable.

## Implementation details
- Passing one of `--help`, `--list`, `--describe`, and `--version` will cause the given action to be run, then exit.
- You can only run one of `--help`, `--list`, `--describe`, `--version`. Running multiple will cause an error and should show help like any other argument error.
- The only required field is `<project directory>`. However, this field is not required if running either `--help`, `--list`, `--describe`, or `--version`.
- You cannot legally specify any argument more than one time.
- If `--output` is given, it indicates the path where a codetf or diff file will be created (depending on the value of `--output-format`). Otherwise no output file is generated.
- All codemod rules are loaded by default unless `--codemod-include` specifies a list. `--codemod-exclude` works off all default codemods.
- Specifying a `--codemod-include` or `--codemod-exclude`  that references a non-existent codemod will result in an error
- You can specify a simple wildcard for `--codemod-include` and `--codemod-exclude` (e.g., `--codemod-include=acme:*`). If this pattern doesn't match any codemods, a warning will be issued.
- If the `<project directory>` doesn’t exist, an error should be thrown
- You can provide multiple `--parameter` arguments, but only one per codemod/name/file/line combination
- The `--parameter` argument contains a set of `name=value` pairs following the LDAPv3 Distinguished Name spec (see [RFC 4514](https://datatracker.ietf.org/doc/html/rfc4514.html)).
    - The attributes of these parameters are as follows. Unexpected attributes should cause an error.
        - **“codemod”:** the codemod to which the parameter applies (required)
        - **“file”:** a file in which the change will be applied (optional — assumed “all” if not present)
        - **“line”:** the codemod to which the parameter applies (optional — assumed “all” if not present)
        - **“name”:** the of the parameter (required)
        - **“value”:** the value of the parameter (required)
- The `--max-workers` argument specifies the maximum number of workers to use for parallel codemod processing. For most codemodders "workers" will be threads. When this parameter is not explicitly provided codemodders should rely on the default behavior of the underlying threading/concurrency provider for their language. Most providers will use reasonable defaults that automatically scale to system resources.
- The `--describe` argument causes detailed codemod metadata to be printed to `stdout` as a JSON blob before exiting. This is intended to be used by upstream tooling to collect detailed metadata about available codemods. This argument honors the `--codemod-include` and `--codemod-exclude` flags to determine which codemods should be included in the output. The format of the JSON mirrors the `results` section of the codetf format, except each entry only includes the following fields: `codemod`, `summary`, `description`, and `references`. For example, the output might look like this:
```json
{
  "results": [
    {
      "codemod": "pixee:java/fix-my-java",
      "summary": "Fixes the Java",
      "description": "A longer detailed description of how to fix Java...",
      "references": [
        {
          "url": "https://www.java.com",
          "description": "Everyone's favorite Java website"
        }
      ]
    }
  ]
}
```

## Path inclusion and exclusion

The `--path-include` and `--path-exclude` patterns are interpreted as relative to the given `<project directory>`. In practice this means that the patterns should be joined with the `<project directory>` when used internally and also when passed to external tools.

In general, codemods that remediate the results of other tools respect the file paths specified in findings by those tools. Explicit configuration provided by the user via `--path-include` and `--path-exclude` takes precedence over any defaults a codemod may define. Remediation codemods must not impose their own defaults: the philosophy here is that an external tool has its own defaults and/or configuration, and this should be respected by codemodder.

Codemods that perform their own detection (i.e. "find-and-fix" codemods) may wish to define reasonable defaults for the paths to be included and excluded for analysis. It is recommended that such codemods should include only relevant source files and ignore test directories and build artifacts by default. For example, such codemods will generally want to exclude `**/tests/**` by default. This will be interpreted relative to the given `<project directory>`, which means that the effective pattern will be `<project directory>/**/tests/**`.

For `--path-include` and `--path-exclude`, specific line numbers can be supplied. For instance, to include `src/Foo.java` but only allow changes found on line 11, you would pass `--path-include src/Foo.java:11`.
- *Included* patterns that contain line numbers should be stripped of the line number before being used by either codemodder or external tools to determine which paths are included.
- *Excluded* patterns that contain line numbers should *not* be used by either codemodder or external tools when determining paths to be excluded. In other words, a single excluded line should not prevent the entire file from being excluded by either codemodder or any external tools.

The line includes/excludes only only specifies if nodes are scanned/considered by the codemods. It won’t guarantee that nodes that matches the rules remains unchanges. For example, for `--path-exclude src/[Foo.java](http://Foo.java):11` any vulnerable node inside line `11` in `Foo.java` will be ignore by individual codemods. However it may be changed as part of a fix for another vulnerable node.

It is up to the individual codemodders to handle edge cases in the line includes/excludes.

## Tool result parameters

Codemodder accepts several parameters that are used to provide tool result inputs to the codemods. These include `--sarif`, `--sonar-issues-json`, `--sonar-hotspots-json`, and a handful of others that are tied to tool-specific formats. The available parameters may be gradually expanded as new tools are supported.

In general each tool result flag accecpts a comma-separated list of paths to files that contain the tool results. It is also possible to combine multiple tool result flags in a single invocation of the codemodder (e.g. to use both `--sarif` and `--sonar-issues-json`), subject to the restriction below.

**NOTE:** It is _not_ allowed to provide multiple SARIF inputs _for the same tool_ in a single invocation of the codemodder. For example, it is not possible to provide two Semgrep SARIF files, although it would be possible to provide e.g. a Semgrep SARIF file and a CodeQL JSON file in the same invocation.

## Configuring LLM Support

### Using OpenAI

You can optionally allow codemods to access OpenAI by running with the following environment variable during execution:
```bash
CODEMODDER_OPENAI_API_KEY=<KEY>
```

In the case of problems communicating with an AI subprocessor, all other codemods should still run normally.

### Using Azure OpenAI

Codemods request access to OpenAI models by name, and by default are given access to types that talk to OpenAI directly. It's possible to use Azure OpenAI in codemods by specifying the following environment variables:

```bash
CODEMODDER_AZURE_OPENAI_API_KEY=<KEY>
CODEMODDER_AZURE_OPENAI_ENDPOINT=<ENDPOINT>
CODEMODDER_AZURE_OPENAI_API_VERSION=<VERSION>
CODEMODDER_AZURE_OPENAI_GPT_3_5_TURBO_2024_12_12_DEPLOYMENT=<DEPLOYMENT_NAME>
CODEMODDER_AZURE_OPENAI_GPT_4_TURBO_2024_04_12_API_DEPLOYMENT=<DEPLOYMENT_NAME>
```

- Providing `CODEMODDER_AZURE_OPENAI_API_KEY` without `CODEMODDER_AZURE_OPENAI_ENDPOINT` (and vice versa) will cause a failure on startup.
- The `CODEMODDER_AZURE_API_VERSION` is optional and codemodders can choose a reasonable default as a fallback. This spec does not intend to be prescriptive about particular fallback versions.
- If using Azure OpenAI and a codemod requests access to a model for which there is no corresponding `CODEMODDER_AZURE_OPENAI_(MODELNAME)_DEPLOYMENT` variable, the deployment name will be assumed to be the name of the model (e.g., "gpt-4o").
- If both Azure and OpenAI instructions are available, Azure will be preferred.

### Using Llama (Azure)

Llama models hosted within Azure can be used with the following environment variables:

```bash
CODEMODDER_AZURE_LLAMA_API_KEY=<KEY>
CODEMODDER_AZURE_LLAMA_ENDPOINT=<ENDPOINT>
```

- Providing `CODEMODDER_AZURE_LLAMA_API_KEY` without `CODEMODDER_AZURE_LLAMA_ENDPOINT` (and vice versa) will cause a failure on startup.
- Configuring the Azure Llama client is orthogonal to configuring the Azure OpenAI client. Both can be used in the same codemodder run.

## Console output

The codemodder CLI output is described in [its own specification](logging.md).

## Exit codes

The following are error codes the codemodder will report. Implementors can report errors under codes not specifically enumerated here. Warnings will not cause error codes.

| Code | Meaning |
| --- | --- |
| 0 | success |
| 1 | project directory doesn’t exist or can’t be read |
| 2 | can’t write output file |
| 3 | codemod instructions conflicted |


## Plugin/Extension arguments

Because codemodder is pluggable, there may be need for plugins/extensions to act on CLI arguments. This behavior isn't specified yet.
