import React from 'react';
import ReactDOM from 'react-dom';
import Card from "@material-ui/core/Card";
import "./main.css"
import GrantsTable from './components/GrantsTable';

function App() {
    return (
        <div className="App">
            <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
            <h1 id='cic-heading'>COVID INFORMATION COMMONS</h1>
            <div className="grants-table">
                <GrantsTable/>
            </div>
            
        </div>
    )
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        