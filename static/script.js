document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let date = new Date(document.getElementById('date').value);
    let day = date.getDate();
    let month = date.getMonth() + 1; // Months are zero-based in JavaScript
    let year = date.getFullYear();

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ day: day, month: month, year: year })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = 'Predicted Price: $' + data.price.toFixed(2);
        resultDiv.style.opacity = 0;
        setTimeout(() => {
            resultDiv.style.opacity = 1;
        }, 100);
    })
    .catch(error => console.error('Error:', error));
});
