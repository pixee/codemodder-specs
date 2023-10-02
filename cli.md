# Codemodder CLI Parameters

To guarantee a consistent user experience when using codemodder codemods, we offer a specification for what CLI parameters must be offered by any codemodder framework.

| Parameter | Description |
| --------- | ----------- |
| --help            | print help, then exit  |
| --list            | print codemod(s) metadata, then exit |
| --output          | the output file to produce (required) |
| --output-format   | the format for the data output file (codetf or diff) |
| --sarif           | comma-separated set of path(s) to SARIF file(s) to feed to the codemods |
| --path-include    | comma-separated, exact-match, set of UNIX glob patterns to include. In the case of a conflict with excludes, excludes are given precedence.|
| --path-exclude    | comma-separated, exact-match, set of UNIX glob patterns to exclude. In the case of a conflict with includes, excludes are given precedence.|
| --dry-run         | do everything except make changes to files|
| --codemod-include | comma-separated set of codemod ID(s) to include|
| --codemod-exclude | comma-separated set of codemod ID(s) to exclude|
| --verbose         | print more log messages|
| --log-format      | human (default), or json|
| --version         | print the version of the codemodder framework, then exit|
| --parameter       | a parameter for individual codemod (can provide multiple)|

## Specifying parameters
The codemods must run in the given format:

```
[executable] [arguments] <project directory>
```

The `executable` could involve multiple command line tokens (e.g., `npm run` or `java -jar my-codemod.jar`) in order to invoke the executable.

## Implementation details
- Passing one of `--help`, `--list` and `--version` will cause the given action to be run, then exit
- You can only run one of `--help`, `--list`, `--version`. Running multiple will cause an error and should show help like any other argument error
- The only required fields are `--output` and `<project directory>`. However, these fields are not required if running either `--help`, `--list` or `--version`.
- You cannot legally specify any argument more than one time
- All codemod rules are loaded by default unless `--codemode-include` specifies a list.  `-codemode-exclude` works off all default codemods.
- Specifying a `--codemod-include`or `--codemod-exclude`  that references a non-existent codemod will result in an error
- For `--path-include` and `--path-exclude`, specific line numbers can be supplied. For instance, to include `src/Foo.java` but only allow changes found on line 11, you would pass `--path-include src/Foo.java:11`.
- The line includes/excludes only only specifies if nodes are scanned/considered by the codemods. I won’t guarantee that nodes that matches the rules remains unchanges. For example, for `--path-exclude src/[Foo.java](http://Foo.java):11` any vulnerable node inside line `11` in `Foo.java` will be ignore by individual codemods. However it may be changed as part of a fix for another vulnerable node.
- It is up to the individual codemodders to handle edge cases in the line includes/excludes.
- If the `<project directory>` doesn’t exist, an error should be thrown
- You can provide multiple `--parameter` arguments, but only one per codemod/name/file/line combination
- The `--parameter` argument contains a set of `name=value` pairs following the LDAPv3 Distinguished Name spec (see [RFC 4514](https://datatracker.ietf.org/doc/html/rfc4514.html)).
    - The attributes of these parameters are as follows. Unexpected attributes should cause an error.
        - **“codemod”:** the codemod to which the parameter applies (required)
        - **“file”:** a file in which the change will be applied (optional — assumed “all” if not present)
        - **“line”:** the codemod to which the parameter applies (optional — assumed “all” if not present)
        - **“name”:** the of the parameter (required)
        - **“value”:** the value of the parameter (required)

## Console output

The output is specified in [logging](logging.md).

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
