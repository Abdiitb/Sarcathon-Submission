async function searchFAQ() {
    const query = document.getElementById("query").value;
    const response = await fetch('http://127.0.0.1:8000/api/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    
    if (result.question) {
        document.getElementById("result").style.display = 'block';
        document.getElementById("result").innerHTML = `
            
            <p>${result.answer}</p>
            
        `;
    } else {
        document.getElementById("result").style.display = 'block';
        document.getElementById("result").innerHTML = `<p>No matching FAQ found.</p>`;
    }
}