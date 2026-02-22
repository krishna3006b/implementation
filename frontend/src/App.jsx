import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Dashboard from './pages/Dashboard'
import PredictRisk from './pages/PredictRisk'
import Statistics from './pages/Statistics'
import About from './pages/About'
import Login from './pages/Login'
import Lifestyle from './pages/Lifestyle'
import ProtectedRoute from './components/ProtectedRoute'
import PageWrapper from './components/PageWrapper'
import './App.css'

function App() {
  const location = useLocation()

  return (
    <div className="app">
      <Navbar />
      <main>
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<PageWrapper><Dashboard /></PageWrapper>} />
            <Route path="/predict" element={<PageWrapper><PredictRisk /></PageWrapper>} />
            <Route path="/statistics" element={<PageWrapper><Statistics /></PageWrapper>} />
            <Route path="/about" element={<PageWrapper><About /></PageWrapper>} />
            <Route path="/login" element={<PageWrapper><Login /></PageWrapper>} />
            <Route path="/lifestyle" element={<ProtectedRoute><PageWrapper><Lifestyle /></PageWrapper></ProtectedRoute>} />
          </Routes>
        </AnimatePresence>
      </main>
      <Footer />
    </div>
  )
}

export default App
