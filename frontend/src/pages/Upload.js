import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an image to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:8000/images/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setLoading(false);
      navigate(`/images/${response.data.id}`);
    } catch (err) {
      setLoading(false);
      setError("Failed to upload image. Please try again.");
    }
  };

  return (
    <div className="container">
      <h1 className="header">Upload an Image</h1>
      <div className="upload-form">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>
      <div className="back-link">
        <Link to="/" className="link">
          Back to Gallery
        </Link>
      </div>
    </div>
  );
};

export default Upload;
