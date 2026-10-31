import React from "react";
import ReactPlayer from "react-player";

export function Pronunciation() {
  return (
    <>
      <div
        style={{ display: "flex", justifyContent: "center", padding: "20px" }}
      >
        {/* Container giữ tỷ lệ chuẩn 16:9 cho video */}
        <div
          style={{
            position: "relative",
            paddingTop: "56.25%",
            width: "100%",
            maxWidth: "800px",
          }}
        >
          <ReactPlayer
            url="https://www.youtube.com/watch?v=2MDmt69mjHs&feature=youtu.be" // Dán link YouTube bất kỳ vào đây
            controls={true} // Hiện thanh điều khiển của YouTube
            width="100%"
            height="100%"
            style={{ position: "absolute", top: 0, left: 0 }}
            playing={false} // Đổi thành true nếu muốn tự động phát
            muted={false} // Đổi thành true nếu muốn tắt tiếng mặc định
          />
        </div>
      </div>
      <table>
        <tr>
          <th>Monophthongs</th>
          <th>Diphthongs</th>
        </tr>
        <tr>
          <td>i:</td>
          <td>i</td>
          <td>u</td>
          <td>u:</td>
          <td>i@</td>
          <td>ei</td>
        </tr>
        <tr>
          <td>e</td>
          <td>@</td>
          <td>3:</td>
          <td>o:</td>
          <td>u@</td>
          <td>oi</td>
          <td>ou</td>
        </tr>
        <tr>
          <td>ae</td>
          <td>^</td>
          <td>a:</td>
          <td>o</td>
          <td>e@</td>
          <td>ai</td>
          <td>au</td>
        </tr>
      </table>
    </>
  );
}
