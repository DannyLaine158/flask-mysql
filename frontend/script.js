const API_URL = "http://127.0.0.1:5000/movies"; // cambia si tu backend está en otro lado

// 📌 Listar películas
async function loadMovies() {
  const res = await fetch(API_URL + "/");
  const movies = await res.json();

  const tbody = document.querySelector("#movies-table tbody");
  tbody.innerHTML = "";

  movies.forEach(m => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${m.id}</td>
      <td>${m.titulo}</td>
      <td>${m.director}</td>
      <td>${m.anio}</td>
      <td>${m.genero || "-"}</td>
      <td>${m.rating ?? "-"}</td>
      <td>${m.imagen ? `<img src="data:image/png;base64,${m.imagen}" width="60">` : "-"}</td>
      <td>
        <button onclick="editMovie(${m.id})">✏️ Editar</button>
        <button onclick="deleteMovie(${m.id})">🗑️ Eliminar</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// 📌 Eliminar película
async function deleteMovie(id) {
  if (!confirm("¿Seguro que deseas eliminar esta película?")) return;
  const res = await fetch(API_URL + "/" + id, { method: "DELETE" });
  const data = await res.json();
  alert(data.message);
  loadMovies();
}

// 📌 Cargar datos al formulario si es edición
async function initForm() {
  const params = new URLSearchParams(window.location.search);
  const movieId = params.get("id");

  const form = document.getElementById("movie-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const movie = Object.fromEntries(formData);

    // convertir archivo en base64 si se seleccionó
    const fileInput = document.getElementById("imagen");
    if (fileInput.files.length > 0) {
      movie.imagen = await toBase64(fileInput.files[0]);
    }

    let method = "POST";
    let url = API_URL + "/";
    if (movieId) {
      method = "PUT";
      url = API_URL + "/" + movieId;
    }

    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(movie),
    });

    const data = await res.json();
    alert(data.message);
    window.location.href = "index.html";
  });

  // Si estamos editando
  if (movieId) {
    document.getElementById("form-title").textContent = "✏️ Editar Película";
    document.getElementById("movie-id").value = movieId;

    const res = await fetch(API_URL + "/" + movieId);
    const movie = await res.json();

    form.titulo.value = movie.titulo;
    form.director.value = movie.director;
    form.anio.value = movie.anio;
    form.genero.value = movie.genero || "";
    form.rating.value = movie.rating ?? "";
  }
}

// 📌 Convertir archivo a Base64
function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.onerror = reject;
  });
}

// 📌 Redirigir a edición
function editMovie(id) {
  window.location.href = "form.html?id=" + id;
}
