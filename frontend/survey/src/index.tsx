import { Component, ReactNode, lazy } from "react";
import ReactDOM from 'react-dom';
import "./main.css"

const SurveyForm = lazy(() => import(/* webpackChunkName: "surveyForm" */ './components/SurveyForm'));

class App extends Component {
    render() {
        return( <SurveyForm/>)
    }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);