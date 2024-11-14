$(document).ready(function(){
    $.ajax({
    type: 'GET',
    url: '/revisar/',
    data:{
        tipo : 'revisar'
    },
    success: function(data){
        if (data.data == 'termino') {
            swal({
                title: "El periodo escolar termino!",
                text: "Ingrese un nuevo periodo escolar",
                type: "warning",
                showCancelButton: false,
                confirmButtonColor: "#5cb85c",
                confirmButtonText: "Entiendo",
                cancelButtonText: "No, cancelar",
                animation: "slide-from-top",
                closeOnConfirm: false 
            });
            botones = $('.bloquear');
            if (botones.length > 0) {
                botones.attr('disabled','disabled');
            }
        }
    },
    error: function(){
        console.log("error!")
    }
    });    
})
