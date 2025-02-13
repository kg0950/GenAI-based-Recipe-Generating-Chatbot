import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [ingredients, setIngredients] = useState("");
    const [recipe, setRecipe] = useState("");
    const [loading, setLoading] = useState(false);

    const generateRecipe = async () => {
        if (!ingredients.trim()) return;
        setLoading(true);
        setRecipe("");

        try {
            const res = await axios.post("http://localhost:5000/generate_recipe", { ingredients });
            setRecipe(res.data.recipe);
        } catch (error) {
            setRecipe("Error generating recipe. Please try again.");
        }
        
        setLoading(false);
    };

    return (
        <div className="chat-container">
            <h2>AI Recipe Generator</h2>
            <textarea 
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value)}
                placeholder="Enter ingredients (e.g., chicken, garlic, tomatoes)..."
            />
            <button onClick={generateRecipe} disabled={loading}>
                {loading ? "Generating..." : "Get Recipe"}
            </button>
            {recipe && <div className="recipe-box"><h3>Generated Recipe:</h3><p>{recipe}</p></div>}
        </div>
    );
}

export default App;
