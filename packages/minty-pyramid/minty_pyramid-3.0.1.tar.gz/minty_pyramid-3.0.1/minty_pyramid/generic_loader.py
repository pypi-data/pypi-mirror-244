# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import logging
import minty
import re
import statsd
from minty import Base
from minty.config.parser.apache import ApacheConfigParser
from minty.infrastructure import _parse_global_config
from minty.logging.mdc import get_mdc, mdc
from minty_pyramid.renderer import jsonapi
from pyramid.config import Configurator
from uuid import uuid4


def new_response_callback(event):
    """Set default headers when a new response is created"""
    if not event.response.headers.get("cache-control"):
        event.response.headers.update({"cache-control": "no-store"})

    event.response.headers.update(
        {"request-id": str(event.request.request_id)}
    )


class GenericEngine(Base):
    """Pyramid configurator for Non Domain Driven Projects."""

    def __init__(self):

        self.config = None

    def setup(self, global_config: dict, **settings) -> object:
        """Set up the application by loading the injecting the CQRS layer.

        :param global_config: Global configuration
        :type global_config: dict
        :return: Returns the Configurator from Pyramid
        :rtype: object
        """

        config = Configurator(settings=settings)

        config.add_request_method(
            lambda r: uuid4(), name="request_id", property=True, reify=True
        )

        configuration_parsed = _parse_global_config(
            settings["minty_service.infrastructure.config_file"],
            ApacheConfigParser(),
        )
        config.add_request_method(
            lambda r: configuration_parsed,
            name="configuration",
            property=True,
            reify=True,
        )

        ### Add renderer
        config.add_renderer(None, jsonapi())

        config.add_tween("minty_pyramid.generic_loader.RequestLoadGauge")
        config.add_tween("minty_pyramid.generic_loader.RequestTimer")
        config.add_tween("minty_pyramid.generic_loader.RequestDataLogger")

        config.add_subscriber(
            "minty_pyramid.generic_loader.new_response_callback",
            "pyramid.events.NewResponse",
        )

        config.scan()
        self.config = config

        if "statsd" in configuration_parsed:
            if "disabled" in configuration_parsed["statsd"]:
                configuration_parsed["statsd"]["disabled"] = bool(
                    int(configuration_parsed["statsd"]["disabled"])
                )
            statsd.Connection.set_defaults(**configuration_parsed["statsd"])
        else:
            # No statsd configuration available; forcefully disable it
            statsd.Connection.set_defaults(disabled=True)

        return config

    def main(self) -> object:
        """Run the application by calling the wsgi_app function of Pyramid.

        :raises ValueError: When setup is forgotten
        :return: wsgi app
        :rtype: object
        """
        if self.config is None:
            raise ValueError("Make sure you run setup before 'main'")

        self.logger.info("Creating WSGI application")

        return self.config.make_wsgi_app()


class RequestLoadGauge(Base):
    """
    Pyramid "tween" class to report load (number of active threads).

    This uses a statsd gauge to report the number of concurrently active
    threads in this process to the platform.
    """

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        # We want a "context free" statsd, so we do not split out the
        # metrics by hostname.

        old_context = self.statsd.context
        self.statsd.context = None

        self.statsd.get_counter("total_requests").increment()
        gauge = self.statsd.get_gauge("active_threads")

        self.statsd.context = old_context

        try:
            gauge.increment()
            response = self.handler(request)
        finally:
            gauge.decrement()

        return response


class RequestTimer(Base):
    """Middleware / tween to log request time and count to statsd."""

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        "Log time and count to statsd before and after execution of handler."

        try:
            # Pre-build the timer & counter objects, so it doesn't matter if
            # `self.handler` (re)sets the context in `minty.STATSD`.
            minty.STATSD.context = request.host.replace(".", "_")
            timer = self.statsd.get_timer("request_duration")
            counter = self.statsd.get_counter("number_of_requests")

            metrics_path = re.sub(r"[^a-zA-Z0-9_]", "_", request.path[1:])

            with timer.time(metrics_path):
                response = self.handler(request)

            counter.increment(str(response.status_int), delta=1)
        finally:
            minty.STATSD.context = None

        return response


def get_logging_info(request):
    logging_info = {}

    logging_info["hostname"] = request.host
    logging_info["request_id"] = request.request_id
    logging_info["action_path"] = request.path_info

    # Log the instance_hostname for this configuration, if available;
    # otherwise the hostname used by the user is used.
    logging_info["instance_hostname"] = request.configuration.get(
        "instance_hostname", request.host
    )

    try:
        logging_info["session_id"] = request.session_id
    except AttributeError:
        logging_info["session_id"] = "<sessions not configured>"

    return logging_info


class RequestDataLogger(Base):
    """Tween to add request-specific information to log entries"""

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        logging_info = get_logging_info(request)
        with mdc(**logging_info):
            response = self.handler(request)

        return response


# Add a "req" key, containing the MDC to logging output in minty-pyramid
# applications.
old_factory = logging.getLogRecordFactory()


def log_record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.req = get_mdc()
    return record


logging.setLogRecordFactory(log_record_factory)
