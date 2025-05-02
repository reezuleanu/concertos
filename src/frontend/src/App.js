import './App.css';
import {BrowserRouter as Router,Routes, Route} from "react-router-dom"
import Programmer from './components/programmer';
import Sidebar from './components/sidebar';
import Settings from './pages/event_settings';
import Image from './components/image';
import Devices from './components/devices';
import Firmware from './components/firmware';



function App() {
  return (
    <div className="App">
      <body className="App-header">
          <header className="Header">
            <h1>ConcertOS</h1>
            <div className='nav'>
              {/* <input type='text' placeholder='Search'></input> */}
              <button>Events</button>
              <a href="/firmware">
                <button>Firmware</button>
              </a>
              <button>About</button>
            </div>

          </header>
          <div> 
            <Router>
            <Routes>
              <Route path = "/create" element = {<Programmer/>}/>
              <Route path = "/sidebar" element = {<Sidebar/>}/>
              <Route path='/settings/:eventid/:option/' element = {<Settings/>}/>
              <Route path="/settings/:eventid/" element = {<Settings/>}/>
              <Route path="/firmware/" element = {<Firmware/>}/>
            </Routes>
          </Router>
          </div>
      </body>
    </div>
  );
}

export default App;
