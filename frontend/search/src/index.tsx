import ReactDOM from 'react-dom';
import "./main.css"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from './app';

ReactDOM.render(
    <Router>
      <App/>
    </Router>,
    document.getElementById('root')
)
        
