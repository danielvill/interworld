// Ingresado validacion para celular y digitos correctos  
window.onload = function() {
    var input = document.getElementById('miInput');
    input.value = '09';

    document.querySelector('form').onsubmit = function (e) {
        var inputs = this.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].value === '') {
                e.preventDefault();
                alert('Llene todos los campos');
                return;
            }
        }

        if (!/^09/.test(input.value)) {
            e.preventDefault();
            alert('El número de teléfono debe comenzar con 09');
            return;
        }

        if (input.value.length != 10) {
            e.preventDefault();
            alert('Por favor, introduce un número de teléfono de 10 dígitos');
            return;
        }

        alert('Guardado exitosamente');
    };
};


    // Funcion para evitar ingreso de caracteres al celular
    function limitarEntrada() {

        let x = document.getElementById("miInput");

        x.value = x.value.replace(/[^0-9]/g, ''); // Elimina cualquier caracter que no sea un número
        if (x.value.length > 10) {
            x.value = x.value.slice(0, 10); // Limita la longitud a 10
        }
    }


// Horas

    // Ingresado de Horas 
    $(document).ready(function () {
        $('#hora').on('change', function () {
            var horaSeleccionada = $(this).val();
            var hora = parseInt(horaSeleccionada.split(':')[0]);

            if ((hora < 9 || (hora > 12 && hora < 15) || hora > 18)) {
                alert('Por favor, selecciona una hora entre las 09:00 a 12:00, o entre las 15:00 a 18:00.');
                $(this).val('');
            }
        });

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
