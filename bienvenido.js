function mostrarMensaje() {
  try {
    // Solicita el nombre del usuario
    let nombreUsuario = prompt("Por favor, ingresa tu nombre:");

    // Si el nombre está vacío o cancelado, usamos "invitado"
    if (!nombreUsuario || nombreUsuario.trim() === "") {
      nombreUsuario = "invitado";
    }

    // Obtenemos la fecha y hora actual
    let ahora = new Date();
    if (isNaN(ahora)) throw new Error("Fecha inválida");

    let horas = ahora.getHours();
    let minutos = ahora.getMinutes();
    let segundos = ahora.getSeconds();

    // Determina el saludo según la hora
    let saludo = "Buenos días";
    if (horas >= 12 && horas < 18) {
      saludo = "Buenas tardes";
    } else if (horas >= 18) {
      saludo = "Buenas noches";
    }

    // Formatea la hora como texto
    let horaTexto = horas.toString().padStart(2, '0') + ":" +
                    minutos.toString().padStart(2, '0') + ":" +
                    segundos.toString().padStart(2, '0');

    // Inserta el mensaje dentro del div con id "saludo"
    document.getElementById("saludo").innerHTML =
      `<h2>Bienvenido(a): ${nombreUsuario}</h2>
       <p>${saludo}</p>
       <p>Fecha: ${ahora.toLocaleDateString()}</p>
       <p>Hora: ${horaTexto}</p>`;
  } catch (error) {
    // Si ocurre un error, muestra un mensaje alternativo
    document.getElementById("saludo").innerHTML =
      `<p>Ocurrió un error al mostrar la bienvenida.</p>`;
  }
}

// Ejecuta la función al cargar el script
mostrarMensaje();
