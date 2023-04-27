This document describes the CodeTF specification.

The `results` and `changeset` fields can be seen as a series of patches against the project directory. Each patch builds on any previous patches seen. Therefore, applying a patch from the middle of a changeset without the others may be invalid.

Note that the `changeset` array can have multiple entries for the same given file.

```json
{
  "run" : {
    "vendor" : "pixee", // org name (required)
    "tool" : "pixee", // tool name (required)
    "version" : "1.0.0", // tool version (required)
    "commandLine" : "pixee change . --dry-run" // literal command line used to re-create this run (required)
    "elapsed" : "105024" // how long, in miliseconds, the analysis and report generation took to execute (required)
    "directory" : "/tmp/path/to/repository/", // the location on disk of the code directory being scanned (required)
    "sarifs" : [ // the analysis inputs from other tools that are informing the analysis (optional)
      {
        "artifact" : "/tmp/path/to/semmle.sarif", // the file containing the SARIF or other input (required) 
        "sha1" : "2F5A14..." // hash representing the artifact (required)
      }
    ]
  },
  
  "results" : [ // the results for codemods that made changes during analysis, and can be empty (required)
     {
        "codemod" : "pixee:java/deserialization", // an ID that maps to a vendor's knowledgebase
        "summary" : "Hardened object deserialization calls against attack", // a phrase describing the changes made (required)
        "description" : "Lengthier description about deserialization risks, protection s, etc...", // (required)
        "references" : [ // set of further reading for understanding the issue or changes (optional)
            {
                "url" : "https://www.oracle.com/technetwork/java/seccodeguide-139067.html#8", // the url (required)
                "description" : "Oracle's Secure Coding Guidelines for Java SE" // the description (optional)
            }
        ],
        "properties" : { }, // An arbitrary set of vendor-specific properties to help storytelling (optional)
        "changeset" : [ // the changes for a given codemod (required)
            {
                "path" : "src/main/java/org/acme/MyDeserializerAction.java", // the relative path of the file, which when combined with the configuration directory, gives the fully qualified path (required)
                "diff" : "... udiff text...", // the unified diff format of the changes made to the file (required)
                "changes" : [
                    {
                        "lineNumber" : "153", // the "primary" line number that was changed (required)
                        "description" : "Added a call to ObjectInputStream#setObjectFilter() to prevent known malicious gadgets..", // human readable description of a given change (optional)
                        "properties" : { }, // An arbitrary set of vendor-specific properties to help storytelling (optional)
                        "dependencies" : [ // the dependencies that were needed to support changes to the file, even if it is already there and injection wasn't necessary (optional)
                            {   
                                "action" : "add",
                                "success": "true",
                                "dependency" : "pkg:maven/io.github.pixee/java-security-toolkit@1.0.2" (required)
                            }
                        ]
                    }
                ],
              "failedFiles" : [ // a set of files that failed to be scanned or failed to be changed (optional)
                "/foo/failed.java"
              ]
            }, 
            {
                "path" : "pom.xml",
                "diff" : "... udiff text...",
                "changes" : [
                    {
                        "lineNumber" : "155",
                        "description" : "Added java-security-toolkit for MyDeserializationAction.java"
                    }
                ]   
            }
        ]
     }
  ]
}
```
