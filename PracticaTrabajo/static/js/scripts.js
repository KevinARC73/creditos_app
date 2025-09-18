const form = document.getElementById('creditoForm');
const tablaBody = document.querySelector('#tablaCreditos tbody');
const apiURL = "http://127.0.0.1:5000/creditos";
let graficoClientes;


// Listar créditos y actualizar tabla + gráfica
async function listarCreditos() {
    const response = await fetch(apiURL);
    const creditos = await response.json();
    tablaBody.innerHTML = '';

    creditos.forEach(c => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${c.id}</td>
            <td>${c.cliente}</td>
            <td>${c.monto}</td>
            <td>${c.tasa_interes}</td>
            <td>${c.plazo}</td>
            <td>${c.fecha_otorgamiento}</td>
            <td>
                <button class="edit" onclick="editarCredito(${c.id})">Editar</button>
                <button class="delete" onclick="eliminarCredito(${c.id})">Eliminar</button>
            </td>
        `;
        tablaBody.appendChild(row);
    });

    actualizarGrafico(creditos);
}

// Crear o actualizar crédito
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('creditoId').value;
    const data = {
        cliente: document.getElementById('cliente').value,
        monto: parseFloat(document.getElementById('monto').value),
        tasa_interes: parseFloat(document.getElementById('tasa_interes').value),
        plazo: parseInt(document.getElementById('plazo').value),
        fecha_otorgamiento: document.getElementById('fecha_otorgamiento').value
    };

    if (id) {
        await fetch(`${apiURL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    } else {
        await fetch(apiURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    }

    form.reset();
    document.getElementById('creditoId').value = '';
    listarCreditos();
});

// Editar crédito
async function editarCredito(id) {
    const response = await fetch(apiURL);
    const creditos = await response.json();
    const credito = creditos.find(c => c.id === id);

    if (credito) {
        document.getElementById('creditoId').value = credito.id;
        document.getElementById('cliente').value = credito.cliente;
        document.getElementById('monto').value = credito.monto;
        document.getElementById('tasa_interes').value = credito.tasa_interes;
        document.getElementById('plazo').value = credito.plazo;
        document.getElementById('fecha_otorgamiento').value = credito.fecha_otorgamiento;
    }
}

// Eliminar crédito
async function eliminarCredito(id) {
    if (confirm("¿Desea eliminar este crédito?")) {
        await fetch(`${apiURL}/${id}`, { method: 'DELETE' });
        listarCreditos();
    }
}

// Gráfica con Chart.js
function actualizarGrafico(creditos) {
    const clientes = [];
    const montos = [];

    creditos.forEach(c => {
        if (!clientes.includes(c.cliente)) {
            clientes.push(c.cliente);
            montos.push(c.monto);
        } else {
            const index = clientes.indexOf(c.cliente);
            montos[index] += c.monto;
        }
    });

    const ctx = document.getElementById('graficoClientes').getContext('2d');

    if (graficoClientes) graficoClientes.destroy();

    graficoClientes = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: clientes,
            datasets: [{
                label: 'Total Créditos por Cliente',
                data: montos,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

// Inicializar
listarCreditos();
