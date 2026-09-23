import React, {useState} from "react";


export function Messages() {
  const [messages, setMessages] = useState<string[]>([])
  const [query, setQuery] = useState<string>("")

  function handleClickSubmit() {
    setMessages(prevMessages => [...prevMessages, query]);
  }

  function handleChangeInput(e: React.ChangeEvent<HTMLInputElement>) {
    setQuery(e.target.value);
  }

  return (
    <>
      {
        messages.map((value, index) => (
          <div key={index}>{value}</div>
        ))
      }
      <input value={query} type="text" onChange={handleChangeInput}></input>
      <button onClick={handleClickSubmit}>
        Submit
      </button>
    </>
  );
}

