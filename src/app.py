import argparse
import logging
import os
import signal
import sys
from argparse import Action

from prometheus_client import REGISTRY, start_http_server

from .artifactory import Artifactory
from .collector import JaeCollector, StorageInfoCollector, UserCollector
from .schedule import Scheduler


def init_logger(level):
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


class EnvAction(Action):
    def __init__(self, env, required=True, default=None, **kwargs):
        if not default and env:
            if env in os.environ:
                default = os.environ[env]
        if required and default:
            required = False
        super(EnvAction, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_opts(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", env="JAE_URL", dest="url", action=EnvAction,
                        help="Artifactory URL which will be monitored")
    parser.add_argument("--access-token", env="JAE_ACCESS_TOKEN", dest="access_token", action=EnvAction,
                        help="Access token used for authentication against Artifactory")
    parser.add_argument("--interval", env="JAE_INTERVAL", default=120, dest="interval", action=EnvAction,
                        help="Interval in seconds")
    parser.add_argument("--ignore-ssl-verification", dest="ignore_ssl", action="store_false")
    parser.add_argument("--log-level", env="JAE_LOG_LEVEL", default="INFO", dest="log_level", action=EnvAction,
                        help="Log level. It can be DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is INFO")
    parser.add_argument("--port", "-p", env="JAE_PORT", default=8998, dest="port", action=EnvAction,
                        help="The port that JAE will listen on. Default is 8998")

    parser.add_argument("--storage-info", dest="storage_info", action="store_false",
                        help="Storage summary information regarding binaries, file store and repositories. "
                             "Requires a privileged user (Admin only)")

    parser.add_argument("--users", dest="users", action="store_false",
                        help="Get number of users by realm. Requires a privileged user (Admin only)")

    return parser.parse_args(args)


def register(jae_collector: JaeCollector, opts):
    artifactory = Artifactory(opts.url, opts.access_token, **{"verify": opts.ignore_ssl})

    # register sub-collectors here
    if opts.storage_info:
        jae_collector.register(StorageInfoCollector(artifactory))
    if opts.users:
        jae_collector.register(UserCollector(artifactory))


def main():
    opts = parse_opts(sys.argv[1:])
    init_logger(opts.log_level)

    scheduler = Scheduler()

    def sigterm_handler(signum, frame):
        if scheduler and signal.SIGTERM == signum:
            scheduler.shutdown()

    signal.signal(signal.SIGTERM, sigterm_handler)

    jae_collector = JaeCollector()
    register(jae_collector, opts)

    # register jae to Prometheus registry
    REGISTRY.register(jae_collector)

    scheduler.schedule(jae_collector, int(opts.interval))
    scheduler.start()

    start_http_server(int(opts.port))
    sys.exit(scheduler.wait())


if __name__ == "__main__":
    main()
