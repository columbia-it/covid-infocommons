import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';
import People from './people_index';
import Publications from "./publications_index";
import Datasets from "./datasets_index";

export default function App() {
    return (
        <div>
          <Routes>
            <Route path="/search" element={<Home />} />
            <Route path="/search/grants" element={<Grants />} />
            <Route path="/search/people" element={<People />} />
            <Route path="/search/publications" element={<Publications />} />
            <Route path="/search/datasets" element={<Datasets />} />
          </Routes>
        </div>
    );
}