const yocoSDK = new window.YocoSDK({ publicKey: yocoPublicKey });

// Popup Payment
document.getElementById("popup-pay").addEventListener("click", function() {
    yocoSDK.showPopup({
        currency: 'ZAR',
        amountInCents: 5000,
        name: 'Etechsolutions Payment',
        callback: function(response) {
            if (response.error) {
                alert(response.error.message);
            } else {
                processPayment(response.id);
            }
        }
    });
});

// Send token to Flask backend
function processPayment(token) {
    fetch('/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
    })
    .then(response => response.json())
    .then(data => alert(data.status || data.error))
    .catch(error => alert("Error: " + error.message));
}
