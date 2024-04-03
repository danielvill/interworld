// Ingresado validacion para celular y digitos correctos  
// Validacion de numero telefonico
document.querySelector('form').addEventListener('submit', function (event) {
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
    }
};
