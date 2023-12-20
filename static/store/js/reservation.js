var selectedTables = [];

function selectTable(event, tableId) {
    event.preventDefault();
    var tableElement = document.getElementById(tableId);

    if (tableElement.classList.contains('already-reserved')) {
        return;
    }

    if (tableElement.classList.contains('selected')) {
        tableElement.classList.remove('selected');
        selectedTables = selectedTables.filter(id => id !== tableId);
    } else {
        tableElement.classList.add('selected');
        selectedTables.push(tableId);
    }

    updateFormDisplay();
}

function updateFormDisplay() {
    var reservationForm = document.getElementById('reservationForm');
    reservationForm.style.display = selectedTables.length > 0 ? 'block' : 'none';

    document.getElementById('selectedTablesInput').value = JSON.stringify(selectedTables);
}