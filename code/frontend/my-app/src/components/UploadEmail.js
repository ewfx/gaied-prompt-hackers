import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

function UploadEmail() {
  const [file, setFile] = useState(null);
  const [categories, setCategories] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setCategories([]);
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
        "http://localhost:8000/upload-email",
        formData
      );
      setCategories(response.data.categories || []);
      setMessage(response.data.status || "Email processed successfully.");
    } catch (error) {
      setMessage("Error processing email. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          📧 Upload Email
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Upload an email file to classify it based on the rules.
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
        {categories.length > 0 && (
          <div style={{ marginTop: "20px" }}>
            <Typography variant="h6">Categories:</Typography>
            <List>
              {categories.map((category, index) => (
                <ListItem key={index}>
                  <ListItemText primary={category} />
                </ListItem>
              ))}
            </List>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default UploadEmail;
