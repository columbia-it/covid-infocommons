import { Component, ReactNode } from "react";
import ReactDOM from 'react-dom';
import "./main.css"
import SurveyForm from "./components/SurveyForm";

class App extends Component {
    render() {
        return( <SurveyForm/>)
    }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);