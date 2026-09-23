import React, {ChangeEvent, DetailedHTMLProps, InputHTMLAttributes, useState} from "react";


export interface QAProps {
  question: string;
  answer: string;
}


export interface QAList {
  items: QAProps[];
}


export function QA() {
  const [qa, setQA] = useState<QAList>({
    items: [
      {question: "1", answer: "one"},
      {question: "2", answer: "two"},
      {question: "3", answer: "three"},
    ]
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState<string>("");
  const [wrong, setWrong] = useState<string>("");


  function handleClickSubmitButton(event: DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>) {
    if (answer === qa.items[currentIndex].answer) {
      setWrong("Correct answer");
      setCurrentIndex(currentIndex + 1);
      setAnswer("");
    } else {
      setWrong("Wrong!!!");
      setAnswer("");
    }
  }


  function handleChangeAnswer(event: ChangeEvent<HTMLInputElement, HTMLInputElement>) {
    setWrong("");
    setAnswer(event.target.value);
  }

  return <>
    <div>{qa.items[currentIndex].question}</div>
    <input value={answer} type="text" onChange={handleChangeAnswer}></input>
    <div>{wrong}</div>
    <input type="submit" onClick={handleClickSubmitButton}></input>
  </>;
}
