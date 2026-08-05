import React, { useState } from "react";

function Chat() {

  const [msg, setMsg] = useState("");
  const [reply, setReply] = useState("");

  const sendMessage = async () => {

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: msg
        }
      );

      setReply(res.data.reply);

    } catch (err) {

      console.log(err);

      if (err.response) {
        alert(err.response.data.detail);
      } else {
        alert("Cannot connect to backend.");
      }

    }

  };

  return (

    <div style={{padding:"30px"}}>

      <h1>AI SaaS ChatGPT</h1>

      <textarea
        rows={6}
        cols={60}
        value={msg}
        onChange={(e)=>setMsg(e.target.value)}
      />

      <br /><br />

      <button onClick={sendMessage}>
        Send
      </button>

      <h3>AI Reply</h3>

      <p>{reply}</p>

    </div>

  );

}

export default Chat;