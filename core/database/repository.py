from abc import ABC

from .protocols import AsyncSessionProtocol, ModelProtocol


class BaseRepository(ABC):
    session_factory: AsyncSessionProtocol
    model: ModelProtocol

    @property
    def query(self):
        return select(self.model)

    def _import(self, schema_in: dict):
        """Convert Pydantic schema to dict"""
        if isinstance(schema_in, dict):
            return schema_in
        data = schema_in.dict(exclude_unset=True)
        return data

    def _fill(self, **kwargs):
        return self.model.fill(**kwargs)

    async def from_query(query):
        async with self.session_factory() as session:
            results = await session.execute(query)
        return results.unique().scalars().all()

    async def save(self, obj):
        """Saves the updated model to the current entity db."""
        async with self.session_factory() as session:
            try:
                session.add(obj)
                await session.flush()
                await session.commit()
            except Exception:
                await session.rollback()
                raise
        return obj

    async def create(self, **kwargs):
        item = self._fill(**kwargs)
        created = await self.save(session, item)
        if created:
            created = await self.find(uid=created.uid)
        return created

    # async def save_all(self, items):
    #     async with self.session_factory() as session:
    #         try:
    #             session.add_all(items)
    #             await session.flush()
    #             await session.commit()
    #         except Exception:
    #             await session.rollback()
    #             raise
    #     return items

    # async def delete(self, obj):
    #     async with self.session_factory() as session:
    #         await session.delete(obj)
    #         await session.flush()
    #         await session.commit()

    # async def destroy(self, *ids):
    #     for uid in ids:
    #         obj = await self.find(uid)
    #         if obj:
    #             await self.delete(obj)

    #     async with self.session_factory() as session:
    #         await session.flush()

    # async def find(self, uid):
    #     stmt = self.query.where(self.model.uid == uid)
    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt)
    #     one_or_none = results.scalars().one_or_none()
    #     return one_or_none

    # async def first_where(cls, **kwargs):
    #     """Return the first value in database based on given args.
    #     Example:
    #         User.get(uid=5)
    #     """
    #     stmt = self.query.where(**kwargs)
    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt)
    #     found = results.scalars().first()
    #     return found

    # async def all(self):
    #     async with self.session_factory() as session:
    #         result = await session.execute(self.query)
    #     _all = result.scalars().all()
    #     return _all

    # async def all_where(self, **kwargs):
    #     stmt = self.where(**kwargs)
    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt)
    #     return results.unique().scalars().all()

    # async def find_or_fail(self, uid):
    #     result = await self.find(uid)
    #     if result:
    #         return result
    #     else:
    #         raise ValueError(
    #             "{self.model.__name__} with uid '{uid}' was not found"
    #         )

    # async def bulk_create(self, items: List):
    #     """
    #     @param items a list of Pydantic models
    #     """
    #     to_save = []
    #     for data in items:
    #         to_save.append(self._fill(**self._import(data)))
    #     return await cls.save_all(to_save)

    # async def update(self, **kwargs):
    #     """Returns a new get instance of the class
    #     This is so that mutations can work well and prevent async IO issues
    #     """
    #     fill = self._fill(**kwargs)
    #     updated = await self.save(fill)
    #     if updated:
    #         updated = await self.find(uid=updated.uid)
    #     return updated

    # async def bulk_update_where(self, update_data: List, filters: Dict):
    #     """
    #     @param update_data a List of dictionary update values.
    #     @param filters is a dict of filter values.
    #     e.g [{'uid': 34, update_values}, ...]
    #     """
    #     to_update = [self._import(data) for data in update_data]

    #     query = update(self.model).where(filters).values(
    #         to_save).execution_options(synchronize_session="fetch")
    #     # query = smart_query(query=update(cls), filters=filters)
    #     # query = query.values(to_update).execution_options(
    #     #     synchronize_session="fetch")

    #     async with self.session_factory() as session:
    #         results = await session.execute(query)
    #     updated = results.scalars().all()
    #     return updated

    # async def bulk_update_with_mappings(self, mappings: List) -> None:
    #     """
    #     @param mappings a List of dictionary update values with pks.
    #     e.g [{'uid': 34, update_values}, ...]
    #     ?? there must be zero many-to-many relations
    #     NB: Function does not return anything
    #     """
    #     if len(mappings) == 0:
    #         return

    #     from sqlalchemy.sql.expression import bindparam

    #     to_update = [self._import(data) for data in mappings]
    #     for item in to_update:
    #         item["_uid"] = item["uid"]

    #     query = update(self.model).where(self.model.uid == bindparam("_uid"))

    #     binds = {}
    #     for key in to_update[0]:
    #         if key != "_uid":
    #             binds[key] = bindparam(key)

    #     stmt = query.values(binds).execution_options(
    #         synchronize_session="fetch")

    #     async with self.session_factory() as session:
    #         await session.execute(stmt, to_update)
    #         await session.flush()
    #         await session.commit()

    # @classmethod
    # async def table_insert(self, table, mappings):
    #     """
    #     @param mappings a dictionary update values.
    #     e.g {'name': 34, 'day': "fff"}
    #     """
    #     async with self.session_factory() as session:
    #         stmt = table.insert()
    #         await session.execute(stmt, mappings)
    #         await session.commit()
    #         await session.flush()

    # @classmethod
    # async def get_related(cls, related: Optional[list] = None, list=False, **kwargs):
    #     """Return the first value in database based on given args."""
    #     try:
    #         del kwargs["related"]
    #     except KeyError:
    #         pass

    #     try:
    #         del kwargs["list"]
    #     except KeyError:
    #         pass

    #     stmt = self.where(**kwargs)
    #     if related:
    #         stmt.options(selectinload(related))

    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt)

    #     if not list:
    #         found = results.scalars().first()
    #     else:
    #         found = results.scalars().all()

    #     return found

    # async def count_where(self, filters):
    #     """
    #     :param filters:
    #     :return: int
    #     """
    #     filter_stmt = smart_query(query=self.query, filters=filters)
    #     count_stmt = select(func.count(filter_stmt.c.uid)
    #                         ).select_from(filter_stmt)
    #     async with self.session_factory() as session:
    #         res = await session.execute(count_stmt)
    #     count = res.scalars().one()
    #     return count

    # @classmethod
    # async def fulltext_search(cls, search_string, field):
    #     """Full-text Search with PostgreSQL"""
    #     stmt = cls.query.filter(
    #         func.to_tsvector("english", getattr(cls.model, field)).match(
    #             search_string, postgresql_regconfig="english"
    #         )
    #     )
    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt)
    #     search = results.scalars().all()
    #     return search

    # @classmethod
    # async def get_by_uids(cls, uids: List[Any]):

    #     stmt = select(cls).where(cls.uid.in_(uids))  # type: ignore

    #     async with self.session_factory() as session:
    #         results = await session.execute(stmt.order_by(cls.uid))

    #     return results.scalars().all()

    # @classmethod
    # async def stream_by_uids(cls, uids: List[Any]) -> AsyncIterator[Any]:

    #     stmt = select(cls).where(cls.uid.in_(uids))  # type: ignore

    #     async with self.session_factory() as session:
    #         stream = await session.stream(stmt.order_by(cls.uid))
    #     async for row in stream:
    #         yield row

    # @classmethod
    # async def stream_all(cls) -> AsyncIterator[Any]:
    #     stmt = select(cls)
    #     async with self.session_factory() as session:
    #         stream = await session.stream(stmt.order_by(cls.uid))
    #     async for row in stream:
    #         yield row

    # # https://engage.so/blog/a-deep-dive-into-offset-and-cursor-based-pagination-in-mongodb/
    # # https://medium.com/swlh/how-to-implement-cursor-pagination-like-a-pro-513140b65f32

    # @classmethod
    # async def paginate_with_cursors(
    #     cls,
    #     page_size: int = None,
    #     after_cursor: Any = None,
    #     before_cursor: Any = None,
    #     filters: Any = None,
    #     sort_by: List[str] = None,
    #     get_related: str = None,
    # ) -> PageCursor:
    #     if not filters:
    #         filters = {}

    #     # get total count without paging filters from cursors
    #     total_count: int = await cls.count_where(filters=filters)
    #     total_count = total_count if total_count else 0

    #     cursor_limit = {}
    #     if has_value_or_is_truthy(after_cursor):
    #         cursor_limit = {"uid__gt": cls.decode_cursor(after_cursor)}

    #     if has_value_or_is_truthy(before_cursor):
    #         cursor_limit = {"uid__lt": cls.decode_cursor(before_cursor)}

    #     # add paging filters
    #     _filters = None
    #     if isinstance(filters, dict):
    #         _filters = [{sa_or_: cursor_limit},
    #                     filters] if cursor_limit else filters
    #     elif isinstance(filters, list):
    #         _filters = filters
    #         if cursor_limit:
    #             _filters.append({sa_or_: cursor_limit})

    #     stmt = cls.smart_query(filters=_filters, sort_attrs=sort_by)

    #     if get_related:
    #         stmt = stmt.options(selectinload(get_related))

    #     if page_size:
    #         stmt = stmt.limit(page_size)

    #     async with self.session_factory() as session:
    #         res = await session.execute(stmt)

    #     qs = res.scalars().all()

    #     if qs is not None:
    #         # items = qs[:page_size]
    #         items = qs
    #     else:
    #         qs = []
    #         items = []

    #     has_additional = (
    #         len(items) == page_size if page_size else True
    #     )  # len(qs) > len(items)s
    #     page_info = {
    #         "start_cursor": cls.encode_cursor(items[0].uid) if items else None,
    #         "end_cursor": cls.encode_cursor(items[-1].uid) if items else None,
    #     }
    #     if page_size is not None:
    #         page_info["has_next_page"] = has_additional
    #         page_info["has_previous_page"] = bool(after_cursor)

    #     return PageCursor(
    #         **{
    #             "total_count": total_count,
    #             "edges": cls.build_edges(items=items),
    #             "items": items,
    #             "page_info": cls.build_page_info(**page_info),
    #         }
    #     )

    # @classmethod
    # def build_edges(cls, items: List[Any]) -> List[EdgeNode]:
    #     if not items:
    #         return []
    #     return [cls.build_node(item) for item in items]

    # @classmethod
    # def build_node(cls, item: Any) -> EdgeNode:
    #     return EdgeNode(**{"cursor": cls.encode_cursor(item.uid), "node": item})

    # @classmethod
    # def build_page_info(
    #     cls,
    #     start_cursor: str = None,
    #     end_cursor: str = None,
    #     has_next_page: bool = False,
    #     has_previous_page: bool = False,
    # ) -> PageInfo:
    #     return PageInfo(
    #         **{
    #             "start_cursor": start_cursor,
    #             "end_cursor": end_cursor,
    #             "has_next_page": has_next_page,
    #             "has_previous_page": has_previous_page,
    #         }
    #     )

    # @classmethod
    # def decode_cursor(cls, cursor):
    #     return cursor

    # @classmethod
    # def encode_cursor(cls, identifier: Any):
    #     return identifier
