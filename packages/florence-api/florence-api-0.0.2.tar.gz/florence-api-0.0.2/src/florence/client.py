from enum import Enum
from typing import List, Optional, Any
import os
import json

import requests
from pydantic import BaseModel as PydanticBaseModel


class FlorenceException(Exception):
    """Florence Exception class"""
    pass


class BaseModel(PydanticBaseModel):
    """Base class for all models."""
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        use_enum_values = True
        allow_population_by_field_name = True
        validate_assignment = True


class AuthorizationUrlResponse(BaseModel):
    """Response model for creating a new API key"""
    url: str
    state: str


class AuthenticationTokenRequest(BaseModel):
    """Request model for creating a new API key"""
    state: str


class S3Configuration(BaseModel):
    """S3 Configuration model"""
    preSignedUrl: str


class TextBasedConfiguration(BaseModel):
    """Text Based Configuration model"""
    text: str


class ProviderType(Enum):
    """Provider Type enum"""
    S3 = "S3"
    TEXT = "Text"


class SchemaProvider(BaseModel):
    """Schema Provider model"""
    type: ProviderType
    s3Configuration: Optional[S3Configuration]
    textBasedConfiguration: Optional[TextBasedConfiguration]


class GlossaryProvider(BaseModel):
    """Glossary Provider model"""
    type: ProviderType
    s3Configuration: Optional[S3Configuration]
    textBasedConfiguration: Optional[TextBasedConfiguration]


class DataSource(BaseModel):
    """Data Source model"""
    id: Optional[str]
    name: str
    type: str
    tenantId: str
    schemaProvider: SchemaProvider
    glossaryProvider: Optional[GlossaryProvider]


class DataSources(BaseModel):
    """Data Sources model"""
    dataSources: List[DataSource]


class DataSourceCreationResponse(BaseModel):
    """Data Source Creation Response model"""
    id: str


class APIKey(BaseModel):
    """API Key model"""
    id: str
    value: str
    usagePlanName: str


class ApiKeyCreationRequest(BaseModel):
    """Request model for creating a new API key"""
    usagePlan: str


class ApiKeyCreationResponse(BaseModel):
    """Response model for creating a new API key"""
    key: str


class Tenant(BaseModel):
    """Tenant model"""
    id: Optional[str]
    name: Optional[str]
    email: str
    isActive: Optional[bool] = True
    apiKeys: Optional[List[APIKey]] = []


class InternalResponse(BaseModel):
    """Response model"""
    body: str
    statusCode: int
    headers: dict


class SQLGenerationContext(BaseModel):
    """Represents the context for the SQL generation"""

    database_schema: Optional[str]
    database_type: Optional[str]
    query: str


class SQLQueryContext(BaseModel):
    """Represents the context for the SQL generation"""
    query: str
    tenantId: str
    datasourceId: str


class GeneratedSQL(BaseModel):
    """Represents the generated SQL"""

    sql: str


class UserAuth(BaseModel):
    """User Auth model"""
    state: str
    creationDateTimeInSeconds: int
    idToken: Optional[str]
    accessToken: Optional[str]
    refreshToken: Optional[str]
    expiresIn: Optional[int]


