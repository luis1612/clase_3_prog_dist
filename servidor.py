import socket
import threading
import sys

class Servidor():
    def __init__(self, host="localhost", puerto=9999):
        self.clientes = []
        self.sock = socket.socket()
        self.sock.bind((host, puerto))
        self.sock.listen(10)

        #PROCESO BLOQUEANTE
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptar_conexiones)
        procesar = threading.Thread(target=self.procesar_conexiones)

        aceptar.setDaemon(True)
        procesar.setDaemon(True)

        aceptar.start()
        procesar.start()

        try:
            while True:
                mensaje = input(">> ")
                if mensaje == 'salir':
                    self.sock.close()
                    sys.exit()
        except:
            self.sock.close()
            sys.exit()

    def aceptar_conexiones(self):
        print("Chat iniciado")
        while True:
            try:
                conexion, direccion = self.sock.accept()
                conexion.setblocking(False)
                self.clientes.append(conexion)
            except:
                pass

    def procesar_conexiones(self):
        print("Procesar conexion")
        while True:
            if len(self.clientes) > 0:
                for cliente in self.clientes:
                    try:
                        datos = cliente.recv(1024)
                        if datos:
                            self.mensaje_todos(datos, cliente)
                    except:
                        pass



    def mensaje_todos(self, mensaje, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(mensaje)
            except:
                self.clientes.remove(cliente)

servidor = Servidor()
