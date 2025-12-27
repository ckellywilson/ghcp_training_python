# Application Layer Instructions

Files in the `application/` directory orchestrate domain logic and remain framework-agnostic.

## Use Case Classes

- Each use case should have a single public method (typically `execute`)
- Depend only on domain interface abstractions
- Return DTOs, not domain entities directly
- Keep use cases focused and single-purpose

Example concept:
```
class CreateOrderUseCase:
    constructor(order_repo: OrderRepository, product_repo: ProductRepository)
    
    execute(request: CreateOrderDTO) -> OrderDTO:
        # Orchestrate domain logic
        order = Order.create(request.customer_id, request.items)
        order_repo.save(order)
        return OrderDTO.from_domain(order)
```

## Data Transfer Objects (DTOs)

- Use framework-appropriate validation models for all DTOs
- Separate input DTOs (requests) from output DTOs (responses)
- Include `from_domain()` and `to_domain()` conversion methods
- Keep DTOs in `application/dtos.py`

Example concept:
```
class CreateOrderDTO:
    customer_id: string
    items: list[OrderItemDTO]

class OrderDTO:
    id: string
    customer_id: string
    total: float
    
    static from_domain(order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            customer_id=order.customer_id,
            total=order.calculate_total()
        )
```

## Dependency Management

- Inject dependencies through constructor
- Depend on interface abstractions, not concrete implementations
- Make all dependencies explicit

## What NOT to Include

- ❌ Web framework dependencies or HTTP concerns
- ❌ Database queries or ORM code
- ❌ Direct external service calls
- ❌ Framework-specific annotations
