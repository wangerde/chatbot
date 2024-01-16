import { useState } from "react";
import { Title } from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const [blob, setBlob] = useState("");

  const createBolbUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages

    const myMessage = { sender: "Xin", blobUrl };
    const messagesArr = [...messages, myMessage];

    // convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // constuct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        // send form data to API endpoint
        await axios
          .post("http://localhost:8000/post-audio", formData, {
            headers: { "Content-Type": "audio/mpeg" },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBolbUrl(blob);

            // append to audio

            const ziegieMessage = {sender: "Ziegie", blobUrl: audio.src};
            messagesArr.push(ziegieMessage);
            setMessages(messagesArr)

            // play our audio
            setIsLoading(false);
            audio.play();
          })
          .catch((err) => {
            console.error(err);
            setIsLoading(false);
          });
      });

    setIsLoading(false);
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;
