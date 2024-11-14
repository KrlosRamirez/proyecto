// -------- Se utiliza para que el campo de texto solo acepte numeros -------- //
function valida(e){
    tecla = (document.all) ? e.keyCode : e.which;

    //Tecla de retroceso para borrar, siempre la permite
    if (tecla==8){
        return true;
    }
        
    // Patron de entrada, en este caso solo acepta numeros
    patron =/[0-9]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}

// -------- Se utiliza para que el campo de texto solo acepte letras -------- //
function soloLetras(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = [8, 37, 39, 46];

    tecla_especial = false
    for(var i in especiales) {
        if(key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla) == -1 && !tecla_especial)
        return false;
}

// -------------------------------------------------------------------------- //


// ----- Desabilitar el autoincrementable de los number input de los formularios ----- //

jQuery(document).ready( function($) {
 
    // Disable scroll when focused on a number input.
    $('form').on('focus', 'input[type=number]', function(e) {
        $(this).on('wheel', function(e) {
            e.preventDefault();
        });
    });
 
    // Restore scroll on number inputs.
    $('form').on('blur', 'input[type=number]', function(e) {
        $(this).off('wheel');
    });
 
    // Disable up and down keys.
    $('form').on('keydown', 'input[type=number]', function(e) {
        if ( e.which == 38 || e.which == 40 )
            e.preventDefault();
    });  
});

// -------------------------------------------------------------------------- //

// -------------------- Habilitar/Deshabilitar Permisos En El Registro Del Usuario -------------------- //
function validar(){

  var Check = document.getElementById('id_is_profesor');

  if (Check.checked == true) {
    Check.checked = true;
  }

}
// -------------------------------------------------------------------------- //


// -------------------- Validacion Campos Educacion Musical -------------------- //
function enableBox(){

  var cat = document.getElementById('id_academ_catedr');
  var nom_cat = document.getElementById('id_nombr_academi');

  if (cat.checked == true){
    nom_cat.disabled = false;
  }
  else{
    nom_cat.disabled = true;
  }
}

function enableBox2(){

  var is_beca = document.getElementById('id_bec_est_esp');
  var curs = document.getElementById('id_estu_cur');
  var inst = document.getElementById('id_inst_empr_bec');

  if (is_beca.checked == true){
    curs.disabled = false;
    inst.disabled = false;
  }
  else{
    curs.disabled = true;
    inst.disabled = true;
  }
}

// ----------------------------------------------------------------- //

// -------------------- Asignacion Del Profesor -------------------- //
function asig(ci){
  var ac = document.getElementById("formcedula")
  document.getElementById("apretar").onclick=function(){
    ci2 = document.getElementById("id_cedula").value;
    if (ci === ci2){
      console.log("si")
      $.ajax({
        url: url,
        type: 'POST',
        datatype:'json',
        data:{
           'csrfmiddlewaretoken':document.getElementsByName("csrfmiddlewaretoken")[0].value,
           'cedu1':ci,
           'cedu2':ci2 
        }  
      }).done(function(data){
        alert("Guardado exitosamente")
        window.location= despues
      })
    }else{
      alert("No Coincide")
    }
  }
} 