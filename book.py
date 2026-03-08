from typing import Self

class Libro:

    __id: int
    __titulo: str
    __autor: str
    __año: int
    __isbn: int


    @property
    def id(self: Self) -> int:
        return self.__id
    
    @id.setter
    def id(self: Self, id: int) -> None:
        self.__id = id

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

    def __str__(self)-> str:
         return f"({self.id}, {self.titulo}, {self.autor}, {self.año}, {self.isbn})"
    def __repr__(self: Self) -> str:
        return f"Libro(id={self.id} titulo='{self.titulo}', autor='${self.autor}', año={self.año}, isbn={self.isbn})"