import { useState } from 'react'
import { Button } from '@mui/material'
import { Routes, Route, Link } from 'react-router-dom'
import Predict from './components/predict'
import Home from './components/home'
import About from './components/about'
import Graphs from './components/graphs'

const navBarStyle = {
  display: 'flex',
  flexDirection: 'row',
  padding: 2,
  gap: '4em',
  alignItems: 'center',
  justifyContent: 'center'
}

const headerStyle = {
  display: 'flex',
  justifyContent: 'center',
  color: 'lightblue'
}

const barStyle = {
  backgroundColor: 'navy',
  display: 'flex',
  flexDirection: 'column'
}

const backgroundStyle = {

}

const contentStyle = {

}

const NavBar = ({ style }) => {
  return (
    <div>
      <div style={style}>
        <Link to="/">
          <Button variant="contained">Home</Button>
        </Link>
        <Link to="/predict">
          <Button variant="contained">Predict</Button>
        </Link>
        <Link to="/graphs">
          <Button variant="contained">Graphs</Button>
        </Link>
        <Link to="/about">
          <Button variant="contained">About</Button>
        </Link>
      </div>
      <div>
        <Home />
      </div>
    </div>
  )
}

const App = () => {
  const [count, setCount] = useState(0)

  return (
    <>
    <div style={barStyle}>
      <h1 style={headerStyle}>Stellar Mass Prediction</h1>
      <NavBar style={navBarStyle}></NavBar>
    </div>

    <Routes>
      <Route path="/" element={<Home />}></Route>
      <Route path="/graphs" element={<Graphs />}></Route>
      <Route path="/predict" element={<Predict />}></Route>
      <Route path="/about" element={<About />}></Route>
    </Routes>
    </>
  )
}

export default App
