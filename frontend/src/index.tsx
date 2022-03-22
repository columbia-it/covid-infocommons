import React from 'react';
import ReactDOM from 'react-dom';
import DataTable from "react-data-table-component";
import Card from "@material-ui/core/Card";
import SortIcon from "@material-ui/icons/ArrowDownward";
import grants from "./grants";
import "./main.css"
import GrantsTable from './components/GrantsTable';

function App() {
    return (
        <div className="App">
            <h1 id='cic-heading'>COVID INFORMATION COMMONS</h1>
            <Card>
                {
                    <GrantsTable/>
                    /* <DataTable
                    title="Grants"
                    columns={columns}
                    data={grants}
                    defaultSortFieldId="title"
                    sortIcon={<SortIcon />}
                    pagination
                    selectableRows
                /> */}
            </Card>
        </div>
    )
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        