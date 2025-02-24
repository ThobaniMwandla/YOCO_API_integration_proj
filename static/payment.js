document.addEventListener('DOMContentLoaded', function() {
    const yocoSDK = new window.YocoSDK({ publicKey: yocoPublicKey });

    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        var amountInput = document.getElementById('amount');
        var amount = amountInput.value;
        
        yocoSDK.showPopup({
            amountInCents: amount * 100,
            currency: 'ZAR',
            callback: function(result) {
                if (result.error) {
                    alert("Error creating token: " + result.error.message); // Error alert
                } else {
                    var token = result.id;
                    fetch('/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            amount: amount,
                            token: token
                        })
                    }).then(response => response.json())
                      .then(data => {
                          if (data.error) {
                              alert("Payment failed: " + data.errorMessage); // Payment failed alert
                          } else {
                              alert("Payment successful!"); // Payment successful alert
                              amountInput.value = ''; // Clear the input field
                          }
                      })
                      .catch(error => {
                          console.error(error);
                          alert("Payment failed: An error occurred."); // Payment failed alert
                      });
                }
            }
        });
    });
});

