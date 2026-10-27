import React, { useState } from "react";
import './style.css';
import { FaImage } from "react-icons/fa6";

function UploadFile(props) {
  const [imageFile, uploadImageFile] = useState();

  function upload(event) {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      uploadImageFile(url);
      props.imageSource(url);
    }
  }

  return (
    <div>
      <label htmlFor={props.id || "uploadedImage"} className="tool-btn" title="이미지 업로드" style={{ cursor: "pointer" }}>
        <input
          type="file"
          onChange={upload}
          accept="image/*"
          id={props.id || "uploadedImage"}
          style={{ display: "none" }}
        />
        <FaImage size="18" />
      </label>
    </div>
  );
}

export default UploadFile;
