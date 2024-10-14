# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 14, 2024 19:35:41
# Database: sqlite:////tmp/tmp.fP7yQMPKPi/crm_3/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Table to store customer information.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    registration_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AddressList : Mapped[List["Address"]] = relationship(back_populates="customer")
    CustomerFeedbackList : Mapped[List["CustomerFeedback"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Employee(SAFRSBaseX, Base):
    """
    description: Table to store employee information.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hire_date = Column(DateTime, nullable=False)
    position = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DepartmentList : Mapped[List["Department"]] = relationship(back_populates="manager")
    EmployeeDepartmentList : Mapped[List["EmployeeDepartment"]] = relationship(back_populates="employee")



class Product(SAFRSBaseX, Base):
    """
    description: Table to store product information.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")



class Supplier(SAFRSBaseX, Base):
    """
    description: Table to store supplier information.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Address(SAFRSBaseX, Base):
    """
    description: Table to store addresses associated with customers.
    """
    __tablename__ = 'addresses'
    _s_collection_name = 'Address'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String)
    postal_code = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("AddressList"))

    # child relationships (access children)



class CustomerFeedback(SAFRSBaseX, Base):
    """
    description: Table to store feedback from customers.
    """
    __tablename__ = 'customer_feedback'
    _s_collection_name = 'CustomerFeedback'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    feedback_text = Column(String, nullable=False)
    feedback_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CustomerFeedbackList"))

    # child relationships (access children)



class Department(SAFRSBaseX, Base):
    """
    description: Table to store department information.
    """
    __tablename__ = 'departments'
    _s_collection_name = 'Department'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    manager_id = Column(ForeignKey('employees.id'))

    # parent relationships (access parent)
    manager : Mapped["Employee"] = relationship(back_populates=("DepartmentList"))

    # child relationships (access children)
    EmployeeDepartmentList : Mapped[List["EmployeeDepartment"]] = relationship(back_populates="department")



class Inventory(SAFRSBaseX, Base):
    """
    description: Table to track inventory stock levels.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Table to store customer orders.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")
    SalesTransactionList : Mapped[List["SalesTransaction"]] = relationship(back_populates="order")



class EmployeeDepartment(SAFRSBaseX, Base):
    """
    description: Table to establish many-to-many relationship between employees and departments.
    """
    __tablename__ = 'employee_departments'
    _s_collection_name = 'EmployeeDepartment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    employee_id = Column(ForeignKey('employees.id'), nullable=False)
    department_id = Column(ForeignKey('departments.id'), nullable=False)

    # parent relationships (access parent)
    department : Mapped["Department"] = relationship(back_populates=("EmployeeDepartmentList"))
    employee : Mapped["Employee"] = relationship(back_populates=("EmployeeDepartmentList"))

    # child relationships (access children)



class OrderItem(SAFRSBaseX, Base):
    """
    description: Table to store items in an order.
    """
    __tablename__ = 'order_items'
    _s_collection_name = 'OrderItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)



class SalesTransaction(SAFRSBaseX, Base):
    """
    description: Table to record sales transactions.
    """
    __tablename__ = 'sales_transactions'
    _s_collection_name = 'SalesTransaction'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    transaction_amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("SalesTransactionList"))

    # child relationships (access children)
