from tkinter import *

window = Tk()
#Definimos un tamaño fijo para la ventana y evitamos que el usuario puede redimensionarla
window.geometry("500x415")
window.resizable(False, False)
window.title("Inventario de Libros")

#----------Labels para los entries---------------
l1 = Label(window, font=("Arial", 10), text="Título")
l2 = Label(window, font=("Arial", 10), text="Autor")
l3 = Label(window, font=("Arial", 10), text="Año")
l4 = Label(window, font=("Arial", 10), text="ISBN")

l1.grid(padx=5, pady=8)
l2.grid(row=0, column=2, padx=5, pady=8)
l3.grid(row=1, pady=8)
l4.grid(row=1, column=2, pady=8)

#----------StringVars para los entries---------
titulo_t = StringVar()
autor_t = StringVar()
año_t = StringVar()
isbn_t = StringVar()

#-----Entries------
titulo = Entry(window, width=30, textvariable=titulo_t)
autor = Entry(window, width=30, textvariable=autor_t)
año = Entry(window, textvariable=año_t)
isbn = Entry(window, textvariable=isbn_t)


titulo.grid(row=0, column=1, padx=8)
autor.grid(row=0, column= 3, padx=8)
año.grid(row=1, column=1, sticky=W)
isbn.grid(row=1, column=3, sticky=W)

#-------Usaremos un listbox para desplegar todas las entradas de la bd-----
booklist = Listbox(window, height=20, width=40)
#Para abarcar más de una fila o columna, especificaremos los argumebtos columnspan y rowspan en el método grid
booklist.grid(row=2, column=0, columnspan=3, rowspan=6)

#Creamos una scrollbar para poder desplazarnos por la lista cuando los registros llenen todo el espacio visible 
sb = Scrollbar(window)
sb.grid(row=2, column=3, rowspan=6, sticky=W)

#Enlazamos ambos widgets
booklist.configure(yscrollcommand=sb.set)
sb.configure(command=booklist.yview)

window.mainloop()