"""A ZipFile like package for extracting data from Aff4 packages"""
from .wrapper import Aff4Wrapper,Aff4WrapperException
__all__ = ['Aff4Wrapper','Aff4WrapperException']
__version__ = "0.1.3"