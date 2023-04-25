This document describes a first-draft version of the CodeTF spec.

```json
{
  "run" : {
    "vendor" : "pixee", // org name
    "tool" : "pixee", // tool name
    "version" : "1.0.0", // tool version
    "commandLine" : "pixee change . --dry-run" // literal command line used to re-create this run
    "elapsed" : "105024" // how long, in miliseconds, the analysis and report generation took to execute
    "configuration" : {
       "projectDirectory" : "/tmp/path/to/repository/", // the location on disk of the code directory being scanned
       "sarifs" : [ // the analysis inputs from other tools that are informing the analysis
          {
            "artifact" : "/tmp/path/to/semmle.sarif", // the file containing the SARIF or other input 
            "sha1" : "2F5A14..." // hash representing the artifact
          }
       ],
       "includes" : ["/path/to/include.java"], // the files specifically included in the scan
       "excludes" : ["/path/to/exclude.js:52"] // the files specifically excluded in the scan
    },
    "fileExtensionsScanned" : [ // describes what types of files were scanned
      {"extension" :  "java", "count" :  "156"},
      {"extension" :  "js", "count" :  "7"},
      {"extension" :  "xml", "count" :  "128"}
    ],
    "failedFiles" : [
      "/foo/failed.java"
    ]
  },
  
  "results" : [
     {
        "codemod" : "pixee:java/deserialization", // an ID that consistently maps to a vendor's knowledgebase
        "files" : [
            {
                "path" : "src/main/java/org/acme/MyDeserializerAction.java", // the relative path of the file, which when combined with the configuration directory, gives the fully qualified path
                "diff" : "... udiff text...", // the unified diff format of the changes made to the file
                "changes" : [
                    {
                        "lineNumber" : "153", // the "primary" line number that was changed (should be deterministic)
                        "description" : "Added a call to ObjectInputStream//setObjectFilter() to prevent known malicious gadgets..", // human readable description of a given change
                        "properties" : { }, // An arbitrary set of vendor-specific properties to help storytelling
                        "dependencies" : [ // the dependencies that were added to support changes to the file
                            {   
                                "dependency" : "io.github.pixee:java-security-toolkit:1.0.2"
                            }
                        ]
                    },
                    {
                        "lineNumber" : "155",
                        "description" : "Added a call to ObjectInputStream#setObjectFilter() to prevent known malicious gadgets..",
                        "properties" : {
                        },
                        "dependencies" : [
                            {   
                                "dependency" : "io.github.pixee:java-security-toolkit:1.0.2"
                            }
                        ]
                    }
                ]
            }, 
            {
                "path" : "pom.xml",
                "diff" : "... udiff text...",
                "changes" : [
                    {
                        "lineNumber" : "155",
                        "description" : "Added dependency"
                    }
                ]   
            }
        ]
     }
  ]
}


```
