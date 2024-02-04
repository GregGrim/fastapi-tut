# Clean Code rules:

Ref: [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) and [Summary](https://gist.githubusercontent.com/wojteklu/73c6914cc446146b8b533c0988cf8d29/raw/c7a44d774fc3b09a0d5f0f58888550ba0ac694b9/clean_code.md)

Code is clean if it can be understood easily – by everyone on the team. Clean code can be read and enhanced by a developer other than its original author. With understandability comes readability, changeability, extensibility and maintainability.
___________________________


## General rules

1. Follow standard conventions.
2. Keep it simple stupid. Simpler is always better. Reduce complexity as much as possible.
3. Boy scout rule. Leave the campground cleaner than you found it.
4. Always find root cause. Always look for the root cause of a problem.

## Design rules

1. Keep configurable data at high levels.
2. Prefer polymorphism to if/else or switch/case.
3. Separate multi-threading code.
4. Prevent over-configurability.
5. Use dependency injection.
6. Follow Law of Demeter. A class should know only its direct dependencies.

## Understandability tips

1. Be consistent. If you do something a certain way, do all similar things in the same way.
2. Use explanatory variables.
3. Encapsulate boundary conditions. Boundary conditions are hard to keep track of. Put the processing for them in one place.
4. Prefer dedicated value objects to primitive type.
5. Avoid logical dependency. Don't write methods which works correctly depending on something else in the same class.
6. Avoid negative conditionals.

## Names rules

1. Choose descriptive and unambiguous names.
2. Make meaningful distinction.
3. Use pronounceable names.
4. Use searchable names.
5. Replace magic numbers with named constants.
6. Avoid encodings. Don't append prefixes or type information.

## Functions rules

1. Small.
2. Do one thing.
3. Use descriptive names.
4. Prefer fewer arguments.
5. Have no side effects.
6. Don't use flag arguments. Split method into several independent methods that can be called from the client without the flag.

## Comments rules

1. Always try to explain yourself in code.
2. Don't be redundant.
3. Don't add obvious noise.
4. Don't use closing brace comments.
5. Don't comment out code. Just remove.
6. Use as explanation of intent.
7. Use as clarification of code.
8. Use as warning of consequences.

## Source code structure

1. Separate concepts vertically.
2. Related code should appear vertically dense.
3. Declare variables close to their usage.
4. Dependent functions should be close.
5. Similar functions should be close.
6. Place functions in the downward direction.
7. Keep lines short.
8. Don't use horizontal alignment.
9. Use white space to associate related things and disassociate weakly related.
10. Don't break indentation.

## Objects and data structures

1. Hide internal structure.
2. Prefer data structures.
3. Avoid hybrids structures (half object and half data).
4. Should be small.
5. Do one thing.
6. Small number of instance variables.
7. Base class should know nothing about their derivatives.
8. Better to have many functions than to pass some code into a function to select a behavior.
9. Prefer non-static methods to static methods.

## Tests

1. One assert per test.
2. Readable.
3. Fast.
4. Independent.
5. Repeatable.

## Code smells

1. Rigidity. The software is difficult to change. A small change causes a cascade of subsequent changes.
2. Fragility. The software breaks in many places due to a single change.
3. Immobility. You cannot reuse parts of the code in other projects because of involved risks and high effort.
4. Needless Complexity.
5. Needless Repetition.
6. Opacity. The code is hard to understand.

# Clean architecture rules:

> [!IMPORTANT] 
> Read full [ARTICLE](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

![clean architecture onion](https://github.com/GregGrim/fastapi-tut/assets/36775237/9f80fd0d-082a-4805-a808-c3803daf2fb1)

## Here will be a quick example of a structure of our code.


### Routers

```python
from typing import Annotated

from fastapi import APIRouter, Depends


from .dependencies import get_pagination, get_use_case
from .entities import Item
from .schemas import Paginated, Pagination
from .use_cases import ItemListUseCase


router = APIRouter(prefix="/item")
@router.get("/list", response_model=Paginated[Item])
def get_list(
    item_list_use_case: Annotated[ItemListUseCase, Depends(get_use_case)],
    pagination: Annotated[Pagination, Depends(get_pagination)],
):
    items = item_list_use_case.execute(pagination.page, pagination.limit)
    return Paginated(items=items, count=len(items))
```

### Entities

```python
from pydantic import UUID4, BaseModel


class Item(BaseModel):
    id: UUID4
    name: str
    properties: list[str] = []
```

### Schemas

```python
from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")

class Paginated(BaseModel, Generic[T]):
    items: list[T]
    count: int


class Pagination(BaseModel):
    page: int
    limit: int
```

### Use Cases

```python
from .entities import Item
from .gateways import ItemGateway
from .repositories import ItemRepository


class ItemListUseCase:
    def __init__(self, item_repository: ItemRepository, item_gateway: ItemGateway):
        self.item_repository = item_repository
        self.item_gateway = item_gateway
    
    def execute(self, page: int, limit: int) -> list[Item]:
        # BUSINESS LOGIC
        items = self.item_repository.get_list(page, limit)

        for item in items:
            item.properties = self.item_gateway.get_properties(str(item.id))
        
        return items
```

### Repositories

```python
import sqlalchemy as sa
from sqlalchemy.orm import Session

from .entities import Item
from .models import ItemModel


class ItemRepository:
    def __init__(self, engine) -> None:
        self.engine = engine
    
    def get_list(self, page: int, limit: int) -> list[Item]:
        with Session(self.engine) as session:
            stmt = sa.select(ItemModel).offset((page - 1) * limit).limit(limit)
            db_items = session.scalars(stmt).all()
            return [Item(id=itm.id, name=itm.name) for itm in db_items]
```

#### ORM models (for relation DBs)

```python
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()  # only for demo

class ItemModel(BaseModel):
    tablename = "item"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
    )
    name = sa.Column(sa.Text())
````

#### Gateways
```python
class ItemGateway:
    def __init__(self, client: ...):
        self.client = client
    
    def get_properties(self, id: str) -> list[str]:
        resp = self.client.get("URL", params={"id": id})
        return [item["prop"] for item in resp.json()]
```

### Dependencies

```python
from typing import Annotated
from fastapi import Depends, Query
from tmp.gateways import ItemGateway

from tmp.repositories import ItemRepository
from tmp.use_cases import ItemListUseCase

from .schemas import Pagination


def get_pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=0),
):
    return Pagination(page=page, limit=limit)


def get_repository(engine: ...):
    ...


def get_gateway(client: ...):
    ...


def get_use_case(
    repository: Annotated[ItemRepository, Depends(get_repository)],
    gateway: Annotated[ItemGateway, Depends(get_gateway)],
) -> ItemListUseCase:
    return ItemListUseCase(repository, gateway)
```
