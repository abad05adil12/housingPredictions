const form = document.getElementById("form");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const size = document.getElementById("size").value;
    const location = document.getElementById("location").value;
    const bedroom = document.getElementById("bedroom").value;
    const age = document.getElementById("age").value;

    result.innerText = "Predicting...";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                Size_sqft: size,
                Bedrooms: bedroom,
                House_Age: age,
                Location: location
            })
        });

        const data = await response.json();

        result.innerText = 
            "Estimated Price: PKR " + data.predicted_price_rupees.toLocaleString();

    } catch (error) {
        result.innerText = "Error connecting to server";
        console.log(error);
    }
});
