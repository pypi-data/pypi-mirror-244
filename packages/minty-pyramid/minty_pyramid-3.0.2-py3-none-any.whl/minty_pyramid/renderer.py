# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import datetime
import logging
from minty.entity import Entity, EntityCollection, ValueObject
from pyramid.renderers import JSON
from typing import Any, Dict
from uuid import UUID

logger = logging.getLogger(__name__)


class jsonapi(JSON):
    jsonapi_adapters = {
        Entity: "_entity_adapter",
        EntityCollection: "_entity_collection_adapter",
        ValueObject: "_value_object_adapter",
        set: "_set_adapter",
        UUID: "_uuid_adapter",
        datetime.datetime: "_datetime_adapter",
        datetime.date: "_datetime_adapter",
    }
    view: Any

    def __init__(self, *args, **kwargs):
        """Constructs the jsonapi class based on Pyramid JSON implementation.

        This will add some default adapters to the system, to handle entities,
        value objects, etc.
        """

        super().__init__(*args, **kwargs)

        for obj, adapter in self.jsonapi_adapters.items():
            self.add_adapter(obj, getattr(self, adapter))

    def __call__(self, info):
        """Returns a plain JSON-encoded string with content-type
        ``application/json``. The content-type may be overridden by
        setting ``request.response.content_type``."""

        # We had top copy this from the Pyramid JSON implementation, because
        # we would like to inject the view on self, so we can use the view
        # class in adapters for generating urls for example
        def _render(value, system):
            request = system.get("request")
            self.view = system.get("view")

            if request is not None:
                response = request.response
                ct = response.content_type
                if ct == response.default_content_type:
                    response.content_type = "application/json"
            default = self._make_default(request)

            return self.serializer(value, default=default, **self.kw)

        return _render

    def _entity_collection_adapter(self, obj, request):
        return [entity for entity in obj]

    def __links_for_entity(self, entity):
        if not hasattr(self.view, "create_link_from_entity"):
            logger.warning(f"Unknown kind of view: {self.view.__module__}")
        self_link = self.view.create_link_from_entity(entity)
        if self_link:
            return {"links": {"self": self_link}}
        else:
            return {}

    def __add_nested_relationships(
        self, relationshipcontent, relationship_response
    ):
        # Retrieve nested relationships within a relationship
        if getattr(relationshipcontent, "entity_relationships", []):
            # Add new field 'relationships' to relationship_response for nested relationships
            relationship_response["relationships"] = {}

            for (
                nested_relationship_name
            ) in relationshipcontent.entity_relationships:
                nested_relationship = getattr(
                    relationshipcontent, nested_relationship_name
                )

                if nested_relationship is None:
                    continue

                # Fill in meta data for nested relationship
                metadata = {}
                if nested_relationship.entity_meta_summary is not None:
                    metadata["meta"] = {
                        "summary": nested_relationship.entity_meta_summary
                    }

                # Add nested relationship to 'relationships' field of relationship_response
                relationship_response["relationships"].update(
                    {
                        nested_relationship_name: {
                            "data": {
                                "type": nested_relationship.entity_type,
                                "id": nested_relationship.entity_id,
                            },
                            **metadata,
                            **self.__links_for_entity(nested_relationship),
                        }
                    }
                )

    def __build_relationships_for_entity(self, obj: Entity, object_attributes):
        object_relationships: Dict[str, Any] = {}

        # Retrieve relationships from entity
        for relationshipkey in obj.entity_relationships:
            relationship = getattr(obj, relationshipkey)
            if relationship is not None:
                list_of_relationships = []
                is_list = None
                if isinstance(relationship, list):
                    list_of_relationships = relationship
                    is_list = True
                else:
                    list_of_relationships = [relationship]

                for relationshipcontent in list_of_relationships:
                    relationshipdata = relationshipcontent.dict()
                    metadata = {}
                    meta_content = self._build_meta(relationshipcontent)
                    if meta_content:
                        metadata["meta"] = meta_content

                    relationship_response = {
                        "data": {
                            "type": relationshipdata["entity_type"],
                            "id": relationshipdata["entity_id"],
                        },
                        **metadata,
                        **self.__links_for_entity(relationshipcontent),
                    }

                    self.__add_nested_relationships(
                        relationshipcontent, relationship_response
                    )

                    if not is_list:
                        object_relationships[
                            relationshipkey
                        ] = relationship_response
                    else:
                        if relationshipkey not in object_relationships:
                            object_relationships[relationshipkey] = []

                        object_relationships[relationshipkey].append(
                            relationship_response
                        )

            del object_attributes[relationshipkey]
        return object_relationships

    def _entity_adapter(self, obj: Entity, request):
        """Transforms an entity in a JSON:API styled format

        See renderers documentation of Pyramid for more information about
        using adapters
        """

        object_attributes = obj.entity_dict()
        object_relationships = self.__build_relationships_for_entity(
            obj, object_attributes
        )

        for entity_id__field in obj.entity_id__fields:
            del object_attributes[entity_id__field]

        relationships_block = {}
        if object_relationships != {}:
            relationships_block["relationships"] = object_relationships

        result = {
            "type": obj.entity_type,
            "id": obj.entity_id,
            "attributes": object_attributes,
            **relationships_block,
            **self.__links_for_entity(obj),
        }
        meta = self._build_meta(obj)
        if meta:
            result["meta"] = meta

        return result

    def _build_meta(self, obj: Entity) -> dict:
        meta = {}
        for field_name in obj.entity_meta__fields:
            short_field_name = field_name.replace("entity_meta_", "")
            value = getattr(obj, field_name)
            if value is not None:
                meta[short_field_name] = value

        return meta

    def _set_adapter(self, obj, request):
        return list(sorted(obj))

    def _uuid_adapter(self, obj, request):
        """Transforms a UUID in a JSONApi styled format"""
        return str(obj)

    def _datetime_adapter(self, obj, request):
        """Transforms a datetime object in a JSONApi styled format"""
        return obj.isoformat()

    def _value_object_adapter(self, obj: ValueObject, request):
        """Transforms a ValueObject in a JSONApi styled format

        See renderers documentation of Pyramid for more information about
        using adapters
        """
        logger = logging.getLogger(__name__)
        logger.info(f"XXX {obj}")
        return obj.dict(by_alias=True)
