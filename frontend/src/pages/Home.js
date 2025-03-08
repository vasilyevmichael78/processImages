import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import axios from "axios";

const fetchImages = async () => {
  const { data } = await axios.get("http://localhost:8000/images");
  return data;
};

const deleteImage = async (imageId) => {
  await axios.delete(`http://localhost:8000/images/${imageId}`);
};

const Home = () => {
  const queryClient = useQueryClient();

  const {
    data: images,
    error,
    isLoading,
  } = useQuery({
    queryKey: ["images"],
    queryFn: fetchImages,
  });

  const mutation = useMutation({
    mutationFn: deleteImage,
    onSuccess: () => {
      queryClient.invalidateQueries(["images"]);
    },
  });

  if (isLoading) return <p>Loading images...</p>;
  if (error) return <p>Error loading images: {error.message}</p>;

  const handleDelete = (imageId) => {
    mutation.mutate(imageId);
  };

  return (
    <div className="container">
      <h1 className="header">Image Gallery</h1>
      <Link to="/upload" className="link">
        Upload New Image
      </Link>
      <div className="image-gallery">
        {images.map((image) => (
          <div key={image.id} className="image-item">
            <Link to={`/images/${image.id}`}>
              <img
                src={`http://localhost:8000/images/serve/latest-thumbnail/${image.id}`}
                alt={image.filename}
                className="image-thumbnail"
              />
            </Link>
            <button
              onClick={() => handleDelete(image.id)}
              className="btn-delete"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
