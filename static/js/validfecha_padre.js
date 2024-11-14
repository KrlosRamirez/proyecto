function isValidDate(day, month, year) {
  var dteDate;

  month = month - 1;
  dteDate = new Date(year, month, day);

  return ((day == dteDate.getDate()) && (month == dteDate.getMonth()) && (year == dteDate.getFullYear()));
}

function validate_fecha(fecha) {
  var patron = new RegExp('^(19|20)+([0-9]{2})([-])([0-9]{1,2})([-])([0-9]{1,2})$');

  if(fecha.search(patron) == 0) {
    var values = fecha.split('-');

    if(isValidDate(values[2],values[1],values[0])) {
      return true;
    }
  }
  return false;
}

function Edad_padre() {
  var fecha = document.getElementById('id_fecha_naci_padre').value;
  var edad_padre = document.getElementById('id_edad_padre').value;

  if(validate_fecha(fecha) == true) {
    var values = fecha.split('-');
    var dia = values[2];
    var mes = values[1];
    var ano = values[0];

    var fecha_hoy = new Date();
    var ahora_ano = fecha_hoy.getYear();
    var ahora_mes = fecha_hoy.getMonth() + 1;
    var ahora_dia = fecha_hoy.getDate();

    var edad_padre = (ahora_ano + 1900) - ano;

    if(ahora_mes < mes) {
      edad_padre--;
    }

    if((mes == ahora_mes) && (ahora_dia < dia)) {
      edad_padre--;
    }

    if(edad > 1900) {
      edad -= 1900;
    }

    var meses = 0;

    if(ahora_mes > mes)
      meses = ahora_mes - mes;
    if(ahora_mes < mes)
      meses = 12 - (mes - ahora_mes);
    if(ahora_mes == mes && dia > ahora_dia)
      meses = 11;

    var dias = 0;
    if(ahora_dia > dia)
      dias = ahora_dia - dia;
    if(ahora_dia < dia) {
      ultimoDiaMes = new Date(ahora_ano, ahora_mes, 0);
      dias = ultimoDiaMes.getDate() - (dia - ahora_dia);
    }

    document.getElementById('id_edad_padre').value = edad_padre
  } else {
    $('#alertaDos').html('La fecha ' + fecha + ' Es incorrecta...').slideDown(500);
    $('#id_fecha_naci_padre').val('');
    $('#id_edad_padre').val('');
    $('#id_fecha_naci_padre').focus();
    return false;
  }

  if( edad_padre <= 17 || edad_padre >= 80 ) {
    $('#alertaDos').html('Usted tiene '+ edad_padre + ' años de edad por lo tanto, ¡NO Puede Ser Registrado!').slideDown(500);
    $('#id_edad_padre').val('');
    $('#id_fecha_naci_padre').val('');
    $('#id_fecha_naci_padre').focus();
    return false;
  }else{
    $('#alertaDos').html('').slideDown(500);

  }
}
