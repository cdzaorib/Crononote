let currentDate = new Date();
let userLogs = {};

const monthNames = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

// Elementos do DOM
const monthYearDisplay = document.getElementById("month-year-display");
const calendarDays = document.getElementById("calendar-days");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");

const modal = document.getElementById("study-modal");
const closeModalBtn = document.getElementById("close-modal-btn");
const cancelBtn = document.getElementById("cancel-btn");
const studyForm = document.getElementById("study-form");
const entryDateInput = document.getElementById("entry-date");
const entryTopicInput = document.getElementById("entry-topic");
const entryNotesInput = document.getElementById("entry-notes");
const modalDateDisplay = document.getElementById("modal-date-display");

document.addEventListener("DOMContentLoaded", () => {
    fetchLogs();

    prevBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    closeModalBtn.addEventListener("click", closeModal);
    cancelBtn.addEventListener("click", closeModal);
    studyForm.addEventListener("submit", handleSave);
});

// Busca os registros via API do Flask
function fetchLogs() {
    fetch("/logs")
        .then(response => response.json())
        .then(data => {
            userLogs = {};
            data.forEach(item => {
                userLogs[item.date] = {
                    topic: item.topic,
                    notes: item.notes
                };
            });
            renderCalendar();
        })
        .catch(err => console.error("Erro ao carregar dados:", err));
}

// Renderiza os blocos dos dias do mês atual
function renderCalendar() {
    calendarDays.innerHTML = "";

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthYearDisplay.textContent = `${monthNames[month]} de ${year}`;

    const firstDayIndex = new Date(year, month, 1).getDay();
    const totalDays = new Date(year, month + 1, 0).getDate();

    // Espaços vazios antes do dia 1
    for (let i = 0; i < firstDayIndex; i++) {
        const emptyDiv = document.createElement("div");
        emptyDiv.classList.add("day-box", "empty");
        calendarDays.appendChild(emptyDiv);
    }

    const today = new Date();

    for (let day = 1; day <= totalDays; day++) {
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("day-box");

        const formattedDate = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;

        if (
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            dayDiv.classList.add("today");
        }

        const dayNumber = document.createElement("span");
        dayNumber.classList.add("day-number");
        dayNumber.textContent = day;
        dayDiv.appendChild(dayNumber);

        if (userLogs[formattedDate] && userLogs[formattedDate].topic) {
            dayDiv.classList.add("has-study");
            const badge = document.createElement("span");
            badge.classList.add("day-badge");
            badge.textContent = userLogs[formattedDate].topic;
            dayDiv.appendChild(badge);
        }

        dayDiv.addEventListener("click", () => openModal(formattedDate, day, month, year));
        calendarDays.appendChild(dayDiv);
    }
}

function openModal(dateString, day, month, year) {
    entryDateInput.value = dateString;
    modalDateDisplay.textContent = `${day} de ${monthNames[month]} de ${year}`;

    if (userLogs[dateString]) {
        entryTopicInput.value = userLogs[dateString].topic || "";
        entryNotesInput.value = userLogs[dateString].notes || "";
    } else {
        entryTopicInput.value = "";
        entryNotesInput.value = "";
    }

    modal.classList.remove("hidden");
    entryTopicInput.focus();
}

function closeModal() {
    modal.classList.add("hidden");
}

// Envia os dados para a rota /save
function handleSave(event) {
    event.preventDefault();

    const date = entryDateInput.value;
    const topic = entryTopicInput.value.trim();
    const notes = entryNotesInput.value.trim();

    fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ date, topic, notes })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro na requisição");
        }
        return response.json();
    })
    .then(result => {
        if (result.success) {
            if (!topic && !notes) {
                delete userLogs[date];
            } else {
                userLogs[date] = { topic, notes };
            }
            closeModal();
            renderCalendar();
        }
    })
    .catch(err => console.error("Erro ao salvar:", err));
}
