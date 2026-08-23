import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("home");

  const [inventory, setInventory] = useState([]);
  const [inventoryLoading, setInventoryLoading] = useState(false);

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [identifiedProduct, setIdentifiedProduct] = useState(null);

  // =========================
  // CAMERA
  // =========================

  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const videoRef = useRef(null);

  // =========================
  // CART
  // =========================

  const [cart, setCart] = useState([]);

  // =========================
  // GENERAL STATE
  // =========================

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // =========================
  // DELETE STATE
  // =========================

  const [productToDelete, setProductToDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  // =========================
  // LOAD INVENTORY
  // =========================

  const loadInventory = async () => {
    try {
      setInventoryLoading(true);
      setError("");

      const response = await fetch(`${API_URL}/inventory`);

      if (!response.ok) {
        throw new Error("Could not load inventory.");
      }

      const data = await response.json();

      setInventory(data);
    } catch (err) {
      console.error(err);
      setError("Could not connect to the backend.");
    } finally {
      setInventoryLoading(false);
    }
  };

  useEffect(() => {
    loadInventory();
  }, []);

  // =========================
  // IMAGE SELECTION
  // =========================

  const handleImageChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setIdentifiedProduct(null);
    setError("");
    setMessage("");
  };

  // =========================
  // CAMERA
  // =========================

  const startCamera = async () => {
    try {
      setError("");
      setMessage("");

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "environment",
        },
        audio: false,
      });

      setCameraStream(stream);
      setCameraOpen(true);

      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      }, 100);
    } catch (err) {
      console.error(err);

      setError(
        "Could not access the camera. Please allow camera permission."
      );
    }
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach((track) => track.stop());
    }

    setCameraStream(null);
    setCameraOpen(false);
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;

    const video = videoRef.current;

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    if (!context) return;

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(
      (blob) => {
        if (!blob) return;

        const capturedFile = new File(
          [blob],
          "camera-photo.jpg",
          {
            type: "image/jpeg",
          }
        );

        setImage(capturedFile);
        setPreview(URL.createObjectURL(capturedFile));
        setIdentifiedProduct(null);
        setError("");
        setMessage("");

        stopCamera();
      },
      "image/jpeg",
      0.9
    );
  };

  // =========================
  // IDENTIFY PRODUCT
  // =========================

  const identifyProduct = async () => {
    if (!image) {
      setError("Please select a product image.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");
      setIdentifiedProduct(null);

      const formData = new FormData();

      formData.append("image", image);

      const response = await fetch(
        `${API_URL}/identify`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Product identification failed."
        );
      }

      if (data.message && !data.product_id) {
        setError(data.message);
        return;
      }

      setIdentifiedProduct(data);
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Could not identify product."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // ADD TO CART
  // =========================

  const addToCart = (product) => {
    setCart((previousCart) => {
      const existing = previousCart.find(
        (item) =>
          item.product_id === product.product_id
      );

      if (existing) {
        return previousCart.map((item) =>
          item.product_id === product.product_id
            ? {
                ...item,
                quantity: item.quantity + 1,
              }
            : item
        );
      }

      return [
        ...previousCart,
        {
          product_id: product.product_id,
          name: product.name,
          price: product.price,
          quantity: 1,
        },
      ];
    });

    setMessage(
      `${product.name} added to cart.`
    );
  };

  // =========================
  // CHANGE CART QUANTITY
  // =========================

  const changeQuantity = (
    productId,
    amount
  ) => {
    setCart((previousCart) =>
      previousCart
        .map((item) =>
          item.product_id === productId
            ? {
                ...item,
                quantity:
                  item.quantity + amount,
              }
            : item
        )
        .filter(
          (item) => item.quantity > 0
        )
    );
  };

  // =========================
  // CART TOTAL
  // =========================

  const cartTotal = cart.reduce(
    (total, item) =>
      total +
      item.price * item.quantity,
    0
  );

  // =========================
  // CHECKOUT CART
  // =========================

  const checkout = async () => {
    if (cart.length === 0) {
      setError("Your cart is empty.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const response = await fetch(
        `${API_URL}/checkout/cart`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            items: cart.map((item) => ({
              product_id:
                item.product_id,
              quantity:
                item.quantity,
            })),
            payment_method: "Cash",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(
          data.error ||
            "Checkout failed."
        );
      }

      setCart([]);

      await loadInventory();

      setMessage(
        "Checkout successful. Bill generated."
      );

      if (data.pdf_url) {
        window.open(
          `${API_URL}${data.pdf_url}`,
          "_blank"
        );
      }
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Checkout failed."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // DELETE PRODUCT
  // =========================

  const deleteProduct = async () => {
    if (!productToDelete) return;

    try {
      setDeleting(true);
      setError("");
      setMessage("");

      const response = await fetch(
        `${API_URL}/products/${productToDelete.id}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(
          data.error ||
            data.detail ||
            "Could not delete product."
        );
      }

      setProductToDelete(null);

      await loadInventory();

      setMessage(
        `${productToDelete.name} was deleted from inventory.`
      );
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Could not delete product."
      );
    } finally {
      setDeleting(false);
    }
  };

  // =========================
  // PAGE TITLE
  // =========================

  const pageTitle = {
    home: "Home",
    add: "Add Product",
    inventory: "Inventory Hub",
    checkout: "Checkout",
  };

  // =========================
  // MAIN RETURN
  // =========================

  return (
    <div className="app">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            S
          </div>

          <div>
            <h2>SnapBill</h2>
            <p>Smart Billing</p>
          </div>

        </div>

        <div className="profile">

          <div className="profile-circle">
            S
          </div>

          <div>
            <strong>
              Store Dashboard
            </strong>

            <span>
              Connected
            </span>
          </div>

        </div>

        <nav className="sidebar-nav">

          <button
            className={
              page === "home"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => {
              setPage("home");
              setError("");
              setMessage("");
            }}
          >
            🏠 Home
          </button>

          <button
            className={
              page === "add"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => {
              setPage("add");
              setError("");
              setMessage("");
            }}
          >
            ➕ Add Product
          </button>

          <button
            className={
              page === "inventory"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => {
              setPage("inventory");
              loadInventory();
              setError("");
              setMessage("");
            }}
          >
            📦 Inventory Hub
          </button>

          <button
            className={
              page === "checkout"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => {
              setPage("checkout");
              setError("");
              setMessage("");
            }}
          >
            🛒 Checkout
          </button>

        </nav>

      </aside>

      {/* =========================
          MAIN AREA
      ========================= */}

      <main className="main">

        <header className="topbar">

          <div>
            <p className="small-label">
              SNAPBILL
            </p>

            <h1>
              {pageTitle[page]}
            </h1>
          </div>

          <div className="backend-status">
            <span></span>
            Backend connected
          </div>

        </header>

        <div className="content">

          {/* =========================
              MESSAGES
          ========================= */}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {message && (
            <div className="success-message">
              {message}
            </div>
          )}

          {/* =========================
              HOME
          ========================= */}

          {page === "home" && (

            <div>

              <div className="welcome-card">

                <div>

                  <p className="small-label">
                    AI-POWERED BILLING
                  </p>

                  <h2>
                    Scan a product and
                    generate a bill
                  </h2>

                  <p>
                    Upload a product image,
                    let the AI identify it,
                    add it to your cart and
                    checkout.
                  </p>

                </div>

                <div className="big-icon">
                  📷
                </div>

              </div>

              <div className="two-column">

                {/* =========================
                    SCANNER
                ========================= */}

                <section className="card">

                  <div className="card-header">

                    <div>

                      <p className="small-label">
                        STEP 1
                      </p>

                      <h2>
                        Identify Product
                      </h2>

                    </div>

                  </div>

                  {/* CAMERA OPEN */}

                  {cameraOpen ? (

                    <div className="camera-box">

                      <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        className="camera-preview"
                      />

                      <div className="camera-controls">

                        <button
                          type="button"
                          className="primary-button"
                          onClick={
                            capturePhoto
                          }
                        >
                          📸 Capture Photo
                        </button>

                        <button
                          type="button"
                          className="secondary-button"
                          onClick={
                            stopCamera
                          }
                        >
                          ✕ Close Camera
                        </button>

                      </div>

                    </div>

                  ) : preview ? (

                    /* =========================
                       IMAGE SELECTED
                    ========================= */

                    <div className="selected-image">

                      <img
                        src={preview}
                        alt="Selected product"
                      />

                      <div className="image-actions">

                        <button
                          type="button"
                          className="secondary-button"
                          onClick={() => {
                            setPreview(null);
                            setImage(null);
                            setIdentifiedProduct(null);
                            setError("");
                            setMessage("");
                          }}
                        >
                          Choose Another Photo
                        </button>

                        <button
                          type="button"
                          className="secondary-button"
                          onClick={
                            startCamera
                          }
                        >
                          📷 Use Camera
                        </button>

                      </div>

                    </div>

                  ) : (

                    /* =========================
                       UPLOAD OPTIONS
                    ========================= */

                    <div className="upload-options">

                      <button
                        type="button"
                        className="upload-option"
                        onClick={
                          startCamera
                        }
                      >

                        <div className="upload-icon">
                          📷
                        </div>

                        <strong>
                          Use Camera
                        </strong>

                        <span>
                          Take a photo of
                          the product
                        </span>

                      </button>

                      <label className="upload-option">

                        <div className="upload-icon">
                          🖼️
                        </div>

                        <strong>
                          Upload Photo
                        </strong>

                        <span>
                          Choose an image
                          from your device
                        </span>

                        <input
                          type="file"
                          accept="image/*"
                          onChange={
                            handleImageChange
                          }
                          hidden
                        />

                      </label>

                    </div>

                  )}

                  <button
                    className="primary-button"
                    onClick={
                      identifyProduct
                    }
                    disabled={
                      loading || !image
                    }
                  >
                    {loading
                      ? "Identifying..."
                      : "Identify Product"}
                  </button>

                </section>

                {/* =========================
                    IDENTIFIED PRODUCT
                ========================= */}

                <section className="card">

                  <p className="small-label">
                    STEP 2
                  </p>

                  <h2>
                    Product Result
                  </h2>

                  {!identifiedProduct ? (

                    <div className="empty-state">

                      <div>
                        🔍
                      </div>

                      <p>
                        Identified product
                        details will appear
                        here.
                      </p>

                    </div>

                  ) : (

                    <div className="product-result">

                      <h3>
                        {identifiedProduct.name}
                      </h3>

                      <div className="details-grid">

                        <div>

                          <span>
                            Product ID
                          </span>

                          <strong>
                            {
                              identifiedProduct.product_id
                            }
                          </strong>

                        </div>

                        <div>

                          <span>
                            Price
                          </span>

                          <strong>
                            ₹
                            {
                              identifiedProduct.price
                            }
                          </strong>

                        </div>

                        <div>

                          <span>
                            Stock
                          </span>

                          <strong>
                            {
                              identifiedProduct.stock
                            }
                          </strong>

                        </div>

                        <div>

                          <span>
                            GST
                          </span>

                          <strong>
                            {
                              identifiedProduct.gst_rate
                            }%
                          </strong>

                        </div>

                      </div>

                      <button
                        className="primary-button"
                        onClick={() =>
                          addToCart(
                            identifiedProduct
                          )
                        }
                      >
                        Add to Cart
                      </button>

                    </div>

                  )}

                </section>

              </div>

            </div>

          )}

          {/* =========================
              ADD PRODUCT
          ========================= */}

          {page === "add" && (

            <AddProduct
              onSuccess={loadInventory}
              setError={setError}
              setMessage={setMessage}
            />

          )}

          {/* =========================
              INVENTORY
          ========================= */}

          {page === "inventory" && (

            <Inventory
              inventory={inventory}
              loading={inventoryLoading}
              onDelete={(product) =>
                setProductToDelete(product)
              }
            />

          )}

          {/* =========================
              CHECKOUT
          ========================= */}

          {page === "checkout" && (

            <section className="card checkout-card">

              <div className="card-header">

                <div>

                  <p className="small-label">
                    CURRENT ORDER
                  </p>

                  <h2>
                    Shopping Cart
                  </h2>

                </div>

                <strong className="cart-total">
                  ₹
                  {cartTotal.toLocaleString(
                    "en-IN"
                  )}
                </strong>

              </div>

              {cart.length === 0 ? (

                <div className="empty-state">

                  <div>
                    🛒
                  </div>

                  <p>
                    Your cart is empty.
                  </p>

                  <button
                    className="secondary-button"
                    onClick={() =>
                      setPage("home")
                    }
                  >
                    Scan a Product
                  </button>

                </div>

              ) : (

                <>

                  <div className="cart-list">

                    {cart.map((item) => (

                      <div
                        className="cart-item"
                        key={
                          item.product_id
                        }
                      >

                        <div>

                          <strong>
                            {item.name}
                          </strong>

                          <span>
                            ₹
                            {item.price}
                            {" "}each
                          </span>

                        </div>

                        <div className="quantity-controls">

                          <button
                            onClick={() =>
                              changeQuantity(
                                item.product_id,
                                -1
                              )
                            }
                          >
                            −
                          </button>

                          <strong>
                            {item.quantity}
                          </strong>

                          <button
                            onClick={() =>
                              changeQuantity(
                                item.product_id,
                                1
                              )
                            }
                          >
                            +
                          </button>

                        </div>

                        <strong>
                          ₹
                          {(
                            item.price *
                            item.quantity
                          ).toLocaleString(
                            "en-IN"
                          )}
                        </strong>

                      </div>

                    ))}

                  </div>

                  <div className="checkout-footer">

                    <div>

                      <span>
                        Total
                      </span>

                      <strong>
                        ₹
                        {cartTotal.toLocaleString(
                          "en-IN"
                        )}
                      </strong>

                    </div>

                    <button
                      className="primary-button"
                      onClick={checkout}
                      disabled={loading}
                    >
                      {loading
                        ? "Processing..."
                        : "Checkout & Generate Bill"}
                    </button>

                  </div>

                </>

              )}

            </section>

          )}

        </div>

      </main>

      {/* =========================
          DELETE CONFIRMATION MODAL
      ========================= */}

      {productToDelete && (

        <div className="modal-overlay">

          <div className="delete-modal">

            <div className="delete-modal-icon">
              ⚠️
            </div>

            <h2>
              Delete Product?
            </h2>

            <p>
              Are you sure you want to
              delete{" "}
              <strong>
                {productToDelete.name}
              </strong>{" "}
              from your inventory?
            </p>

            <p className="delete-warning">
              This action cannot be undone.
            </p>

            <div className="modal-actions">

              <button
                type="button"
                className="secondary-button"
                disabled={deleting}
                onClick={() =>
                  setProductToDelete(null)
                }
              >
                Cancel
              </button>

              <button
                type="button"
                className="delete-confirm-button"
                disabled={deleting}
                onClick={deleteProduct}
              >
                {deleting
                  ? "Deleting..."
                  : "Yes, Delete"}
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}


// ======================================================
// ADD PRODUCT COMPONENT
// ======================================================

function AddProduct({
  onSuccess,
  setError,
  setMessage,
}) {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");
  const [gst, setGst] = useState("0");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const submitProduct = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");

    if (!name || !price || !image) {
      setError(
        "Product name, price and image are required."
      );
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("name", name);
      formData.append(
        "price",
        parseFloat(price)
      );
      formData.append(
        "stock",
        parseInt(stock || "1")
      );
      formData.append(
        "gst_rate",
        parseFloat(gst)
      );
      formData.append(
        "image",
        image
      );

      const response = await fetch(
        `${API_URL}/products`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Could not create product."
        );
      }

      setMessage(
        `${data.name || name} was successfully added to the database.`
      );

      setName("");
      setPrice("");
      setStock("");
      setGst("0");
      setImage(null);
      setPreview(null);

      await onSuccess();
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Could not add product."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleImage = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setImage(file);
    setPreview(
      URL.createObjectURL(file)
    );
  };

  return (
    <form
      className="card add-product-card"
      onSubmit={submitProduct}
    >

      <div className="card-header">

        <div>

          <p className="small-label">
            PRODUCT ENROLLMENT
          </p>

          <h2>
            Add Product to Database
          </h2>

        </div>

      </div>

      <div className="form-grid">

        <div className="form-group full">

          <label>
            Product Image
          </label>

          <label className="image-upload">

            {preview ? (

              <img
                src={preview}
                alt="Product preview"
              />

            ) : (

              <>
                <span>
                  📷
                </span>

                <strong>
                  Choose Product Image
                </strong>

                <small>
                  This image will be used
                  by the AI identification
                  system.
                </small>
              </>

            )}

            <input
              type="file"
              accept="image/*"
              onChange={handleImage}
              hidden
            />

          </label>

        </div>

        <div className="form-group full">

          <label>
            Product Name
          </label>

          <input
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            placeholder="e.g. Amul Milk"
          />

        </div>

        <div className="form-group">

          <label>
            Price (₹)
          </label>

          <input
            type="number"
            value={price}
            onChange={(e) =>
              setPrice(e.target.value)
            }
            placeholder="50"
          />

        </div>

        <div className="form-group">

          <label>
            Initial Stock
          </label>

          <input
            type="number"
            value={stock}
            onChange={(e) =>
              setStock(e.target.value)
            }
            placeholder="10"
          />

        </div>

        <div className="form-group">

          <label>
            GST Rate
          </label>

          <select
            value={gst}
            onChange={(e) =>
              setGst(e.target.value)
            }
          >
            <option value="0">
              0%
            </option>

            <option value="5">
              5%
            </option>

            <option value="12">
              12%
            </option>

            <option value="18">
              18%
            </option>
          </select>

        </div>

      </div>

      <button
        className="primary-button"
        type="submit"
        disabled={loading}
      >
        {loading
          ? "Adding Product..."
          : "Enroll Product in Database"}
      </button>

    </form>
  );
}


// ======================================================
// INVENTORY COMPONENT
// ======================================================

function Inventory({
  inventory,
  loading,
  onDelete,
}) {
  const [search, setSearch] =
    useState("");

  const filteredInventory =
    inventory.filter(
      (item) =>
        item.name
          ?.toLowerCase()
          .includes(
            search.toLowerCase()
          ) ||
        String(item.id).includes(
          search
        )
    );

  return (
    <section className="card">

      <div className="card-header">

        <div>

          <p className="small-label">
            STORE DATABASE
          </p>

          <h2>
            Inventory
          </h2>

        </div>

        <input
          className="search-input"
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          placeholder="Search products..."
        />

      </div>

      {loading ? (

        <div className="empty-state">
          Loading inventory...
        </div>

      ) : filteredInventory.length === 0 ? (

        <div className="empty-state">

          <div>
            📦
          </div>

          <p>
            No products found.
          </p>

        </div>

      ) : (

        <div className="inventory-table">

          {/* HEADER */}

          <div className="inventory-header">

            <span>
              ID
            </span>

            <span>
              Product
            </span>

            <span>
              Price
            </span>

            <span>
              GST
            </span>

            <span>
              Stock
            </span>

            <span>
              Actions
            </span>

          </div>

          {/* ROWS */}

          {filteredInventory.map(
            (item) => (

              <div
                className="inventory-row"
                key={item.id}
              >

                <span>
                  #{item.id}
                </span>

                <strong>
                  {item.name}
                </strong>

                <span>
                  ₹
                  {Number(
                    item.price
                  ).toLocaleString(
                    "en-IN"
                  )}
                </span>

                <span>
                  {item.gst_rate}%
                </span>

                <span
                  className={
                    item.stock > 0
                      ? "stock-good"
                      : "stock-bad"
                  }
                >
                  {item.stock}
                </span>

                <button
                  type="button"
                  className="delete-button"
                  onClick={() =>
                    onDelete(item)
                  }
                >
                  🗑 Delete
                </button>

              </div>

            )
          )}

        </div>

      )}

    </section>
  );
}


export default App;