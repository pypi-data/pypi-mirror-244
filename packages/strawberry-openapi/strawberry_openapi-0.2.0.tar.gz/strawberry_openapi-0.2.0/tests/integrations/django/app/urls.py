from __future__ import annotations

import strawberry
from tests.conftest import Mutation, Query

from sourcetypes import graphql
from strawberry_openapi.django import DjangoOpenAPI

operation: graphql = """
query GetUser($id: ID!) @endpoint(url: "/users/$id", method: "GET") {
    user(id: $id) {
        id
    }
}
"""

delete_operation: graphql = """
mutation DeleteUser($id: ID!) @endpoint(url: "/users/$id", method: "DELETE") {
    deleteUser(id: $id)
}
"""

schema = strawberry.Schema(query=Query, mutation=Mutation)

rest_api = DjangoOpenAPI(schema=schema, documents=[operation, delete_operation])


urlpatterns = rest_api.paths
