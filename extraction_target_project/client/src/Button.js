import React from "react";
import './style.css';

function Button({ value, name, buttonFunction }) {
  return (
    <button
      value={value}
      title={name}
      style={{
        backgroundColor: value,
        width: "22px",
        height: "22px",
        borderRadius: "50%",
        border: "2px solid rgba(255, 255, 255, 0.4)",
        cursor: "pointer",
        padding: 0,
        margin: "2px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.3)"
      }}
      onClick={(event) => { buttonFunction(event); }}
      className="color-picker-btn"
    />
  );
}

export default Button;