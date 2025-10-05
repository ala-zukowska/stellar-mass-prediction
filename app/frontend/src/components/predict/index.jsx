import { useState } from "react"
import { Button, TextField, Typography } from "@mui/material"

const inputStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4em',
    border: 'solid gray'
}

const Predict = () => {
    const [luminosity, setLuminosity] = useState("")
    const [metallicity, setMetallicity] = useState("")
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    luminosity: parseFloat(luminosity),
                    metallicity: parseFloat(metallicity),
                }),
        });
        if (!response.ok) throw new Error("Server error");

        const data = await response.json();
        setResult(data.prediction);
        } catch (err) {
            setError("Failed to get prediction");
        } finally {
            setLoading(false);
        }
    }
    return (
        <div style={inputStyle}>
        <h3>Input values to predict stellar mass</h3>

        <form onSubmit={handleSubmit}>
            <TextField
                label="Luminosity"
                variant="standard"
                type="number"
                value={luminosity}
                onChange={(e) => setLuminosity(e.target.value)}
                required
            />
            <TextField
                label="Metallicity"
                variant="standard"
                type="number"
                value={metallicity}
                onChange={(e) => setMetallicity(e.target.value)}
                required
            />
            <br />
            <Button variant="contained" type="submit" disabled={loading}>
                {loading ? "Predicting..." : "Predict"}
            </Button>
        </form>

        {result !== null && (
            <Typography variant="h6" style={{ marginTop: "1em" }}>
                Predicted Stellar Mass: {result}
            </Typography>
        )}

        {error && (
            <Typography color="error" style={{ marginTop: "1em" }}>
                {error}
            </Typography>
        )}
        </div>
    )
}

export default Predict