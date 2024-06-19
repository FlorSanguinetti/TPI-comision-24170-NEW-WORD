/*VALIDAR FORMULARIO*/

/*Evitar que el form se envie
document.getElementById('formulario').addEventListener('submit', function(event) {
  event.preventDefault(); // Detener el envío del formulario
  console.log("preveted");
});*/

/*Valida campos obligatorios - NOMBRE, APELLIDO, DNI Y CORREO*/
document.getElementById('formulario').addEventListener('submit', function(event) {
  
  event.preventDefault(); // Detener el envío del formulario
  console.log("preveted");

  var nombre = document.getElementById('nombre').value;
  var apellido = document.getElementById('apellido').value;
  var dni = document.getElementById('dni').value;
  var correo = document.getElementById('correo').value;
  

  if (nombre === ''|| apellido === '' || dni === '' || correo === '') {
    alert('Por favor, completa todos los campos obligatorios.');
    event.preventDefault(); 
  }
});

