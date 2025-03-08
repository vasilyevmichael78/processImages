import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { useState, useEffect } from "react";

const fetchImageDetails = async (imageId) => {
  const { data } = await axios.get(`http://localhost:8000/images/${imageId}`);
  return data;
};

const fetchImageVersions = async (imageId) => {
  const { data } = await axios.get(
    `http://localhost:8000/images/versions/${imageId}`
  );
  return data;
};

const editImage = async ({ imageId, transformation }) => {
  const { data } = await axios.post(
    `http://localhost:8000/images/edit/${imageId}`,
    { transformation }
  );
  return data;
};

const revertVersion = async ({ imageId, versionId }) => {
  const { data } = await axios.post(
    `http://localhost:8000/images/revert/${imageId}/${versionId}`
  );
  return data;
};

const ImageDetails = () => {
  const { imageId } = useParams();
  const queryClient = useQueryClient();
  const [transformation, setTransformation] = useState("");
  const [imageUrl, setImageUrl] = useState(
    `http://localhost:8000/images/serve/latest/${imageId}`
  );

  const {
    data: image,
    error,
    isLoading,
  } = useQuery({
    queryKey: ["image", imageId],
    queryFn: () => fetchImageDetails(imageId),
  });

  const {
    data: versions,
    isLoading: isLoadingVersions,
    error: errorVersions,
  } = useQuery({
    queryKey: ["versions", imageId],
    queryFn: () => fetchImageVersions(imageId),
  });

  const mutation = useMutation({
    mutationFn: editImage,
    onSuccess: () => {
      queryClient.invalidateQueries(["image", imageId]);
      queryClient.invalidateQueries(["versions", imageId]);
      setImageUrl(
        `http://localhost:8000/images/serve/latest/${imageId}?t=${new Date().getTime()}`
      );
    },
  });

  const revertMutation = useMutation({
    mutationFn: revertVersion,
    onSuccess: () => {
      queryClient.invalidateQueries(["image", imageId]);
      queryClient.invalidateQueries(["versions", imageId]);
      setImageUrl(
        `http://localhost:8000/images/serve/latest/${imageId}?t=${new Date().getTime()}`
      );
    },
  });

  if (isLoading || isLoadingVersions) return <p>Loading image details...</p>;
  if (error || errorVersions)
    return (
      <p>Error loading image: {error?.message || errorVersions?.message}</p>
    );

  if (!image) return <p>No image data available</p>;

  const handleEdit = (e) => {
    e.preventDefault();
    mutation.mutate({ imageId, transformation });
  };

  const handleRevert = (versionId) => {
    revertMutation.mutate({ imageId, versionId });
  };

  return (
    <div className="container">
      <h1 className="header">{image.filename}</h1>
      <div className="image-container">
        <img src={imageUrl} alt={image.filename} className="main-image" />
      </div>
      <p className="version-id">
        Current Version ID: {versions[0]?.version_id}
      </p>
      <form onSubmit={handleEdit} className="transformation-form">
        <label htmlFor="transformation" className="form-label">
          Select Transformation:
        </label>
        <select
          id="transformation"
          value={transformation}
          onChange={(e) => setTransformation(e.target.value)}
          className="form-select"
        >
          <option value="">Select a transformation</option>
          <option value="rotate">Rotate</option>
          <option value="flip">Flip</option>
          <option value="grayscale">Grayscale</option>
          <option value="brightness">Brightness</option>
        </select>
        <button type="submit" className="btn">
          Apply Transformation
        </button>
      </form>
      <h2 className="sub-header">Image Versions</h2>
      <div className="versions-list">
        {versions.map((version) => (
          <div key={version.version_id} className="version-item">
            <img
              src={`http://localhost:8000/images/serve-by-path/?image_path=${version.thumbnail}`}
              alt={`Version ${version.version_id}`}
              className="version-thumbnail"
            />
            <button
              onClick={() => handleRevert(version.version_id)}
              className="btn-revert"
            >
              Revert to Version {version.version_id}
            </button>
          </div>
        ))}
      </div>
      <div className="edit-link">
        <Link to={`/`} className="link">
          Back to Gallery
        </Link>
      </div>
    </div>
  );
};

export default ImageDetails;
