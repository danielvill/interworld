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


// Horas
// Obtener todos los elementos con la clase 'fecha'
var elementosFecha = document.getElementsByClassName('fecha');

// Añadir el evento 'change' a cada elemento
for (var i = 0; i < elementosFecha.length; i++) {
    elementosFecha[i].addEventListener('change', function() {
        var fecha = new Date();
        var hora = fecha.getHours();
        var minutos = fecha.getMinutes();

        // Horarios laborales
        var inicioJornada1 = 9;  // 9:00 AM
        var finJornada1 = 12;    // 12:00 PM
        var inicioJornada2 = 15; // 3:00 PM
        var finJornada2 = 18;    // 6:00 PM

        // Verificar si la hora actual está dentro de los horarios laborales
        if ((hora >= inicioJornada1 && hora < finJornada1) || (hora >= inicioJornada2 && hora < finJornada2)) {
            // Formatear la hora y los minutos para que siempre tengan dos dígitos
            var horaFormateada = ("0" + hora).slice(-2) + ":" + ("0" + minutos).slice(-2);
            document.getElementById('hora').value = horaFormateada;
        } else {
            alert("No es un horario laboral. Los horarios laborales son de 09:00 AM a 12:00 PM y de 03:00 PM a 06:00 PM.");
        }
    });
}


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
