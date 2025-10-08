import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import ApiPost from "./components/listAllMessages"
import './App.css'
import InputPButton from "./components/postReqPart"

function Home() {
  //if %2==0 then white, !=0 is grey
  const [disable, setDis] = useState(false);
  const [messages, setMessages] = useState([])
  const [loading, setLoad] = useState(false)

    // useEffect(()=>{
    //     let functionCall = async ()=>{
    //         let currentMessage = {messages: user, sender: "User"}
    //         setMessages(prev => [...prev, currentMessage])
    //         const addData = await fetch("", {
    //             method: "POST",
    //             headers:{"Content-Type": "text/plain"},
    //             body: user
    //         })
    //         let checkIn = await addData.text();
    //         let aiForm = {messages: checkIn, sender: "AI"}
    //         setMessages(prev=>[...prev, aiForm])
    //     }
    //     functionCall()
    // }, [user])

    useEffect(()=>{
        if(messages.length==0) return;
        if(messages[messages.length-1].sender=="AI") return;
        let functionCall = async ()=>{
            let aiForm = {messages: "lol im an ai here", sender: "AI"}
            setMessages(prev=>[...prev, aiForm])
            setLoad(false)
        }
        let das = setInterval(()=>{functionCall(), clearInterval(das)}, 5000)
        // functionCall()
    }, [messages])

  return (
    <div className='backGrandScrollOverf'>
      <div className="coverAllPosts">
          <ApiPost posts={messages} />
          {(loading)?(<h3 className='AiSection'><i>Loading</i></h3>):("")}
      </div>
      <InputPButton loading={loading} disable={disable} setDis={setDis} setLoad={setLoad} setUserMessages={setMessages} />
    </div>
  )
}

export default Home
