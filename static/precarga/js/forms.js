// ------- Select En La Asginacion De Los Alumnos/Instrumento ------- //
$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});

function validacion(id){
    var elem=document.getElementById(id);
    if(elem.checkValidity())
        elem.style.borderColor="green";
    else
        elem.style.borderColor="red";
}

$(function() {
    $( "#datepicker" ).datepicker();
    $( "#datepicker2" ).datepicker();
    $( "#datepicker3" ).datepicker();
});
