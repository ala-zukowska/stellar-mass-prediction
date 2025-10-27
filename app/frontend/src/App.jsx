import './App.css'
import { Button } from '@mui/material'
import { createTheme } from '@mui/material/styles';
import { Routes, Route, Link } from 'react-router-dom'
import Predict from './components/predict'
import Home from './components/home'
import Graphs from './components/graphs'
import Def from './components/definitions'


const theme = createTheme({
  palette: {
    ochre: {
      main: '#CE8236',
      light: '#DDD',
      dark: '#A1420C',
      contrastText: '#242105',
    },
  },
});

const NavBar = () => {
  return (
    <div>
      <div className="nav-bar">
        <Link to="/">
          <Button color="custom">Home</Button>
        </Link>
        <Link to="/predict">
          <Button color="custom">Predict</Button>
        </Link>
        <Link to="/graphs">
          <Button color="custom">Graphs</Button>
        </Link>
        <Link to="/definitions">
          <Button color="custom">Definitions</Button>
        </Link>
      </div>
    </div>
  )
}

const App = () => {

  return (
    <>
    <div className="bar">
      <h1 className="header">Stellar Mass Prediction</h1>
      <NavBar/>
    </div>

    <Routes>
      <Route path="/" element={<Home />}></Route>
      <Route path="/graphs" element={<Graphs />}></Route>
      <Route path="/predict" element={<Predict />}></Route>
      <Route path="/definitions" element={<Def />}></Route>
    </Routes>
    </>
  )
}

export default App
