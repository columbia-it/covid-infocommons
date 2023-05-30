import { Outlet, Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

function handleChange(e:any){
  let navigate = useNavigate();
  navigate('/grants')
}

const Layout = () => {
  return (
    <>
      <select name="models" id="select-models" onChange={handleChange}>
        <option value="all">All</option>
        <option value="grants">Grants</option>
        <option value="people">People</option>
        <option value="publications">Publications</option>
      </select>
      {/* <nav>
        <ul>
          <li>
            <Link to="/search/:q">Home</Link>
          </li>
          <li>
            <Link to="/search/grants/:q">Grants</Link>
          </li>
        </ul>
      </nav> */}

      <Outlet />
    </>
  )
};

export default Layout;