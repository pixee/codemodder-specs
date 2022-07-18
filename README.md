# Code Transformation Format

This repository holds the definition of the Code Transformation Format (CodeTF).

This open format describes code changes or suggestions made by an automated tool. Much how the SARIF format published by Microsoft helped static analysis tools drive consistent interoperation, we believe an open format can benefit developers to begin contributing towards platforms that make and suggest changes, as well as reduce the need for vendor-specific viewers, parsers, etc.

# The specification

The specification is dirty right now -- it's a document with some marked-up JSON. It's not versioned yet. The plan is to when we find some product stability. 

We intend to publish this spec through an open body like OASIS (https://www.oasis-open.org/).

Stylistically, we probably want to follow in the footsteps of SARIF (https://docs.oasis-open.org/sarif/sarif/v2.1.0/csprd01/sarif-v2.1.0-csprd01.html) -- not only because it's a successful standard but also our results will be closely linked with SARIF, so we'll have many users in common.

Note that like SARIF, this format is not intended to be a replacement for a diagnostic log. It should have minimum diagnostics to help with reproducibility.
