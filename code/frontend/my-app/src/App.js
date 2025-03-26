import React, { useState } from "react";
import { Container, Grid, Typography, Box } from "@mui/material";
import UploadRules from "./components/UploadRules";
import UploadEmail from "./components/UploadEmail";

function App() {
  const [rulesUploaded, setRulesUploaded] = useState(false); // Track if rules are uploaded

  return (
    <Container
      maxWidth="lg"
      style={{ marginTop: "60px", marginBottom: "40px" }}
    >
      {/* Title Section */}
      <Box textAlign="center" mb={6}>
        <Typography variant="h3" gutterBottom>
          📧 Email Classification Dashboard
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Seamlessly upload classification rules and process emails with ease.
        </Typography>
      </Box>

      {/* Upload Sections */}
      <Grid container spacing={6}>
        <Grid item xs={12} md={6}>
          <UploadRules setRulesUploaded={setRulesUploaded} />
        </Grid>
        <Grid item xs={12} md={6}>
          <UploadEmail rulesUploaded={rulesUploaded} />
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
