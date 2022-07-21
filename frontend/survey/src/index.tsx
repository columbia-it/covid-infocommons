import { Component } from "react";
import ReactDOM from 'react-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import SurveyForm from "./components/survey_form";
class App extends Component {
    render() {
        return (
        <div>
            <SurveyForm/>
        </div>
    )};
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);




