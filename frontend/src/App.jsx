import { useState } from 'react'
import axios from 'axios';
import ChatInterface from './components/ChatInterface';

function App() {
  const [responseData, setResponseData] = useState(null);

  const handleQuery = async () => {
    try {
      // Appel à l'API backend
      const res = await axios.get('http://localhost:4000/api/query', {
        params: { request: 'Bonjour, comment ça va ?' }
      });
      setResponseData(res.data);
    } catch (error) {
      console.error("Erreur lors de l'appel à l'API:", error);
    }
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>Interface Utilisateur</h1>
      <button onClick={handleQuery}>Envoyer une requête</button>
      {responseData && (
        <div style={{ marginTop: '20px' }}>
          <h2>Réponse du Backend</h2>
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      )}
      <ChatInterface />
    </div>
  )
}

export default App
