function validarFormulario() {
    var correo = document.getElementById('correo').value;
    var user = document.getElementById('user').value;
    
    if (!correo || !user ) {
        alert('Campos vacíos');
        return false;
    }

    var regex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    if (!regex.test(correo)) {
        alert('Por favor, ingresa un correo válido');
        return false;
    }
    alert('Envío exitoso');
    return true;
}