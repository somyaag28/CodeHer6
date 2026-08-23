import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleImageChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setProduct(null);
    setError("");
  };

  const identifyProduct = async () => {
    if (!image) {
      setError("Please select a product image first.");
      return;
    }

    setLoading(true);
    setError("");
    setProduct(null);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch(`${API_URL}/identify`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await response.json();

      if (data.message && !data.product_id) {
        setError(data.message);
      } else {
        setProduct(data);
      }
    } catch (err) {
      setError(
        "Could not connect to the backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          <span className="logo-mark">C</span>
          <span>CodeHer6</span>
        </div>

        <nav>
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Scan Product</button>
          <button className="nav-item">Products</button>
          <button className="nav-item">Checkout</button>
        </nav>

        <div className="status">
          <span className="status-dot"></span>
          Backend connected
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div>
            <p className="eyebrow">AI-POWERED SMART CHECKOUT</p>

            <h1>
              Welcome to <span>CodeHer6</span>
            </h1>

            <p className="subtitle">
              Identify products with AI, manage your cart, and calculate
              billing automatically.
            </p>

            <div className="hero-buttons">
              <label className="primary-button">
                Choose Product Image
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  hidden
                />
              </label>

              <button
                className="secondary-button"
                onClick={identifyProduct}
                disabled={loading}
              >
                {loading ? "Identifying..." : "Identify Product"}
              </button>
            </div>
          </div>

          <div className="scanner-card">
            <div className="scanner-icon">⌁</div>

            <h2>AI Product Scanner</h2>

            <p>
              Select a product image and CodeHer6 will identify it using
              the AI model.
            </p>

            {preview && (
              <img
                src={preview}
                alt="Selected product"
                className="product-preview"
              />
            )}

            <label className="scan-button">
              {image ? "Change Image" : "Start Scanning"}
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                hidden
              />
            </label>
          </div>
        </section>

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

        {product && (
          <section className="result-card">
            <p className="eyebrow">PRODUCT IDENTIFIED</p>

            <h2>{product.name}</h2>

            <div className="product-details">
              <div>
                <span>Product ID</span>
                <strong>{product.product_id}</strong>
              </div>

              <div>
                <span>Price</span>
                <strong>₹{product.price}</strong>
              </div>

              <div>
                <span>Stock</span>
                <strong>{product.stock}</strong>
              </div>

              <div>
                <span>GST</span>
                <strong>{product.gst_rate}%</strong>
              </div>

              <div>
                <span>Similarity</span>
                <strong>{product.similarity}</strong>
              </div>
            </div>

            <button className="primary-button">
              Add to Cart
            </button>
          </section>
        )}

        <section className="workflow">
          <div className="section-heading">
            <p className="eyebrow">HOW IT WORKS</p>
            <h2>From image to checkout</h2>
          </div>

          <div className="workflow-grid">
            <div className="workflow-card">
              <span>01</span>
              <h3>Capture</h3>
              <p>
                Select or capture a picture of the product.
              </p>
            </div>

            <div className="workflow-card">
              <span>02</span>
              <h3>Identify</h3>
              <p>
                AI creates an embedding and finds the matching product.
              </p>
            </div>

            <div className="workflow-card">
              <span>03</span>
              <h3>Checkout</h3>
              <p>
                Add the product to the cart and generate the final bill.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;