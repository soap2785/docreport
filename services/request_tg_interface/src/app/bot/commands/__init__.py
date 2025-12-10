from .admin import StartAdminRouter, OrdersAdminRouter
from .searchdata import router as SearchDataRouter
from .cancel import router as CancelRouter
from .search import router as SearchRouter
from .start import router as StartRouter
from .new_order import router as NewOrderRouter

__all__ = (
    StartRouter, SearchRouter, SearchDataRouter,
    CancelRouter, StartAdminRouter, OrdersAdminRouter,
    NewOrderRouter

)
