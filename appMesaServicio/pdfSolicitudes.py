from fpdf import FPDF
from datetime import datetime


class PdF(FPDF):
    def header(self):
        # logo
        self.image("media/fotos/logoSena.jpg", 10, 8, 33)
        self.set_font("Arial","B",15)
        self.ln()
        # moverse a la derecha
        self.cell(60)
        # titulo
        self.cell(80,10,"Mesa de servicios CTPI-Cauca",0,0,"C")
        self.ln()
        self.cell(60)
        self.cell(80,10,"REPORTE SOLICITUDES",0, 0, 'C')
        # salo de linea
        self.ln(30)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(0,10,'page'+ str(self.page_no()) + '/{nb}',0,0,'C')
        
    def mostrarDatos(self, solicitudes):
        self.cell(30,10,"Fecha: ")
        fecha= datetime.now()
        # colocar fecha actual
        
        self.cell(40,10, str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year))
        
        self.ln()
        
        # crear en cabezado de la tabla
        self.set_font("Arial","B",12)
        self.cell(40,10,"Instructor",1,0,'C')
        self.cell(100,10,"Solitud",1,0,'C')
        self.cell(30,10,"Ambiente",1,0,'C')
        self.cell(20,10,"Fecha",1,0,'C')
        self.ln()
        
        fila=110
        
        self.set_font("Arial","",8)
        for solicitud in solicitudes:
            self.cell(40, 10, f"{solicitud.solUsuario.first_name}{
                solicitud.solUsuario.last_name}",1,0,"L")
            
            self.cell(100,10,solicitud.solDescripcion,1,0,'L')
            self.cell(30,10,solicitud.solOficinaAmbiente.ofiNombre,1,0,'L')
            self.cell(20,10,str(solicitud.fechaHoraCreacion),1,0,'C')
            self.ln()
            fila += 4
            
        self.ln()
        self.set_font("Arial","B",12)
        self.cell(200,10,'__________________________',0,0,'C')
        self.ln()
        self.cell(200,10,'lider TIC CTPI',0,0,'C')
        
        
            
        
        
        
        