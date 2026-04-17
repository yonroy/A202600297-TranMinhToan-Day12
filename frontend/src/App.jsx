import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [city, setCity] = useState('')
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const fetchWeather = async () => {
    if (!city) return
    setLoading(true)
    setError(null)
    
    try {
      // In production, we use relative paths if hosted on the same domain
      const apiHost = import.meta.env.VITE_API_BASE_URL || ''
      const apiKey = import.meta.env.VITE_API_AUTH_KEY || 'super-secret-key'
      
      const response = await fetch(`${apiHost}/api/weather?city=${city}`, {
        headers: {
          'x-api-key': apiKey
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to fetch weather')
      }
      
      const data = await response.json()
      setWeather(data)
    } catch (err) {
      setError(err.message)
      setWeather(null)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchWeather()
    }
  }

  return (
    <div className={`container ${mounted ? 'fade-in' : ''}`}>
      <div className="circle circle-1"></div>
      <div className="circle circle-2"></div>
      
      <div className="glass-card">
        <h1>SkyCast</h1>
        
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Search city..." 
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={fetchWeather}>Check</button>
        </div>

        {loading && <div className="loading">Seeking the clouds...</div>}
        
        {error && <div className="error-msg">{error}</div>}

        {weather && !loading && (
          <div className="weather-info">
            <div className="city-name">{weather.city}</div>
            <div className="description">{weather.description}</div>
            
            <div className="temp-container">
              {Math.round(weather.temp)}<span className="unit">°C</span>
            </div>

            <div className="details-grid">
              <div className="detail-item">
                <span className="detail-label">Humidity</span>
                <span className="detail-value">{weather.humidity}%</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Wind</span>
                <span className="detail-value">{weather.wind_speed} km/h</span>
              </div>
            </div>
          </div>
        )}

        {!weather && !loading && !error && (
          <div className="loading" style={{opacity: 0.5}}>Enter a city to see the magic.</div>
        )}
      </div>
    </div>
  )
}

export default App
