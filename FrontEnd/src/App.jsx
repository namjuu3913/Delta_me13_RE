import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Home from "./home"
import { Route, Routes } from 'react-router-dom'

function App() {
  const [error, setErr] = useState("");
  return (
    <>
    <Routes>
      <Route path='/' element={<Home setErr={setErr} />} />
    </Routes>
    </>
  )
}

export default App