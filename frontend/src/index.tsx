import React from 'react';
import ReactDOM from 'react-dom';
import Card from "@material-ui/core/Card";
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
        