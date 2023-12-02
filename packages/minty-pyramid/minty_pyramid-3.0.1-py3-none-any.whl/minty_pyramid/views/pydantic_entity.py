# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import logging
import re
from minty.cqrs import UserInfo
from minty.entity import RedirectResponse
from minty.validation import assert_never
from minty_pyramid.session_manager import (
    check_user_permission,
    get_logged_in_user,
)
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden
from pyramid.response import Response
from typing import Dict, Literal, Optional, Set, TypedDict, Union
from uuid import UUID

log = logging.getLogger(__name__)

# Default page size if none is specified.
# Note that this is a str() because it's a default for a query parameter.
DEFAULT_PAGE_SIZE = str(50)


SupportedHTTPMethods = Literal["GET", "POST"]
CQType = Literal["command", "query"]


# Until PEP-655 lands, we need this workaround for optional keys in a TypedDict
class FromDefinition(TypedDict, total=False):
    request_params: dict
    json: dict


class PagingDefinitionBase(TypedDict):
    max_results: int


class PagingDefinition(PagingDefinitionBase, total=False):
    page: Literal["page"]
    page_size: Literal["page_size"]


ViewMappingBase = TypedDict(
    "ViewMappingBase",
    {
        "cq": CQType,
        "auth_permissions": Set[str],
        "domain": str,
        "run": str,
        "from": FromDefinition,
    },
)


class ViewMapping(ViewMappingBase, total=False):
    entity_type: str
    command_primary: str
    paging: PagingDefinition


ViewMapper = Dict[SupportedHTTPMethods, Dict[str, ViewMapping]]


