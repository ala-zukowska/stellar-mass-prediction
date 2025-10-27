import { useEffect, useState } from "react"
import { Button, TextField, Typography } from "@mui/material"
import Plot from "react-plotly.js"

const inputStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '3em',
    alignItems: 'center',
    justifyContent: 'center',
}

const Predict = () => {
    const [luminosity, setLuminosity] = useState("")
    const [metallicity, setMetallicity] = useState("")
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [plot, setPlot] = useState(null)

    useEffect(() => {
        const fetchGraph = async () => {
            try {
                const response = await fetch("/graph_data");
                if (!response.ok) throw new Error("Failed to load base data")
                const d = await response.json()
                setData(d)
                setPlot(true)
            } catch (err) {
                setError("Could not load initial graph")
            }
        }
        fetchGraph()
    }, [])

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
        <div style={{ position: "relative", width: "100%", minHeight: "90vh", padding: "0", backgroundColor: "rgba(0, 0, 0, 0.8)", ...inputStyle }}>
            <div style={{ paddingTop: "10%", padding: '2em', display: 'flex', flexDirection: 'column', gap: '2em'}}>
                <h3>Input values to predict stellar mass</h3>
                <form onSubmit={handleSubmit}
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: "1em",
                        color: "#DDD"
                }}>
                    <div style={{ display: "flex", flexDirection: "row", gap: "1em" }}>
                        <TextField
                        variant="outlined"
                        color="warning"
                        sx={{
                            "& .MuiOutlinedInput-root": {
                            color: "#DDD",
                            fontFamily: "Arial",
                            "& fieldset": {
                                borderColor: "#DDD",
                                borderWidth: "2px",
                            },
                            "&:hover fieldset": {
                                borderColor: "#DDD",
                            },
                            "&.Mui-focused fieldset": {
                                borderColor: "#CE8236",
                                borderWidth: "3px",
                            },
                            },
                        }}
                        InputLabelProps={{
                            sx: {
                            color: "#DDD",
                            "&.Mui-focused": {
                                color: "#CE8236",
                            },
                            },
                        }}
                        label="Luminosity (L☉)"
                        type="number"
                        value={luminosity}
                        onChange={(e) => setLuminosity(e.target.value)}
                        required
                        />
                        <TextField
                        variant="outlined"
                        color="warning"
                        sx={{
                            "& .MuiOutlinedInput-root": {
                            color: "#DDD",
                            fontFamily: "Arial",
                            "& fieldset": {
                                borderColor: "#DDD",
                                borderWidth: "2px",
                            },
                            "&:hover fieldset": {
                                borderColor: "#DDD",
                            },
                            "&.Mui-focused fieldset": {
                                borderColor: "#CE8236",
                                borderWidth: "3px",
                            },
                            },
                        }}
                        InputLabelProps={{
                            sx: {
                            color: "#DDD",
                            "&.Mui-focused": {
                                color: "#CE8236",
                            },
                            },
                        }}
                        label="Metallicity (Fe/H)"
                        type="number"
                        value={metallicity}
                        onChange={(e) => setMetallicity(e.target.value)}
                        required
                        />
                    </div>
                    <div>
                        <Button color="custom" variant="outlined" type="submit" disabled={loading}>
                            {loading ? "Predicting..." : "Predict"}
                        </Button>
                    </div>
                </form>

                {data?.predicted && (
                    <Typography color="custom" variant="h6" style={{ marginTop: "1em" }}>
                        Predicted Stellar Mass: {data.predicted.M} M☉
                    </Typography>
                )}

                {error && (
                    <Typography color="error" style={{ marginTop: "1em" }}>
                        {error}
                    </Typography>
                )}
            </div>

            {plot &&
            <div style={{ width: "100%", height: "720px"}}>
            <Plot
                data={[
                    {
                        x: data.stars.map(s => s.M),
                        y: data.stars.map(s => s.L),
                        mode: "markers",
                        marker: { color: "#d9a638ff", size: 5 },
                        name: "Stars"
                    },
                    {
                        x: data?.predicted?.M ? [data.predicted.M] : [],
                        y: data?.predicted?.L ? [data.predicted.L]: [],
                        mode: "markers",
                        marker: { color: '#822020ff', size: 8 },
                        name: "Predicted"
                    },
                    {
                        x: data.labels.map(s => s.M),
                        y: data.labels.map(s => s.L),
                        mode: "markers+text",
                        text: data.labels.map(s => s.Name),
                        textposition: "top center",
                        marker: { color: "#6ca9d5ff", size: 8 },
                        name: "Labeled stars",
                        hovertext: data.labels.map(s => s.Info)
                    }
                ]}
                layout={{
                    paper_bgcolor: "rgba(0, 0, 0, 0)",
                    plot_bgcolor: "rgba(0,0,0,0)",
                    font: { color: '#DDD' },
                    autosize: true,
                    margin: { l: 80, r: 40, b: 70, t: 70 },
                    xaxis: { title: { text: "Mass (M☉)" }, automargin: true, showgrid: false, zeroline: false, showline: false, showticklabels: false },
                    yaxis: { title: { text: "Luminosity (L☉)" }, type: "log", automargin: true, showgrid: false, zeroline: false, showline: false, showticklabels: false },
                    title: { text: "Mass-Luminosity relation"}
                }}
                useResizeHandler={true}
                style={{ width: "100%", height: "100%" }}
            />
            </div>}
        </div>
    )
}

export default Predict