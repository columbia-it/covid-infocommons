import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import NativeSelect from '@mui/material/NativeSelect';
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const ModelSelect = (props:any) => {

    const [selectedModel,setSelectedModel] = useState();

    const navigate = useNavigate();

    function handleModelChange(e:any) {
        console.log(e.target.value)
        setSelectedModel(e.target.value)
        switch (Number(e.target.value)) {
            case 0:
                navigate('/search');
                break;
            case 1:
                navigate('/search/grants');
                break;
            case 2:
                navigate('/search/people');
                break;
            case 3:
                navigate('/search/publications');
                break;
            case 4:
                navigate('/search/datasets');
                break;
        }
    }
    return (
        <div className='flex-child'>
            <FormControl fullWidth>
                {<InputLabel variant="outlined" htmlFor="uncontrolled-native">
                </InputLabel>}
                <NativeSelect
                    defaultValue={ props.selected_model }
                    inputProps={{
                        name: 'model',
                        id: 'uncontrolled-native',
                    }}
                    onChange={ handleModelChange }
                    variant='outlined'
                    value={ selectedModel }
                >   
                    <option value={0}>All</option>
                    <option value={1}>Grants</option>
                    <option value={2}>People</option>
                    <option value={3}>Publications</option>
                    <option value={4}>Datasets</option>
                </NativeSelect>
            </FormControl>
        </div>
    )
}

export default ModelSelect;
