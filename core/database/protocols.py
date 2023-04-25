from typing import Any, AsyncIterator, Dict, List, Optional, Protocol


class AsyncSessionProtocol(Protocol):
    async def refresh(self, instance, attribute_names=None, with_for_update=None):
        ...

    async def run_sync(self, fn, *arg, **kw):
        ...

    async def execute(
        self, statement, params=None, execution_options={}, bind_arguments=None, **kw
    ):
        ...

    async def scalar(
        self, statement, params=None, execution_options={}, bind_arguments=None, **kw
    ):
        ...

    async def scalars(
        self, statement, params=None, execution_options={}, bind_arguments=None, **kw
    ):
        ...

    async def get(
        self,
        entity,
        ident,
        options=None,
        populate_existing=False,
        with_for_update=None,
        identity_token=None,
    ):
        ...

    async def stream(
        self, statement, params=None, execution_options={}, bind_arguments=None, **kw
    ):
        ...

    async def stream_scalars(
        self, statement, params=None, execution_options={}, bind_arguments=None, **kw
    ):
        ...

    async def delete(self, instance):
        ...

    async def merge(self, instance, load=True, options=None):
        ...

    async def flush(self, objects=None):
        ...

    def get_transaction(self):
        ...

    def get_nested_transaction(self):
        ...

    def get_bind(self, mapper=None, clause=None, bind=None, **kw):
        ...

    async def connection(self, **kw):
        ...

    def begin(self, **kw):
        ...

    def begin_nested(self, **kw):
        ...

    async def rollback(self):
        ...

    async def commit(self):
        ...

    async def close(self):
        ...

    async def invalidate(self):
        ...

    @classmethod
    async def close_all(self):
        ...


class ModelProtocol(Protocol):
    uid: str

    def fill(self, **kwargs):
        ...

    def marshal_simple(self, exclude=None) -> dict:
        ...

    def marshal_nested(self, obj=None):
        ...


class RepositoryProtocol(Protocol):
    def _import(self, **kwargs):
        ...

    def _fill(self, **kwargs):
        ...

    @classmethod
    async def all_by_page(cls, page: int = 1, limit: int = 20, **kwargs) -> Dict:
        ...

    async def delete(self):
        ...

    @classmethod
    async def destroy(cls, *ids):
        ...

    @classmethod
    async def all(cls):
        ...

    @classmethod
    async def first(cls):
        ...

    @classmethod
    async def find(cls, id_):
        ...

    @classmethod
    async def find_or_fail(cls, id_):
        ...

    @classmethod
    async def get(cls, **kwargs):
        ...

    @classmethod
    async def create(cls, **kwargs):
        ...

    @classmethod
    async def bulk_create(cls, items: List):
        ...

    async def update(self, **kwargs):
        ...

    @classmethod
    async def bulk_update_where(cls, update_data: List, filters: Dict):
        ...

    @classmethod
    async def bulk_update_with_mappings(cls, mappings: List) -> None:
        ...

    @classmethod
    async def table_insert(cls, table, mappings):
        ...

    @classmethod
    async def get_related(cls, related: Optional[list] = None, list=False, **kwargs):
        ...

    @classmethod
    def _import(cls, schema_in: Dict | Any):
        ...

    async def save(self):
        ...

    @classmethod
    async def save_all(cls, items):
        ...

    @classmethod
    async def get_one(cls, **kwargs):
        ...

    @classmethod
    async def get_all(cls, **kwargs):
        ...

    @classmethod
    async def from_smart_query(cls, query):
        ...

    @classmethod
    async def count_where(cls, filters):
        ...

    @classmethod
    async def fulltext_search(cls, search_string, field):
        ...

    @classmethod
    async def get_by_uids(cls, uids: List[Any]):
        ...

    @classmethod
    async def stream_by_uids(cls, uids: List[Any]) -> AsyncIterator[Any]:
        ...

    @classmethod
    async def stream_all(cls) -> AsyncIterator[Any]:
        ...

    @classmethod
    async def paginate_with_cursors(
        cls,
        page_size: int = None,
        after_cursor: Any = None,
        before_cursor: Any = None,
        filters: Any = None,
        sort_by: List[str] = None,
        get_related: str = None,
    ) -> Any:
        ...

    @classmethod
    def build_edges(cls, items: List[Any]) -> List[Any]:
        ...

    @classmethod
    def build_node(cls, item: Any) -> Any:
        ...

    @classmethod
    def build_page_info(
        cls,
        start_cursor: str = None,
        end_cursor: str = None,
        has_next_page: bool = False,
        has_previous_page: bool = False,
    ) -> Any:
        ...

    @classmethod
    def decode_cursor(cls, cursor):
        ...

    @classmethod
    def encode_cursor(cls, identifier: Any):
        ...
