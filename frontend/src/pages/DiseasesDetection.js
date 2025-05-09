import React, { useState, useRef } from 'react';
import Services from '../services/services'; // Import service

const DiseasesDetection = () => {
    const [image, setImage] = useState(null); // Lưu trữ ảnh người dùng upload
    const [preview, setPreview] = useState(null); // Hiển thị ảnh preview
    const [resultImage, setResultImage] = useState(null); // Ảnh được backend trả về
    const [resultBoxs, setResultBoxs] = useState([]); // Ảnh được backend trả về
    const [loading, setLoading] = useState(false); // Trạng thái loading
    const [isModalOpen, setIsModalOpen] = useState(false); // Trạng thái modal phóng to ảnh
    const [modelImage, setModelImage] = useState(null); // Ảnh trong modal
    const videoRef = useRef(null); // Tham chiếu đến thẻ video
    const canvasRef = useRef(null); // Tham chiếu đến thẻ canvas
    const fileInputRef = useRef(null); // Tham chiếu đến input file
    const [webcamActive, setWebcamActive] = useState(false); // Trạng thái webcam

    // Bắt đầu truy cập webcam
    const startWebcam = async () => {
        try {
            setWebcamActive(true); // Đánh dấu webcam đang hoạt động
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoRef.current.srcObject = stream;
            videoRef.current.play();
        } catch (error) {
            console.error('Lỗi khi truy cập webcam:', error);
            alert('Không thể truy cập webcam. Vui lòng kiểm tra quyền truy cập.');
        }
    };

    // Tắt webcam
    const stopWebcam = () => {
        const stream = videoRef.current?.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach((track) => track.stop()); // Dừng tất cả các track
        }
        videoRef.current.srcObject = null; // Xóa nguồn video
        setWebcamActive(false); // Đánh dấu webcam đã tắt
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

    // Xử lý khi người dùng chọn file
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file)); // Hiển thị ảnh preview
        }
    };

    // Xử lý khi người dùng kéo thả file
    const handleDrop = async (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        console.log(file);
        if (file) {
          // Nếu kéo thả file từ hệ thống tệp
          setImage(file);
          setPreview(URL.createObjectURL(file)); // Hiển thị ảnh preview
        } else {
          // Nếu kéo thả từ trình duyệt (ví dụ: Google Images)
          const url = event.dataTransfer.getData('text/uri-list') || event.dataTransfer.getData('text/plain');
          if (url) {
            try {
              // Tải ảnh từ URL và chuyển thành Blob
              const response = await fetch(url);
              const blob = await response.blob();
              const fileFromUrl = new File([blob], 'image-from-url.jpg', { type: blob.type });
      
              setImage(fileFromUrl);
              setPreview(URL.createObjectURL(fileFromUrl)); // Hiển thị ảnh preview
            } catch (error) {
              console.error('Không thể tải ảnh từ URL:', error);
              alert('Không thể tải ảnh từ URL. Vui lòng thử lại.');
            }
          } else {
            alert('Không thể nhận diện ảnh. Vui lòng thử lại.');
          }
        }
    };

    // Ngăn chặn hành vi mặc định khi kéo thả
    const handleDragOver = (event) => {
        event.preventDefault();
    };

    // Gửi ảnh đến API để phân tích
    const handleSubmit = async () => {
        if (!image) {
            alert('Vui lòng chọn hoặc chụp một ảnh!');
            return;
        }

        setLoading(true);

        try {
            let imageBlob;

            // Nếu ảnh là base64 (chụp từ webcam), chuyển đổi thành Blob
            if (typeof image === 'string' && image.startsWith('data:image')) {
                imageBlob = await fetch(image).then((res) => res.blob());
            } else {
                imageBlob = image; // Nếu là file, sử dụng trực tiếp
            }

            // Gọi service predictRiceLeafDisease
            const response = await Services.predictRiceLeafDisease(imageBlob);

            if (response.ok) {
                // Lấy ảnh kết quả từ response
                const resultImageBlob = await response.blob();
                const resultImageUrl = URL.createObjectURL(resultImageBlob); // Tạo URL để hiển thị ảnh

                // Lấy dữ liệu bounding box từ header
                const boundingBoxes = response.headers.get('Bounding-Boxes');
                const parsedBoundingBoxes = boundingBoxes ? JSON.parse(boundingBoxes) : [];
                setResultBoxs(parsedBoundingBoxes); // Lưu trữ bounding boxes

                // Cập nhật state để hiển thị kết quả
                setResultImage(resultImageUrl); // URL ảnh được backend trả về
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
            <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">Phát hiện bệnh lá lúa</h1>

            {/* Vùng chọn hoặc kéo thả ảnh */}
            <div
                className="mb-6 border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer bg-gray-50 hover:bg-gray-100"
                onClick={() => fileInputRef.current.click()} // Click để mở hộp thoại chọn file
                onDrop={handleDrop} // Xử lý khi kéo thả file
                onDragOver={handleDragOver} // Ngăn chặn hành vi mặc định khi kéo thả
            >
                <p className="text-gray-700 text-center">Kéo thả ảnh vào đây hoặc nhấn để chọn ảnh</p>

            </div>

            {/* Input file ẩn */}
            <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
            />

            {/* Chụp ảnh từ webcam */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Chụp ảnh từ camera</h3>
                <div className="flex flex-col items-center">
                    {webcamActive && <video ref={videoRef} className="w-full max-h-96 border border-gray-300 rounded-lg mb-4" />}
                    <canvas ref={canvasRef} className="hidden" /> {/* Canvas để chụp ảnh */}
                    <div className="flex gap-4">
                        {!webcamActive ? (
                            <button
                                onClick={startWebcam}
                                className="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600"
                            >
                                Kết nối camera
                            </button>
                        ) : (
                            <button
                                onClick={stopWebcam}
                                className="py-2 px-4 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600"
                            >
                                Tắt camera
                            </button>
                        )}
                        <button
                            onClick={captureImage}
                            disabled={!webcamActive}
                            className={`py-2 px-4 text-white font-semibold rounded-lg shadow-md ${webcamActive ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-400 cursor-not-allowed'
                                }`}
                        >
                            Chụp Ảnh
                        </button>
                    </div>
                </div>
            </div>

            {preview && (
                <img
                    src={preview}
                    alt="Preview"
                    onClick={() => {
                        setIsModalOpen(true);
                        setModelImage(preview);
                    }} // Mở modal khi nhấn vào ảnh
                    className="mt-4 w-full max-h-96 object-contain border border-gray-300 rounded-lg"
                />
            )}

            {/* Nút gửi ảnh */}
            <button
                onClick={handleSubmit}
                disabled={loading}
                className={`w-full py-2 px-4 text-white font-semibold rounded-lg shadow-md ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
                    }`}
            >
                {loading ? 'Đang phân tích...' : 'Phân tích ảnh'}
            </button>

            {/* Hiển thị kết quả */}
            {resultImage && (
                <div className={`mt-6 rounded-lg p-4 border border-black ${resultBoxs.length > 0 ? 'bg-red-200' : 'bg-green-200'}`}>
                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Kết quả phân tích: {resultBoxs.length == 0 ? "không có bệnh" : `phát hiện ${resultBoxs.length} vùng có bệnh`}</h3>
                    <img
                        src={resultImage}
                        alt="Kết quả phân tích"
                        className="w-full max-h-96 object-contain border border-black rounded-lg cursor-pointer"
                        onClick={() => {
                            setIsModalOpen(true);
                            setModelImage(resultImage);
                        }} // Mở modal khi nhấn vào ảnh
                    />
                    {resultBoxs.length > 0 && (
                    <p className="mt-4 text-gray-800 font-medium">
                            {resultBoxs.map((box, index) => (
                                <div key={index} className="border border-red-500 p-1 mb-2 bg-white rounded flex flex-col">
                                    <p className="text-gray-800">Bệnh: {box.label}</p>
                                    <p className="text-gray-800">Độ chắc chắn: {box.score}</p>
                                </div>
                            ))}
                    </p>
                    )}
                </div>
            )}

            {/* Modal phóng to ảnh */}
            {isModalOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
                    onClick={() => setIsModalOpen(false)} // Đóng modal khi nhấn vào nền
                >
                    <img
                        src={modelImage}
                        alt="Phóng to"
                        className="max-w-full max-h-full"
                    />
                </div>
            )}
        </div>
    );
};

export default DiseasesDetection;