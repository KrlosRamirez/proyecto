window.addEventListener("load", function(e){
  let elements = document.getElementsByClassName('form-control')
  for( let cont = 0; cont <= elements.length -1; cont++ ) {
    if(elements[cont].type === 'textarea') {
      elements[cont].closest('.form-group')
      .classList.add('textarea');
    }
  }

  var inp = document.getElementsByTagName("input");
  //var inp = document.getElementsByTagName("textarea");
  for (var i = 0; i < inp.length; i++){
    inp[i].addEventListener("blur", borrarEspacio);
    inp[i].addEventListener("blur", mayuscula);
    inp[i].addEventListener("paste", noPaste);
    if (inp[i].hasAttribute("validate")) {
      inp[i].addEventListener("keydown", validarKey);
      inp[i].addEventListener("blur", function (e){
        if(blur2 !== undefined){
          validarblur(e, blur2)
        }else{
          validarblur(e);
        }
      });
    }
  }

  var text = document.getElementsByTagName("textarea");
  for (var i = 0; i < text.length; i++){
    text[i].addEventListener("blur", borrarEspacio);
    text[i].addEventListener("blur", mayuscula);
    text[i].addEventListener("paste", noPaste);
    if (text[i].hasAttribute("validate")) {
      text[i].addEventListener("keydown", validarKey);
      text[i].addEventListener("blur", function (e){
        if(blur2 !== undefined){
          validarblur(e, blur2)
        }else{
          validarblur(e);
        }
      });
    }
  }

  var sel = document.getElementsByTagName("sel");
  for (var i = 0; i < sel.length; i++){
    sel[i].addEventListener("blur", borrarEspacio);
    sel[i].addEventListener("blur", mayuscula);
    sel[i].addEventListener("paste", noPaste);
    if (sel[i].hasAttribute("validate")) {
      sel[i].addEventListener("keydown", validarKey);
      sel[i].addEventListener("blur", function (e){
        if(blur2 !== undefined){
          validarblur(e, blur2)
        }else{
          validarblur(e);
        }
      });
    }
  }

});

//!
//!  var sel = document.getElementsByTagName("select");
//!  for (var i = 0; i < sel.length; i++){
//!    sel[i].addEventListener("blur", borrarEspacio);
//!    sel[i].addEventListener("blur", mayuscula);
//!    sel[i].addEventListener("paste", noPaste);
//!    if (sel[i].hasAttribute("validate")) {
//!      sel[i].addEventListener("keydown", validarKey);
//!      sel[i].addEventListener("blur", function (e){
//!        if(blur2 !== undefined){
//!          validarblur(e, blur2)
//!        }else{
//!          validarblur(e);
//!        }
//!      });
//!    }
//!  }

//!}); 

function validarblur(e, a=null) {
  var ra = true;
  if(a !== null){
    ra = a(e);
  }
  e.srcElement.parentElement.parentElement.classList.remove('has-success');
  if (e.srcElement.hasAttribute("minlength")) {
    //REQUERIDO Y ESTA VACIO ERROR
    //!REQUERIDO Y ESTA VACIO NO ERROR
    if (e.srcElement.value.length < e.srcElement.getAttribute("minlength")){
      if(!e.srcElement.hasAttribute("required") && e.srcElement.value.length == 0){

      }else{
        e.srcElement.parentElement.parentElement.classList.add('has-error');
        return false;
      }
    }
  }
  for (var z = 0; z < e.srcElement.value.length; z++) {
    if (!my_contiene(e.srcElement.value[z].charCodeAt(), e.srcElement.getAttribute("validate").split(","), 1)) {
      e.srcElement.parentElement.parentElement.classList.add('has-error');
      return false;
    }
  }
  if(!ra){
    e.srcElement.parentElement.parentElement.classList.add('has-error');
    return false;
  }
  e.srcElement.parentElement.parentElement.classList.remove('has-error');
  if(e.srcElement.value.length != 0){
    e.srcElement.parentElement.parentElement.classList.add('has-success');
  }
}
function validarKey(e){
  var cd, tcd;
  if (e.key.length === 1) {
    cd = e.key.charCodeAt();
    tcd = 1;
  } else {
    cd = e.which || e.keyCode;
    tcd = 2;
  }
  if (cd !== 8 && cd !== 9) {
    if (!my_contiene(cd, e.srcElement.getAttribute("validate").split(","), tcd)) {
      e.preventDefault();
      return;
    }
  }
}
function borrarEspacio(e) {
  var txt = e.srcElement.value;
  var txta;
  do {
    txta = txt;
    txt = txt.replace("-", "-");
  } while (txt !== txta);
  e.srcElement.value = txt.trim();
};

function mayuscula(e) {
  var txt = e.srcElement.value;
  var txta;
  do {
    txta = txt;
    txt = txt.toUpperCase();
  } while (txt !== txta);
  e.srcElement.value = txt;
};


function noPaste(e) {
  e.preventDefault();
}
function my_contiene(valor, haystack, tipo) {
  for (var i = 0; i < haystack.length; i++) {
    if (haystack[i].toUpperCase() === "NUMEROS") {
      if (valor >= 48 && valor <= 57) {
        return true;
      }
    } else if (haystack[i].toUpperCase() === "LETRAS") {
      if (valor >= 97 && valor <= 122 || valor === 241 || valor >= 65 && valor <= 90 || valor === 209) {
        return true;
      }
    } else if (haystack[i].toUpperCase() === "LETRASMINUS") {
      if (valor >= 97 && valor <= 122 || valor === 241) {
        return true;
      }
    } else if (haystack[i].toUpperCase() === "LETRASMAYUS") {
      if (valor >= 65 && valor <= 90 || valor === 209) {
        return true;
      }
    } else if (haystack[i].toUpperCase() === "SIMBOLOS") {
      if (valor >= 33 && valor <= 47 || valor >= 58 && valor <= 64 || valor >= 91 && valor <= 96 || valor >= 123 && valor <= 125) {
        return true;
      }
    } else if (haystack[i].toUpperCase() === "FLECHAS") {
      if (tipo === 2) {
        if (valor >= 37 && valor <= 40) {
          return true;
        }
      }
    } else if (haystack[i].toUpperCase() === "ENTER") {
      if (tipo === 2) {
        if (valor === 13) {
          return true;
        }
      }
    } else if (haystack[i].toUpperCase() === "ESPACIO") {
      if (valor === 32) {
        return true;
      }
    } else {
      if (haystack[i] === "\\" && haystack[i + 1] === "") {
        haystack[i] = ",";
      }
      if (haystack[i] === "''") {
        haystack[i] = "\"";
      }
      if (valor === haystack[i].charCodeAt()) {
        return true;
      }
      if (haystack[i] === "\\" && haystack[i + 1] === "") {
        i++;
      }
    }
  }
  return false;
}
