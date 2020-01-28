function validacion() {
    if (document.forms['CamposReg']['NombUsInname'].value.includes(" ")) {
        // Si no se cumple la condicion...
        alert('[ERROR] El campo Nombre no puede tener espacios');
        return false;
    }
    if (document.forms['CamposReg']['NombUsInname'].value.includes(" ")) {
        // Si no se cumple la condicion...
        alert('[ERROR] El campo Nombre no puede tener espacios');
        return false;
    }
    if (document.forms['CamposReg']['NombUsInname'].value.length < 5) {
        // Si no se cumple la condicion...
        alert('[ERROR] El campo Nombre no puede ser menor de 5 caracteres');
        return false;
    }
    if (document.forms['CamposReg']['ContInname'].value.length<8) {
        // Si no se cumple la condicion...
        alert('[ERROR] La contraseña debe contener al menos 8 caracteres');
        return false;
    }
    if (document.forms['CamposReg']['ContInname'].value != document.forms['CamposReg']['Cont2'].value) {
        // Si no se cumple la condicion...
        alert('[ERROR] Las contraseñas deben ser iguales');
        return false;
    }
    if (!document.forms['CamposReg']['EmaiIlnname'].value.includes("@")) {
        // Si no se cumple la condicion...
        alert('[ERROR] El campo Email tiene que ser un email valido');
        return false;
    }
    if (document.forms['CamposReg']['TarInname'].value.length != 16) {
        // Si no se cumple la condicion...
        alert('[ERROR] La tarjeta debe tener 16 caracteres');
        return false;
    }
    return true;
}
function getaleatorio(num){
    let ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function(){
        document.getElementById("rand").innerHTML = this.responseText;
    }
    ajax.open("GET", num, true);
    ajax.send();

}
$(document).ready(function () {
    $("#ContInname").keyup(function(event){
        var num = 0;
        if($(this).val().length<8){
            $('#fortaleza').val(0);
            return true;
        }
        if($(this).val().length>8){
            num+=33;
        }
        if($(this).val().includes(".") || $(this).val().includes(",") || $(this).val().includes("_") || $(this).val().includes("-")){
            num+=33;
        }
        if($(this).val().toLowerCase() != $(this).val() && $(this).val().toUpperCase() != $(this).val()){
            num+=33;
        }
        $('#fortaleza').val(num);
        return true;
    });
});