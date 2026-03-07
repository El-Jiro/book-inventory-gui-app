from typing import Self


class Libro:

    __id: int
    __titulo: str
    __autor: str
    __año: int
    __isbn: int

    def __init__(self, titulo: str, autor: str, año: int, isbn:int)->None:
        self.__titulo = titulo
        self.__autor = autor
        self.__año = año
        self.__isbn = isbn

    @classmethod
    def con_id(cls, id: int, titulo: str, autor: str, año: int, isbn: int) -> Self:
        pass

    @property
    def id(self: Self) -> int:
        return self.__id
    @property
    def titulo(self: Self) -> str:
        return self.__titulo
    
    @titulo.setter
    def titulo(self: Self, valor: str)-> None:
        self.__titulo = valor

    @property
    def autor(self: Self) -> str:
        return self.__autor
    
    @autor.setter
    def autor(self: Self, valor: int) -> None:
        self.__autor = valor
    
    @property
    def año(self: Self)->int:
        return self.__año
    
    @año.setter
    def año(self: Self, valor: int) -> None:
        self.__año = valor

    @property 
    def isbn(self: Self) -> int:
        return self.__isbn
    
    @isbn.setter
    def isbn(self: Self, valor: int) -> None:
        self.__isbn = valor