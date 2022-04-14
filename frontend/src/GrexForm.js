import React, { useState } from "react";
import {
    Grid,
    TextField,
    FormControlLabel,
    FormControl,
    FormLabel,
    Button
} from '@mui/material';

const GrexForm = () => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(name);
    console.log(value);
    setInputValue(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(inputValue);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container alignItems="center" justify="center" direction="column">
        <Grid item>
          <TextField
            id="grex-input"
            name="grex"
            label="Enter a series of comma-separated strings below to receive a regex which matches them"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
          />
        </Grid>

        <Button variant="contained" color="primary" type="submit">
          Submit
        </Button>
      </Grid>
    </form>
  );
};

export default GrexForm;
