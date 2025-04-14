// const formData = new FormData();
// formData.append("image", imageFile); // This can be a Blob or File object

// fetch("http://localhost:5000/predict", {
//   method: "POST",
//   body: formData,
// })
//   .then((response) => response.json())
//   .then((data) => {
//     console.log("Prediction:", data);
//     // Use the prediction result in your UI
//   })
//   .catch((error) => console.error("Error:", error));

// document.getElementById("startBtn").addEventListener("click", async () => {
//   const statusDiv = document.getElementById("status");
//   const videoFeed = document.getElementById("videoFeed");

//   // Update the status to indicate that detection is starting
//   statusDiv.textContent = "Status: Starting detection...";
//   statusDiv.style.color = "blue";

//   try {
//     // Send a request to the Flask backend to start detection
//     const response = await fetch("http://127.0.0.1:5000/start-detection", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//     });

//     if (response.ok) {
//       const data = await response.json();

//       // Update the status based on the detection result
//       if (data.drowsy) {
//         statusDiv.textContent = "Status: Drowsy!";
//         statusDiv.style.color = "red";
//       } else {
//         statusDiv.textContent = "Status: Normal";
//         statusDiv.style.color = "green";
//       }
//     } else {
//       // Handle errors from the backend
//       statusDiv.textContent = "Status: Error starting detection.";
//       statusDiv.style.color = "red";
//     }
//   } catch (error) {
//     // Handle network or other errors
//     console.error("Error:", error);
//     statusDiv.textContent = "Status: Unable to connect to backend.";
//     statusDiv.style.color = "red";
//   }
// });
const img = document.getElementById("videoFeed");
const statusDiv = document.getElementById("status");

// Set video feed source
img.src = "http://localhost:5000/video";
img.onerror = () => {
  console.error("Failed to load video feed");
  statusDiv.textContent = "Error: Video feed unavailable";
};

// Update status periodically
setInterval(async () => {
  try {
    const response = await fetch("http://localhost:5000/status");
    const data = await response.json();
    if (data.drowsy) {
      statusDiv.textContent = `Status: Drowsiness Detected! (Blinks: ${data.blink_count}, Yawns: ${data.yawn_count})`;
      statusDiv.style.color = "red";
    } else {
      statusDiv.textContent = `Status: Driver Awake (Blinks: ${data.blink_count}, Yawns: ${data.yawn_count})`;
      statusDiv.style.color = "green";
    }
  } catch (error) {
    console.error("Error fetching status:", error);
    statusDiv.textContent = "Status: Error";
  }
}, 1000);
