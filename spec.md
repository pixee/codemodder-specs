This document describes a first-draft version of the CodeTF spec.

```
{
  "run" : {
    "vendor" : "pixee", # org name
    "tool" : "pixee", # tool name
    "commandLine" : "pixee change . --dry-run" # literal command line used to re-create this run
    "elapsed" : "105024" # how long, in miliseconds, the analysis and report generation took to execute
    "configuration" : {
       "directory" : "/tmp/path/to/repository/", # the location on disk of the code directory being scanned
       "inputs" : [ # the analysis inputs from other tools that are informing the analysis
          {
            "artifact" : "/tmp/path/to/semmle.sarif", # the file containing the SARIF or other input 
            "sha1" : "2F5A14...", # hash representing the artifact
            "vendor" : "Semmle/v1.2" # the vendor who created the input
          }
       ]
       "modules" : [ # the set of modules enabled within the tool that performed the analysis 
         "java/v1.2",
         "javascript/v5.0"
       ],
       "includes" : ["/path/to/include.java"], # the files specifically included in the scan
       "excludes" : ["/path/to/exclude.js:52"] # the files specifically excluded in the scan
    },
    "fileExtensionsScanned" : [ # describes what types of files were scanned
      {"extension" :  "java", "count" :  156},
      {"extension" :  "js", "count" :  7},
      {"extension" :  "xml", "count" :  128}
    ],
    "failedFiles" : [
      "/foo/failed.java"
    ]
  },
  
  "results" : [
     {
        "path" : "src/main/java/org/acme/Foo.java", # the relative path of the file, which when combined with the configuration directory, gives the fully qualified path
        "diff" : "... udiff text...", # the unified diff format of the changes made to the file
        "changes" : [ # a description of the changes being suggested or applied
           { 
             "lineNumber" : "153", # the line where the analysis discovered a place to make a change. can't be relied on for anything except re-running with "include"/"exclude" with this  
             "category" : "pixee:java/deserialization-hardening", # a "code" or "rule ID" that consistently maps to a vendor's knowledgebase and allows customized storytelling  
             "description" : "Added a call to ObjectInputStream#setObjectFilter() to prevent known malicious gadgets..",
             "properties" : { } # An arbitrary set of vendor-specific properties to help storytelling
           },
           { 
             "lineNumber" : "71",
             "category" : "pixee:java/secure-random",
             "description" : "Replaced a call to java.util.Random with java.secure.SecureRandom",
             "properties" : { "something" : "customValue" }
           }
        ] 
     }
  ]
}
```
