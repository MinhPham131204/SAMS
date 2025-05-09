import React, { useState, useRef } from 'react';

const DiseasesDetection = () => {
  const [image, setImage] = useState(null); // Lưu trữ ảnh người dùng upload
  const [preview, setPreview] = useState(null); // Hiển thị ảnh preview
  const [resultImage, setResultImage] = useState(null); // Ảnh được backend trả về
  const [report, setReport] = useState(''); // Báo cáo số lượng bệnh
  const [loading, setLoading] = useState(false); // Trạng thái loading
  const videoRef = useRef(null); // Tham chiếu đến thẻ video
  const canvasRef = useRef(null); // Tham chiếu đến thẻ canvas

  // Bắt đầu truy cập webcam
  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    } catch (error) {
      console.error('Lỗi khi truy cập webcam:', error);
      alert('Không thể truy cập webcam. Vui lòng kiểm tra quyền truy cập.');
    }
  };

  // Chụp ảnh từ webcam
  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/png'); // Lưu ảnh dưới dạng base64
    setImage(imageData);
    setPreview(imageData); // Hiển thị ảnh preview
  };

  // Gửi ảnh đến API để phân tích
  const handleSubmit = async () => {
    if (!image) {
      alert('Vui lòng chọn hoặc chụp một ảnh!');
      return;
    }

    setLoading(true);
    const formData = new FormData();

    // Nếu ảnh là base64 (chụp từ webcam), chuyển đổi thành Blob
    if (image.startsWith('data:image')) {
      const blob = await fetch(image).then((res) => res.blob());
      formData.append('file', blob, 'webcam-image.png');
    } else {
      formData.append('file', image);
    }

    try {
      const response = await fetch('https://your-api-endpoint.com/detect', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResultImage(data.result_image_url); // URL ảnh được backend trả về
        setReport(`Số lượng bệnh phát hiện: ${data.disease_count}`); // Báo cáo số lượng bệnh
      } else {
        alert('Phân tích ảnh thất bại. Vui lòng thử lại.');
      }
    } catch (error) {
      console.error('Lỗi khi gửi ảnh:', error);
      alert('Đã xảy ra lỗi. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">Phát hiện lá lúa sâu bệnh</h1>

      {/* Lựa chọn upload ảnh */}
      <div className="mb-6">
        <label className="block mb-2 text-gray-700 font-medium">
          Upload ảnh:
          <input
            type="file"
            accept="image/*"
            onChange={(event) => {
              const file = event.target.files[0];
              if (file) {
                setImage(file);
                setPreview(URL.createObjectURL(file)); // Hiển thị ảnh preview
              }
            }}
            className="block w-full mt-2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          />
        </label>
      </div>

      {/* Chụp ảnh từ webcam */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Chụp ảnh từ webcam:</h3>
        <div className="flex flex-col items-center">
          <video ref={videoRef} className="w-full max-h-96 border border-gray-300 rounded-lg mb-4" />
          <canvas ref={canvasRef} className="hidden" /> {/* Canvas để chụp ảnh */}
          <div className="flex gap-4">
            <button
              onClick={startWebcam}
              className="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600"
            >
              Bật Webcam
            </button>
            <button
              onClick={captureImage}
              className="py-2 px-4 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600"
            >
              Chụp Ảnh
            </button>
          </div>
        </div>
      </div>

      {/* Hiển thị ảnh preview */}
      {preview && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Ảnh đã chọn:</h3>
          <img
            src={preview}
            alt="Preview"
            className="w-full max-h-96 object-contain border border-gray-300 rounded-lg"
          />
        </div>
      )}

      {/* Nút gửi ảnh */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        className={`w-full py-2 px-4 text-white font-semibold rounded-lg shadow-md ${
          loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
        }`}
      >
        {loading ? 'Đang phân tích...' : 'Gửi ảnh'}
      </button>

      {/* Hiển thị kết quả */}
      {resultImage && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Kết quả phân tích:</h3>
          <img
            src={resultImage}
            alt="Kết quả phân tích"
            className="w-full max-h-96 object-contain border border-gray-300 rounded-lg"
          />
          <p className="mt-4 text-gray-800 font-medium">{report}</p>
        </div>
      )}
    </div>
  );
};

export default DiseasesDetection;