import { useState } from "react"
import { Button, TextField } from "@mui/material"

const inputStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4em',
    border: 'solid gray'
}

const Predict = () => {
    const handleSubmit = (e) => {
        e.preventDefault()
    }
    return (
        <div style={inputStyle}>
            <h3>Input values to predict stellar mass</h3>
            <form onSubmit={handleSubmit}>
                <TextField label="Luminosity" variant="standard" />
                <TextField label="Metallicity" variant="standard" />
                <br />
                <Button type="submit">Predict</Button>
            </form>
        </div>
    )
}

export default Predict