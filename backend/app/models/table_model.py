from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


def generate_base_table_model(use_timezone_aware_datetime: bool = False):
    class BaseTableModel:
        __tablename__ = ""

        updated_at = Column(
            DateTime(timezone=use_timezone_aware_datetime),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
        created_at = Column(
            DateTime(timezone=use_timezone_aware_datetime),
            server_default=func.now(),
            nullable=False,
        )
        deleted_at = Column(DateTime(timezone=use_timezone_aware_datetime), default=None)

        def __str__(self) -> str:
            return str(self.__dict__)

        def __init__(self, *args, **kwargs):
            kwargs2 = {k: v for k, v in kwargs.items() if hasattr(self.__class__, k)}
            super().__init__(*args, **kwargs2)

    return BaseTableModel


TableModel = generate_base_table_model()

TableModelTimezoneAware = generate_base_table_model(use_timezone_aware_datetime=True)
