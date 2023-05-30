import { useNavigate } from "react-router-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';

export default function App() {
    const navigate = useNavigate();

    function handleChange(event:any) {
        console.log('//////')
        console.log(event)
        const params = new URLSearchParams(window.location.search)
        console.log(params.get('keyword'))
        let url = '/search/grants?keyword='+params.get('keyword')
        navigate(url)
    }
    
    return (
        <div>
          <select name="models" id="select-models" onChange={ e => handleChange(e) }>
            <option value="all">All</option>
            <option value="grants">Grants</option>
            <option value="people">People</option>
            <option value="publications">Publications</option>
            </select>
          <Routes>
            <Route path="/search" element={<Home />} />
            <Route path="/search/grants" element={<Grants />} />
          </Routes>
        </div>
    );
}