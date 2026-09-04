function openAddShipment() {
    const modal = document.getElementById("shipmentModal");

    if (modal) {
        modal.style.display = "flex";
    }
}

function closeAddShipment() {
    const modal = document.getElementById("shipmentModal");

    if (modal) {
        modal.style.display = "none";
    }
}

async function addShipment() {
    const trackingId = document.getElementById("newTrackingId").value.trim();
    const product = document.getElementById("newProduct").value.trim();
    const destination = document.getElementById("newDestination").value.trim();
    const status = document.getElementById("newStatus").value;

    if (!trackingId || !product || !destination || !status) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch("/api/shipments", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tracking_id: trackingId,
                product: product,
                destination: destination,
                status: status
            })
        });

        const data = await response.json();

        if (data.success) {
            alert("Shipment added successfully!");

            closeAddShipment();

            document.getElementById("newTrackingId").value = "";
            document.getElementById("newProduct").value = "";
            document.getElementById("newDestination").value = "";
            document.getElementById("newStatus").value = "In Transit";

            location.reload();
        } else {
            alert(data.message);
        }

    } catch (error) {
        alert("Unable to add shipment.");
    }
}

function trackShipment() {
    const input = document.getElementById("trackingInput");
    const result = document.getElementById("trackingResult");

    if (!input || !result) {
        return;
    }

    const trackingId = input.value.trim();

    if (!trackingId) {
        result.style.display = "block";
        result.innerHTML = "Please enter a tracking ID.";
        return;
    }

    fetch("/api/shipments/" + trackingId)
        .then(response => response.json())
        .then(data => {
            result.style.display = "block";

            if (data.success) {
                result.innerHTML = `
                    <strong>${data.shipment.tracking_id}</strong><br>
                    Product: ${data.shipment.product}<br>
                    Destination: ${data.shipment.destination}<br>
                    Status: ${data.shipment.status}
                `;
            } else {
                result.innerHTML = "Shipment not found.";
            }
        })
        .catch(() => {
            result.style.display = "block";
            result.innerHTML = "Unable to track shipment.";
        });
}