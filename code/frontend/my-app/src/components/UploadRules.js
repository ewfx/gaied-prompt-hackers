import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  CircularProgress,
} from "@mui/material";

function UploadRules() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload.");
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
    } catch (error) {
      setMessage("Error uploading rules. Please try again.");
    } finally {
      setIsLoading(false);
    }
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
        {message && (
          <Typography
            variant="body1"
            color={message.includes("Error") ? "error" : "primary"}
            style={{ marginTop: "10px" }}
          >
            {message}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default UploadRules;
