

class Selects(object):

    def Productos(self):
        return(
            ('' ,''),
            ('Litro', 'Litro'),
            ('Gramo', 'Gramo'),
            ('Kilo', 'kilo'),
            ('Lata', 'Lata'),

            )
    def posee_documento(self):
        return (
            ('', '' ),
            ('SI','SI'),
            ('NO','NO'),


        )


    
    def nivelEducacion(self):
        return(
            ('',''),
            ('Preescolar','Preescolar'),
            ('Primaria','Primaria'),
            ('Secundaria','Secundaria'),
            ('Universitaria','Universitaria'),

        )

    def fallecio(self):
        return (
            ('', '' ),
            ('SI','SI'),
            ('NO','NO'),


        )

    def tratamientos(self):
        return (
            ('', 'Seleccione una opcion'),
            ('PSICOLÓGICO', 'PSICOLÓGICO'),
            ('PSICOPEDAGÓGICA', 'PSICOPEDAGÓGICA'),
            ('TERAPIA DE LENGUAJE', 'TERAPIA DE LENGUAJE'),
            ('OTROS', 'OTROS'),

        )

    def padece_enfermedad(self):
        return (
            ('', 'Seleccione una opcion'),
            ('SI', 'SI'),
            ('NO', 'NO'),

        )

    def se_encuentra(self):
        return(
            ('' , 'Seleccione'),
            ('SI', 'SI'),
            ('NO', 'NO'),
        )

    def Cilindro_unidad(self):
        return(
            ('' ,''),
            ('10kg', '10kg'),
            ('18kg', '18kg'),
            ('27kg', '27kg'),
            ('43kg', '43kg'),
            )

    def tamaño(self):
        return(
            ('' ,''),
            ('Grande','Grande'),
            ('Mediana','Mediana'),
            ('Pequeña','Pequeña'),
            )

    def tipo_gas(self):
        return(
            ('' ,''),
            ('Granel Doméstico (líquido)','Granel Doméstico (líquido)'),
            ('Granel Doméstico (Gaseoso)','Granel Doméstico (Gaseoso)'),
            )

    def nacionalidad(self):
        return(
            ('' ,''),
            ('V', 'V'),
            ('E', 'E'),
            )

    def sexo(self):
        return (
            ('', ''),
            ('Masculino', 'Masculino'),
            ('Femenino', 'Femenino'),

            )

    def opciones(self):
        return (
            ('', 'Seleccione una opcion'),
            ('HIJO(A)', 'HIJO(A)'),
            ('HERMANO(A)', 'HERMANO(A)'),
            ('NIETO(A)', 'NIETO(A)'),
            ('SOBRINO(A)', 'SOBRINO(A)'),
            ('AHIJADO(A)', 'AHIJADO(A)'),
            ('PRIMO(A)', 'PRIMO(A)'),
            ('OTROS', 'OTROS'),
        )

    def Posee_cedula(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )

    def Trabajo(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )
    def mujer_embarazada(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )
    def mujer_lactancia(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )
    def posee_discapacidad(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )
    def habitante_encamada(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )
    def vota(self):
        return(
            ('' , ''),
            ('Si', 'Si'),
            ('No', 'No'),
            )

    def padres(self):
        return (
            ('', 'Seleccione una opcion'),
            ('PADRE', 'PADRE'),
            ('MADRE', 'MADRE'),

        )

    def codigo_telefono(self):
        return(
            ('', ''),
            ('0257', '0257'),
            )

    def codigo_movil(self):
        return (
            ('' , ''),
            ('0426' ,'0426'),
            ('0416', '0416'),
            ('0424', '0424'),
            ('0414', '0414'),
            ('0412', '0412'),
            )

    def ocupa(self):
        return(
            ('' , ''),
            ('Informatico','Informatico'),
            ('Funcionario','Funcionario'),
            ('Medico','Medico'),
            ('Mecanico','Mecanico'),
            ('Electricista','Electricista'),
            ('Docente','Docente'),
            ('Obrero','Obrero'),
            ('Otros','Otros'),
        )


    def parentescos(self):
        return(
            ('',''),
            ('Conyuge','Concubino'),
            ('Abuelo','Abuela'),
            ('Suegro','Suegra'),
            ('Padre','Madre'),
            ('Tio','Tia'),
            ('Hermano','Hermana'),
            ('Cuñado','Cuñada'),
            ('Yerno','Nuera'),
            ('Hijo','Hija'),
            ('Primo','Prima'),
            ('Sobrino','Sobrina'),
            ('Nieto','Nieta'),
            )


    def tipo_de_Em(self):
        return(
            ('' , ''),
            ('Publica', 'Publica'),
            ('Privada', 'Privada'),
            ('Ninguna', 'Ninguna'),
        )

    def municipio(self):
        return(
            ('',''),
            ('Guanare','Guanare'),


        )

    def tipo_de_p(self):
        return(
            ('' , ''),
            ('Casa', 'Casa'),
            ('Apartamento', 'Apartamento'),
            ('Rancho', 'Rancho'),
            ('Quinta', 'Quinta'),
            ('Casa-Quinta', 'Casa-Quinta'),  
            ('Otros', 'Otros'),            
        )

    def NivelEducacion(self):
        return(
            ('',''),
            ('Preescolar','Preescolar'),
            ('Primaria','Primaria'),
            ('Secundaria','Secundaria'),
            ('Universitaria','Universitaria'),

        )

    def Estado_civil(self):
        return (
            ('', ''),
            ('Casado','Casado'),
            ('Soltero','Soltero'),
            ('Divorciado','Divorciado'),
            ('Viudo','Viudo')

            )

    def Mujer_embarazada(self):
        return (
            ('', ''),
            ('Sí','Sí'),
            ('No','No')

            )

    def Mujer_lactancia(self):
        return (
            ('', ''),
            ('Sí','Sí'),
            ('No','No')

            )

    def Discapacidad(self):
        return (
            ('', ''),
            ('Sí','Sí'),
            ('No','No')

            )

    def Habitante_encamada(self):
        return (
            ('', ''),
            ('Sí','Sí'),
            ('No','No')

            )

    def Vota(self):
        return (
            ('', ''),
            ('Sí','Sí'),
            ('No','No')

            )

    def media_depago(self):
        return (
            ('' , ''),
            ('Punto' ,'Punto'),
            ('Efectivo', 'Efectivo'),
            ('Tranferencia', 'Tranferencia'),
            ('Pago_movil', 'Pago_movil'),
            )

    