class FlorenceClient:
    """Client for interacting with the Florence API."""

    DEFAULT_API_URL = "https://e6hojy8yq1.execute-api.ap-southeast-1.amazonaws.com/dev"
    DEFAULT_REQUEST_TIMEOUT_IN_SECS = 100
    FLORENCE_API_KEY_ENV_VAR = "FLORENCE_API_KEY"

    def __init__(self, api_key: str = None, api_url: str = None, bearer_token: str = None):
        """Initialise the client."""
        self._api_url = api_url if api_url else FlorenceClient.DEFAULT_API_URL
        api_key_env = os.environ.get(FlorenceClient.FLORENCE_API_KEY_ENV_VAR)
        self._api_key = api_key_env if api_key_env else api_key
        self._bearer_token = bearer_token

    def authorization_url(self) -> AuthorizationUrlResponse:
        """Get the authorization URL."""
        headers = self._request_headers_with_api_key(use_api_key=False)
        response = requests.get(
            f"{self._api_url}/authorization_url", headers=headers,
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, AuthorizationUrlResponse)

    def token(self, token_request: AuthenticationTokenRequest) -> UserAuth:
        """Get the token."""
        headers = self._request_headers_with_api_key(use_api_key=False)
        response = requests.post(
            f"{self._api_url}/auth/token", headers=headers, json=token_request.dict(),
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, UserAuth)

    def add_tenant(self, tenant: Tenant) -> Tenant:
        """Add a new tenant."""
        headers = self._request_headers_with_api_key(use_api_key=False)
        response = requests.post(
            f"{self._api_url}/tenant", headers=headers, json=tenant.dict(),
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, Tenant)

    def add_tenant_api_key(self, tenant_id: str, usage_plan_name: str) -> ApiKeyCreationResponse:
        """Add a new tenant API key."""
        headers = self._request_headers_with_api_key(use_api_key=False)
        response = requests.post(
            f"{self._api_url}/tenant/{tenant_id}/api_key", headers=headers,
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS,
            json=ApiKeyCreationRequest(**{"usagePlan": usage_plan_name}).dict())
        return self._handle_response(response, ApiKeyCreationResponse)

    def add_tenant_datasource(self, datasource: DataSource) -> DataSourceCreationResponse:
        """Add a new tenant datasource."""
        headers = self._request_headers_with_api_key()
        response = requests.post(
            f"{self._api_url}/datasource", headers=headers, json=datasource.dict(),
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSourceCreationResponse)

    def get_tenant_datasources(self, tenant_id: str) -> DataSources:
        """Get tenant datasources."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/datasource/{tenant_id}", headers=headers,
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSources)

    def get_tenant_datasource(self, tenant_id: str, datasource_id: str) -> DataSource:
        """Get a tenant datasource."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/datasource/{tenant_id}/{datasource_id}", headers=headers,
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSource)

    def get_tenant(self, tenant_id: str) -> Tenant:
        """Get a tenant."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/tenant/{tenant_id}", headers=headers,
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, Tenant)

    def get_sql(self, context: SQLQueryContext) -> GeneratedSQL:
        """Get SQL."""
        headers = self._request_headers_with_api_key()
        tenant_id = context.tenantId
        datasource_id = context.datasourceId
        sql_generation_context = SQLGenerationContext(query=context.query)
        response = requests.post(
            f"{self._api_url}/sql/{tenant_id}/{datasource_id}", headers=headers,
            json=sql_generation_context.dict(),
            timeout=FlorenceClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, GeneratedSQL)

    def update_api_key(self, api_key: str) -> None:
        """Update an API key."""
        self._api_key = api_key

    def update_bearer_token(self, bearer_token: str) -> None:
        """Update a bearer token."""
        self._bearer_token = bearer_token

    def _handle_response(self, response: requests.Response, response_model: Any = None) -> [BaseModel, None]:
        """Handle the response from the API."""
        if response.status_code != 200:
            raise FlorenceException(
                f"Error: {response.status_code} - {response.text}")
        response_as_json = response.json()
        print(response_as_json)
        internal_response = InternalResponse(**response_as_json)
        if internal_response.statusCode != 200:
            raise FlorenceException(internal_response.body)
        if not response_model:
            return
        reponse_body_as_dict = json.loads(internal_response.body)
        return response_model(**reponse_body_as_dict)

    def _request_headers_with_api_key(self, use_api_key=True) -> dict:
        """Get the request headers with the API key."""
        headers = {"Content-Type": "application/json"}
        if self._api_key and use_api_key:
            headers["x-api-key"] = self._api_key
        if self._bearer_token:
            headers["Authorization"] = self._bearer_token
        return headers
