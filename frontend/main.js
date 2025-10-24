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
const API_URL = "https://flask-backend-bxx5.onrender.com/movies";

/* UTILIDADES  */
async function fetchJSON(url, options = {}) {
    try {
        const res = await fetch(url, options);
        // console.log(res);
        // Codigo 200 = ok
        if (!res.ok) throw new Error("Error en la petición " + res.status);
        return await res.json(); // Devuelve la petición con código
    } catch (error) {
        console.log(error);
        alert("Ocurrió un error");
        return null;
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

// Listar películas
async function loadMovies(params = {}) {
    const query = new URLSearchParams(params).toString();

    // Viene en forma de promesa
    const movies = await fetchJSON(`${API_URL}/?${query}`) // Viene como una lista de JSON
    if (!movies) return;

    // Obteniendo el elemento <tbody>
    const tbody = document.querySelector("#movies-table tbody");
    tbody.innerHTML = "";

    movies.forEach(m => tbody.appendChild(createMovieRow(m)));
}

function createMovieRow(m) {
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

    return row;
}

document.addEventListener("click", e => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;

    const id = btn.dataset.id;
    const action = btn.dataset.action;

    if (action == "edit") return editMovie(id);
    if (action == "delete") return deleteMovie(id);
})

// Eliminar películas
async function deleteMovie(id) {
    if (!confirm("¿Seguro que quieres eliminar esta película?")) return;

    const data = await fetchJSON(API_URL + "/" + id, { method: "DELETE" });
    if (data) {
        alert(data.message);
        loadMovies();
    }
}

// Editar películas
function editMovie(id) {
    window.location.href = "form.html?id=" + id;
}

async function initForm() {
    const form = document.getElementById("movie-form");
    // Obtener parámetro que viene de la URL
    const params = new URLSearchParams(window.location.search);
    const movieId = params.get("id");

    const imagen_actual_input = document.getElementById("imagen_actual");
    const imagen_preview = document.getElementById("imagen-preview");
    const preview_field = document.getElementById("preview-field");
    const file_name = document.getElementById("file-name");
    const fileInput = document.getElementById("imagen");

    setupFileInput(fileInput, file_name, imagen_preview, preview_field);

    if (movieId) {
        await loadMovieData(movieId, form, file_name, imagen_preview, preview_field, imagen_actual_input)
    }

    form.addEventListener("submit", async (e) => {
        handleFormSubmit(e, form, fileInput, imagen_actual_input, movieId);
    });
}

async function loadMovieData(id, form, fileNameSpan, imagen_preview, preview_field, imagen_actual_input) {
    document.getElementById("form-title").textContent = "Editar pelicula";
    document.getElementById("movie-id").value = id;

    const movie = await fetchJSON(API_URL + "/" + id);
    if (!movie) return;

    const fields = ["titulo", "director", "anio", "genero", "rating"];
    fields.forEach(f => form[f].value = movie[f]);

    if (movie.imagen) {
        imagen_actual_input.value = movie.imagen;
        imagen_preview.src = "data:image/png;base64,"+movie.imagen;
        preview_field.style.display = "";
        fileNameSpan.textContent = "Imagen actual cargada";
    }

    /* 
    form.titulo.value = movie.titulo;
    form.director.value = movie.director;
    form.anio.value = movie.anio;
    form.genero.value = movie.genero;
    form.rating.value = movie.rating;
    */
}

function setupFileInput(fileInput, fileNameSpan, imagenPreview, previewField) {
    if (!fileInput) return;

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameSpan.textContent = file.name;
            imagenPreview.src = URL.createObjectURL(file);
            previewField.style.display = "";
        } else {
            fileNameSpan.textContent = "Ningún archivo seleccionado";
            previewField.style.display = "none";
        }
    })
}

async function handleFormSubmit(e, form, fileInput, imagen_actual_input, movieId) {
    e.preventDefault();

    // Preparación para enviar la película
    const formData = new FormData(form);
    const movie = Object.fromEntries(formData);

    if (fileInput.files.length > 0) {
        movie.imagen = await toBase64(fileInput.files[0]);
    } else {
        movie.imagen = imagen_actual_input.value || "";
    }

    console.log(movieId);

    let url = API_URL + "/";
    let method = "POST";

    if (movieId) {
        method = "PUT";
        url = API_URL + "/" + movieId;
    }

    const data = await fetchJSON(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(movie)
    });

    if (data) {
        alert(data.message);
        window.location.href = "index.html";
    }
}

function getFilters() {
    return {
        genero: document.querySelector("#filter-genero").value.trim(),
        min_rating: document.querySelector("#filter-rating").value.trim()
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadMovies();

    const filterBtn = document.querySelector("#filter-btn");

    filterBtn.addEventListener("click", () => {
        const filters = getFilters();
        loadMovies(filters);
    })
});