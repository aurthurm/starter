import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import (GRAPHQL_TRANSPORT_WS_PROTOCOL,
                                      GRAPHQL_WS_PROTOCOL)

from api.graphql.schema import gql_schema  # noqa
from api.rest.v1 import api_router  # noqa
from core.config import settings  # noqa
from core.database.db import get_sync_engine
from core.graphql.acquire import get_graphql_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_app_events(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        ...

    @app.on_event("shutdown")
    async def shutdown():
        ...


def register_app_middlewares(app: FastAPI):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_app_publics(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)
    graphql_app = GraphQLRouter(
        gql_schema,
        subscription_protocols=[GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL],
        graphiql=settings.DEBUG,
        context_getter=get_graphql_context,
    )
    app.include_router(
        graphql_app,
        prefix="/graphql",
        include_in_schema=False,
    )
    app.add_websocket_route("/graphql", graphql_app, "app-subscriptions")


def register_app_tracing(app: FastAPI):
    if settings.RUN_OPEN_TRACING:
        logging.info(
            f"Open Tracing activated :) Sending to: {settings.OTLP_SPAN_EXPORT_URL}"
        )
        resource = Resource(attributes={"service.name": "FelicityLIMS"})
        tracer = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer)
        tracer.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.OTLP_SPAN_EXPORT_URL))
        )

        LoggingInstrumentor().instrument()
        FastAPIInstrumentor.instrument_app(app)

        SQLAlchemyInstrumentor().instrument(
            engine=get_sync_engine(),
        )


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    register_app_events(app)
    register_app_middlewares(app)
    register_app_publics(app)
    register_app_tracing(app)

    return app
