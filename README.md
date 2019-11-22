# JFrog Artifactory Exporter

Usage:
```
usage: jae [-h] --url URL --access-token ACCESS_TOKEN [--interval INTERVAL]
           [--ignore-ssl-verification] [--log-level LOG_LEVEL] [--port PORT]
           [--storage-info] [--users]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Artifactory URL which will be monitored
  --access-token ACCESS_TOKEN
                        Access token used for authentication against
                        Artifactory
  --interval INTERVAL   Interval in seconds
  --ignore-ssl-verification
  --log-level LOG_LEVEL
                        Log level. It can be DEBUG, INFO, WARNING, ERROR,
                        CRITICAL. Default is INFO
  --port PORT, -p PORT  The port that JAE will listen on. Default is 8998
  --storage-info        Storage summary information regarding binaries, file
                        store and repositories. Requires a privileged user
                        (Admin only)
  --users               Get number of users by realm. Requires a privileged
                        user (Admin only)
```
Docker:
```bash
docker run -d nthienan/artifactory-exporter --storage-info --users --url https://artifactory.example.com/artifactory --access-token <ACCESS_TOKEN>
```
Metrics:
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 2559.0
python_gc_objects_collected_total{generation="1"} 367.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 81.0
python_gc_collections_total{generation="1"} 7.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="7",patchlevel="4",version="3.7.4"} 1.0
# HELP artifactory_system_version Artifactory version
# TYPE artifactory_system_version gauge
artifactory_system_version{version="6.11.3"} 6.11039e+07
# HELP artifactory_storage_binaries_count Number of binaries
# TYPE artifactory_storage_binaries_count gauge
artifactory_storage_binaries_count 2930.0
# HELP artifactory_storage_binaries_size_megabytes Total size of binaries (MB)
# TYPE artifactory_storage_binaries_size_megabytes gauge
artifactory_storage_binaries_size_megabytes 28310.0
# HELP artifactory_storage_artifacts_size_megabytes Total size of artifacts (MB)
# TYPE artifactory_storage_artifacts_size_megabytes gauge
artifactory_storage_artifacts_size_megabytes 103850.0
# HELP artifactory_storage_artifacts_count The total number of artifacts pointing to the physical binaries stored on the system
# TYPE artifactory_storage_artifacts_count gauge
artifactory_storage_artifacts_count 5591.0
# HELP artifactory_storage_item_count The total number of items (both files and folders) in the system
# TYPE artifactory_storage_item_count gauge
artifactory_storage_item_count 6666.0
# HELP artifactory_total_storage_megabytes Total storage of the system (MB)
# TYPE artifactory_total_storage_megabytes gauge
artifactory_total_storage_megabytes 500000.0
# HELP artifactory_used_storage_megabytes Total storage of the system (MB)
# TYPE artifactory_used_storage_megabytes gauge
artifactory_used_storage_megabytes 132320.0
# HELP artifactory_free_storage_megabytes Total storage of the system (MB)
# TYPE artifactory_free_storage_megabytes gauge
artifactory_free_storage_megabytes 367680.0
# HELP artifactory_repo_used_space_megabytes Used space of the repo in MB
# TYPE artifactory_repo_used_space_megabytes gauge
artifactory_repo_used_space_megabytes{packageType="Docker",repoKey="docker",repoType="LOCAL"} 50610.0
artifactory_repo_used_space_megabytes{packageType="BuildInfo",repoKey="artifactory-build-info",repoType="LOCAL"} 0.0
artifactory_repo_used_space_megabytes{packageType="NA",repoKey="auto-trashcan",repoType="NA"} 19.74
artifactory_repo_used_space_megabytes{packageType="Go",repoKey="go-cache",repoType="CACHE"} 0.0
artifactory_repo_used_space_megabytes{packageType="NA",repoKey="jfrog-support-bundle",repoType="NA"} 0.0
artifactory_repo_used_space_megabytes{packageType="Maven",repoKey="maven-cache",repoType="CACHE"} 0.0
artifactory_repo_used_space_megabytes{packageType="Pypi",repoKey="python-cache",repoType="CACHE"} 0.0
artifactory_repo_used_space_megabytes{packageType="NA",repoKey="TOTAL",repoType="NA"} 103850.0
# HELP artifactory_repo_files Number of files in the repo
# TYPE artifactory_repo_files gauge
artifactory_repo_files{packageType="Docker",repoKey="docker",repoType="LOCAL"} 2510.0
artifactory_repo_files{packageType="BuildInfo",repoKey="artifactory-build-info",repoType="LOCAL"} 0.0
artifactory_repo_files{packageType="NA",repoKey="auto-trashcan",repoType="NA"} 12.0
artifactory_repo_files{packageType="Go",repoKey="go-cache",repoType="CACHE"} 0.0
artifactory_repo_files{packageType="NA",repoKey="jfrog-support-bundle",repoType="NA"} 0.0
artifactory_repo_files{packageType="Maven",repoKey="maven-cache",repoType="CACHE"} 0.0
artifactory_repo_files{packageType="Pypi",repoKey="python-cache",repoType="CACHE"} 0.0
artifactory_repo_files{packageType="NA",repoKey="TOTAL",repoType="NA"} 5591.0
# HELP artifactory_repo_items Number of items in the repo
# TYPE artifactory_repo_items gauge
artifactory_repo_items{packageType="Docker",repoKey="docker",repoType="LOCAL"} 3066.0
artifactory_repo_items{packageType="BuildInfo",repoKey="artifactory-build-info",repoType="LOCAL"} 0.0
artifactory_repo_items{packageType="NA",repoKey="auto-trashcan",repoType="NA"} 17.0
artifactory_repo_items{packageType="Go",repoKey="go-cache",repoType="CACHE"} 0.0
artifactory_repo_items{packageType="NA",repoKey="jfrog-support-bundle",repoType="NA"} 0.0
artifactory_repo_items{packageType="Maven",repoKey="maven-cache",repoType="CACHE"} 0.0
artifactory_repo_items{packageType="Pypi",repoKey="python-cache",repoType="CACHE"} 0.0
artifactory_repo_items{packageType="NA",repoKey="TOTAL",repoType="NA"} 6666.0
# HELP artifactory_users Number of users
# TYPE artifactory_users gauge
artifactory_users{realm="internal"} 3.0
artifactory_users{realm="ldap"} 2.0
```
