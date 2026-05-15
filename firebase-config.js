// Configuración Firebase del proyecto QR Photo Drop para la boda
// Guillermo & Loren · 16 de mayo de 2026.
//
// IMPORTANTE: este proyecto Firebase debe ser NUEVO, separado de cualquier
// otro proyecto del usuario. Crear en https://console.firebase.google.com
// y pegar acá las credenciales reales antes de hacer deploy en Vercel.

export const firebaseConfig = {
  apiKey: "__REEMPLAZAR_API_KEY__",
  authDomain: "__REEMPLAZAR_AUTH_DOMAIN__",
  projectId: "__REEMPLAZAR_PROJECT_ID__",
  storageBucket: "__REEMPLAZAR_STORAGE_BUCKET__",
  messagingSenderId: "__REEMPLAZAR_SENDER_ID__",
  appId: "__REEMPLAZAR_APP_ID__"
};

// Identificador raíz dentro de Storage. No tocar salvo que cambie el evento.
export const BODA_ID = "boda-guillermo-loren";
export const TOTAL_MESAS = 7;
export const COUPLE_NAME = "Guillermo & Loren";
export const WEDDING_DATE = "16 de mayo de 2026";

// Lista de invitados por mesa (tomada del seating chart real).
// Se usa para poblar el dropdown "Tu nombre" en la pantalla de bienvenida.
// Si un invitado no aparece, igual puede escribir su nombre como texto libre.
export const INVITADOS_POR_MESA = {
  1: [
    "Yurany Pedraza", "Andrés Cortés", "María Paula Cortés", "Ariana Cortés",
    "Cristian Pedraza", "Daniela Meneses", "Luciana Pedraza",
    "María Camila Pedraza", "Brandon Pedraza", "Alexandra Ortega"
  ],
  2: [
    "Miguel Capela", "María Peñaloza", "Hugo Capela", "Angie Montes",
    "Alan Capela", "Blanca Castro", "Neyin Forero", "Sneidher Yara",
    "Jeison Castro", "Junnel Bravo"
  ],
  3: [
    "Viviana Melendez", "Helen", "Maylen", "Angel", "Julio Martínez",
    "Katherine Visbal", "Francisco Delgado", "Gabriel Salcedo", "Beyorit Salcedo"
  ],
  4: [
    "Benigno King", "Ana Pacheco", "Santiago King", "Camila King",
    "Roberto Tapias", "Natalia King", "Habech Haecky", "Carlos Medina",
    "Sebastián Medina", "Laura Bohorquez"
  ],
  5: [
    "Luis Gabriel Silvera", "Astrid Peluffo", "Luis Gabriel Tapias",
    "Julieth Ramos", "Liliana Peluffo", "Yimis Benitez", "Rubén Barbas",
    "Claudia Barbas", "Alfredo Fernandez", "Maria José Fernandez"
  ],
  6: [
    "Navia Capela", "Julio Muñoz", "Juliana Muñoz", "Isabella Muñoz",
    "Marlene Capela", "Sara Vargas", "Jairo Villaveces", "Carla Jimenez",
    "Alejandra Vargas", "Angello Jimenez"
  ],
  7: [
    "Francisco Arenas", "Auri Manzur", "Melissa Arenas", "Justin De las Aguas",
    "Fidel Madero", "Cristina Madero", "Veronica Barcas", "Iván Barcas",
    "Samuel Madero", "Valentina De Las Aguas"
  ]
};
