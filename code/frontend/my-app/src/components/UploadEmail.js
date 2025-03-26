import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tooltip,
  Box,
  Paper,
} from "@mui/material";

function UploadEmail({ rulesUploaded }) {
  const [files, setFiles] = useState([]); // State to store multiple files
  const [emailResponses, setEmailResponses] = useState([]); // State to store responses for all emails
  const [selectedResponse, setSelectedResponse] = useState(null); // State for the selected email response
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false); // State to control the modal

  const handleFileChange = (e) => {
    setFiles(e.target.files); // Store multiple files
    setEmailResponses([]);
    setSelectedResponse(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      alert("Please select at least one file to upload.");
      return;
    }

    const formData = new FormData();
    Array.from(files).forEach((file) => {
      formData.append("files", file); // Append multiple files
    });

    try {
      setIsLoading(true);
      const response = await axios.post(
        "http://localhost:8000/upload-emails", // Backend endpoint for multiple emails
        formData
      );

      // Parse and clean the classification field for each email
      const parsedResponses = response.data.map((emailResponse) => {
        const classification = emailResponse.classification[0]?.classification;
        let parsedClassification = null;

        if (classification) {
          try {
            // Remove Markdown-style code block markers and parse JSON
            parsedClassification = JSON.parse(
              classification.replace(/```json|```/g, "").trim()
            );
          } catch (error) {
            console.error("Error parsing classification JSON:", error);
          }
        }

        return {
          ...emailResponse,
          parsedClassification,
        };
      });

      // Store responses for all emails
      setEmailResponses(parsedResponses);
    } catch (error) {
      alert("Error processing emails. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRowClick = (response) => {
    setSelectedResponse(response); // Set the selected email response
    setOpen(true); // Open the modal
  };

  const handleClose = () => {
    setOpen(false); // Close the modal
  };

  return (
    <>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            📧 Upload Emails
          </Typography>
          <Typography variant="body2" color="textSecondary" gutterBottom>
            Upload multiple email files to classify them based on the rules.
          </Typography>
          <form onSubmit={handleSubmit} style={{ marginTop: "10px" }}>
            <TextField
              type="file"
              onChange={handleFileChange}
              inputProps={{ multiple: true }} // Allow multiple file selection
              fullWidth
              variant="outlined"
              margin="normal"
              disabled={!rulesUploaded} // Disable file input if rules are not uploaded
            />
            <Tooltip
              title={
                !rulesUploaded
                  ? "Please upload classification rules first."
                  : ""
              }
              arrow
            >
              <span>
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

          {/* Modal to display the selected email response */}
          <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
            <DialogTitle>Email Details</DialogTitle>
            <DialogContent>
              {selectedResponse && selectedResponse.parsedClassification && (
                <>
                  <Typography variant="h6" gutterBottom>
                    Classification Details:
                  </Typography>
                  <Typography variant="body2">
                    <strong>Request Type:</strong>{" "}
                    {
                      selectedResponse.parsedClassification.classification
                        ?.request_type
                    }
                  </Typography>
                  <Typography variant="body2">
                    <strong>Sub-Request Type:</strong>{" "}
                    {
                      selectedResponse.parsedClassification.classification
                        ?.sub_request_type
                    }
                  </Typography>
                  <Typography variant="body2">
                    <strong>Reasoning:</strong>{" "}
                    {
                      selectedResponse.parsedClassification.classification
                        ?.reasoning
                    }
                  </Typography>

                  <Box mt={2}>
                    <Typography variant="h6" gutterBottom>
                      Extracted Data:
                    </Typography>
                    <Typography variant="body2">
                      <strong>Deal Name:</strong>{" "}
                      {
                        selectedResponse.parsedClassification.extracted_data
                          ?.deal_name
                      }
                    </Typography>
                    <Typography variant="body2">
                      <strong>Amount:</strong>{" "}
                      {
                        selectedResponse.parsedClassification.extracted_data
                          ?.amount
                      }
                    </Typography>
                    <Typography variant="body2">
                      <strong>Expiration Date:</strong>{" "}
                      {
                        selectedResponse.parsedClassification.extracted_data
                          ?.expiration_date
                      }
                    </Typography>
                  </Box>

                  <Box mt={2}>
                    <Typography variant="h6" gutterBottom>
                      Duplicate Email Detection:
                    </Typography>
                    <Typography variant="body2">
                      <strong>Is Duplicate:</strong>{" "}
                      {selectedResponse.parsedClassification.duplicate_email}
                    </Typography>
                  </Box>
                </>
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
      <>
        {/* Table to display email responses */}
        {emailResponses.length > 0 && (
          <TableContainer
            component={Paper}
            style={{
              marginTop: "20px",
              width: "80vw",
              position: "relative",
              right: "-22%",
              marginLeft: "-50vw",
              marginRight: "-50vw",
            }}
          >
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>
                    <strong>Email File</strong>
                  </TableCell>
                  <TableCell>
                    <strong>Status</strong>
                  </TableCell>
                  <TableCell>
                    <strong>Actions</strong>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {emailResponses.map((response, index) => (
                  <TableRow
                    key={index}
                    hover
                    onClick={() => handleRowClick(response)}
                  >
                    <TableCell>
                      {response.file_name || `Email ${index + 1}`}
                    </TableCell>
                    <TableCell>{response.status}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        color="primary"
                        onClick={() => handleRowClick(response)}
                      >
                        View Details
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </>
    </>
  );
}

export default UploadEmail;
