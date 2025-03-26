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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tooltip,
} from "@mui/material";

function UploadEmail({ rulesUploaded }) {
  const [file, setFile] = useState(null);
  const [categories, setCategories] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false); // State to control the modal

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setCategories([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload.");
      setOpen(true); // Open the modal to show the message
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
      setOpen(true); // Open the modal to show the response
    }
  };

  const handleClose = () => {
    setOpen(false); // Close the modal
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
            disabled={!rulesUploaded} // Disable file input if rules are not uploaded
          />
          <Tooltip
            title={
              !rulesUploaded ? "Please upload classification rules first." : ""
            }
            arrow
          >
            <span>
              {/* Wrapping Button in a span to handle disabled tooltip */}
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={!rulesUploaded || isLoading} // Disable button if rules are not uploaded or loading
              >
                {isLoading ? <CircularProgress size={24} /> : "Upload"}
              </Button>
            </span>
          </Tooltip>
        </form>

        {/* Modal to display the response */}
        <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
          <DialogTitle>Response</DialogTitle>
          <DialogContent>
            <Typography
              variant="body1"
              color={message.includes("Error") ? "error" : "primary"}
              gutterBottom
            >
              {message}
            </Typography>
            {categories.length > 0 && (
              <div>
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
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </CardContent>
    </Card>
  );
}

export default UploadEmail;
