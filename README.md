# processImages

This project is a web application for processing and managing images. It consists of a frontend built with React and a backend built with FastAPI. The backend uses a PostgreSQL database to store image metadata.

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+
- Node.js and npm (for running the frontend separately)

## Running the Project with Docker Compose

To run the entire project using Docker Compose, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/processImages.git
   cd processImages
   ```

2. Set up environment variables:

   ```sh

   DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@db:5432/your_postgres_db
   ```

3. Build and start the containers:

   ```sh
   docker-compose up --build
   ```

4. Open your browser and navigate to `http://localhost:3000` to access the frontend.

## Running the Backend Separately

To run the backend separately, follow these steps:

1. Navigate to the backend directory:

   ```sh
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory with the following content:

   ```env
   DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db
   ```

5. Run the FastAPI server:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Running the Frontend Separately

To run the frontend separately, follow these steps:

1. Navigate to the frontend directory:

   ```sh
   cd frontend
   ```

2. Install the dependencies:

   ```sh
   npm install
   ```

3. Start the development server:

   ```sh
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000` to access the frontend.

## Setting Up PostgreSQL Database

To set up a PostgreSQL database, follow these steps:

1. Install PostgreSQL on your machine if you haven't already.

2. Create a new PostgreSQL database and user:

   ```sh
   psql -U postgres
   CREATE DATABASE your_postgres_db;
   CREATE USER your_postgres_user WITH ENCRYPTED PASSWORD 'your_postgres_password';
   GRANT ALL PRIVILEGES ON DATABASE your_postgres_db TO your_postgres_user;
   ```

3. Update the `DATABASE_URL` in your `.env` file with the appropriate values:

   ```env
   DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_postgres_db
   ```

## API Endpoints

| Method | Endpoint                                  | Description                                |
| ------ | ----------------------------------------- | ------------------------------------------ |
| POST   | /images/upload                            | Upload a new image                         |
| GET    | /images                                   | List all images                            |
| GET    | /images/{image_id}                        | Get details of a specific image            |
| DELETE | /images/{image_id}                        | Delete a specific image                    |
| POST   | /images/edit/{image_id}                   | Apply a transformation to a specific image |
| GET    | /images/versions/{image_id}               | Get all versions of a specific image       |
| POST   | /images/revert/{image_id}/{version_id}    | Revert to a specific version of an image   |
| GET    | /images/serve/{image_id}                  | Serve the original image                   |
| GET    | /images/serve/latest/{image_id}           | Serve the latest processed image           |
| GET    | /images/serve/latest-thumbnail/{image_id} | Serve the latest processed thumbnail       |
| GET    | /images/serve-by-path                     | Serve an image by its file path            |

## Viewing API Documentation

FastAPI automatically generates interactive API documentation. You can view the documentation by navigating to the following URLs:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These endpoints provide a user-friendly interface to explore and test the API.

## Architecture Decisions

- **Frontend**: The frontend is built with React to provide a responsive and interactive user interface.
- **Backend**: The backend is built with FastAPI to leverage its high performance and ease of use for building APIs.
- **Database**: PostgreSQL is used as the database to store image metadata due to its robustness and support for complex queries.
- **Docker**: Docker and Docker Compose are used to containerize the application, making it easy to deploy and manage dependencies.

## Assumptions and Limitations

- **Assumptions**: It is assumed that the user has Docker, Docker Compose, Python, and Node.js installed on their machine.
- **Limitations**: The current implementation does not include user authentication and authorization. Additionally, the image processing operations are limited to a few basic transformations.

## Potential Improvements

- **Authentication**: Implement user authentication and authorization to secure the application.
- **Advanced Image Processing**: Add more advanced image processing features such as filters, cropping, and resizing.
- **Scalability**: Improve the scalability of the application by using a distributed file storage system for storing images.
- **Testing**: Add unit tests and integration tests to ensure the reliability of the application.
- **CI/CD**: Set up continuous integration and continuous deployment pipelines to automate the testing and deployment process.
- **Batch Processing**: Add batch processing for multiple images.
- **Metadata Extraction**: Create image metadata extraction.
- **Format Conversion**: Implement image format conversion.
- **Abstraction Layers**: Add abstraction layers like services for getting data from the database to improve code maintainability and separation of concerns.
