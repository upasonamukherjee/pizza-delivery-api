from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
from models import User, Order
from schemas import OrderModel, OrderResponse, OrderStatusModel
from auth_routes import get_current_username

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = SessionLocal()


@order_router.get('/', summary="Orders health check")
async def hello():
    """
    A simple check that the orders router is running.
    """
    return {"message": "Hello World"}


@order_router.post(
    '/order',
    status_code=status.HTTP_201_CREATED,
    summary="Place an order",
    responses={401: {"description": "Missing or invalid access token"}},
)
async def place_an_order(
    order: OrderModel,
    username: str = Depends(get_current_username)
):
    """
    Place a new order for the logged-in user.

    The request body needs:
    - **quantity**: number of pizzas
    - **pizza_size**: `SMALL`, `MEDIUM`, `LARGE` or `EXTRA-LARGE`

    New orders start with the status `PENDING`.
    """
    user = session.query(User).filter(User.username == username).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )
    new_order.user = user

    session.add(new_order)
    session.commit()

    return {
        "id": new_order.id,
        "quantity": new_order.quantity,
        "pizza_size": new_order.pizza_size.code,
        "order_status": new_order.order_status.code,
    }


@order_router.get(
    '/orders',
    response_model=List[OrderResponse],
    summary="List all orders (staff only)",
    responses={
        401: {"description": "Missing or invalid access token"},
        403: {"description": "User is not staff"},
    },
)
async def list_all_orders(username: str = Depends(get_current_username)):
    """
    List every order from every user.

    **Staff only.** Non-staff users receive `403 Forbidden`.
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None or not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can view all orders"
        )

    return session.query(Order).all()


@order_router.get(
    '/orders/{id}',
    response_model=OrderResponse,
    summary="Get any order by id (staff only)",
    responses={
        401: {"description": "Missing or invalid access token"},
        403: {"description": "User is not staff"},
        404: {"description": "Order not found"},
    },
)
async def get_order_by_id(id: int, username: str = Depends(get_current_username)):
    """
    Retrieve a single order by its id.

    **Staff only.** Use `/orders/user/order/{id}` to read your own order.

    - **id**: the order's id
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None or not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can view an order by id"
        )

    order = session.query(Order).filter(Order.id == id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found"
        )

    return order


@order_router.get(
    '/user/orders',
    response_model=List[OrderResponse],
    summary="List my orders",
    responses={
        401: {"description": "Missing or invalid access token"},
        404: {"description": "User not found"},
    },
)
async def get_user_orders(username: str = Depends(get_current_username)):
    """
    List all orders that belong to the logged-in user.

    The user is identified from the access token, so no user id is needed.
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user.orders


@order_router.get(
    '/user/order/{id}',
    response_model=OrderResponse,
    summary="Get one of my orders",
    responses={
        401: {"description": "Missing or invalid access token"},
        404: {"description": "Order not found for this user"},
    },
)
async def get_user_order(id: int, username: str = Depends(get_current_username)):
    """
    Retrieve one order by id, only if it belongs to the logged-in user.

    Another user's order returns `404`, the same as an order that doesn't exist.

    - **id**: the order's id
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    order = session.query(Order).filter(
        Order.id == id,
        Order.user_id == user.id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order with id {id} found for this user"
        )

    return order


@order_router.put(
    '/order/update/{id}',
    response_model=OrderResponse,
    summary="Update my order",
    responses={
        401: {"description": "Missing or invalid access token"},
        404: {"description": "Order not found for this user"},
    },
)
async def update_order(
    id: int,
    order_data: OrderModel,
    username: str = Depends(get_current_username)
):
    """
    Update the quantity and pizza size of one of your own orders.

    - **id**: the order's id
    - **quantity**: the new quantity
    - **pizza_size**: `SMALL`, `MEDIUM`, `LARGE` or `EXTRA-LARGE`

    The order status can't be changed here. Staff use `/orders/order/status/{id}`.
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    order = session.query(Order).filter(
        Order.id == id,
        Order.user_id == user.id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order with id {id} found for this user"
        )

    order.quantity = order_data.quantity
    order.pizza_size = order_data.pizza_size

    session.commit()

    return order


@order_router.patch(
    '/order/status/{id}',
    response_model=OrderResponse,
    summary="Update an order's status (staff only)",
    responses={
        401: {"description": "Missing or invalid access token"},
        403: {"description": "User is not staff"},
        404: {"description": "Order not found"},
    },
)
async def update_order_status(
    id: int,
    status_data: OrderStatusModel,
    username: str = Depends(get_current_username)
):
    """
    Change an order's status.

    **Staff only.**

    - **id**: the order's id
    - **order_status**: `PENDING`, `IN-TRANSIT` or `DELIVERED`
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None or not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can update order status"
        )

    order = session.query(Order).filter(Order.id == id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found"
        )

    order.order_status = status_data.order_status

    session.commit()

    return order


@order_router.delete(
    '/order/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an order",
    responses={
        401: {"description": "Missing or invalid access token"},
        404: {"description": "Order not found"},
    },
)
async def delete_order(id: int, username: str = Depends(get_current_username)):
    """
    Delete an order.

    Customers can delete only their own orders. Staff can delete any order.
    An order that is not yours returns `404`, the same as one that doesn't exist.

    - **id**: the order's id
    """
    user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    order = session.query(Order).filter(Order.id == id).first()

    if order is None or (order.user_id != user.id and not user.is_staff):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No order with id {id} found"
        )

    session.delete(order)
    session.commit()

    return None