import logging
from abc import ABC, abstractmethod

from prometheus_client import Gauge

from .artifactory import Artifactory
from .utility import str_to_megabytes, str_to_int


class JaeCollector:

    def __init__(self):
        self._cached_metrics = []
        self._collectors = []

    def register(self, *collectors):
        self._collectors.extend(collectors)

    def collect(self):
        return self._cached_metrics

    def run(self):
        new_data = []
        for c in self._collectors:
            logging.debug("%s is running..." % c.name)
            new_data.extend(c.run())
            logging.debug("%s has been successfully run" % c.name)
        self._cached_metrics = new_data


class Collector(ABC):

    def __init__(self, artifactory: Artifactory):
        self._artifactory = artifactory

    @abstractmethod
    def run(self):
        raise NotImplemented()


class UserCollector(Collector):

    def __init__(self, artifactory):
        super().__init__(artifactory)
        self.name = "user_collector"
        self.user_gauge = Gauge("artifactory_users", "Number of users", ["realm"])

    def run(self):
        logging.debug("Starting collect storage info...")
        users = self._artifactory.get_users()
        internal = 0
        ldap = 0
        for u in users:
            if u["realm"] == "internal":
                internal += 1
            elif u["realm"] == "ldap":
                ldap += 1
        self.user_gauge.labels("internal").set(internal)
        self.user_gauge.labels("ldap").set(ldap)
        return self.user_gauge.collect()


class StorageInfoCollector(Collector):

    def __init__(self, artifactory):
        super().__init__(artifactory)
        self.name = "storage_collector"
        self.binaries_count = Gauge("artifactory_storage_binaries_count",
                                    "Number of binaries")
        self.binaries_size = Gauge("artifactory_storage_binaries_size_megabytes",
                                   "Total size of binaries (MB)")
        self.artifacts_size = Gauge("artifactory_storage_artifacts_size_megabytes",
                                    "Total size of artifacts (MB)")
        self.artifacts_count = Gauge("artifactory_storage_artifacts_count",
                                     "The total number of artifacts pointing to "
                                     "the physical binaries stored on the system")
        self.item_count = Gauge("artifactory_storage_item_count",
                                "The total number of items (both files and folders) in the system")
        self.total = Gauge("artifactory_total_storage_megabytes",
                           "Total storage of the system (MB)")
        self.used = Gauge("artifactory_used_storage_megabytes",
                          "Total storage of the system (MB)")
        self.free = Gauge("artifactory_free_storage_megabytes",
                          "Total storage of the system (MB)")
        self.repo_used_space = Gauge("artifactory_repo_used_space_megabytes",
                                     "Used space of the repo in MB",
                                     ["repoKey", "repoType", "packageType"])
        self.repo_file = Gauge("artifactory_repo_files",
                               "Number of files in the repo",
                               ["repoKey", "repoType", "packageType"])
        self.repo_item = Gauge("artifactory_repo_items",
                               "Number of items in the repo",
                               ["repoKey", "repoType", "packageType"])

    def run(self):
        logging.debug("Starting collect storage info...")
        result = []
        data = self._artifactory.get_storage_info()

        binaries_summary = data["binariesSummary"]

        self.binaries_count.set(int(binaries_summary["binariesCount"].replace(",", "")))
        result.extend(self.binaries_count.collect())

        self.binaries_size.set(str_to_megabytes(binaries_summary["binariesSize"]))
        result.extend(self.binaries_size.collect())

        self.artifacts_size.set(str_to_megabytes(binaries_summary['artifactsSize']))
        result.extend((self.artifacts_size.collect()))

        self.artifacts_count.set(str_to_int(binaries_summary['artifactsCount']))
        result.extend(self.artifacts_count.collect())

        self.item_count.set(str_to_int(binaries_summary['itemsCount']))
        result.extend(self.item_count.collect())

        file_store_summary = data["fileStoreSummary"]
        self.total.set(str_to_megabytes(file_store_summary["totalSpace"]))
        result.extend(self.total.collect()[:])

        self.used.set(str_to_megabytes("%s %s" %
                                       (file_store_summary["usedSpace"].split(" ")[0],
                                        file_store_summary["usedSpace"].split(" ")[1])))
        result.extend(self.used.collect()[:])

        self.free.set(str_to_megabytes("%s %s" %
                                       (file_store_summary["freeSpace"].split(" ")[0],
                                        file_store_summary["freeSpace"].split(" ")[1])))
        result.extend(self.free.collect())

        for repo in data["repositoriesSummaryList"]:
            repo_key = repo["repoKey"]
            repo_type = repo["repoType"]
            package_type = "NA"
            if repo_key != "TOTAL":
                package_type = repo["packageType"]
            self.repo_used_space.labels(repo_key, repo_type, package_type).set(str_to_megabytes(repo["usedSpace"]))
            self.repo_file.labels(repo_key, repo_type, package_type).set(repo["filesCount"])
            self.repo_item.labels(repo_key, repo_type, package_type).set(repo["itemsCount"])
        result.extend(self.repo_used_space.collect())
        result.extend(self.repo_file.collect())
        result.extend(self.repo_item.collect())
        logging.debug("Storage info collected")
        return result
