const video = document.getElementById("video");
const statusDiv = document.getElementById("status");
const videoWrapper = document.getElementById("videoWrapper");

// Start the webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Error accessing camera:", err);
    statusDiv.textContent = "🚫 Camera access denied!";
  });

async function captureAndSend() {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);

  const imageBase64 = canvas.toDataURL("image/jpeg").split(',')[1];
  statusDiv.textContent = "⏳ Verifying...";

  fetch('/unlock', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_base64: imageBase64 })
  })
    .then(async response => {
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const data = await response.json();

        if (data.status === "unlocked") {
          videoWrapper.classList.remove("border-red-500");
          videoWrapper.classList.add("border-green-500", "animate-pulse");
          statusDiv.textContent = "✅ Unlocked!";
        } else {
          videoWrapper.classList.remove("border-green-500");
          videoWrapper.classList.add("border-red-500", "animate-pulse");
          statusDiv.textContent = "❌ Access Denied";
        }

        // Remove pulse effect after 2 seconds
        setTimeout(() => {
          videoWrapper.classList.remove("animate-pulse");
        }, 2000);
      } else {
        const text = await response.text();
        console.error("Unexpected response:", text);
        statusDiv.textContent = "⚠️ Unexpected server error";
      }
    })
    .catch(error => {
      console.error("Error during fetch:", error);
      statusDiv.textContent = "🚫 Request failed";
    });
}
