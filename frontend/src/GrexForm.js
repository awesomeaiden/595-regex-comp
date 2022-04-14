import React, { useState } from "react";
import {
    Grid,
    TextField,
    Button,
    Paper
} from '@mui/material';
import './GrexForm.css';

const GrexForm = () => {
    const [inputValue, setInputValue] = useState("");
    const [grexResponse, setGrexResponse] = useState("");

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setInputValue(value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        // Parse input
        console.log(inputValue);
        let stringArray = inputValue.split(',');
        console.log(stringArray);

        const postConfig = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                strings: stringArray
            })
        };

        fetch("http://localhost:8000/grex", postConfig).then(async function (response) {
            response = await response.json();
            let regex = response.grex;
            console.log(regex);
            setGrexResponse(regex);
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <Grid container alignItems="center" justify="center" direction="column">
                <Grid item>
                    Enter a comma-separated list of strings below to receive a regular expression that matches them:
                </Grid>

                <Grid item>
                    <TextField
                        id="grex-input"
                        name="grex"
                        label="Input strings"
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        sx={{
                            margin: 2,
                            width: 500
                        }}
                    />
                </Grid>

                <Grid item id="grex-output">
                    <Paper elevation={3} id="grex-output">
                        {grexResponse}
                    </Paper>
                </Grid>

                <Button variant="contained" color="primary" type="submit" id="grex-submit">
                    Get Regex
                </Button>
            </Grid>
        </form>
    );
};

export default GrexForm;
