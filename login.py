#importamos librerías

from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN #not installed
import numpy as np


#Función para almacenar el registro facial

def registro_facial():
    #capturar rostro
    cap = cv2.VideoCapture(0) #elegimos la cámara con la q vamos hacer la detección
    while(True):
        ret, frame = cap.read() #leemos el video
        cv2.imshow('Registro Facial',frame) #mostramos video en pantalla
        if cv2.waitKey(1) == 27:   #al oprimir ESC rompe el video
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)   #guardamos la última captura del video como imagen y asignamos el nombre del usuario
    cap.release()  #cerramos
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)  #limpiamos los text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro facial exitoso", fg = "green", font = ("Calibri", 11)).pack()

  #detectamos el rostro y exportamos los pixeles

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150,200), interpolation = cv2.INTER_CUBIC) #guardamos la imagen en un tamaño de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)

# función para el login facial
def login_facial():
# vamos a capturar el rostro
    cap = cv2.VideoCapture(0)  #elegimos la cámara con la q vamos hacer la detección
    while(True):
        ret,frame = cap.read() #leemos el video
        cv2.imshow('Login Facial',frame) #mostramos el video en pantalla
        if cv2.waitKey(1) == 27: #cuando oprimimos ESC rompre el video
            break   
    usuario_login = verificacion_usuario.get() #con esta variable guardamos la foto pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login+"LOG.jpg",frame)#guardamos la ùltima captura del video como imagen y asignamos el nombre del usuario
    cap.release()  #cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)  #limpiamos los text variables
    contra_entrada2.delete(0, END)

#función para guardar el rostro
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150,200), interpolation = cv2.INTER_CUBIC)  # guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #detectamos el rostro
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)
    #función para comparar los rostros
    def orb_sim(img1, img2):
        orb = cv2.ORB_create()  #creamos el objeto de comparaciòn

        kpa, descr_a = orb.detectAndCompute(img1, None) #creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None) #creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #creamos comparador de fuerza 

        matches = comp.match(descr_a, descr_b) #aplicamos comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #extraemos las regiones similares en base a los puntos claves
        if len(matches)  == 0:
            return 0
        return len (regiones_similares)/len(matches) #exportamos el porcentaje de similitud

    #importamos las imágenes y llamamos la función de comparación

    im_archivos = os.listdir() #importamos la lista de archivos con la librería os
    if usuario_login+".jpg" in im_archivos: #commparamos los archivos con el q nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0) #importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0) #importamos el rostro del inicio de sesión
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.9:
            Label(pantalla2, text = "Inicio de sesión exitoso", fg = "green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del resgistro: ",similitud)
        else:
            print("Rostro incorrecto, certifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label (pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()



#función para registrar el usuario

def registrar_usuario ():
  usuario_info = usuario.get() #obtener información almacenada en usuario
  contra_info = contra.get() #obtener información almacenada en contra

  archivo = open(usuario_info, "w") #abrir información en modo escritura
  archivo.write(usuario_info + "\n") #escribimos la info
  archivo.write(contra_info)
  archivo.close()

  #limpieza de los text variable
  usuario_entrada.delete(0, END)
  contra_entrada.delete(0, END)

  #mensaje para usuario "su registro ha sido exitoso"
  Label (pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()



# función q asigna el botón login
def login():
  global pantalla2
  global verificacion_usuario
  global verificacion_contra
  global usuario_entrada2
  global contra_entrada2

  pantalla2 = Toplevel(pantalla)
  pantalla2.title("Login")
  pantalla2.geometry("400x500")  #creamos la ventana
  Label(pantalla2, text = "Login facial: debe asignar un usuario:").pack()
  Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña:").pack()
  Label(pantalla2, text = "").pack()  #dejamos un espacio

  verificacion_usuario = StringVar()
  verificacion_contra = StringVar()

  # ingresamos los datos
  Label(pantalla2, text = "Usuario * ").pack()
  usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
  usuario_entrada2.pack()
  Label(pantalla2, text = "Contraseña * ").pack()
  contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
  contra_entrada2.pack()
  Label(pantalla2, text = "").pack()
  #Button (pantalla2, text = "Inicio de sesion tradicional", width = 20, height = 1, command = verificacion_login). pack()
  
  #Crear botón para login facial
  Label(pantalla2, text = "").pack()
  Button(pantalla2, text = "Inicio de sesion facial", width = 20, height = 1, command = login_facial).pack()

#Creamos una función para asignar al botón registro
def registro():
    global usuario
    global contra #globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #esta pantalla es de un nivel superior
    pantalla1.title("Registro")
    pantalla1.geometry("300x250") #asignamos el tamaño de la ventana

    #empezamos a crear las entradas

    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text = "Registro facial: debe asignar un usuario:").pack()
    #Label (pantalla1, text = "").pack() #dejamos un poco de espacio
    Label(pantalla1, text = "Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text = "").pack() #dejamos un poco de espacio
    Label(pantalla1, text = "Usuario * ").pack()  #mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1, textvariable = usuario) #creamos un txt variable para q el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack() #mostramos en la pantalla 1 la contraseña
    contra_entrada = Entry(pantalla1, textvariable = contra)  #creamos un text variable para q el usuario ingrese la contra
    contra_entrada.pack()
    Label(pantalla, text = "").pack() #espacio para creación del botón
    Button(pantalla1, text = "Registro tradicional", width = 15, height = 1, command = registrar_usuario).pack() #creaciòn de botón

    #creación de botón para registro facial
    Label(pantalla1, text = "").pack()
    Button(pantalla1, text = "Registro Facial", width = 15, height = 1, command = registro_facial).pack()

def pantalla_principal():
    global pantalla #globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("400x400") #asignamos el tamaño de la ventana
    pantalla.title("SMART LOGIN SCREEN")  #asignamos título de la pantalla
    Label(text = "Smart Login", bg = "red", width = "400", height = "2",fg = "white" , font = ("Times", 15)).pack() #asignamos características de la ventana

    #Creación de botones

    Label(text = "").pack()         #Creamos el espacio entre el titulo y el primer botón
    Button(text = "Login", height = "2", width = "30", command=login).pack()
    Label (text = "").pack() #espacio entre el primer botón y el segundo botón
    Button(text = "Register", height = "2", width = "30", command=registro).pack()

    pantalla.mainloop()




pantalla_principal()