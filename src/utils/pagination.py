
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, load_only
from sqlalchemy.orm.strategy_options import _AbstractLoad, _AttrType
from sqlalchemy.sql.selectable import Select


class Page:
    
    def __init__(
            self,
            page: int,
            items_per_page: int,
            filters: dict[str, object],
            *,
            session: AsyncSession,
            pagination: "Pagination",
        ) -> None:

        self.page = page
        self.items_per_page = items_per_page
        self.filters = filters
        self.session = session
        self.pagination = pagination

    async def get_items(self) -> list[dict]:
        query = self.pagination.get_items_query(page=self.calc_page, filters=self.filters)
        result = await self.session.execute(query)
        return list(map(dict, result.mappings().all()))
    
    async def get_count(self) -> int:
        query = self.pagination.get_count_query(filters=self.filters)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_prev(self) -> bool:
        return self.calc_page > 0
    
    async def is_next(self) -> bool:
        return self.page < await self.get_pages_count()
    
    @property
    def calc_page(self) -> int:
        return self.page - 1
    
    async def get_pages_count(self) -> int:
        count = await self.get_count()
        return (count + self.items_per_page - 1) // self.items_per_page


class Pagination:
    def __init__(
            self, 
            model: type[DeclarativeBase],
            load_only_fields: set[_AttrType] | None = None,
            items_per_page: int = 10,
        ) -> None:

        self.model = model
        self.load_only_fields = load_only_fields or set()
        self.items_per_page = items_per_page
    

    def get_items_query(self, page: int, filters: dict[str, object]) -> Select:
        limit = self.items_per_page
        offset = page * self.items_per_page
        _load_only = self._get_load_only()

        return (
            select(self.model)
            .filter_by(**filters)
            .limit(limit)
            .offset(offset)
            .options(_load_only)
        )
    
    def get_count_query(self, filters: dict[str, object]) -> Select:
        return (
            select(func.count())
            .select_from(self.model)
            .filter_by(**filters)
        )
    
    def _get_load_only(self) -> _AbstractLoad:
        return load_only(*self.load_only_fields)
        
    def create_page(self, page: int, *, session: AsyncSession, filters: dict[str, object]) -> Page:
        new_page = Page(
            page=page,
            items_per_page=self.items_per_page,
            filters=filters,
            session=session,
            pagination=self,
        )
        return new_page
