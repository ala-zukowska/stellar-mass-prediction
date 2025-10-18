import { useState } from "react"
import { Button, TextField, Typography } from "@mui/material"
import Plot from "react-plotly.js"

const inputStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4em',
    border: 'solid gray',
    backgroundColor: 'lightgray'
}

const Predict = () => {
    const [luminosity, setLuminosity] = useState("")
    const [metallicity, setMetallicity] = useState("")
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [plot, setPlot] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setData(null)
        setPlot(null)
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

        const d = await response.json()
        setData(d)
        setPlot(true)
        } catch (err) {
            setError("Failed to get prediction")
        } finally {
            setLoading(false)
        }
    }
    return (
        <div style={inputStyle}>
        <h3>Input values to predict stellar mass</h3>

        <form onSubmit={handleSubmit}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "1em",
        }}>
            <div style={{ display: "flex", flexDirection: "row" }}>
                <TextField
                    label="Luminosity (L☉)"
                    variant="standard"
                    type="number"
                    value={luminosity}
                    onChange={(e) => setLuminosity(e.target.value)}
                    required
                />
                <TextField
                    label="Metallicity (Fe/H)"
                    variant="standard"
                    type="number"
                    value={metallicity}
                    onChange={(e) => setMetallicity(e.target.value)}
                    required
                />
            </div>
            <div>
                <Button variant="contained" type="submit" disabled={loading}>
                    {loading ? "Predicting..." : "Predict"}
                </Button>
            </div>
        </form>

        {data !== null && (
            <Typography variant="h6" style={{ marginTop: "1em" }}>
                Predicted Stellar Mass: {data.predicted.M}
            </Typography>
        )}

        {error && (
            <Typography color="error" style={{ marginTop: "1em" }}>
                {error}
            </Typography>
        )}

        {plot && <Plot
            data={[
                {
                    x: data.stars.map(s => s.M),
                    y: data.stars.map(s => s.L),
                    mode: "markers",
                    marker: { color: "black", size: 5 },
                    name: "Stars"
                },
                {
                    x: [data.predicted.plot_M],
                    y: [data.predicted.L],
                    mode: "markers",
                    marker: { color: "red", size: 10 },
                    name: "Predicted"
                },
                {
                    x: data.labels.map(s => s.M),
                    y: data.labels.map(s => s.L),
                    mode: "markers+text",
                    text: data.labels.map(s => s.Name),
                    textposition: "top center",
                    marker: { color: "blue", size: 8 },
                    name: "Labeled stars",
                    hovertext: data.labels.map(s => s.Info)
                }
            ]}
            layout={{
                xaxis: { title: "M (M☉)" },
                yaxis: { title: "L (L☉)", type: "log" },
                title: "Mass-Luminosity Relation"
            }}
        />}
        </div>
    )
}

export default Predict