# This will be moved to minty-pyramid in a next iteration
class JSONAPIEntityView:
    """
    View Base class for Pyramid Views which return Entity objects

    Use this as a base class for your own view. E.g.

        class DogView(JSONAPIEntityView):
            view_mapper = {
                "GET": {
                    "get_dog": {
                        "cq": "query",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "get_dog_by_uuid",
                        "from": {"request_params": {"uuid": "uuid"}},
                    },
                    "filter_dogs": {
                        "cq": "query",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "get_dog_by_uuid",
                        "from": {"request_params": {"filter[]": "filter_params"}},
                    }
                },
                "POST": {
                    "create_dog": {
                        "cq": "command",
                        "auth_permissions": ["gebruiker"],
                        "domain": "zsnl_domains.case_management",
                        "run": "create_dog",
                        "from": {
                            "request_params": {"uuid": "uuid"},
                            "json": {"_all": True},
                        },
                        "command_primary": "uuid",
                        "entity_type": "dog",
                    }
                }
            }

            def create_link_from_entity(
                self, entity=None, entity_type=None, entity_id=None
            ):
                if entity is not None:
                    entity_type = entity.entity_type
                    entity_id = str(entity.entity_id)

                if entity_type == "dog":
                    return self.request.route_url(
                        "get_dog_object", _query={"uuid": entity_id}, _scheme="https"
                    )

    The view_mappers has as it's first key the method of the API call, e.g.
    POST or GET. Define the action in the url as the first key of the following
    dict (get_dog, create_dog) in the above example.

    Other parameters:
        cq (Enum("query", "command")):  Defines whether to call on the Query or
                                        Command class
        auth_permissions (Set[str]): The list of permissions to check
        domain (str): The domain to run this command or query against
        run (str): the command or query to run
        from (dict): A dict of parameters, see below
        command_primary (str):  The "reference" of the command extracted from
                                the given "parameter
        entity_type (str):  The string entity_type, so we know when we got no
                            Entity as a return value, which type to set

    The "from" parameter extracts input parameters from either the given
    "request_parameters" or the "json_body" of the request. The following
    dict contains a key value pair. The key correspondents to the key from the
    input. The value correspondents to the key for the command to run.

    Using array[] options in request_params:
    When a key of a request_params ends with the characters [] (e.g.: see
    filter_dogs above), then it will transform the variables into a dict.

    For instance: ?filter[name]=frits&filter[gender]=male
    Will transform into:
        {
            "name": "frits",
            "gender": "male"
        }

    """

    view_mapper: ViewMapper

    def __init__(self, context, request):
        """Initializes this object from Pyramid"""

        self.request = request
        self.call = request.matched_route.name

    def _check_protected_route(self, calldata):
        """Verifies authentication permissions against our session"""

        user_info = get_logged_in_user(self.request, log)
        if not check_user_permission(calldata["auth_permissions"], user_info):
            raise HTTPForbidden(
                json={"error": "You do not have permission to access this."}
            )

        return user_info

    def _get_cqrs_instance(self, calldata: ViewMapping, user_info: UserInfo):
        """Gets the command or query instance for the called api view"""
        cq = calldata["cq"]

        cmdqry = getattr(self.request, f"get_{cq}_instance")
        return cmdqry(
            domain=calldata["domain"],
            user_info=user_info,
            user_uuid=user_info.user_uuid,
        )

    def __call__(self):
        """Reads and runs the called API route defined in view_mapper"""

        calldata = self.view_mapper[self.request.method][self.call]

        user_info = self._check_protected_route(calldata)
        cqinstance = self._get_cqrs_instance(calldata, user_info)

        run = getattr(cqinstance, calldata["run"])
        params = self._collect_params(calldata)

        response = run(**params)

        return self.transform_response_from_command_or_query(
            response, calldata, params
        )

    def transform_response_from_entity(
        self, entity_type: str, entity_id: UUID
    ):
        """Transform response from entity"""

        link = self.create_link_from_entity(
            entity_type=entity_type,
            entity_id=entity_id,
        )

        if link:
            links_block = {"links": {"self": link}}
        else:
            links_block = {}

        return {
            **links_block,
            "type": entity_type,
            "id": entity_id,
        }

    def transform_response_from_command(
        self, calldata: ViewMapping, params
    ) -> dict:
        """Transform response from command"""

        if "command_primary" not in calldata or "entity_type" not in calldata:
            return {"data": None}

        if params.get(calldata["command_primary"], None):
            call_definition_entity_type = calldata["entity_type"]

            try:
                entity_type = params[call_definition_entity_type]
            except KeyError:
                entity_type = call_definition_entity_type

            if isinstance(params[calldata["command_primary"]], list):
                res = []
                for entity_id in params[calldata["command_primary"]]:
                    res.append(
                        self.transform_response_from_entity(
                            entity_type, entity_id
                        )
                    )
            else:
                entity_id = params[calldata["command_primary"]]
                res = self.transform_response_from_entity(
                    entity_type, entity_id
                )
            return {"data": res}
        else:
            return {"data": None}

    def transform_response_from_query(self, response) -> Union[dict, Response]:
        """Transform response from query"""
        if response is None:
            return {"data": None}
        elif isinstance(response, RedirectResponse):
            return Response(status_int=302, location=response.location)
        else:
            json_response = {
                "data": response,
                "links": {"self": self.request.current_route_path()},
            }
            self._apply_included_entities(response, json_response)
            self._apply_meta(response, json_response)
            return json_response

    def transform_response_from_command_or_query(
        self, response, calldata: ViewMapping, params
    ) -> Optional[Union[dict, Response]]:
        """
        Transforms a response from a command to a proper JSONApi structure

        Args:
            response (Optional[Entity]): The response from our query or command
            calldata (dict): The configuration defined in our view_mapper
            params (dict): The collected parameters from our query and jsonbody

        Returns:
            Structured dict for our jsonapi serializer:

                {
                    "data": {
                        "links": {
                            "self": "http://url",
                        },
                        "type": "name_of_entity",
                        "id": "12434-abcde-1234-acbewe-233aba"
                    }
                }

        """
        if calldata["cq"] == "command":
            return self.transform_response_from_command(calldata, params)
        elif calldata["cq"] == "query":
            return self.transform_response_from_query(response)

        assert_never(calldata["cq"])  # pragma: no cover

    def _apply_meta(self, response, json_response: dict):
        """Add meta data to json_response if available"""

        if (
            hasattr(response, "total_results")
            and response.total_results is not None
        ):
            json_response["meta"] = {"total_results": response.total_results}

    def _apply_included_entities(self, response, json_response: dict):
        if (
            hasattr(response, "included_entities")
            and response.included_entities is not None
        ):
            json_response["included"] = response.included_entities

    def _collect_params_as_array(self, k, v, params):
        for pk, pv in self.request.params.items():
            match = re.search(r"^" + k + r"\[([^\]]+)\]$", pk)

            if match:
                if v not in params:
                    params[v] = {}

                params[v][match[1]] = pv

    def _convert_value(self, request_param, domain_param_config):
        param_key = domain_param_config["name"]
        param_type = domain_param_config["type"]

        try:
            param_value = param_type(request_param)
        except ValueError:
            # View mapper defined a type, but the parameter can't be converted from
            # string to that type.
            raise HTTPBadRequest

        return (param_key, param_value)

    def _extract_request_params(self, calldata, request_params):
        final_params = {}

        for http_param_name, domain_param_name in calldata["from"][
            "request_params"
        ].items():
            # Special array functionality
            if http_param_name.endswith("[]"):
                http_param_name = http_param_name.replace("[]", "")
                self._collect_params_as_array(
                    http_param_name, domain_param_name, final_params
                )

                continue

            if http_param_name not in request_params:
                continue

            if isinstance(domain_param_name, dict):
                (domain_param, converted_value) = self._convert_value(
                    request_param=request_params[http_param_name],
                    domain_param_config=domain_param_name,
                )
                final_params[domain_param] = converted_value
            else:
                final_params[domain_param_name] = request_params[
                    http_param_name
                ]

        return final_params

    def _collect_params(self, calldata):
        """Collects parameters according to the configuration in view_mapper"""
        params = {}

        if "request_params" in calldata["from"]:
            params = self._extract_request_params(
                calldata, self.request.params
            )

        if "json" in calldata["from"]:
            if (
                "_all" in calldata["from"]["json"]
                and calldata["from"]["json"]["_all"] is True
            ):
                for k in self.request.json_body.keys():
                    params[k] = self.request.json_body[k]
            else:
                for k, v in calldata["from"]["json"].items():
                    if k not in self.request.json_body:
                        continue
                    params[v] = self.request.json_body[k]

        if "paging" in calldata:
            paging_params = self._extract_paging_params(
                calldata, self.request.params
            )
            params.update(paging_params)

        return params

    def create_link_from_entity(
        self, entity=None, entity_type=None, entity_id=None
    ) -> Optional[str]:
        log.debug(
            "create_link_from_entity called, but not overridden in view class"
        )
        return None

    def _extract_paging_params(self, calldata, request_params):
        final_params = {}
        final_params["page"] = request_params.get("page", "1")
        final_params["page_size"] = request_params.get(
            "page_size", DEFAULT_PAGE_SIZE
        )

        self._check_paging_limits(
            int(final_params["page"]),
            int(final_params["page_size"]),
            int(calldata["paging"]["max_results"]),
        )
        return final_params

    def _check_paging_limits(
        self, page: int, page_size: int, max_results: int
    ):
        if page < 1:
            raise HTTPBadRequest(
                json={"errors": [{"title": "'page' must be >= 1"}]}
            )

        if page_size < 1:
            raise HTTPBadRequest(
                json={"errors": [{"title": "'page_size' must be >= 1"}]}
            )

        if page_size > max_results:
            raise HTTPBadRequest(
                json={
                    "errors": [
                        {
                            "title": f"Requested page size {page_size} > max size {max_results}."
                        }
                    ]
                }
            )
