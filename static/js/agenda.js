// Ingresado validacion para celular y digitos correctos  
// Validacion de numero telefonico
document.querySelector('form').addEventListener('submit', function(event) {
    var telefono = document.querySelector('input[name="telefono"]').value;
    var regex = /^09\d{8}$/; // Expresión regular para validar números de celular ecuatorianos

    if (!regex.test(telefono)) {
        alert('Por favor, ingresa un número de celular  válido.');
        event.preventDefault(); // Evita que el formulario se envíe
    }
});


    // Funcion para evitar ingreso de caracteres al celular
    function limitarEntrada() {

        let x = document.getElementById("miInput");

        x.value = x.value.replace(/[^0-9]/g, ''); // Elimina cualquier caracter que no sea un número
        if (x.value.length > 10) {
            x.value = x.value.slice(0, 10); // Limita la longitud a 10
        }
    }



// Validacion si los campos estan vacios
document.querySelector('form').onsubmit = function (e) {
    var inputs = this.querySelectorAll('input');
    var todosLlenos = true; // Asume que todos los campos están llenos

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            todosLlenos = false; // Si un campo está vacío, establece todosLlenos en falso
            break; // No necesitas verificar el resto de los campos, así que puedes salir del bucle
        }
    }

    if (!todosLlenos) {
        e.preventDefault(); // Previene el envío del formulario
        alert('Los campos estan vacios');
    } else {
        alert('Guardado exitosamente');
    }
};



// Horas
// Obtener todos los elementos con la clase 'fecha'
document.getElementById('fecha').addEventListener('change', function() {
    let fecha = new Date();
    let horas = fecha.getHours();
    let minutos = fecha.getMinutes();
    let ampm = horas >= 12 ? 'pm' : 'am';
    horas = horas % 12;
    horas = horas ? horas : 12; // la hora '0' debe ser '12'
    minutos = minutos < 10 ? '0'+minutos : minutos;
    let strHora = horas + ':' + minutos + ' ' + ampm;
    document.getElementById('hora').value = strHora;
});



//    // Ingresado de Horas 
    $(document).ready(function () {
        //$('#hora').on('change', function () {
        //    var horaSeleccionada = $(this).val();
        //    var hora = parseInt(horaSeleccionada.split(':')[0]);
//
        //    if ((hora < 9 || (hora > 12 && hora < 15) || hora > 18)) {
        //        alert('Por favor, selecciona una hora entre las 09:00 a 12:00, o entre las 15:00 a 18:00.');
        //        $(this).val('');
        //    }
        //});

        // Ingresado de fechas

        $('#fecha').on('change', function () {
            var fechaSeleccionada = new Date($(this).val());
            console.log('Fecha seleccionada: ', fechaSeleccionada);

            var dia = fechaSeleccionada.getDay();


            if (dia == 0) { // 0 corresponde al domingo
                alert('Los domingos no están disponibles. Por favor, selecciona otro día.');
                $(this).val('');
            }
        });
    });
    // Ingresado de codigos aleatorios 

    var codigo = document.getElementById('codigo');
    var numeroAleatorio = Math.floor(1000 + Math.random() * 9000);
    codigo.value = numeroAleatorio;
