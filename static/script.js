function openModal(modalId) {
    const modal = document.getElementById(modalId);

    if (modal) {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
    }
}


function closeModal(modalId) {
    const modal = document.getElementById(modalId);

    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = "";
    }
}


window.addEventListener("click", function (event) {

    if (event.target.classList.contains("modal")) {

        event.target.style.display = "none";
        document.body.style.overflow = "";

    }

});


function openStatusModal(shipmentId, currentStatus) {

    const modal = document.getElementById("statusModal");
    const form = document.getElementById("statusForm");
    const select = document.getElementById("statusSelect");

    if (!modal || !form || !select) {
        return;
    }

    form.action = "/update-shipment/" + shipmentId;

    select.value = currentStatus;

    openModal("statusModal");
}


function confirmDelete(itemName) {

    return confirm(
        "Are you sure you want to delete this " +
        itemName +
        "?"
    );

}


function validateShipmentForm() {

    const trackingId =
        document.querySelector(
            'input[name="tracking_id"]'
        ).value.trim();

    if (trackingId.length < 3) {

        alert(
            "Tracking ID must contain at least 3 characters."
        );

        return false;

    }

    return true;

}


function showSettingsMessage() {

    alert(
        "Settings saved successfully!"
    );

}


document.addEventListener("DOMContentLoaded", function () {

    const dateInput =
        document.getElementById("shipmentDate");

    if (dateInput && !dateInput.value) {

        const today = new Date();

        const year =
            today.getFullYear();

        const month =
            String(
                today.getMonth() + 1
            ).padStart(2, "0");

        const day =
            String(
                today.getDate()
            ).padStart(2, "0");

        dateInput.value =
            `${year}-${month}-${day}`;

    }

});


setTimeout(function () {

    const alerts =
        document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        alert.style.opacity = "0";

        setTimeout(function () {
            alert.remove();
        }, 300);

    });

}, 4000);