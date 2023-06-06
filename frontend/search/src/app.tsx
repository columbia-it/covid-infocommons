import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './home';
import Grants from './grants_index';
import People from './people_index';
import Publications from "./publications_index";
import Datasets from "./datasets_index";

export default function App() {
    // const navigate = useNavigate();

    // function handleChange(event:any) {
    //     console.log('//////')
    //     console.log(event)
    //     const params = new URLSearchParams(window.location.search)
    //     console.log(params.get('keyword'))
    //     let url = '/search/grants?keyword='+params.get('keyword')
    //     navigate(url)
    // }
    
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