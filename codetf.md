# Code Transformation Format (CodeTF)

This describes Code Transformation Format (CodeTF).

This open format describes code changes or suggestions made by an automated tool. Much how the SARIF format published by Microsoft helped static analysis tools drive consistent interoperation, we believe an open format can benefit developers to begin contributing towards platforms that make and suggest changes, as well as reduce the need for vendor-specific viewers, parsers, etc. We hope to one day publish this spec through an open body like OASIS (https://www.oasis-open.org/).

# The specification JSON

The [specification](codetf.json) is dirty right now -- it's some marked-up JSON. It's not officially versioned yet. The plan is to do that when we find some product stability. Stylistically, we probably want to follow in the footsteps of SARIF (https://docs.oasis-open.org/sarif/sarif/v2.1.0/csprd01/sarif-v2.1.0-csprd01.html) -- not only because it's a successful standard but also our results will be closely linked with SARIF, so we'll have many users in common.

Note that like SARIF, this format is not intended to be a replacement for a diagnostic log. It should have minimum diagnostics to help with reproducibility.

# Notes

The `results` and `changeset` fields can be seen as a series of patches against the project directory. Each patch builds on any previous patches seen. Therefore, applying a patch from the middle of a changeset without the others may be invalid. Multiple locations can be changed in a single file within the scope of a single codemod and be represented by a single `changeset` array entry.

Note that the `changeset` array can have multiple entries for the same given file.

Note that the `lineNumber` field should be deterministic, and this can't be traded for accuracy. The purpose of the line number is only to capture a location to be used in a `--path-include` or `--path-exclude` argument. 
