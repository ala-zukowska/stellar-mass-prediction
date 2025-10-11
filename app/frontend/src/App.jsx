import { Button } from '@mui/material'
import { Routes, Route, Link } from 'react-router-dom'
import Predict from './components/predict'
import Home from './components/home'
import Graphs from './components/graphs'

const navBarStyle = {
  display: 'flex',
  flexDirection: 'row',
  padding: 10,
  gap: '1.5em',
  alignItems: 'center',
  justifyContent: 'center',

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
      </div>
    </div>
  )
}

const App = () => {

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
    </Routes>
    </>
  )
}

export default App
