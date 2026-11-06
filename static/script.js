function confirmDelete(message) {
    return window.confirm(message || "Sigur vrei sa stergi?");
}

function updateTotalCost() {
    const parts = Number(document.getElementById("parts_cost")?.value || 0);
    const labor = Number(document.getElementById("labor_cost")?.value || 0);
    const total = document.getElementById("total_cost");

    if (total) {
        total.value = (parts + labor).toFixed(2);
    }
}

document.querySelectorAll(".cost-input").forEach((input) => {
    input.addEventListener("input", updateTotalCost);
});

updateTotalCost();
