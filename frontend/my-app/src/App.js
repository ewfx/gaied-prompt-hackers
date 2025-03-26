import React from "react";
import { Container, Grid, Typography } from "@mui/material";
import UploadRules from "./components/UploadRules";
import UploadEmail from "./components/UploadEmail";

function App() {
  return (
    <Container maxWidth="lg" style={{ marginTop: "20px" }}>
      <Typography variant="h3" align="center" gutterBottom>
        Email Classification Dashboard
      </Typography>
      <Typography variant="subtitle1" align="center" gutterBottom>
        Manage your email classification rules and process emails effortlessly.
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <UploadRules />
        </Grid>
        <Grid item xs={12} md={6}>
          <UploadEmail />
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
