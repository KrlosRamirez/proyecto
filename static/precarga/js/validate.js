function SoloLetra(lista, evt){
  for (i=0; i<lista.length; i++){
    document.getElementById(lista[i]).onkeydown = function (evt) {
    key = evt.keyCode || evt.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = "8-37-39-46";

    tecla_especial = false
    for(var i in especiales){
        if(key == especiales[i]){
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla)==-1 && !tecla_especial){
        return false;
      }
    }
  }
}

SoloLetra(["id_Nombre","id_Apellido","id_Nivel_instruccion","id_Curso_realizar","id_Cursa_otra_actividad"])

function SoloNumeros(lista, evt){
  for (i=0; i<lista.length; i++){
    document.getElementById(lista[i]).onkeypress = function (evt) {
     if(window.event){//asignamos el valor de la tecla a keynum
        keynum = evt.keyCode; //IE
      }
      else{
        keynum = evt.which; //FF
      } 
      //comprobamos si se encuentra en el rango numérico y que teclas no recibirá.
      if((keynum > 47 && keynum < 58) || keynum == 8 || keynum == 13 || keynum == 6 ){
        return true;
      }
      else{
        return false;
      }
    }
  }
}

SoloNumeros(["id_cedula_alumno","id_Telefono","id_Celular","id_Fecha_nacimiento"])