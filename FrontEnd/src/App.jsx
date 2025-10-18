import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Home from "./home"
import { Route, Routes } from 'react-router-dom'
import ErrorDisplay from './errorHandlingPage/errorPage'
import Connecting from './connectBackend'

function App() {
  const [error, setErr] = useState("");
  return (
    <>
    <Routes>
      <Route path='/' element={<Connecting setErr={setErr} />} />
      <Route path='/chatNow' element={<Home setErr={setErr} />} />
      <Route path='/error' element={<ErrorDisplay error={error} />} />
    </Routes>
    </>
  )
}

export default App