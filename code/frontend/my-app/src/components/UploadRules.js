import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  CircularProgress,
  Snackbar,
  Alert,
} from "@mui/material";

function UploadRules({ setRulesUploaded }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false); // State to control Snackbar visibility

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload.");
      setSnackbarOpen(true); // Show Snackbar for error
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsLoading(true);
      const response = await axios.post(
        "http://localhost:8000/upload-rules",
        formData
      );
      setMessage(response.data.status || "Rules uploaded successfully.");
      setRulesUploaded(true); // Notify parent that rules are uploaded
      setSnackbarOpen(true); // Show Snackbar for success
    } catch (error) {
      setMessage("Error uploading rules. Please try again.");
      setRulesUploaded(false); // Reset the status on failure
      setSnackbarOpen(true); // Show Snackbar for error
    } finally {
      setIsLoading(false);
    }
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false); // Close the Snackbar
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          📜 Upload Classification Rules
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Upload a JSON file containing your classification rules.
        </Typography>
        <form onSubmit={handleSubmit} style={{ marginTop: "10px" }}>
          <TextField
            type="file"
            onChange={handleFileChange}
            fullWidth
            variant="outlined"
            margin="normal"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            disabled={isLoading}
          >
            {isLoading ? <CircularProgress size={24} /> : "Upload"}
          </Button>
        </form>

        {/* Snackbar for success or error messages */}
        <Snackbar
          open={snackbarOpen}
          autoHideDuration={5000} // Automatically hide after 5 seconds
          onClose={handleSnackbarClose}
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
        >
          <Alert
            onClose={handleSnackbarClose}
            severity={message.includes("Error") ? "error" : "success"}
            sx={{ width: "100%" }}
          >
            {message}
          </Alert>
        </Snackbar>
      </CardContent>
    </Card>
  );
}

export default UploadRules;
