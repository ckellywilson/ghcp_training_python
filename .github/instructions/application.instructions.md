# Application Layer Instructions

Files in the `application/` directory orchestrate domain logic and remain framework-agnostic.

## Use Case Classes

- Each use case should have a single public method (typically `execute`)
- Depend only on domain Protocol interfaces
- Return DTOs, not domain entities directly
- Keep use cases focused and single-purpose

```python
class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self._order_repo = order_repo
        self._product_repo = product_repo
    
    def execute(self, request: CreateOrderDTO) -> OrderDTO:
        # Orchestrate domain logic
        order = Order.create(request.customer_id, request.items)
        self._order_repo.save(order)
        return OrderDTO.from_domain(order)
```

## Data Transfer Objects (DTOs)

- Use Pydantic models for all DTOs
- Separate input DTOs (requests) from output DTOs (responses)
- Include `from_domain()` and `to_domain()` conversion methods
- Keep DTOs in `application/dtos.py`

```python
from pydantic import BaseModel

class CreateOrderDTO(BaseModel):
    customer_id: str
    items: list[OrderItemDTO]

class OrderDTO(BaseModel):
    id: str
    customer_id: str
    total: float
    
    @classmethod
    def from_domain(cls, order: Order) -> "OrderDTO":
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            total=order.calculate_total()
        )
```

## Dependency Management

- Inject dependencies through constructor
- Depend on Protocol interfaces, not concrete implementations
- Make all dependencies explicit

## What NOT to Include

- ❌ FastAPI dependencies or HTTP concerns
- ❌ Database queries or ORM code
- ❌ Direct external service calls
- ❌ Framework-specific annotations
