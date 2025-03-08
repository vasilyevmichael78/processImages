import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Upload from "./pages/Upload";
import ImageDetails from "./pages/ImageDetails";

import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/images/:imageId" element={<ImageDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
