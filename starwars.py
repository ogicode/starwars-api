from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

BASE_URL = "https://swapi.dev/api/people/"

@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
    <html>
        <head>
            <title>Star Wars Character Lookup</title>
        </head>
        <body>
            <h2>Enter a Star Wars Character ID</h2>
            <form id="characterForm" onsubmit="event.preventDefault(); fetchCharacter();">
                <label for="character_id">Character ID:</label>
                <input type="number" id="character_id" name="character_id" min="1">
                <button type="button" onclick="fetchCharacter()">Search</button>
            </form>
            <div id="result"></div>
            <script>
                // Function to fetch the character details
                async function fetchCharacter() {
                    const characterId = document.getElementById('character_id').value;
                    const response = await fetch(`/character/${characterId}`);
                    const data = await response.json();
                    
                    // Display the results
                    if (data.error) {
                        document.getElementById('result').innerHTML = `<p style="color: red;">${data.error}</p>`;
                    } else {
                        document.getElementById('result').innerHTML = `
                            <h3>Character Details:</h3>
                            <p><strong>Name:</strong> ${data.name}</p>
                            <p><strong>Height:</strong> ${data.height}</p>
                            <p><strong>Mass:</strong> ${data.mass}</p>
                            <p><strong>Hair Color:</strong> ${data.hair_color}</p>
                            <p><strong>Skin Color:</strong> ${data.skin_color}</p>
                            <p><strong>Eye Color:</strong> ${data.eye_color}</p>
                            <p><strong>Birth Year:</strong> ${data.birth_year}</p>
                            <p><strong>Gender:</strong> ${data.gender}</p>
                        `;
                    }
                }

                // Add 'Enter' key event listener
                document.getElementById("character_id").addEventListener("keydown", function(event) {
                    if (event.key === "Enter") {
                        event.preventDefault();
                        fetchCharacter();
                    }
                });
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/character/{character_id}")
async def get_character(character_id: int):
    url = f"{BASE_URL}{character_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Character not found"}

# Run the app using: uvicorn main:app --reload
