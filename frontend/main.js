// Trabajando la lógica del frontend
/*
titulo = document.getElementById("titulo-personalizado");

titulo.innerHTML = `
    <p class='has-text-warning'>Un titulo nuevo</p>
`;


nuevoParrafo = document.createElement("p");
nuevoParrafo.textContent = "Soy generado desde JS";
document.body.appendChild(nuevoParrafo);
*/
const API_URL = "http://127.0.0.1:5000/movies";

// Listar películas
async function loadMovies() {
    // Viene en forma de promesa
    const res = await fetch(API_URL + "/");
    const movies = await res.json(); // Viene como una lista de JSON
    console.log(movies);

    // Obteniendo el elemento <tbody>
    const tbody = document.querySelector("#movies-table tbody");
    tbody.innerHTML = "";

    movies.forEach(m => {
        // Creamos una fila para cada elemento
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${m.id}</td>
            <td>${m.titulo}</td>
            <td>${m.director}</td>
            <td>${m.anio}</td>
            <td>${m.genero}</td>
            <td>${m.rating}</td>
            <td>
                <img width='100' 
                    src='data:image/png;base64,${m.imagen}' />
            </td>
            <td>
                <button onclick='editMovie(${m.id})' 
                    class='button m-2 is-warning'>Editar</button>
                <button onclick='deleteMovie(${m.id})'
                    class='button m-2 is-danger'>Eliminar</button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

// Eliminar películas
async function deleteMovie(id) {
    if (!confirm("¿Seguro que quieres eliminar esta película?")) return;

    const res = await fetch(API_URL + "/" + id, { method: "DELETE" });
    const data = await res.json();
    alert(data.message);

    loadMovies();
}

// Editar películas
function editMovie(id) {
    window.location.href = "form.html?id=" + id;
}

async function initForm() {
    // Obtener parámetro que viene de la URL
    const params = new URLSearchParams(window.location.search);
    const movieId = params.get("id");

    const form = document.getElementById("movie-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Preparación para enviar la película
        const formData = new FormData(form);
        const movie = Object.fromEntries(formData);


        const fileInput = document.getElementById("imagen");
        if (fileInput.files.length > 0)
            movie.imagen = await toBase64(fileInput.files[0]);

        let url = API_URL + "/" + movieId;
        let method = "PUT";

        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });

        const data = await res.json();
        alert(data.message);
        window.location.href = "index.html";
    });
    
    if (movieId) {
        document.getElementById("form-title").textContent = "Editar pelicula";
        document.getElementById("movie-id").value = movieId;

        const res = await fetch(API_URL + "/" + movieId);
        const movie = await res.json();

        form.titulo.value = movie.titulo;
        form.director.value = movie.director;
        form.anio.value = movie.anio;
        form.genero.value = movie.genero;
        form.rating.value = movie.rating;
    }
}

// Convertir el archivo en cadena de texto
function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        // Obtenemos el archivo
        reader.onload = () => resolve(reader.result.split(",")[1]);

        // Si hubo un error, se devuelve aquí
        reader.onerror = reject;
    });
}

// Crear películas